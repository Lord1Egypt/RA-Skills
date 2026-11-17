"""元素纠正：自动识别会出错，允许改，但不许借着"改"把元素弄没。

这条边界和 keep_source_code 是同一个道理：**自由文字理由不能单独获得
豁免**。要省略一个元素，必须它本来就是纯装饰，而且用固定代码声明。
必需元素——正文、标题、图、表、公式、脚注、题录——一个都不许删。

每一次纠正都留痕：改了哪个元素、改成什么、谁改的、什么时候、依据是什么。
合并保留原 ID，拆分保留父 ID，随时能追回去。
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from academic_pdf_translation.contracts.enums import (
    PAGE_FURNITURE_TYPES,
    ElementType,
)
from academic_pdf_translation.contracts.models import (
    SourceElement,
    SourceElementInventory,
    normalize_bbox,
    union_bbox,
)

OVERRIDES_FILE_NAME = "element_overrides.json"
SCHEMA_VERSION = "2.0"

# --- 允许的动作 -------------------------------------------------------------

ACTION_RETYPE = "retype"
ACTION_SPLIT = "split"
ACTION_MERGE = "merge"
ACTION_MOVE_BBOX = "move-bbox"
ACTION_LINK = "link"
ACTION_UNLINK = "unlink"
ACTION_OMIT = "omit-nonsemantic"

ALLOWED_ACTIONS = (
    ACTION_RETYPE,
    ACTION_SPLIT,
    ACTION_MERGE,
    ACTION_MOVE_BBOX,
    ACTION_LINK,
    ACTION_UNLINK,
    ACTION_OMIT,
)

#: 省略理由的固定代码。自由文字不在此列，单独不能省略任何东西。
OMIT_CODES = (
    "page-header",
    "page-footer",
    "page-number",
    "watermark",
    "decorative-rule",
    "duplicate-of-another-element",
)

#: 这些类型可以被省略。其余一律不行。
OMITTABLE_TYPES = frozenset(PAGE_FURNITURE_TYPES) | {ElementType.UNKNOWN}


class OverrideError(ValueError):
    """纠正本身不合法。"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class ElementOverride:
    """一条纠正记录。"""

    action: str
    element_id: str
    reason: str
    author: str
    recorded_at: str = field(default_factory=_now)
    #: 结构化证据：坐标、页码、截图路径等。自由文字不算证据。
    evidence: dict[str, Any] = field(default_factory=dict)
    new_type: str | None = None
    omit_code: str | None = None
    bbox: list[float] | None = None
    #: split 用：子元素的类型与坐标。
    parts: list[dict[str, Any]] = field(default_factory=list)
    #: merge 用：被并进来的其他元素 ID。
    merge_with: list[str] = field(default_factory=list)
    relation: str | None = None
    target_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value not in (None, [], {})}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise OverrideError(message)


def validate_override(
    override: ElementOverride,
    inventory: SourceElementInventory,
) -> None:
    """先把不合法的纠正挡在门外。"""

    _require(
        override.action in ALLOWED_ACTIONS,
        f"不支持的纠正动作: {override.action!r}；只能是 "
        + "、".join(ALLOWED_ACTIONS),
    )
    _require(bool(override.reason.strip()), "每条纠正都必须写明理由")
    _require(bool(override.author.strip()), "每条纠正都必须记录修改人")

    element = inventory.by_id(override.element_id)
    _require(
        element is not None,
        f"元素不存在: {override.element_id}",
    )
    assert element is not None

    if override.action == ACTION_OMIT:
        _require(
            override.omit_code in OMIT_CODES,
            "省略必须给出固定的 omit_code："
            + "、".join(OMIT_CODES)
            + "；自由文字理由单独不能省略任何元素",
        )
        _require(
            element.type in OMITTABLE_TYPES,
            f"{element.id} 是 {element.type.value}，属于必需元素，不能省略。"
            "只有页眉、页脚、页码、水印这类纯装饰元素可以省略",
        )
        _require(
            not element.required,
            f"{element.id} 是必需元素，不能被标记为省略",
        )

    if override.action == ACTION_RETYPE:
        _require(bool(override.new_type), "retype 必须给出 new_type")
        try:
            new_type = ElementType(str(override.new_type))
        except ValueError as exc:
            raise OverrideError(
                f"无效的元素类型: {override.new_type!r}"
            ) from exc
        # 把必需元素改成可省略类型，等于绕过清单。
        if element.required and new_type in OMITTABLE_TYPES:
            raise OverrideError(
                f"{element.id} 是必需元素，不能改判为 {new_type.value}；"
                "这会让它绕过结构对账"
            )

    if override.action == ACTION_SPLIT:
        _require(
            len(override.parts) >= 2,
            "split 至少要拆成两个子元素",
        )
        for index, part in enumerate(override.parts):
            _require(
                normalize_bbox(part.get("bbox")) is not None,
                f"parts[{index}] 缺少有效坐标",
            )
            _require(
                bool(part.get("type")),
                f"parts[{index}] 缺少类型",
            )

    if override.action == ACTION_MERGE:
        _require(bool(override.merge_with), "merge 必须给出要合并的元素")
        for other_id in override.merge_with:
            other = inventory.by_id(other_id)
            _require(other is not None, f"要合并的元素不存在: {other_id}")
            assert other is not None
            _require(
                other.page == element.page,
                f"{other_id} 与 {element.id} 不在同一页，不能合并",
            )

    if override.action == ACTION_MOVE_BBOX:
        _require(
            normalize_bbox(override.bbox) is not None,
            "move-bbox 必须给出有效坐标",
        )

    if override.action in {ACTION_LINK, ACTION_UNLINK}:
        _require(bool(override.relation), "link/unlink 必须给出关系名")
        _require(bool(override.target_id), "link/unlink 必须给出目标元素")
        _require(
            inventory.by_id(str(override.target_id)) is not None,
            f"目标元素不存在: {override.target_id}",
        )


