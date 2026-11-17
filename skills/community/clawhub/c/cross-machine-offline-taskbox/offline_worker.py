#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""断网 Worker：读本地任务箱的待办任务，逐条调本机 Ollama 跑，结果写回任务箱。

断网可跑——模型权重在本地，Ollama 监听 127.0.0.1:11434，不触外网。
依赖：本地已 `ollama pull` 好模型；同目录下的 local_taskbox.py。

用法：
  python offline_worker.py                # 用默认模型
  python offline_worker.py --model qwen2.5:7b   # 指定模型，无需改代码
"""
import os
import subprocess
import sys
import argparse

import local_taskbox as tb

DEFAULT_MODEL = "deepseek-r1:7b"   # 默认模型；也可用 --model 临时指定
OLLAMA_CLI = "ollama"             # 若在 PATH 外，填绝对路径


def run_ollama(prompt, model):
    """调用本机 Ollama 推理，断网可用。"""
    try:
        out = subprocess.run(
            [OLLAMA_CLI, "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=900,
        )
        return (out.stdout or "").strip() or (out.stderr or "").strip()
    except Exception as e:  # 超时 / 进程缺失等
        return f"[调用失败] {e}"


def main():
    p = argparse.ArgumentParser(description="断网 Worker：调本机 Ollama 处理任务箱")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Ollama 模型名（默认 {DEFAULT_MODEL}），如 qwen2.5:7b")
    args = p.parse_args()
    model = args.model

    try:
        tasks = tb.load()
    except SystemExit:
        return
    todo = [t for t in tasks if t["status"] in ("queued", "running")]
    if not todo:
        print("没有待办任务，退出。")
        return
    todo.sort(key=lambda t: t.get("priority", 5))

    for t in todo:
        print(f"== 处理 #{t['id']}：{t['title']}（模型 {model}）")
        t["status"] = "running"
        t["updated_at"] = tb.now()
        tb.save(tasks)

        prompt = (
            f"任务：{t['title']}\n详情：{t['detail']}\n"
            f"请完成上述任务并给出结果。\n"
            f"输出格式要求：\n"
            f"1. 以「【结论】」开头，一句话给出最终结论；\n"
            f"2. 正文分点说明（每点 ≤50 字）；\n"
            f"3. 以「【下一步】」结尾，给出 1-3 条建议。\n"
            f"全程使用简体中文，总长度控制在 300 字以内。"
        )
        result = run_ollama(prompt, model)

        t["status"] = "done"
        t["result"] = result
        t["updated_at"] = tb.now()
        tb.save(tasks)
        print(f"== 完成 #{t['id']}，结果长度 {len(result)}")


if __name__ == "__main__":
    main()
