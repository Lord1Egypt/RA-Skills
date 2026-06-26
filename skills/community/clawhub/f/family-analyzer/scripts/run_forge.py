#!/usr/bin/env python3
"""
soul-forge: Agent-friendly pipeline runner

用法（供 OpenClaw agent 调用）：
  python3 run_forge.py --file /path/to/chat.json        # 完整运行
  python3 run_forge.py --file /path/to/chat.json --stage 1,2   # 指定阶段
  python3 run_forge.py --status                          # 查看当前进度
  python3 run_forge.py --resume                          # 从断点继续
  python3 run_forge.py --soul-only                       # 只生成 soul，跳过 persona
  python3 run_forge.py --persona-only                    # 跳过 soul，只生成 persona

输出约定（agent 解析用）：
  [STAGE:N:START]  阶段N开始
  [STAGE:N:DONE]   阶段N完成
  [PROGRESS:N/M]   进度
  [OUTPUT:path]    生成文件路径
  [ERROR:msg]      错误
  [DONE]           全部完成
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ── 路径 ──────────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
PIPELINE_DIR = SKILL_DIR / "pipeline"
PROMPTS_DIR = SKILL_DIR / "prompts"

# 输出目录：优先用环境变量，否则在 skill 目录旁边建 output/
OUTPUT_DIR = Path(os.environ.get("SOUL_FORGE_OUTPUT", SKILL_DIR.parent / "soul-forge-output"))
STATE_FILE = OUTPUT_DIR / ".forge_state.json"

STAGES = {
    1: ("01_parse.py",    "解析聊天记录"),
    2: ("02_denoise.py",  "去噪 + 对话分块"),
    3: ("03_extract.py",  "LLM 批量提取行为模式"),
    4: ("04_synthesize.py","合成 soul.md + persona"),
}

# ── 状态管理 ──────────────────────────────────────────────────────────────────
def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"completed_stages": [], "source_file": None, "started_at": None, "outputs": []}

def save_state(state: dict):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def emit(tag: str, msg: str = ""):
    """输出 agent 可解析的标记行"""
    line = f"[{tag}]" + (f" {msg}" if msg else "")
    print(line, flush=True)

# ── 运行单个阶段 ───────────────────────────────────────────────────────────────
def run_stage(stage_num: int, source_file: Path, extra_args: list = None) -> bool:
    script_name, label = STAGES[stage_num]
    script_path = PIPELINE_DIR / script_name

    emit(f"STAGE:{stage_num}:START", label)

    env = os.environ.copy()
    env["SOUL_FORGE_SOURCE"] = str(source_file)
    env["SOUL_FORGE_OUTPUT"] = str(OUTPUT_DIR)
    env["PYTHONPATH"] = str(PIPELINE_DIR)

    cmd = [sys.executable, str(script_path)]
    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, env=env, text=True)

    if result.returncode != 0:
        emit(f"STAGE:{stage_num}:FAIL", f"退出码 {result.returncode}")
        return False

    emit(f"STAGE:{stage_num}:DONE", label)
    return True

# ── 主流程 ────────────────────────────────────────────────────────────────────
def cmd_run(args):
    source_file = Path(args.file).expanduser().resolve()
    if not source_file.exists():
        emit("ERROR", f"文件不存在：{source_file}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    state = load_state()
    state["source_file"] = str(source_file)
    state["started_at"] = datetime.now().isoformat()
    save_state(state)

    # 决定运行哪些阶段
    if args.stages:
        stages = sorted(int(s) for s in args.stages.split(","))
    elif args.persona_only:
        stages = [4]
    elif args.soul_only:
        stages = [1, 2, 3, 4]  # stage 4 will use --soul-only flag
    else:
        stages = [1, 2, 3, 4]

    total = len(stages)
    for i, stage_num in enumerate(stages, 1):
        emit(f"PROGRESS", f"{i}/{total} 阶段{stage_num}")

        extra = []
        if stage_num == 4:
            if args.soul_only:
                extra = ["--soul-only"]
            elif args.persona_only:
                extra = ["--persona-only"]

        ok = run_stage(stage_num, source_file, extra)
        if not ok:
            emit("ERROR", f"阶段{stage_num}失败，中止")
            sys.exit(1)

        state["completed_stages"].append(stage_num)
        save_state(state)

    # 列出生成的文件
    output_files = list(OUTPUT_DIR.glob("*.md"))
    for f in sorted(output_files):
        emit("OUTPUT", str(f))
        state["outputs"].append(str(f))

    save_state(state)
    emit("DONE", f"共生成 {len(output_files)} 个文件 → {OUTPUT_DIR}")

def cmd_status(args):
    state = load_state()
    if not state["source_file"]:
        print("尚未运行过 soul-forge")
        return

    print(f"源文件：{state['source_file']}")
    print(f"开始时间：{state['started_at']}")
    print(f"已完成阶段：{state['completed_stages']}")
    remaining = [s for s in [1,2,3,4] if s not in state["completed_stages"]]
    print(f"待完成阶段：{remaining}")
    if state["outputs"]:
        print("输出文件：")
        for f in state["outputs"]:
            print(f"  {f}")

def cmd_resume(args):
    state = load_state()
    if not state["source_file"]:
        emit("ERROR", "没有可恢复的任务，请先用 --file 指定源文件")
        sys.exit(1)

    completed = set(state["completed_stages"])
    remaining = [s for s in [1, 2, 3, 4] if s not in completed]

    if not remaining:
        emit("DONE", "所有阶段已完成，无需恢复")
        return

    print(f"从阶段 {remaining[0]} 继续…")
    source_file = Path(state["source_file"])

    for i, stage_num in enumerate(remaining, 1):
        emit(f"PROGRESS", f"{i}/{len(remaining)} 阶段{stage_num}（恢复）")
        ok = run_stage(stage_num, source_file)
        if not ok:
            emit("ERROR", f"阶段{stage_num}失败")
            sys.exit(1)
        state["completed_stages"].append(stage_num)
        save_state(state)

    output_files = list(OUTPUT_DIR.glob("*.md"))
    for f in sorted(output_files):
        emit("OUTPUT", str(f))
    emit("DONE", f"恢复完成，共 {len(output_files)} 个文件")

# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="soul-forge pipeline runner")
    sub = parser.add_subparsers(dest="cmd")

    # run（默认）
    run_p = parser.add_argument_group("run options")
    parser.add_argument("--file", "-f", help="聊天记录文件路径（JSON）")
    parser.add_argument("--stages", help="指定阶段，逗号分隔，如 1,2 或 3,4")
    parser.add_argument("--soul-only", action="store_true", help="只生成 soul.md，跳过 persona")
    parser.add_argument("--persona-only", action="store_true", help="跳过 soul，只生成/更新 persona")
    parser.add_argument("--status", action="store_true", help="查看当前进度")
    parser.add_argument("--resume", action="store_true", help="从断点继续")

    args = parser.parse_args()

    if args.status:
        cmd_status(args)
    elif args.resume:
        cmd_resume(args)
    elif args.file:
        cmd_run(args)
    else:
        parser.print_help()
        sys.exit(1)
