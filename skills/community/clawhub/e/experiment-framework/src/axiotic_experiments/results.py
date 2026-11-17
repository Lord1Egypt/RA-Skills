from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol


class MetricSink(Protocol):
    def log(self, metrics: dict[str, Any], *, step: int) -> None: ...


def append_metric(path: Path, *, step: int, metrics: dict[str, Any]) -> None:
    if step < 0:
        raise ValueError("step must be non-negative")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {"step": step, "metrics": metrics},
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        )


def replay_metrics(path: Path, sink: MetricSink) -> dict[str, int | None]:
    records = 0
    first_step: int | None = None
    last_step: int | None = None
    previous_step = -1
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            step = record.get("step")
            metrics = record.get("metrics")
            if not isinstance(step, int) or step < 0 or not isinstance(metrics, dict):
                raise ValueError(f"invalid metric record at line {line_number}")
            if step < previous_step:
                raise ValueError(f"metric steps regress at line {line_number}")
            sink.log(metrics, step=step)
            previous_step = step
            first_step = step if first_step is None else first_step
            last_step = step
            records += 1
    return {"records": records, "first_step": first_step, "last_step": last_step}
