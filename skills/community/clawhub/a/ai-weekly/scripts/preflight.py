#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""preflight.py — 流水线启动前的飞书凭据预检（SEC-12）。

背景：2026-10-05 那次周报，飞书推送在流水线第 6 步失败（rc=3）却被上游脚本吞掉，
产物照常生成、校验 25/25 通过、.run.log 写着 errors: 0，用户直到手动追问才发现
没收到消息。根因有两层：脚本不判退出码（已单独修复）+ 凭据问题直到第 6 步才暴露。
本脚本解决第二层：把「凭据是否可用」从流水线第 6 步提前到第 0 步暴露。

做什么：
  调``lark-cli doctor``，解析其 JSON 输出，抽取三项决定推送成败的检查：
    * ``identity_ready`` —— 至少有一种身份可用（fail 则完全推不了）
    * ``bot_identity``   —— bot 身份就绪；warn/fail 时机器人发消息会报20140
    * ``app_resolved``   —— app_id/app_secret 能解析出（fail 则凭据无效）

为什么必须显式回退路径：
  ``lark-cli`` 由宿主连接器安装在 ``~/.workbuddy/binaries/node/cli-connector-packages/``，
  该目录实测**不在用户 PATH 里**，PowerShell 下直接敲 ``lark-cli`` 会
  ``command not recognized``。所以先 ``shutil.which`` 探测，探测不到就回退到
  硬编码的安装位置——这是本次修复的核心回归点，有对应的单测守着。

退出码语义：
  0  预检通过（identity_ready 与 bot_identity 均非 fail/warn）
  1  预检不通过（凭据不可用，或 doctor 输出缺必需检查项，stderr 给出可操作修复步骤）
  2  用法错误（argparse 自身）

用法：
  python scripts/preflight.py# 人类可读输出
  python scripts/preflight.py --json     # 机器可读结果，供 automation 消费
  python scripts/preflight.py --quiet    # 只在失败时输出（成功静默，退出码 0）
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# 复用项目既有的人话错误体系（aiweekly.errors），不另写一套错误码/打印逻辑
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aiweekly.errors import UserFacingError, print_error  # noqa: E402

# 宿主连接器安装目录（lark-cli 不在 PATH 时回退到这里）
_CLI_DIR = Path.home() / ".workbuddy" / "binaries" / "node" / "cli-connector-packages"

# 飞书「以机器人身份发消息」失败时的错误码，用于把技术故障翻译成人话
_FEISHU_BOT_CODE = 20140

# doctor 输出里我们关心的三项检查 -> 该项不通时的人话含义
_CHECK_LABELS = {
    "identity_ready": "飞书身份未就绪",
    "bot_identity": "飞书 bot 身份未就绪",
    "app_resolved": "飞书应用凭据无法解析",
}

# 判定推送成败所**必需**的检查项。键不在 checks 里即视为预检失败——
# 缺键说明 doctor 的输出结构变了，我们对凭据可用性其实一无所知，
# 不能因为「没看到 fail」就报「已通过」。见 evaluate()。
_REQUIRED_CHECKS = ("identity_ready", "bot_identity", "app_resolved")

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2


class PreflightError(UserFacingError):
    """预检失败。用项目统一的 ERR-* 码 + 解决步骤，CLI 侧走 print_error 输出。"""


def resolve_lark_cli() -> str | None:
    """定位 ``lark-cli`` 可执行文件，返回命令字符串；找不到返回 ``None``。

    先 ``shutil.which`` 走 PATH，再回退到宿主连接器安装目录。
    Windows 下必须用 ``.cmd`` 后缀——目录里那个无后缀的 ``lark-cli`` 是给
    sh/Git Bash 用的脚本，Windows 上直接执行会失败。
    """
    found = shutil.which("lark-cli")
    if found:
        return found

    if os.name == "nt":
        candidate = _CLI_DIR / "lark-cli.cmd"
    else:
        candidate = _CLI_DIR / "lark-cli"
    if candidate.is_file():
        return str(candidate)
    return None


