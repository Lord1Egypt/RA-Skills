#!/usr/bin/env python3
"""Compare multiple AgentScope models on a shared task."""

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path
from typing import List

from agentscope.agent import Agent
from agentscope.model import OpenAIChatModel
from agentscope.tool import Toolkit


def build_model(model_name: str):
    if model_name.startswith("gpt-") or model_name.startswith("o1-") or model_name.startswith("o3-"):
        return OpenAIChatModel(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name=model_name,
        )
    return OpenAIChatModel(
        api_key=os.environ.get("DASHSCOPE_API_KEY", os.environ["OPENAI_API_KEY"]),
        model_name=model_name,
    )


async def run_task(model_name: str, task: str) -> dict:
    model = build_model(model_name)
    agent = Agent(
        name=f"Agent-{model_name}",
        system_prompt="You are a helpful assistant.",
        model=model,
        toolkit=Toolkit(tools=[]),
    )
    start = time.perf_counter()
    result = await agent(task)
    elapsed = time.perf_counter() - start
    content = result.choices[0].message.content if hasattr(result, "choices") else str(result)
    return {
        "model": model_name,
        "elapsed_sec": round(elapsed, 3),
        "output_length": len(content or ""),
        "output": content,
    }


async def main_async(models: List[str], task: str) -> int:
    results = []
    for model in models:
        try:
            results.append(await run_task(model, task))
        except Exception as exc:
            results.append({"model": model, "error": str(exc)})

    print("# AgentScope Model Compare\n")
    print(f"Task: {task}\n")
    for item in results:
        if "error" in item:
            print(f"- {item['model']}: FAILED: {item['error']}")
        else:
            print(f"- {item['model']}: {item['elapsed_sec']}s, {item['output_length']} chars")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare AgentScope models")
    parser.add_argument("--task", required=True, type=str)
    parser.add_argument("--models", nargs="*", default=["gpt-4o", "gpt-4o-mini"])
    args = parser.parse_args()
    if "OPENAI_API_KEY" not in os.environ and "DASHSCOPE_API_KEY" not in os.environ:
        print("FAIL: OPENAI_API_KEY or DASHSCOPE_API_KEY is required")
        return 1
    return asyncio.run(main_async(args.models, args.task))


if __name__ == "__main__":
    sys.exit(main())
