"""阶段计时与重复调用计数。

这是性能基线工具，不参与质量判断。默认只在内存中累计，成本可忽略；
设置环境变量 ``ACADEMIC_PDF_TRACE`` 指向一个 JSON 路径后，进程结束时
自动落盘。

设计约束：

- 不改变任何业务输出；
- 关闭时不做文件读写；
- 计数只在明确的调用点递增，不猜测调用次数。
"""

from __future__ import annotations

import atexit
import json
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


TRACE_ENV_VAR = "ACADEMIC_PDF_TRACE"

COUNTER_SOURCE_PDF_OPEN = "source_pdf_open"
COUNTER_CANDIDATE_PDF_OPEN = "candidate_pdf_open"
COUNTER_PDF_OPEN = "pdf_open"
COUNTER_TEXT_DICT = "get_text_dict"
COUNTER_TEXT_PLAIN = "get_text_plain"
COUNTER_TEXT_BLOCKS = "get_text_blocks"
COUNTER_DRAWINGS = "get_drawings"
COUNTER_IMAGE_INFO = "get_image_info"
COUNTER_SHA256_READ = "sha256_file_read"
COUNTER_SHA256_CACHE_HIT = "sha256_cache_hit"
COUNTER_RENDER_ATTEMPT = "render_attempt"
COUNTER_TRANSLATION_BATCH = "translation_batch"
COUNTER_ANALYSIS_CACHE_HIT = "analysis_cache_hit"


class PerfTrace:
    """进程内的阶段耗时与调用计数账本。"""

    def __init__(self) -> None:
        self._stages: list[dict[str, Any]] = []
        self._counters: dict[str, int] = {}
        self._depth = 0

    def reset(self) -> None:
        self._stages.clear()
        self._counters.clear()
        self._depth = 0

    def count(self, name: str, amount: int = 1) -> None:
        if not name or amount <= 0:
            return
        self._counters[name] = self._counters.get(name, 0) + int(amount)

    def counter(self, name: str) -> int:
        return int(self._counters.get(name, 0))

    @contextmanager
    def stage(self, name: str, **metadata: Any) -> Iterator[dict[str, Any]]:
        record: dict[str, Any] = {
            "stage": name,
            "depth": self._depth,
            "status": "ok",
            "metadata": dict(metadata),
        }
        self._stages.append(record)
        self._depth += 1
        started = time.perf_counter()
        try:
            yield record
        except BaseException:
            record["status"] = "error"
            raise
        finally:
            self._depth -= 1
            record["elapsed_seconds"] = round(
                time.perf_counter() - started, 6
            )

    def snapshot(self) -> dict[str, Any]:
        totals: dict[str, dict[str, Any]] = {}
        for record in self._stages:
            entry = totals.setdefault(
                record["stage"],
                {"calls": 0, "total_seconds": 0.0, "errors": 0},
            )
            entry["calls"] += 1
            entry["total_seconds"] = round(
                entry["total_seconds"]
                + float(record.get("elapsed_seconds") or 0.0),
                6,
            )
            if record.get("status") == "error":
                entry["errors"] += 1
        return {
            "schema_version": "1.0",
            "pid": os.getpid(),
            "counters": dict(sorted(self._counters.items())),
            "stage_totals": dict(
                sorted(
                    totals.items(),
                    key=lambda item: item[1]["total_seconds"],
                    reverse=True,
                )
            ),
            "stages": list(self._stages),
        }

    def write(self, path: Path) -> Path:
        path = Path(path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = (
            json.dumps(self.snapshot(), ensure_ascii=False, indent=2) + "\n"
        )
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as handle:
            handle.write(payload)
            temp_path = Path(handle.name)
        os.replace(temp_path, path)
        return path


TRACE = PerfTrace()


def count(name: str, amount: int = 1) -> None:
    TRACE.count(name, amount)


def counter(name: str) -> int:
    return TRACE.counter(name)


def stage(name: str, **metadata: Any):
    return TRACE.stage(name, **metadata)


def snapshot() -> dict[str, Any]:
    return TRACE.snapshot()


def reset() -> None:
    TRACE.reset()


def _write_on_exit() -> None:
    target = os.environ.get(TRACE_ENV_VAR, "").strip()
    if not target:
        return
    try:
        TRACE.write(Path(target))
    except OSError:
        pass


atexit.register(_write_on_exit)