def apply_override(
    override: ElementOverride,
    inventory: SourceElementInventory,
) -> SourceElementInventory:
    """把一条纠正应用到清单上。清单原地修改并返回。"""

    validate_override(override, inventory)
    element = inventory.by_id(override.element_id)
    assert element is not None

    history = element.detail.setdefault("override_history", [])
    history.append(override.as_dict())

    if override.action == ACTION_RETYPE:
        element.detail["original_type"] = element.detail.get(
            "original_type", element.type.value
        )
        element.type = ElementType(str(override.new_type))
        element.signals.append("retyped-by-override")

    elif override.action == ACTION_OMIT:
        element.detail["omitted"] = True
        element.detail["omit_code"] = override.omit_code
        element.signals.append("omitted-by-override")

    elif override.action == ACTION_MOVE_BBOX:
        element.detail["original_bbox"] = (
            list(element.bbox) if element.bbox else None
        )
        element.bbox = normalize_bbox(override.bbox)
        element.signals.append("bbox-corrected-by-override")

    elif override.action == ACTION_LINK:
        element.link(str(override.relation), str(override.target_id))
        element.signals.append("linked-by-override")

    elif override.action == ACTION_UNLINK:
        targets = element.relations.get(str(override.relation), [])
        if override.target_id in targets:
            targets.remove(str(override.target_id))
        element.signals.append("unlinked-by-override")

    elif override.action == ACTION_MERGE:
        others = [
            inventory.by_id(other_id) for other_id in override.merge_with
        ]
        boxes = [element.bbox] + [
            other.bbox for other in others if other is not None
        ]
        element.bbox = union_bbox([box for box in boxes if box is not None])
        merged_ids = element.detail.setdefault("merged_element_ids", [])
        for other in others:
            if other is None:
                continue
            # 原 ID 必须留在历史里，随时能追回去。
            merged_ids.append(other.id)
            element.source_block_ids.extend(other.source_block_ids)
            element.translation_unit_ids.extend(other.translation_unit_ids)
            for relation, targets in other.relations.items():
                for target in targets:
                    element.link(relation, target)
            inventory.elements.remove(other)
        element.source_block_ids = sorted(set(element.source_block_ids))
        element.signals.append("merged-by-override")

    elif override.action == ACTION_SPLIT:
        children: list[SourceElement] = []
        for index, part in enumerate(override.parts, 1):
            child = SourceElement(
                id=f"{element.id}-part{index:02d}",
                page=element.page,
                type=ElementType(str(part["type"])),
                bbox=normalize_bbox(part.get("bbox")),
                confidence=float(part.get("confidence", element.confidence)),
                source_block_ids=[
                    int(value) for value in part.get("source_block_ids", [])
                ],
                signals=["split-by-override"],
                detail={"parent_element_id": element.id},
                text=str(part.get("text") or ""),
            )
            children.append(child)
        position = inventory.elements.index(element)
        inventory.elements[position : position + 1] = children
        for child in children:
            child.detail["override_history"] = list(history)

    return inventory


def load_overrides(job_dir: Path) -> list[ElementOverride]:
    path = Path(job_dir) / OVERRIDES_FILE_NAME
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        ElementOverride(**entry) for entry in data.get("overrides", [])
    ]


def save_overrides(job_dir: Path, overrides: list[ElementOverride]) -> Path:
    path = Path(job_dir) / OVERRIDES_FILE_NAME
    path.write_text(
        json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "allowed_actions": list(ALLOWED_ACTIONS),
                "omit_codes": list(OMIT_CODES),
                "note": (
                    "只用于纠正自动识别。必需元素不能删除，"
                    "省略必须使用固定 omit_code，自由文字理由无效。"
                ),
                "overrides": [item.as_dict() for item in overrides],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def apply_all(
    inventory: SourceElementInventory,
    overrides: list[ElementOverride],
) -> SourceElementInventory:
    for override in overrides:
        apply_override(override, inventory)
    return inventory
