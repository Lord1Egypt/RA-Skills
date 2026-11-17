#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""provision_agent_responsiveness.py —— 「重活外派 · 随时应答」规则块的跨平台幂等落地器。

做什么
    探测本机已有的 Agent 环境，把一份平台无关的作业纪律规则块写进「能被 Agent 读到」的位置：
      * Hermes        -> <HERMES_HOME>/SOUL.md（含各 profile 的 SOUL.md）
      * Claude Code   -> ~/.claude/CLAUDE.md（全局指令文件）
    这两条是有实测把握的落点。其余平台（Codex / Cursor / WorkBuddy / 未知平台）
    一律不猜配置文件路径，改为**导出一份可直接粘贴的规则块**（默认 ./agent-ops-rules.md），
    由用户自己粘到系统提示 / 自定义指令里。

安全约定（硬要求）
    * 默认 **dry-run**，只报告将要做什么，不写任何文件；加 `--apply` 才真正写入。
    * 写入前自动备份原文件：<文件名>.bak-agent-ops-<时间戳>。
    * 幂等：规则块用 `<!-- agent-ops-rules:v1 -->` … `<!-- /agent-ops-rules -->` 标记包裹；
      重复执行不重复写、不覆盖用户已有内容（只替换自己标记过的区块）。
    * 纯标准库、零第三方依赖；pathlib 全路径处理，Windows / macOS / Linux 通用。

用法
    python3 provision_agent_responsiveness.py                 # 预演（不写盘）
    python3 provision_agent_responsiveness.py --apply         # 真正写入 + 导出可粘贴规则块
    python3 provision_agent_responsiveness.py --apply --out ~/my-rules.md
    python3 provision_agent_responsiveness.py --hermes-home /tmp/fake-hermes   # 指定位置探测
    python3 provision_agent_responsiveness.py --json --apply

退出码
    0  正常（dry-run 或已应用）
    1  参数 / IO 错误
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------- 常量

RULES_START = "<!-- agent-ops-rules:v1 -->"
RULES_END = "<!-- /agent-ops-rules -->"
RULES_VERSION = 1

# v1.0 版（Hermes 专版）铁律块的特征字样：用于识别「旧版已装、但没带标记」的情况
LEGACY_MARK = "重活派子代理"

EXPORT_FILE_NAME = "agent-ops-rules.md"

# 内嵌兜底副本：找不到 templates/agent-ops-rules.md 时使用（与模板内容一致）
EMBEDDED_RULES = """<!-- agent-ops-rules:v1 -->
## ⚡ 重活外派 · 随时应答（作业纪律）

**角色定位**：主脑 = 规划 · 统筹 · 验收 · 整合结论；执行一律下沉子代理。

0. **先判级再动手（四级分流）**
   - **L0 问答**（问一句答一句）→ 直接答，**不派**，1 轮出结果。
   - **L1 单步快活**（≤1 次工具调用且 ≤20 秒）→ 直接干，不派。
   - **L2 多步 / 长活 / 批量多条目 / 联网抓取 / 多文件** → **一律派子代理**，主脑不亲自跑。
   - **L3 需用户拍板**（口径未定、涉及取舍/预算/对外承诺）→ 先回一句“这要您定 X”，**不闷头干**。
1. **重活一律出主脑**：L2 全部交给平台的子代理 / 后台任务工具；主脑只做拆解、派活、验收、汇报。
2. **派完立刻收尾让出对话**：派出去之后立刻回一句“已派出（谁在干什么）”，然后结束本回合——结果由平台送回。
   **禁止在主脑里干等或轮询**（干等 = 没派，用户就没人应答）。
3. **长命令不许堵主脑**：任何可能超过 60 秒的命令 / 脚本，放进后台执行并在完成时通知；
   前台长命令会把整个回合占死，用户插话只能排队。
4. **子代理只回收结论**：中间过程 / 大日志不许灌回主脑，只要结论 + 产物路径 + 关键证据（大输出先落盘再筛）；
   整合分析由主脑做。
5. **用户插话最高优先**：用户任何时候说话，先立刻应一声（“收到，正在跑 X，完成后提交”），能答就答；
   答不了也必须先回，绝不让用户干等。
6. **需要提问的活留在主脑**：多数平台上子代理问不了人（没有向用户提问的通道）；口径未定、需用户确认的任务不派。
<!-- /agent-ops-rules -->
"""


def _reconfigure_stdout() -> None:
    """Windows 控制台/重定向到文件时避免中文编码炸掉。"""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass


# ---------------------------------------------------------------- 规则块


def load_rules(script_file: Path) -> tuple[str, str]:
    """返回 (规则块文本, 来源说明)。优先读包内模板，读不到就用内嵌副本。"""
    tpl = script_file.resolve().parent.parent / "templates" / EXPORT_FILE_NAME
    try:
        text = tpl.read_text(encoding="utf-8")
    except OSError:
        return EMBEDDED_RULES.strip("\n"), "内嵌副本（未找到 templates/%s）" % EXPORT_FILE_NAME
    if RULES_START not in text or RULES_END not in text:
        return EMBEDDED_RULES.strip("\n"), "内嵌副本（模板缺少标记）"
    return text.strip("\n"), "templates/%s" % EXPORT_FILE_NAME


