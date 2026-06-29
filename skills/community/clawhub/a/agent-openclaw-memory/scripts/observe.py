"""
observe.py — 工具调用观察注册
在工具调用后注册观察数据到本地队列，由 heartbeat 批量处理。

用法: python scripts/observe.py --hook post_tool_use --tool edit --input '...' --output '...'
      echo '{"hookType":"post_tool_use","toolName":"edit",...}' | python scripts/observe.py --stdin
"""
import _suppress_windows

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

OBSERVE_QUEUE = Path.home() / ".openclaw" / "observe_queue.jsonl"
MAX_QUEUE_SIZE = 5000  # 队列最大行数，超出则轮替


def observe(hook_type: str, tool_name: str = None,
            tool_input: str = None, tool_output: str = None,
            user_prompt: str = None, session_id: str = None):
    """注册一条观察（追加到队列，不阻塞）"""
    # 截断大内容
    if tool_input and len(tool_input) > 4000:
        tool_input = tool_input[:4000] + "\n[...截断]"
    if tool_output and len(tool_output) > 4000:
        tool_output = tool_output[:4000] + "\n[...截断]"
    if user_prompt and len(user_prompt) > 2000:
        user_prompt = user_prompt[:2000] + "\n[...截断]"

    entry = {
        "hookType": hook_type,
        "toolName": tool_name,
        "toolInput": tool_input,
        "toolOutput": tool_output,
        "userPrompt": user_prompt,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sessionId": session_id or os.environ.get("OPENCLAW_SESSION_ID", "unknown"),
    }

    # 确保目录存在
    OBSERVE_QUEUE.parent.mkdir(parents=True, exist_ok=True)

    # 追加到队列
    with open(OBSERVE_QUEUE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 检查队列大小，超出则轮替
    size = OBSERVE_QUEUE.stat().st_size
    if size > 1024 * 1024:  # 1MB 上限
        rotate_queue()


def rotate_queue():
    """队列轮替：备份当前队列，重建空队列"""
    backup = OBSERVE_QUEUE.with_suffix(".bak")
    if OBSERVE_QUEUE.exists():
        OBSERVE_QUEUE.replace(backup)
        OBSERVE_QUEUE.write_text("", encoding="utf-8")


def process_queue():
    """处理队列（调用 compress.py 压缩后索引到 Qdrant）"""
    import subprocess
    from pathlib import Path

    compress_script = Path(__file__).parent / "compress.py"

    result = subprocess.run(
        ["python", str(compress_script), "--process-queue"],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return result.stderr.strip()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--hook", help="Hook 类型 (post_tool_use, prompt_submit, ...)")
    parser.add_argument("--tool", help="工具名")
    parser.add_argument("--input", help="工具输入")
    parser.add_argument("--output", help="工具输出")
    parser.add_argument("--prompt", help="用户提示")
    parser.add_argument("--session", help="会话 ID")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取 JSON")
    parser.add_argument("--process", action="store_true", help="处理队列中的观察")
    opts = parser.parse_args()

    if opts.process:
        result = process_queue()
        print(result)
        return

    if opts.stdin:
        input_str = sys.stdin.read()
        if input_str.strip():
            data = json.loads(input_str)
            if isinstance(data, list):
                for item in data:
                    observe(
                        item.get("hookType", "unknown"),
                        item.get("toolName"),
                        json.dumps(item.get("toolInput"), ensure_ascii=False) if isinstance(item.get("toolInput"), dict) else str(item.get("toolInput", "")),
                        str(item.get("toolOutput", "")),
                        str(item.get("userPrompt", "")),
                        item.get("sessionId"),
                    )
                print(f"已注册 {len(data)} 条观察")
            else:
                observe(
                    data.get("hookType", "unknown"),
                    data.get("toolName"),
                    json.dumps(data.get("toolInput"), ensure_ascii=False) if isinstance(data.get("toolInput"), dict) else str(data.get("toolInput", "")),
                    str(data.get("toolOutput", "")),
                    str(data.get("userPrompt", "")),
                    data.get("sessionId"),
                )
                print("已注册 1 条观察")
        return

    observe(
        opts.hook or "unknown",
        opts.tool,
        opts.input,
        opts.output,
        opts.prompt,
        opts.session,
    )
    print("已注册 1 条观察")


if __name__ == "__main__":
    main()


