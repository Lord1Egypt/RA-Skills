"""按计划逐批执行翻译，并在最后核对账目。

执行器只负责调度，不负责放宽检查：每一批仍然走
`apply_translation_batch`，因此逐单元校验、锚点检查和译文真实性检查
一项都不会少。

行为约定：

- 每批成功后立刻原子写回 translation.json 与计划状态；
- 单批失败只重试该批，其他批次不受影响；
- 中断后再次运行，从最后一个已验证批次继续；
- 第一版最多 2 个批次并发；
- 合并严格按冻结单元 ID，不按完成顺序；
- 结束时比较计划批次、已验证批次和实际单元数量，对不上就失败。

翻译能力由受信任的 Python 调用方传入：
``translate(batch) -> results``。命令行只提供账目核对，不接受外部命令。
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from _common import SkillError, load_json, write_json
from apply_translation_batch import (
    apply_cached_batches,
    apply_translation_batch,
    verify_plan_execution,
)
from plan_translation_batches import load_plan

MAX_CONCURRENT_BATCHES = 2
DEFAULT_MAX_RETRIES = 2

Translator = Callable[[dict[str, Any]], list[dict[str, Any]]]


def _pending_entries(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        entry
        for entry in plan.get("batches", [])
        if isinstance(entry, dict) and entry.get("status") != "applied"
    ]


def run_translation_batches(
    job_dir: Path,
    translate: Translator,
    *,
    model: str | None = None,
    max_retries: int = DEFAULT_MAX_RETRIES,
    use_cache: bool = True,
    max_concurrency: int = MAX_CONCURRENT_BATCHES,
) -> dict[str, Any]:
    job_dir = Path(job_dir).resolve()
    if not 1 <= max_concurrency <= MAX_CONCURRENT_BATCHES:
        raise SkillError(
            f"并发批次数必须位于 1..{MAX_CONCURRENT_BATCHES}"
        )
    restored = apply_cached_batches(job_dir) if use_cache else []

    plan = load_plan(job_dir)
    planned_model = str(plan.get("model") or "") or None
    effective_model = model or planned_model
    pending = _pending_entries(plan)
    executed: list[str] = []
    failures: list[dict[str, Any]] = []

    with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
        cursor = 0
        inflight: list[tuple[dict[str, Any], Any, float]] = []
        while cursor < len(pending) or inflight:
            while len(inflight) < max_concurrency and cursor < len(pending):
                entry = pending[cursor]
                batch = load_json(job_dir / entry["file"])
                inflight.append(
                    (entry, pool.submit(translate, batch), time.perf_counter())
                )
                cursor += 1
            # 按计划顺序写回，不按完成顺序：合并顺序由冻结单元 ID 决定。
            entry, future, started = inflight.pop(0)
            batch_id = str(entry["batch_id"])
            attempt = 0
            while True:
                try:
                    results = future.result()
                    apply_translation_batch(
                        job_dir,
                        batch_id,
                        results,
                        elapsed_seconds=round(
                            time.perf_counter() - started, 3
                        ),
                        model=effective_model,
                        retries=attempt,
                    )
                except Exception as exc:  # noqa: BLE001
                    attempt += 1
                    if attempt > max_retries:
                        failures.append(
                            {
                                "batch_id": batch_id,
                                "attempts": attempt,
                                "error": str(exc)[:2000],
                            }
                        )
                        break
                    # 只重试这一批，其他批次已经落盘，不受影响。
                    batch = load_json(job_dir / entry["file"])
                    started = time.perf_counter()
                    future = pool.submit(translate, batch)
                    continue
                executed.append(batch_id)
                break

    if failures:
        detail = "\n".join(
            f"- {item['batch_id']} 重试 {item['attempts']} 次仍失败: "
            f"{item['error']}"
            for item in failures
        )
        raise SkillError(f"以下批次未能完成翻译:\n{detail}")

    verification = verify_plan_execution(job_dir)
    report = {
        "job_dir": str(job_dir),
        "model": effective_model,
        "restored_from_cache": restored,
        "executed_batches": executed,
        "verification": verification,
    }
    write_json(job_dir / "translation-run.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="只核对账目：计划批次、已验证批次与实际单元数量",
    )
    args = parser.parse_args()
    try:
        if args.verify_only:
            print(
                json.dumps(
                    verify_plan_execution(args.job_dir),
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
        raise SkillError(
            "命令行只支持 --verify-only；翻译执行由受信任的 Python 调用方提供"
        )
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