def norm(text: str) -> str:
    """归一化用于比较：统一换行、去掉行尾空格、丢掉首尾空行。"""
    flat = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in flat.split("\n")).strip("\n")


def extract_block(text: str) -> str | None:
    """取出文件中已被标记的规则块（含标记行）。找不到返回 None。"""
    flat = text.replace("\r\n", "\n").replace("\r", "\n")
    start = flat.find(RULES_START)
    if start < 0:
        return None
    end = flat.find(RULES_END, start)
    if end < 0:
        return flat[start:]
    return flat[start:end + len(RULES_END)]


def insertion_index(text: str) -> int:
    """插入位置：跳过 YAML frontmatter，放在文件最前面（保证置顶）。"""
    flat = text.replace("\r\n", "\n").replace("\r", "\n")
    if flat.startswith("---"):
        lines = flat.split("\n")
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                # 插在 frontmatter 结束行之后
                return len("\n".join(lines[: i + 1])) + 1
    return 0


def plan_change(text: str, block: str) -> tuple[str, str]:
    """返回 (新文本, 动作)。动作 ∈ {NOCHANGE, UPDATE, INSERT, SKIP_LEGACY}。"""
    flat = text.replace("\r\n", "\n").replace("\r", "\n")
    existing = extract_block(text)
    if existing is not None:
        if norm(existing) == norm(block):
            return text, "NOCHANGE"
        return flat.replace(existing, block, 1), "UPDATE"
    if LEGACY_MARK in flat:
        return text, "SKIP_LEGACY"
    idx = insertion_index(flat)
    head, tail = flat[:idx], flat[idx:]
    sep = "" if (not head or head.endswith("\n")) else "\n"
    return head + sep + block + "\n\n" + tail.lstrip("\n"), "INSERT"


# ---------------------------------------------------------------- 目标探测


def default_hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME", "").strip()
    if env:
        return Path(env).expanduser()
    home = Path.home()
    if os.name == "nt":
        return home / "AppData" / "Local" / "hermes"
    for cand in (home / ".hermes", home / "AppData" / "Local" / "hermes"):
        if cand.is_dir():
            return cand
    return home / ".hermes"


def default_claude_dir() -> Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR", "").strip()
    if env:
        return Path(env).expanduser()
    return Path.home() / ".claude"


def discover(args: argparse.Namespace) -> tuple[list[dict], list[dict]]:
    """返回 (可写入的目标列表, 探测到的平台列表)。

    目标 dict: {"platform", "path", "scope"}
    平台 dict: {"platform", "root", "detected", "detail"}
    """
    targets: list[dict] = []
    platforms: list[dict] = []

    # --- Hermes：HERMES_HOME/SOUL.md + 各 profile 的 SOUL.md ---
    hh = Path(args.hermes_home).expanduser() if args.hermes_home else default_hermes_home()
    hh_detected = hh.is_dir()
    hh_detail = str(hh) if hh_detected else "未找到目录 %s" % hh
    platforms.append({"platform": "Hermes", "root": str(hh), "detected": hh_detected, "detail": hh_detail})
    if hh_detected:
        root_soul = hh / "SOUL.md"
        targets.append({"platform": "Hermes", "path": str(root_soul), "scope": "主目录 SOUL.md"})
        prof_dir = hh / "profiles"
        if prof_dir.is_dir():
            for child in sorted(prof_dir.iterdir()):
                if child.is_dir() and not child.name.startswith((".", "_")):
                    soul = child / "SOUL.md"
                    if soul.is_file():
                        targets.append(
                            {"platform": "Hermes", "path": str(soul), "scope": "profile %s" % child.name}
                        )

    # --- Claude Code：~/.claude/CLAUDE.md ---
    if args.claude_home:
        cd = Path(args.claude_home).expanduser()
        claude_detected = cd.is_dir()   # 显式指定目录：只认该目录，不被本机其它探测信号干扰
    else:
        cd = default_claude_dir()
        claude_detected = cd.is_dir() or (Path.home() / ".claude.json").is_file()

    platforms.append(
        {
            "platform": "Claude Code",
            "root": str(cd),
            "detected": claude_detected,
            "detail": (str(cd / "CLAUDE.md") if claude_detected else "未找到目录 %s" % cd),
        }
    )
    if claude_detected:
        targets.append({"platform": "Claude Code", "path": str(cd / "CLAUDE.md"), "scope": "全局指令文件"})

    return targets, platforms


# ---------------------------------------------------------------- 主流程


def backup(path: Path, stamp: str) -> Path:
    dest = path.with_name(path.name + ".bak-agent-ops-" + stamp)
    shutil.copy2(str(path), str(dest))
    return dest


