"""证据的新鲜度：每份报告都要能证明"我说的就是这一份候选"。

固定文件名的报告有一个天生的洞：新候选生成后，旧报告还躺在原地，
调用方一看"文件在、status=READY"就把旧结论用到新 PDF 上。

对策是两条：

1. **运行目录。** 每次首次构建开一个 ``runs/{run_id}/``，每轮尝试
   一个 ``attempt-{n}/``，证据只往自己的目录里写。旧证据保留，
   但它属于历史，路径本身就说明了这一点。
2. **五元绑定。** 每份证据带上 run_id、attempt_id、候选哈希、
   渲染计划哈希、渲染器构建 ID。校验时五个全对才算当前证据，
   差一个就是 ``EVIDENCE_STALE``。

``current-run.json`` 是唯一的"现在"指针，原子写入——先写临时文件
再改名，读到的它要么是旧的完整版，要么是新的完整版，不会是半截。
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EVIDENCE_STALE = "EVIDENCE_STALE"

CURRENT_RUN_FILE = "current-run.json"

#: 绑定必须逐项一致的字段。少一个、错一个都算旧证据。
BINDING_FIELDS = (
    "run_id",
    "attempt_id",
    "candidate_sha256",
    "render_plan_sha256",
    "renderer_build_id",
)


@dataclass(frozen=True)
class RunIdentity:
    """一轮尝试的完整身份。"""

    run_id: str
    attempt_id: int
    candidate_sha256: str
    render_plan_sha256: str = ""
    renderer_build_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def new_run_id() -> str:
    """新运行 ID：时间戳 + 随机尾巴，可读又不会撞。"""

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{uuid.uuid4().hex[:8]}"


def attempt_dir(delivery_dir: Path, run_id: str, attempt_id: int) -> Path:
    """这一轮尝试的证据目录。"""

    return Path(delivery_dir) / "runs" / run_id / f"attempt-{attempt_id}"


def write_current_run(delivery_dir: Path, identity: RunIdentity) -> Path:
    """原子更新"现在"指针。

    先把完整内容写进同目录的临时文件，再 ``os.replace`` 改名——
    replace 在同一文件系统上是原子的，读者不可能读到半截。
    """

    delivery_dir = Path(delivery_dir)
    delivery_dir.mkdir(parents=True, exist_ok=True)
    target = delivery_dir / CURRENT_RUN_FILE
    payload = json.dumps(identity.as_dict(), ensure_ascii=False, indent=2)
    temp = target.with_name(f".{CURRENT_RUN_FILE}.tmp")
    temp.write_text(payload, encoding="utf-8")
    os.replace(temp, target)
    return target


def read_current_run(delivery_dir: Path) -> RunIdentity | None:
    """读"现在"指针。没有就是还没跑过。"""

    path = Path(delivery_dir) / CURRENT_RUN_FILE
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return RunIdentity(
        run_id=str(data.get("run_id") or ""),
        attempt_id=int(data.get("attempt_id") or 0),
        candidate_sha256=str(data.get("candidate_sha256") or ""),
        render_plan_sha256=str(data.get("render_plan_sha256") or ""),
        renderer_build_id=str(data.get("renderer_build_id") or ""),
    )


def verify_binding(
    binding: dict[str, Any], identity: RunIdentity
) -> list[str]:
    """一份证据的绑定对得上当前身份吗？

    返回不一致清单；空列表表示证据属于当前候选。任何一项缺失或
    不同都算 ``EVIDENCE_STALE``——旧证据不许验证新候选。
    """

    expected = identity.as_dict()
    problems: list[str] = []
    for field_name in BINDING_FIELDS:
        want = expected[field_name]
        got = binding.get(field_name)
        if got is None or got == "":
            problems.append(
                f"{EVIDENCE_STALE}: 证据没有 {field_name} 绑定，"
                "无法证明它属于当前候选"
            )
        elif str(got) != str(want):
            problems.append(
                f"{EVIDENCE_STALE}: 证据的 {field_name}={got!r} 与当前 "
                f"{want!r} 不一致"
            )
    return problems
