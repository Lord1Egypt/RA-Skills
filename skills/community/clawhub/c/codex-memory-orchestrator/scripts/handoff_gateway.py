#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键新对话承接：按 Agent 能力矩阵生成/登记恢复包并注入续接文本。

分级（references/agent-gateways.md）：
- full_auto   codex：在本 app 内经 create_thread/fork_thread 同目录新建，把续接文本作为首条 user 消息；
- deep_link   支持“新窗口 + 注入文本”的 Agent：打开深链并把续接文本复制到剪贴板；
- manual      只支持新窗口：生成恢复包 + 复制到剪贴板 + 打开目标应用/项目目录，用户粘贴。

全程本地：不做任何网络调用。跳转第三方 Agent 属于本机应用启动与剪贴板注入。
"""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
STATE = Path(os.environ.get("CODEX_MEMORY_STATE", Path.home() / ".codex" / "memory" / "state.json"))
AUDIT = Path(os.environ.get("CODEX_AUDIT_LOG", Path.home() / ".codex" / "audit.log"))

# capability 矩阵：agent -> (capability, scheme_or_None, app_or_None, 说明)
CAPS = {
    "codex": {"capability": "full_auto", "scheme": None, "app": None,
              "hint": "在本 app 内调用 create_thread/fork_thread（同目录），把续接文本作为新线程首条 user 消息，并打开 codex://threads/<新threadId>"},
    "claude": {"capability": "deep_link", "scheme": "claude://new?text=", "app": "Claude",
               "hint": "新窗口可带初始文本 → open 深链后把续接文本复制到剪贴板"},
    "cursor": {"capability": "manual", "scheme": None, "app": "Cursor",
               "hint": "无公开的注入初始文本 API → 新窗口 + 剪贴板承接"},
    "cline": {"capability": "manual", "scheme": None, "app": "Cline",
              "hint": "VSCode 扩展，无独立深链 → 打开项目并复制承接文本"},
    "windsurf": {"capability": "manual", "scheme": None, "app": "Windsurf",
                 "hint": "无公开注入 API → 新窗口 + 剪贴板承接"},
    "chatgpt": {"capability": "manual", "scheme": None, "app": "ChatGPT",
                "hint": "网页/桌面版无注入文本 API → 生成恢复包 + 剪贴板，用户粘贴"},
    "local": {"capability": "manual", "scheme": None, "app": None,
              "hint": "其他本机 Agent：只生成恢复包并复制承接文本到剪贴板"},
}
UNKNOWN = {"capability": "manual", "scheme": None, "app": None,
           "hint": "未知 Agent：只生成恢复包 + 复制剪贴板，必要时用 --open-app 指定打开目标应用"}


def load_state():
    d = {}
    if STATE.exists():
        try:
            d.update(json.loads(STATE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return d


def _dialog_slice(d, agent, project, thread_id):
    dialogs = d.get("dialogs") or {}
    if not isinstance(dialogs, dict):
        return None
    for key, s in dialogs.items():
        if not isinstance(s, dict):
            continue
        owner = s.get("owner") or s.get("agent") or ("codex" if "@" not in key else key.split("@")[-1])
        if owner != agent:
            continue
        if thread_id and s.get("thread_id") != thread_id:
            continue
        if project and s.get("active_project") != project:
            continue
        return s
    return None


def make_recovery_path(project, out_dir):
    date = datetime.now().strftime("%Y%m%d")
    return Path(out_dir) / f"恢复包-{project}-{date}.md"


def make_skeleton(agent, project, thread_id, ctx, recovery_path):
    ts = time.strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")
    proj = project or ctx.get("active_project") or "未命名项目"
    tid = thread_id or ctx.get("thread_id") or ""
    turns = ctx.get("turn_count") if ctx else None
    turn_line = (f"{turns} 轮" if turns is not None else "未知") + ("（实时自检轮数，非对话正文）" if turns is not None else "（超出本机可读范围）")
    return f"""# 恢复包：{proj}

- 会话日期：{today}
- 最近一次更新：{ts}
- 状态：待核对
- 来源 Agent：{agent}
- 对话框：{tid}（{turn_line}）
- 本机路径：{recovery_path}

## 1 目标
【待补充】本次任务目标。

## 2 已完成
- 【待补充】关键成果 1（含文件路径）
- 【待补充】关键成果 2

