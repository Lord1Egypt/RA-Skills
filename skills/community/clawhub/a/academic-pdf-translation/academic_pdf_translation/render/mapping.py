"""候选页映射：记录每个对象落在候选 PDF 的哪一页。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。这里放锚点
Flowable、事件记录器和带页眉页脚的文档模板，它们只和 reportlab 打交道，
不读写作业目录。

三处原来的 scripts 层依赖按包内规则改写：异常改成本模块自己的
``MappingError``，由调用侧翻译回 SkillError；时间戳和界面文案分别由
调用侧用 ``now_fn`` 和 ``message_fn`` 注入。
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    PageTemplate,
    Paragraph,
    Table,
)

from .flowables import VectorPayloadFlowable


class MappingError(RuntimeError):
    """候选页映射数据不完整。

    以前抛的是 scripts 层的 SkillError；包不该依赖 scripts，所以这里
    自己定义。调用侧把它翻译回 SkillError，对外行为不变。
    """


@dataclass(frozen=True)
class MappingEvent:
    phase: str
    object_type: str
    object_id: str
    source_page: int
    candidate_page: int
    candidate_y: float


class MappingTracker:
    def __init__(self) -> None:
        self.events: list[MappingEvent] = []
        self.orphan_regions: list[dict[str, Any]] = []
        self._pending_heading: dict[str, Any] | None = None

    def record(
        self,
        anchor: MappingAnchor,
        candidate_page: int,
        candidate_y: float,
    ) -> None:
        self.events.append(
            MappingEvent(
                phase=anchor.phase,
                object_type=anchor.object_type,
                object_id=anchor.object_id,
                source_page=anchor.source_page,
                candidate_page=candidate_page,
                candidate_y=candidate_y,
            )
        )

    def note_heading(
        self,
        *,
        candidate_page: int,
        text: str,
        unit_id: str | None,
    ) -> None:
        self.resolve_heading(candidate_page)
        self._pending_heading = {
            "candidate_page": candidate_page,
            "unit_id": unit_id,
            "text": text[:160],
        }

    def resolve_heading(self, content_page: int) -> None:
        pending = self._pending_heading
        if pending is None:
            return
        if int(pending["candidate_page"]) != int(content_page):
            self.orphan_regions.append(
                {
                    **pending,
                    "next_content_page": int(content_page),
                    "reason": "heading-separated-from-following-content",
                }
            )
        self._pending_heading = None

    def finalize_heading_check(self) -> None:
        pending = self._pending_heading
        if pending is not None:
            self.orphan_regions.append(
                {
                    **pending,
                    "next_content_page": None,
                    "reason": "heading-without-following-content",
                }
            )
            self._pending_heading = None

    def _ranges(self, object_type: str) -> dict[str, tuple[int, int, int]]:
        starts: dict[str, tuple[int, int]] = {}
        ends: dict[str, int] = {}
        for event in self.events:
            if event.object_type != object_type:
                continue
            if event.phase == "start":
                starts.setdefault(
                    event.object_id,
                    (event.source_page, event.candidate_page),
                )
            elif event.phase == "end":
                ends[event.object_id] = event.candidate_page
        result: dict[str, tuple[int, int, int]] = {}
        for object_id, (source_page, start) in starts.items():
            end = max(start, ends.get(object_id, start))
            result[object_id] = (source_page, start, end)
        return result

    def build_map(
        self,
        *,
        job: dict[str, Any],
        translation: dict[str, Any],
        retained_payloads: list[dict[str, Any]],
        unit_layout_roles: dict[str, str],
        page_size: tuple[float, float],
        margins: tuple[float, float, float, float],
        candidate_page_count: int,
        candidate_sha256: str,
        now_fn: Callable[[], str],
    ) -> dict[str, Any]:
        source_ranges = self._ranges("source-page")
        unit_ranges = self._ranges("unit")
        complex_ranges = self._ranges("complex")
        retained_ranges = self._ranges("retained")
        retained_payload_by_id = {
            str(payload["id"]): payload
            for payload in retained_payloads
            if isinstance(payload, dict) and str(payload.get("id") or "")
        }
        source_page_count = int(job["source"]["page_count"])
        units_by_source: dict[int, list[str]] = defaultdict(list)
        for unit in translation.get("units", []):
            if isinstance(unit, dict) and isinstance(unit.get("page"), int):
                units_by_source[int(unit["page"])].append(str(unit["id"]))
        complex_by_source: dict[int, list[str]] = defaultdict(list)
        for object_id, (source_page, _, _) in complex_ranges.items():
            complex_by_source[source_page].append(object_id)
        retained_by_source: dict[int, list[str]] = defaultdict(list)
        for object_id, (source_page, _, _) in retained_ranges.items():
            retained_by_source[source_page].append(object_id)

        source_entries: list[dict[str, Any]] = []
        reverse: dict[int, set[int]] = defaultdict(set)
        for source_page in range(1, source_page_count + 1):
            key = f"source-page-{source_page:04d}"
            if key not in source_ranges:
                raise MappingError(f"统一生成器未记录源页 {source_page}")
            _, start, end = source_ranges[key]
            pages = list(range(start, end + 1))
            for candidate_page in pages:
                reverse[candidate_page].add(source_page)
            source_entries.append(
                {
                    "source_page": source_page,
                    "candidate_pages": pages,
                    "unit_ids": units_by_source.get(source_page, []),
                    "complex_item_ids": sorted(
                        complex_by_source.get(source_page, [])
                    ),
                    "retained_region_ids": sorted(
                        retained_by_source.get(source_page, [])
                    ),
                }
            )
        unit_entries = []
        for unit_id, (source_page, start, end) in unit_ranges.items():
            unit_entries.append(
                {
                    "unit_id": unit_id,
                    "source_page": source_page,
                    "candidate_pages": list(range(start, end + 1)),
                    "layout_role": unit_layout_roles.get(unit_id),
                }
            )
        complex_entries = [
            {
                "complex_item_id": object_id,
                "source_page": source_page,
                "candidate_pages": list(range(start, end + 1)),
            }
            for object_id, (source_page, start, end) in complex_ranges.items()
        ]
        retained_entries = []
        page_width, page_height = page_size
        left, right, top, bottom = margins
        for object_id, (source_page, start, end) in retained_ranges.items():
            start_event = next(
                (
                    event
                    for event in self.events
                    if event.object_type == "retained"
                    and event.object_id == object_id
                    and event.phase == "start"
                ),
                None,
            )
            end_event = next(
                (
                    event
                    for event in reversed(self.events)
                    if event.object_type == "retained"
                    and event.object_id == object_id
                    and event.phase == "end"
                ),
                None,
            )
            candidate_regions = []
            if start_event is not None and end_event is not None:
                for candidate_page in range(start, end + 1):
                    region_top = (
                        max(top, page_height - start_event.candidate_y)
                        if candidate_page == start
                        else top
                    )
                    region_bottom = (
                        min(
                            page_height - bottom,
                            page_height - end_event.candidate_y,
                        )
                        if candidate_page == end
                        else page_height - bottom
                    )
                    if region_bottom > region_top + 0.5:
                        candidate_regions.append(
                            {
                                "candidate_page": candidate_page,
                                "bbox": [
                                    round(left, 3),
                                    round(region_top, 3),
                                    round(page_width - right, 3),
                                    round(region_bottom, 3),
                                ],
                            }
                        )
            payload = retained_payload_by_id.get(object_id, {})
            retained_entries.append(
                {
                    "retained_region_id": object_id,
                    "source_page": source_page,
                    "category": str(payload.get("category") or ""),
                    "candidate_pages": list(range(start, end + 1)),
                    "candidate_regions": candidate_regions,
                }
            )
        candidate_entries = [
            {
                "candidate_page": candidate_page,
                "source_pages": sorted(reverse.get(candidate_page, set())),
                "unit_ids": sorted(
                    entry["unit_id"]
                    for entry in unit_entries
                    if candidate_page in entry["candidate_pages"]
                ),
                "unit_layout_roles": {
                    entry["unit_id"]: entry["layout_role"]
                    for entry in unit_entries
                    if (
                        candidate_page in entry["candidate_pages"]
                        and entry.get("layout_role")
                    )
                },
                "complex_item_ids": sorted(
                    entry["complex_item_id"]
                    for entry in complex_entries
                    if candidate_page in entry["candidate_pages"]
                ),
                "retained_region_ids": sorted(
                    entry["retained_region_id"]
                    for entry in retained_entries
                    if candidate_page in entry["candidate_pages"]
                ),
                "retained_regions": [
                    {
                        "retained_region_id": entry["retained_region_id"],
                        "category": entry["category"],
                        "bbox": region["bbox"],
                    }
                    for entry in retained_entries
                    for region in entry.get("candidate_regions", [])
                    if region["candidate_page"] == candidate_page
                ],
            }
            for candidate_page in range(1, candidate_page_count + 1)
        ]
        return {
            "schema_version": "1.0",
            "generated_at": now_fn(),
            "mapping_mode": "flow-unit-anchors-v1",
            "layout_policy": "continuous-reading",
            "complete": True,
            "source_sha256": job["source"]["sha256"],
            "translation_sha256": None,
            "candidate_sha256": candidate_sha256,
            "source_page_count": source_page_count,
            "candidate_page_count": candidate_page_count,
            "source_pages": source_entries,
            "candidate_pages": candidate_entries,
            "units": sorted(unit_entries, key=lambda item: item["unit_id"]),
            "complex_items": sorted(
                complex_entries,
                key=lambda item: item["complex_item_id"],
            ),
            "retained_regions": sorted(
                retained_entries,
                key=lambda item: item["retained_region_id"],
            ),
        }


class MappingAnchor(Flowable):
    def __init__(
        self,
        phase: str,
        object_type: str,
        object_id: str,
        source_page: int,
        *,
        keep_with_next: bool = False,
    ) -> None:
        super().__init__()
        self.phase = phase
        self.object_type = object_type
        self.object_id = object_id
        self.source_page = source_page
        self.keepWithNext = phase == "start" or keep_with_next
        self.width = 0
        self.height = 0.01

    def wrap(self, available_width: float, available_height: float) -> tuple[float, float]:
        return 0, self.height

    def draw(self) -> None:
        return None


class MappingDocTemplate(BaseDocTemplate):
    def __init__(
        self,
        filename: str,
        *,
        tracker: MappingTracker,
        page_size: tuple[float, float],
        margins: tuple[float, float, float, float],
        regular_font: str,
        title: str,
        target_language: str,
        message_fn: Callable[..., str],
    ) -> None:
        self.message_fn = message_fn
        left, right, top, bottom = margins
        super().__init__(
            filename,
            pagesize=page_size,
            leftMargin=left,
            rightMargin=right,
            topMargin=top,
            bottomMargin=bottom,
            title=title,
            author="",
            subject=message_fn(target_language, "pdf_subject"),
        )
        self.tracker = tracker
        self.regular_font = regular_font
        self.target_language = target_language
        self._active_unit_id: str | None = None
        width, height = page_size
        frame = Frame(
            left,
            bottom,
            width - left - right,
            height - top - bottom,
            id="body",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(
            [
                PageTemplate(
                    id="continuous-reading",
                    frames=[frame],
                    onPage=self._draw_page_furniture,
                )
            ]
        )

    def _draw_page_furniture(self, canvas, document) -> None:
        width, height = self.pagesize
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D5D9DE"))
        canvas.setLineWidth(0.4)
        canvas.line(self.leftMargin, height - 24, width - self.rightMargin, height - 24)
        canvas.setFillColor(colors.HexColor("#6B747D"))
        canvas.setFont(self.regular_font, 7.2)
        canvas.drawString(
            self.leftMargin,
            height - 18,
            self.message_fn(self.target_language, "reading_version"),
        )
        canvas.drawRightString(
            width - self.rightMargin,
            17,
            str(document.page),
        )
        canvas.restoreState()

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, MappingAnchor):
            frame = getattr(self, "frame", None)
            candidate_y = float(getattr(frame, "_y", 0.0))
            self.tracker.record(
                flowable,
                int(self.page),
                candidate_y,
            )
            if flowable.phase == "start":
                if flowable.object_type == "unit":
                    pending = self.tracker._pending_heading
                    if (
                        pending is not None
                        and pending.get("unit_id") != flowable.object_id
                    ):
                        self.tracker.resolve_heading(int(self.page))
                    self._active_unit_id = flowable.object_id
                elif flowable.object_type in {"complex", "retained"}:
                    self.tracker.resolve_heading(int(self.page))
            elif (
                flowable.phase == "end"
                and flowable.object_type == "unit"
                and self._active_unit_id == flowable.object_id
            ):
                self._active_unit_id = None
            return
        if isinstance(flowable, Paragraph):
            style_name = str(getattr(flowable.style, "name", "")).lower()
            if style_name in {"h1", "h2", "title"}:
                self.tracker.note_heading(
                    candidate_page=int(self.page),
                    text=flowable.getPlainText(),
                    unit_id=self._active_unit_id,
                )
            elif style_name != "source-anchor":
                self.tracker.resolve_heading(int(self.page))
            return
        if isinstance(flowable, (Table, Image, VectorPayloadFlowable)):
            self.tracker.resolve_heading(int(self.page))