def run_doctor(cli_cmd: str) -> tuple[dict, str]:
    """执行 ``lark-cli doctor``，返回 ``(解析后的 JSON, 原始 stdout)``。

    Windows 的 ``.cmd`` 批处理会把 Node 的警告打到 stderr（噪音），
    故只取 stdout 解析，stderr 仅在 JSON 解析失败时作为诊断信息回传。

    必须显式传 ``env``：``.cmd`` 是批处理，它要靠 PATH 找到 ``node.exe`` 才能
    执行 shim。若父进程 PATH 为空且走的是回退路径，子进程会因找不到 node 而
    什么都不输出——那正是本脚本要防的场景，却会先把自己弄崩。
    """
    env = os.environ.copy()
    # Windows 上补回 PATH 里必然存在的 System32，避免 node 定位失败。
    # 注意：Windows 环境变量名**不区分大小写**，不同 shell / 沙箱里可能是
    # ``SystemRoot`` 或 ``SYSTEMROOT``，因此这里大小写无关地取值，
    # 否则取不到会拼出一个空路径，反而制造新问题。
    if os.name == "nt" and env.get("PATH"):
        windows_root = (
            env.get("SystemRoot") or env.get("SYSTEMROOT")
            or env.get("windir") or env.get("WINDIR")
            or r"C:\Windows"
        )
        system32 = os.path.join(windows_root, "System32")
        parts = [p for p in env["PATH"].split(os.pathsep) if p]
        if not any(p.lower() == system32.lower() for p in parts):
            parts.append(system32)
            env["PATH"] = os.pathsep.join(parts)
    proc = subprocess.run(
        [cli_cmd, "doctor"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
    )
    raw = (proc.stdout or "").strip()
    try:
        return json.loads(raw), raw
    except json.JSONDecodeError as e:
        detail = (proc.stderr or "").strip() or raw or "(无输出)"
        raise PreflightError(
            "ERR-FS-CLI-002",
            "lark-cli doctor 输出无法解析为 JSON",
            ["确认 lark-cli 版本：lark-cli --version",
             "手动跑一次看原始输出：lark-cli doctor",
             f"若输出被环境变量污染，可清空 LARK_* 相关变量后重试"],
            verbose=f"JSONDecodeError: {e} / stdout+stderr={detail[:400]}",
        )


def collect_checks(doctor: dict) -> dict:
    """把 doctor 的 ``checks`` 数组转成 ``{name: {status, message, hint}}``。"""
    out = {}
    for item in doctor.get("checks") or []:
        name = item.get("name")
        if name:
            out[name] = item
    return out


def evaluate(checks: dict) -> list[str]:
    """按检查项返回问题列表；空列表表示通过。

    判定规则：
      * **三个必需键缺任一即 fail** —— 缺键意味着无法判断凭据可用性，
        此时「没有发现问题」不等于「没问题」，而是「没看清」。
        旧实现对缺键用 ``.get(...) or {}`` 兜底，``status`` 取到 None，
        三条if 全部不进分支 -> 静默绿灯。只要 lark-cli 升级改个字段名，
        预检就会永远显示「已通过」，比没有门禁更危险：它给出的是虚假的安全感。
      * ``identity_ready`` 为 fail —— 没有任何可用身份，推送必失败
      * ``bot_identity``为 warn/fail —— bot 凭据不可用，发消息会报 20140
      * ``app_resolved`` 为 fail —— app_id/app_secret 解析不出来
    """
    problems: list[str] = []

    # 反向断言：必需键必须齐备。缺键时 doctor 的输出结构可能变了（例如上游
    # 把 bot_identity 改名），此时任何 status 判断都建立在「键不存在」之上，
    # 不能当作通过——故此处与真实不通过同级处理。
    missing = [k for k in _REQUIRED_CHECKS if k not in checks]
    if missing:
        # 同时给出原始键名与中文释义：原始键名可直接拿去 grep / 对照上游 changelog，
        # 中文释义让用户不必理解内部字段就能读懂问题。
        detail = "、".join(f"{k}（{_CHECK_LABELS.get(k, k)}）" for k in missing)
        present = "、".join(sorted(checks)) or "（无）"
        problems.append(
            f"lark-cli doctor 输出缺少必需检查项：{detail}"
            f"（缺失 {len(missing)}/{len(_REQUIRED_CHECKS)} 项）。"
            f"通常是 lark-cli 升级后改了检查项名称或输出结构，不是你没登录——"
            f"请升级 lark-cli 后重跑；doctor 当前实际返回的检查项：{present}"
        )

    identity = checks.get("identity_ready") or {}
    if identity.get("status") == "fail":
        problems.append(
            f"{_CHECK_LABELS['identity_ready']}："
            f"{identity.get('message', 'no identity available')}"
        )

    bot = checks.get("bot_identity") or {}
    if bot.get("status") in ("warn", "fail"):
        problems.append(
            f"{_CHECK_LABELS['bot_identity']}："
            f"{bot.get('message', 'bot identity not ready')}。"
            f"bot 凭据不可用，消息推送会失败（错误码 {_FEISHU_BOT_CODE}）"
        )

    app = checks.get("app_resolved") or {}
    if app.get("status") == "fail":
        problems.append(
            f"{_CHECK_LABELS['app_resolved']}："
            f"{app.get('message', 'app not resolved')}"
        )

    return problems


def build_exit(problems: list[str]) -> int:
    """把问题列表转成退出码，并打印人话说明。空列表 -> 0。"""
    if not problems:
        return EXIT_OK

    steps = ["按顺序修复以下问题后重跑本脚本："]
    steps += [f"  {i + 1}. {p}" for i, p in enumerate(problems)]
    steps += [
        "",
        "常见修法：",
        "  * 登录 / 重新登录：lark-cli auth login",
        "  * 检查 app_id 与 app_secret 是否在 lark-cli 配置中且未过期",
        "  * 确认机器人的消息发送权限（im:message:send_as_bot）已开通",
    ]
    print_error(PreflightError(
        "ERR-FS-PREFLIGHT-001",
        f"飞书凭据预检未通过（{len(problems)} 项）",
        steps,
        verbose="; ".join(problems),
    ))
    return EXIT_FAIL


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="流水线启动前的飞书凭据预检（避免跑完 6 步才在推送步失败）",
    )
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON 结果")
    parser.add_argument("--quiet", action="store_true", help="只在失败时输出")
    args = parser.parse_args(argv)

    cli_cmd = resolve_lark_cli()
    if not cli_cmd:
        # 报错文案用「~形式」而非 _CLI_DIR 的真实展开：这份输出会进 CI 日志与
        # issue 贴图，带 C:/Users/<用户名>/ 会泄露本机目录结构。
        err = PreflightError(
            "ERR-FS-CLI-001",
            "找不到 lark-cli",
            ["确认宿主连接器已安装：ls ~/.workbuddy/binaries/node/cli-connector-packages",
             "或在 PATH 中提供 lark-cli"],
            verbose="shutil.which('lark-cli') -> None，且回退路径不存在",
        )
        if args.json:
            print(json.dumps({"ok": False, "problems": ["找不到 lark-cli"]},
                             ensure_ascii=False, indent=2))
        if not args.quiet:
            print_error(err)
        return EXIT_FAIL

    try:
        doctor, _raw = run_doctor(cli_cmd)
    except PreflightError as e:
        if args.json:
            print(json.dumps({"ok": False, "problems": [e.title]},
                             ensure_ascii=False, indent=2))
        if not args.quiet:
            print_error(e)
        return EXIT_FAIL

    checks = collect_checks(doctor)
    problems = evaluate(checks)
    rc = build_exit(problems) if problems else EXIT_OK

    if args.json:
        print(json.dumps({
            "ok": not problems,
            "exit_code": rc,
            # 只输出文件名：`cli_cmd` 是含用户名的本机绝对路径
            # （C:/Users/<用户名>/.workbuddy/...），本JSON 会被粘进 issue /
            # CI 日志，只留 basename 即可定位，泄露则会把本机目录结构带出去。
            "cli": Path(cli_cmd).name,
            "identity_ready": (checks.get("identity_ready") or {}).get("status"),
            "bot_identity": (checks.get("bot_identity") or {}).get("status"),
            "app_resolved": (checks.get("app_resolved") or {}).get("status"),
            "problems": problems,
        }, ensure_ascii=False, indent=2))
    elif not args.quiet and not problems:
        print("✅ 飞书凭据预检通过：identity_ready=pass / bot_identity=pass"
              "（推送可用）")

    return rc


if __name__ == "__main__":
    sys.exit(main())