## 3 关键决策与依据
| 决策 | 依据 | 状态 |
|---|---|---|
| 【待补充】 | 用户要求/规范/经验 | 待确认 |

## 4 下一步（可执行）
- [ ] 【待补充】具体动作 1（命令或文件路径）
- [ ] 【待补充】具体动作 2

## 5 未决 / 风险
- 【待补充】需用户确认事项
- 【待补充】环境或数据风险

## 6 交接
- 交接对象：新对话 / 用户
- 验证方式：读恢复包后向用户复述 5 行摘要
- 提示：以上【待补充】项请先在原对话框内完成“总结/恢复/交接”手续后填写，再粘贴到新对话。
"""


def _clip_copy(content):
    if os.environ.get("HANDOFF_NO_CLIPBOARD"):
        return False, "env HANDOFF_NO_CLIPBOARD=1 跳过剪贴板"
    try:
        if sys.platform == "darwin":
            p = subprocess.run(["pbcopy"], input=content.encode("utf-8"))
        elif os.name == "nt":
            ps = ("powershell", "-NoProfile", "-Command",
                  "Set-Clipboard -Value ([Console]::In.ReadToEnd())")
            p = subprocess.run(ps, input=content.encode("utf-8"), shell=False)
        elif shutil.which("xclip"):
            p = subprocess.run(["xclip", "-selection", "clipboard"], input=content.encode("utf-8"))
        elif shutil.which("wl-copy"):
            p = subprocess.run(["wl-copy"], input=content.encode("utf-8"))
        else:
            return False, "未找到可用剪贴板工具（pbcopy/xclip/wl-copy），仅保留恢复包"
        if p.returncode == 0:
            return True, "已复制续接文本到剪贴板"
        return False, f"剪贴板命令退出码 {p.returncode}"
    except Exception as e:
        return False, f"剪贴板失败：{e}"


def _app_available(app):
    """目标应用在本机是否可被打开（只检测，不启动）。macOS 用 LaunchServices 的 -Ra。"""
    if not app:
        return False
    try:
        if sys.platform == "darwin":
            r = subprocess.run(["open", "-Ra", app], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=15)
            return r.returncode == 0
        if os.name == "nt":
            return bool(shutil.which(app))
        return bool(shutil.which(app))
    except Exception:
        return False


def _open_cmd(app):
    if not app:
        return None
    if sys.platform == "darwin":
        return ["open", "-a", app]
    if os.name == "nt":
        return ["cmd", "/c", "start", "", app]
    return ["xdg-open", app]


def _run_open(cmd, dry_run):
    if dry_run:
        return True, "dry-run（未真实打开）: " + " ".join(cmd)
    try:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True, "已打开目标应用"
    except Exception as e:
        return False, f"打开目标应用失败：{e}"


def _register_index(project, path, dry_run):
    if dry_run:
        return True, f"dry-run 跳过登记索引；应登记 {project} -> {path}"
    r = subprocess.run([sys.executable, str(SKILL_DIR / "scripts" / "recovery.py"),
                        "--add", project, str(path)],
                       capture_output=True, text=True)
    if r.returncode == 0:
        return True, r.stdout.strip()
    return False, r.stderr.strip() or r.stdout.strip()


def _audit(agent, thread_id, project, recovery, capability, dry_run, ok):
    try:
        AUDIT.parent.mkdir(parents=True, exist_ok=True)
        line = (f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] memory-orchestrator handoff "
                f"agent={agent} thread={thread_id} project={project} recovery={recovery} "
                f"capability={capability} mode={'dry-run' if dry_run else 'real'} result={'ok' if ok else 'fail'}\n")
        with open(str(AUDIT), "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass




def _urlquote(s):
    """极简本地百分号编码（纯 stdlib 手写，无网络库），用于深链注入续接文本。"""
    out = []
    safe = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~/")
    for b in s.encode("utf-8"):
        ch = chr(b)
        if ch in safe:
            out.append(ch)
        else:
            out.append("%%%02X" % b)
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="一键新对话承接（能力矩阵降级）")
    ap.add_argument("--agent", default=os.environ.get("MEMORY_AGENT") or "codex", help="目标 Agent 名")
    ap.add_argument("--project", default="", help="项目名")
    ap.add_argument("--thread-id", default="", help="对话框 ID")
    ap.add_argument("--recovery-path", default=None, help="已有恢复包路径（缺省自动生成骨架）")
    ap.add_argument("--out-dir", default=str(Path.home() / ".codex" / "memory"), help="自动生成恢复包的目录（默认 $CODEX_HOME/memory）")
    ap.add_argument("--open-app", default=None, help="打开的目标应用名（覆盖能力矩阵默认）")
    ap.add_argument("--dry-run", action="store_true", help="只打印命令，不真实打开应用/不写审计")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    caps = CAPS.get(args.agent, UNKNOWN)
    capability = caps["capability"]
    app = args.open_app or caps.get("app")
    if capability == "deep_link" and not _app_available(app):
        capability = "manual"
        app = None
        caps = {"capability": "manual", "scheme": None, "app": None,
                "hint": "目标 Agent 应用未安装或未注册 deep_link，已降级为生成恢复包 + 剪贴板承接"}

    d = load_state()
    ctx = _dialog_slice(d, args.agent, args.project, args.thread_id) or {}

    if args.recovery_path:
        rp = Path(args.recovery_path)
        if not rp.exists():
            print(json.dumps({"ok": False, "error": f"恢复包不存在: {rp}"}, ensure_ascii=False))
            sys.exit(2)
        content = rp.read_text(encoding="utf-8")
    else:
        rp = make_recovery_path(args.project or ctx.get("active_project") or "未命名项目", args.out_dir)
        rp.parent.mkdir(parents=True, exist_ok=True)
        content = make_skeleton(args.agent, args.project, args.thread_id, ctx, rp)
        if not args.dry_run:
            rp.write_text(content, encoding="utf-8")

    copied = False
    copy_note = ""
    if not args.dry_run:
        copied, copy_note = _clip_copy(content)

    registered = False
    reg_note = ""
    # v1.9.2：原有 `if args.recovery_path and not args.dry_run: pass` 是空分支（死逻辑），
    # 实际由下一行无条件登记索引；此处保留注释说明意图，不再保留空 if。
    registered, reg_note = _register_index(args.project or ctx.get("active_project") or "未命名项目", rp, args.dry_run)

    open_cmd = _open_cmd(app)
    opened = False
    open_note = ""
    if open_cmd and not (args.agent == "codex" and capability == "full_auto"):
        opened, open_note = _run_open(open_cmd, args.dry_run)

    scheme = caps.get("scheme")
    deep_link = None
    deep_note = ""
    if scheme:
        _link = scheme + _urlquote(content)
        # v1.9.2：URL 长度保护——长恢复包编进 deep link 会超浏览器/OS 限制（约 8KB），
        # 超限时不给链接，改为提示用剪贴板内容粘贴，避免用户点开一个截断的对话。
        if len(_link) > 7500:
            deep_note = "恢复包过长（%d 字符），已跳过 deep link，请用剪贴板内容手动粘贴" % len(_link)
        else:
            deep_link = _link

    hint = caps["hint"]
    action = "full_auto_codex" if (args.agent == "codex") else capability
    if capability == "manual":
        action = "生成恢复包 + 剪贴板" + (" + 打开目标应用" if open_cmd else "")

    ok = bool(rp.exists() or args.dry_run)
    if not args.dry_run:
        _audit(args.agent, args.thread_id, args.project or ctx.get("active_project") or "",
               str(rp), capability, args.dry_run, ok)

    result = {
        "ok": ok,
        "agent": args.agent,
        "capability": capability,
        "action": action,
        "recovery_path": str(rp),
        "recovery_exists": rp.exists(),
        "copied": copied,
        "clipboard_note": copy_note,
        "registered": registered,
        "register_note": reg_note,
        "deep_link": deep_link,
        "open_command": [" ".join(open_cmd)] if open_cmd else None,
        "opened": opened,
        "open_note": open_note,
        "hint": hint,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"承接包能力={result['capability']} 动作={result['action']}")
        print(f"  恢复包: {rp}（{'存在' if result['recovery_exists'] else 'dry-run 未落盘'}）")
        print(f"  剪贴板: {'✓ ' + copy_note if copied else ('（dry-run，未复制）' if args.dry_run else copy_note)}")
        print(f"  登记: {reg_note}")
        if deep_link:
            print(f"  深链: {deep_link}")
        if open_cmd:
            print(f"  打开命令: {' '.join(open_cmd)} → {open_note}")
        print(f"  能力说明: {hint}")


if __name__ == "__main__":
    main()
