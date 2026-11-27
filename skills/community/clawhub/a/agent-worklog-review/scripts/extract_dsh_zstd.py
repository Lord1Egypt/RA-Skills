#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解压 dsh 的 zstd 会话，提取真实用户任务补充元数据提取的不足。

环境无关：自动探测带 zstandard 的 Python；若无 zstd 则打印说明并优雅退出，
不中断主流程。也可由 run_all.py 用探测到的 Python 显式调用本脚本。

输出：$OUTPUT_DIR/dsh_zstd_tasks.jsonl
"""
import os, sys, json, glob, re, subprocess, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import all_homes, out_dir, ts, clean

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    zstd = None
    HAS_ZSTD = False

OUT = os.path.join(out_dir(), "dsh_zstd_tasks.jsonl")
SYSTEM_MARKERS = [
    "you are a code review", "你是代码审查", "subagent", "system prompt",
    "<instructions>", "# agents.md", "tool_result", "以下为系统",
]
dctx = zstd.ZstdDecompressor() if HAS_ZSTD else None


def valid(s):
    if not s or len(s) < 5:
        return False
    low = s.lower()
    return not any(m in low for m in SYSTEM_MARKERS)


def extract_one(fp):
    """从单个 zstd 会话提取 (prompt, ts, cwd)。"""
    sid = os.path.basename(os.path.dirname(fp))
    proj = os.path.basename(os.path.dirname(os.path.dirname(fp)))
    prompt = first_ts = cwd = ""
    try:
        with open(fp, "rb") as f:
            with dctx.stream_reader(f) as reader:
                raw = reader.read().decode("utf-8", errors="replace")
        for line in raw.splitlines():
            try:
                d = json.loads(line)
            except Exception:
                continue
            typ = d.get("type", "")
            data = d.get("data") or {}
            if typ == "session":
                if not cwd:
                    cwd = d.get("cwd", "")
                if not first_ts:
                    first_ts = str(d.get("createdAt", ""))
            if not first_ts:
                t = d.get("time")
                if t:
                    first_ts = str(t)
            # dsh 事件流：用户消息在 agent/inbox/spliced 的 data.inserted[].content[].text
            if typ == "agent/inbox/spliced":
                for item in data.get("inserted", []):
                    if item.get("role") == "user":
                        for c in item.get("content", []):
                            if isinstance(c, dict) and c.get("type") == "text":
                                t = clean(c.get("text", ""))
                                if valid(t):
                                    prompt = t
                                    break
                    if prompt:
                        break
            elif typ in ("message", "user_message", "conversation/user"):
                cont = data.get("content") or d.get("content")
                if isinstance(cont, list):
                    cont = " ".join(str(c.get("text", "")) for c in cont if isinstance(c, dict))
                if isinstance(cont, str):
                    t = clean(cont)
                    if valid(t) and not prompt:
                        prompt = t
            if prompt:
                break
    except Exception as e:
        print(f"  ERR {sid[:8]}: {str(e)[:80]}")
    return {
        "agent": "dsh-zstd", "session_id": sid, "project_dir": proj, "cwd": cwd,
        "title": prompt[:80] if prompt else "(未能提取用户任务)",
        "prompt": prompt, "timestamp": ts(first_ts), "source": "zstd",
    }


def main():
    if not HAS_ZSTD:
        # 输出空文件占位，保证下游链路文件齐全
        with open(OUT, "w", encoding="utf-8") as f:
            pass
        print("SKIP dsh zstd: 当前 Python 无 zstandard 模块。")
        print("  如需统计 dsh 压缩会话，请安装：pip install zstandard（或用 conda Python 运行本脚本）。")
        return
    files = []
    for h in all_homes():
        root = os.path.join(h, ".dsh", "sessions")
        if os.path.isdir(root):
            files += glob.glob(os.path.join(root, "**", "*.zstd"), recursive=True)
    print(f"zstd files: {len(files)}")
    rows = [extract_one(fp) for fp in files]
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ok = sum(1 for r in rows if r["prompt"])
    print(f"extracted {len(rows)} sessions, {ok} with prompt -> {OUT}")
    for r in rows[:8]:
        print(f"  [{r['project_dir'][:40]}] {r['title'][:80]}")


if __name__ == "__main__":
    main()
