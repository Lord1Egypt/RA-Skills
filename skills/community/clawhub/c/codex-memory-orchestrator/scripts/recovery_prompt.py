#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据恢复包生成 create_thread 提示词（Codex 新对话首条 user 消息）。

支持：
- --recovery-path <恢复包.md>：读取已有恢复包，生成“先读恢复包再续接”的提示词；
- 未提供恢复包时：用 --project / --thread-id 生成最小骨架提示词；
- --json：输出 {prompt, recovery_path, source} 便于程序使用。

全程本地，不做网络调用。
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
import time
from pathlib import Path

def build_prompt(recovery_path=None, project="", thread_id=""):
    ts = time.strftime("%Y-%m-%d %H:%M")
    proj = project or "未命名项目"
    tid = thread_id or proj
    if recovery_path and Path(recovery_path).exists():
        src = f"恢复包：{recovery_path}"
        read_hint = (f"第一步先读取恢复包文件：`{recovery_path}`，逐项理解“目标 / 已完成 / "
                     "关键决策与依据 / 下一步 / 未决与风险”。若有【待补充】项或状态与用户描述不一致，先向用户确认，不得臆造。")
    else:
        src = "骨架（未提供恢复包路径）"
        read_hint = "以用户在原会话中给出的目标与已完成内容为准；不清楚的地方先向用户确认。"
    prompt = (
        f"请继续承接原 Codex 对话：项目「{proj}」，原对话框 {tid}。\n"
        f"{read_hint}\n"
        f"承接后先用不超过 5 行向用户复述：当前目标、已完成、下一步、未决风险，确认后再执行下一步；"
        "不得丢失未决问题、关键数字与文件路径。完成后按 memory-orchestrator 规则做校验并保留长期记忆。\n"
        f"交接信息（生成于 {ts}）：{src}"
    )
    return prompt

def main():
    ap = argparse.ArgumentParser(description="生成 create_thread 提示词（恢复包承接）")
    ap.add_argument("--recovery-path", default="", help="恢复包 Markdown 路径（已有）")
    ap.add_argument("--project", default="", help="项目名")
    ap.add_argument("--thread-id", default="", help="原对话框 ID")
    ap.add_argument("--json", action="store_true", help="输出 JSON {prompt,...}")
    args = ap.parse_args()

    recovery_path = args.recovery_path.strip()
    if recovery_path and not Path(recovery_path).exists():
        print(json.dumps({"ok": False, "error": f"恢复包不存在: {recovery_path}"}, ensure_ascii=False))
        raise SystemExit(2)

    prompt = build_prompt(recovery_path or None, args.project, args.thread_id)
    if args.json:
        print(json.dumps({
            "ok": True,
            "prompt": prompt,
            "recovery_path": recovery_path or None,
            "project": args.project or "",
            "thread_id": args.thread_id or "",
            "source": "recovery_prompt.py",
        }, ensure_ascii=False, indent=2))
    else:
        print(prompt)

if __name__ == "__main__":
    main()