def run(args: argparse.Namespace) -> int:
    script_file = Path(__file__).resolve()
    block, block_source = load_rules(script_file)
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    targets, platforms = discover(args)

    actions: list[dict] = []
    applied = False

    for t in targets:
        path = Path(t["path"])
        exists = path.is_file()
        old = path.read_text(encoding="utf-8") if exists else ""
        new, action = plan_change(old, block) if exists else (block + "\n", "CREATE")
        rec = {
            "platform": t["platform"],
            "scope": t["scope"],
            "path": str(path),
            "action": action,
            "existed": exists,
            "backup": None,
            "bytes_before": len(old),
            "bytes_after": len(new),
        }
        if action in ("CREATE", "INSERT", "UPDATE") and not args.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            if exists:
                rec["backup"] = str(backup(path, stamp))
            path.write_text(new, encoding="utf-8", newline="")
            applied = True
        actions.append(rec)

    # --- 可粘贴规则块的导出（探测不到平台时必做；--export 时强制） ---
    export_path = Path(args.out).expanduser() if args.out else (Path.cwd() / EXPORT_FILE_NAME)
    need_export = (not targets) or args.export
    export_rec = None
    if need_export:
        old_export = export_path.read_text(encoding="utf-8") if export_path.is_file() else ""
        export_action = "NOCHANGE" if old_export.strip() == block.strip() else ("UPDATE" if old_export else "CREATE")
        export_rec = {"path": str(export_path), "action": export_action}
        if export_action != "NOCHANGE" and not args.dry_run:
            export_path.parent.mkdir(parents=True, exist_ok=True)
            export_path.write_text(block + "\n", encoding="utf-8", newline="")
            applied = True

    # ---------------------------------------------------------- 输出
    if args.json_output:
        sys.stdout.write(
            json.dumps(
                {
                    "dryRun": bool(args.dry_run),
                    "rulesSource": block_source,
                    "rulesVersion": RULES_VERSION,
                    "platforms": platforms,
                    "targets": actions,
                    "export": export_rec,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        return 0

    mode = "DRY-RUN（预演，不写盘）" if args.dry_run else "APPLY（实写）"
    print("重活外派 · 随时应答 —— 规则块落地器 v%d" % RULES_VERSION)
    print("模式：%s  ｜ 规则块来源：%s" % (mode, block_source))
    print("")
    print("① 平台探测")
    for p in platforms:
        flag = "✅ 探测到" if p["detected"] else "— 未探测到"
        print("  %-12s %s  %s" % (p["platform"], flag, p["root"]))
    print("")
    print("② 落地目标")
    if not targets:
        print("  未检测到支持的平台（Hermes / Claude Code 都未探测到）→ 走「导出可粘贴规则块」路径。")
    else:
        for a in actions:
            line = "  [%s] %s（%s）" % (a["action"], a["path"], a["scope"])
            print(line)
            if a["backup"]:
                print("        备份：%s" % a["backup"])
            if a["action"] == "SKIP_LEGACY":
                print("        说明：检测到 v1.0 版规则块（无标记包裹），未自动改动——")
                print("              请手工删除旧块后重跑，或保留旧块（新版内容已并入）。")
    print("")
    print("③ 可粘贴规则块")
    if export_rec:
        print("  [%s] %s" % (export_rec["action"], export_rec["path"]))
        print("  用法：把该文件的全部内容粘到你的系统提示 / 自定义指令 / 项目规则里即生效。")
    else:
        print("  （已探测到可直接写入的平台，未导出。需要导出时加 --export）")
    print("")
    if args.dry_run:
        print("预演结束：未写入任何文件。确认无误后加 --apply 执行。")
    elif applied:
        print("完成：规则块已写入。重启对应 Agent 进程后生效（多数平台只在启动时读一次指令文件）。")
    else:
        print("完成：无改动（规则块已在位且为最新）。")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="provision_agent_responsiveness.py",
        description="跨平台幂等落地「重活外派 · 随时应答」规则块（默认 dry-run）。",
        epilog="示例：python3 provision_agent_responsiveness.py ｜ ... --apply ｜ ... --json",
    )
    ap.add_argument("--apply", action="store_true", help="真正写盘（不加则只预演）")
    ap.add_argument("--dry-run", action="store_true", help="显式预演（默认行为，便于脚本里写清意图）")
    ap.add_argument("--json", dest="json_output", action="store_true", help="以 JSON 输出")
    ap.add_argument("--export", action="store_true", help="无论是否探测到平台，都额外导出可粘贴规则块")
    ap.add_argument("--out", default="", help="导出路径（默认 ./%s）" % EXPORT_FILE_NAME)
    ap.add_argument("--hermes-home", default="", help="覆盖 Hermes 主目录（默认 $HERMES_HOME 或平台默认位置）")
    ap.add_argument("--claude-home", default="", help="覆盖 Claude Code 配置目录（默认 ~/.claude）")
    return ap


def main(argv: list[str] | None = None) -> int:
    _reconfigure_stdout()
    args = build_parser().parse_args(argv)
    if args.dry_run:
        args.apply = False
    args.dry_run = not args.apply
    try:
        return run(args)
    except OSError as exc:
        sys.stderr.write("错误：文件操作失败 —— %s\n" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
