#!/usr/bin/env python3
"""Run one or more Fotor tasks from a JSON spec on stdin or file.

Single task:
  echo '{"task_type":"text2image","params":{"prompt":"A cat","model_id":"seedream-4-5-251128"}}' | python scripts/run_task.py

Batch (array of specs):
  echo '[{"task_type":"text2image","params":{"prompt":"A cat","model_id":"seedream-4-5-251128"},"tag":"cat"},
        {"task_type":"text2video","params":{"prompt":"Sunset","model_id":"kling-v3"},"tag":"sunset"}]' | python scripts/run_task.py

Options:
  --input FILE       Read specs from FILE instead of stdin
  --concurrency N    Max parallel tasks (default: 5)
  --poll-interval S  Seconds between polls (default: 2.0)
  --timeout S        Max polling seconds (default: 1200)

Output: JSON array of results, one per task.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import sys

from fotor_sdk import (
    FotorClient,
    TaskResult,
    FotorAPIError,
    text2image,
    image2image,
    image_upscale,
    background_remove,
    text2video,
    single_image2video,
    start_end_frame2video,
    multiple_image2video,
)

_TASK_FN = {
    "text2image": text2image,
    "image2image": image2image,
    "image_upscale": image_upscale,
    "background_remove": background_remove,
    "text2video": text2video,
    "single_image2video": single_image2video,
    "start_end_frame2video": start_end_frame2video,
    "multiple_image2video": multiple_image2video,
}

_FALLBACK_MODEL_BY_TASK = json.loads(
    (
        Path(__file__).resolve().parent.parent / "references" / "fallback_models.json"
    ).read_text(encoding="utf-8")
)


def _result_to_dict(r: TaskResult) -> dict:
    return {
        "task_id": r.task_id,
        "status": r.status.name,
        "success": r.success,
        "result_url": r.result_url,
        "error": r.error,
        "elapsed_seconds": round(r.elapsed_seconds, 2),
        "creditsIncrement": getattr(r, "creditsIncrement", 0),
        "tag": r.metadata.get("tag", ""),
        "fallback_used": False,
        "original_model_id": "",
        "fallback_model_id": "",
    }


def _fallback_model_id(task_type: str, model_id: str) -> str:
    return _FALLBACK_MODEL_BY_TASK.get(task_type, {}).get(model_id, "")


def _is_insufficient_credits_error(error: FotorAPIError) -> bool:
    code = str(getattr(error, "code", "") or "")
    message = str(error)
    return code == "510" or "No enough credits" in message


async def _run_single(client: FotorClient, spec: dict) -> dict:
    task_type = spec.get("task_type", "")
    params = dict(spec.get("params", {}))
    fn = _TASK_FN.get(task_type)
    if fn is None:
        return {"task_id": "", "status": "FAILED", "success": False,
                "error": f"Unknown task_type: {task_type}", "result_url": None,
                "elapsed_seconds": 0, "creditsIncrement": 0, "tag": spec.get("tag", ""),
                "fallback_used": False, "original_model_id": "", "fallback_model_id": ""}
    try:
        result = await fn(client, **params)
        d = _result_to_dict(result)
        d["tag"] = spec.get("tag", "")
        return d
    except FotorAPIError as e:
        original_model_id = str(params.get("model_id", ""))
        if _is_insufficient_credits_error(e):
            return {"task_id": "", "status": "FAILED", "success": False,
                    "error": f"{e} (code={e.code})", "result_url": None,
                    "elapsed_seconds": 0, "creditsIncrement": 0, "tag": spec.get("tag", ""),
                    "fallback_used": False,
                    "original_model_id": original_model_id,
                    "fallback_model_id": ""}
        fallback_model_id = _fallback_model_id(task_type, original_model_id)
        if fallback_model_id:
            retry_params = dict(params)
            retry_params["model_id"] = fallback_model_id
            try:
                retry_result = await fn(client, **retry_params)
                d = _result_to_dict(retry_result)
                d["tag"] = spec.get("tag", "")
                d["fallback_used"] = True
                d["original_model_id"] = original_model_id
                d["fallback_model_id"] = fallback_model_id
                return d
            except FotorAPIError as retry_error:
                return {
                    "task_id": "",
                    "status": "FAILED",
                    "success": False,
                    "error": (
                        f"primary={e} (code={e.code}); "
                        f"fallback={retry_error} (code={retry_error.code})"
                    ),
                    "result_url": None,
                    "elapsed_seconds": 0,
                    "creditsIncrement": 0,
                    "tag": spec.get("tag", ""),
                    "fallback_used": True,
                    "original_model_id": original_model_id,
                    "fallback_model_id": fallback_model_id,
                }
        return {"task_id": "", "status": "FAILED", "success": False,
                "error": f"{e} (code={e.code})", "result_url": None,
                "elapsed_seconds": 0, "creditsIncrement": 0, "tag": spec.get("tag", ""),
                "fallback_used": False,
                "original_model_id": original_model_id,
                "fallback_model_id": ""}


async def _run_batch(client: FotorClient, specs: list[dict], concurrency: int) -> list[dict]:
    semaphore = asyncio.Semaphore(concurrency)
    results: list[dict | None] = [None] * len(specs)
    total = len(specs)
    completed = 0

    async def _run_one(index: int, spec: dict) -> None:
        nonlocal completed
        async with semaphore:
            result = await _run_single(client, spec)
        results[index] = result
        completed += 1
        tag = result.get("tag", "") or result.get("task_id", "") or f"task-{index + 1}"
        status = "OK" if result.get("success") else result.get("status", "FAILED")
        if result.get("fallback_used"):
            status = f"{status} (fallback)"
        print(f"[{completed}/{total}] {tag} -> {status}", file=sys.stderr)

    await asyncio.gather(*[_run_one(i, spec) for i, spec in enumerate(specs)])
    return [r for r in results if r is not None]


async def main() -> int:
    parser = argparse.ArgumentParser(description="Run Fotor tasks from JSON")
    parser.add_argument("--input", help="JSON file path (default: stdin)")
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=1200)
    args = parser.parse_args()

    api_key = os.environ.get("FOTOR_OPENAPI_KEY", "")
    if not api_key:
        print(json.dumps({"error": "FOTOR_OPENAPI_KEY not set"}), file=sys.stderr)
        return 1

    client = FotorClient(
        api_key=api_key,
        endpoint=os.environ.get("FOTOR_OPENAPI_ENDPOINT", "https://api-b.fotor.com"),
        poll_interval=args.poll_interval,
        max_poll_seconds=args.timeout,
    )

    raw = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    data = json.loads(raw.strip())

    if isinstance(data, dict):
        result = await _run_single(client, data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif isinstance(data, list):
        results = await _run_batch(client, data, args.concurrency)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": "Input must be a JSON object or array"}), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
