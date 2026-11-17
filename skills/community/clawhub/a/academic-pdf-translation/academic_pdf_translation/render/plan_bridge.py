"""把渲染计划翻成生成器认识的条目。

阶段 15 的基准查出一件事：渲染计划里的降级决定，生成器根本看不见。
计划说"这张图重建不了，退到保留原文区域"，生成器照旧按老路子走，
返修跑完产出一个字没变。

这里补的就是那一段缺失的翻译：读渲染计划，把落到保留级的元素，
变成生成器已经认识的复杂内容条目。**只翻译保留这两级**——
其余策略仍由生成器原来的路径处理，一块一块换，不一次掀桌子。

两条边界：

- 只翻译计划里确实定到保留级的元素。计划没说的，这里不替它决定。
- 元素必须有页码和坐标。没有坐标就没法保留区域，如实报出来，
  不猜一个框。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import normalize_bbox
from academic_pdf_translation.planning.mode_policy import (
    FALLBACK_PRESERVE_ELEMENT_REGION,
    FALLBACK_PRESERVE_FULL_PAGE,
)

SCHEMA_VERSION = "1.0"

#: 渲染计划里所有"保留原文区域"一族的策略。
#: 前两个是通用降级；其余是按内容类型定的保留决定——表格网格不可靠、
#: 公式不重排、矢量图不重画、位图原样保留时，计划会选它们。
#: 生成器统一按区域保留执行。
#:
#: ``preserve-original-image`` 也在这里。位图曾经被排除在外，理由是
#: "它有自己的既有渲染路径"——真实样本证明那条路径并不存在：作者照片
#: 落到这个策略上，桥接不接、生成器不画，候选里一张图都没有。
PRESERVATION_STRATEGIES = (
    FALLBACK_PRESERVE_ELEMENT_REGION,
    FALLBACK_PRESERVE_FULL_PAGE,
    "preserve-table-region-with-translation-key",
    "preserve-formula-region",
    "preserve-geometry-with-label-overlay",
    "preserve-geometry-with-numbered-legend",
    "preserve-original-image",
)

#: 生成的条目走这个 kind，方便在产物里一眼认出它来自返修降级。
KIND_PRESERVED = "preserved-source"
STATUS_READY = "ready"

#: 保留区域插在这一页原有内容之前还是之后。
#: 保留的是原文那一块，放在译文之前，读者先看到实物再看译文。
RENDER_POLICY = "insert-before"

#: 元素指向它图题的关系名。
CAPTION_RELATION = "caption"
#: 图内嵌入标签的关系名。
EMBEDDED_LABEL_RELATION = "embedded-label"
CJK_TEXT_RE = __import__("re").compile(r"[\u3400-\u9fff]")

#: 公式区域的扩展量（点）。公式检测框常只框住主行，求和号的上下标、
#: 左右紧贴的括号会溢出框外几到二十几点；行末的公式编号更远。
#: 展示公式独占自己的竖向条带，横向扩展是安全的。
FORMULA_PAD_X = 28.0
FORMULA_PAD_Y = 5.0


class PlanBridgeError(RuntimeError):
    """渲染计划翻不成生成器条目。"""


@dataclass
class BridgeResult:
    """一次翻译的结果与说不通的地方。"""

    schema_version: str = SCHEMA_VERSION
    items: list[dict[str, Any]] = field(default_factory=list)
    skipped: list[dict[str, str]] = field(default_factory=list)

    @property
    def element_ids(self) -> list[str]:
        return [str(item["source_element_id"]) for item in self.items]

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "item_count": len(self.items),
            "skipped_count": len(self.skipped),
            "items": list(self.items),
            "skipped": list(self.skipped),
        }


@dataclass
class _Planned:
    element_id: str
    strategy: str


def _planned_preservations(render_plan: dict[str, Any]) -> list[_Planned]:
    planned: list[_Planned] = []
    for entry in render_plan.get("elements", []):
        if not isinstance(entry, dict):
            continue
        strategy = str(entry.get("strategy") or "")
        if strategy not in PRESERVATION_STRATEGIES:
            continue
        element_id = str(entry.get("element_id") or "")
        if not element_id:
            continue
        planned.append(_Planned(element_id=element_id, strategy=strategy))
    return planned


def caption_text_for(
    element: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
    unit_texts_by_element: dict[str, str],
) -> str:
    """这个元素的图题译文。

    图题必须跟着图走：图在第 4 页、图题在第 5 页，两样东西都废了。
    把图题挂在保留条目上，生成器就能把它和图锁成一块，
    正文里那一份也会被自动抑制，不会印两遍。
    """

    for caption_id in (element.get("relations") or {}).get(
        CAPTION_RELATION, []
    ):
        text = unit_texts_by_element.get(str(caption_id), "").strip()
        if text:
            return text
        caption_element = by_id.get(str(caption_id))
        if caption_element is None:
            continue
        excerpt = str(caption_element.get("text_excerpt") or "").strip()
        if excerpt:
            return excerpt
    return ""


def _expand_formula_box(
    box: tuple, page_size: tuple[float, float] | None
) -> list[float]:
    """把公式框扩到能盖住碎片和行末编号。"""

    x0 = box[0] - FORMULA_PAD_X
    x1 = box[2] + FORMULA_PAD_X
    y0 = box[1] - FORMULA_PAD_Y
    y1 = box[3] + FORMULA_PAD_Y
    if page_size:
        width, height = page_size
        # 行末编号靠版心右缘，右边直接扩到接近页缘。
        x1 = max(x1, width - 100.0)
        x0 = max(0.0, x0)
        x1 = min(width, x1)
        y0 = max(0.0, y0)
        y1 = min(height, y1)
    return [x0, y0, x1, y1]


MATH_TOKEN_RE = __import__("re").compile(
    r"[∑∈∏√≤≥±×∞∂∇Ωσℓ]|\(x\)|\blog\b|^\(?\d{1,2}\)?$"
)
CJK_RE = __import__("re").compile(r"[\u3400-\u9fff]")


def _is_formula_fragment(unit: dict[str, Any]) -> bool:
    """这个单元是不是公式的碎片。

    公式整块保留后，它的碎片行要从正文里删掉；但同一竖向带里可能混着
    真正文（原版式里公式和句子同行）。判据看语义不看坐标一刀切：
    有中文译文的是句子，留下；没有中文、带数学记号或只是个编号的，
    是公式的一部分，随图走。
    """

    translation = str(unit.get("translation") or "").strip()
    if CJK_RE.search(translation):
        return False
    text = translation or str(unit.get("source") or "").strip()
    if not text:
        return True
    if len(text) <= 3:
        return True
    return bool(MATH_TOKEN_RE.search(text))


def build_preservation_items(
    render_plan: dict[str, Any],
    elements: list[dict[str, Any]],
    *,
    unit_texts_by_element: dict[str, str] | None = None,
    page_sizes: dict[int, tuple[float, float]] | None = None,
    units: list[dict[str, Any]] | None = None,
    skip_elements: set[str] | None = None,
    source_pages: dict[int, Any] | None = None,
) -> BridgeResult:
    """把计划里定到保留级的元素翻成复杂内容条目。

    ``unit_texts_by_element`` 是元素到译文的映射，用来取图题。
    取不到就不带图题——宁可图题留在正文里，也不要凭空造一句。
    """

    if not isinstance(render_plan, dict):
        raise PlanBridgeError("渲染计划必须是字典")

    by_id = {
        str(element.get("id") or ""): element
        for element in elements
        if isinstance(element, dict)
    }
    texts = unit_texts_by_element or {}
    result = BridgeResult()

    for planned in _planned_preservations(render_plan):
        if planned.element_id in (skip_elements or set()):
            # 别处已经用更好的方式（比如结构化中文重建）处理了它。
            continue
        element = by_id.get(planned.element_id)
        if element is None:
            result.skipped.append(
                {
                    "element_id": planned.element_id,
                    "reason": "元素清单里找不到它，无法取得坐标",
                }
            )
            continue
        page = int(element.get("page") or 0)
        box = normalize_bbox(element.get("bbox"))
        if page <= 0:
            result.skipped.append(
                {"element_id": planned.element_id, "reason": "元素没有页码"}
            )
            continue
        if planned.strategy == FALLBACK_PRESERVE_ELEMENT_REGION and box is None:
            result.skipped.append(
                {
                    "element_id": planned.element_id,
                    "reason": "元素没有有效坐标，保留不了区域；不猜一个框",
                }
            )
            continue

        full_page = planned.strategy == FALLBACK_PRESERVE_FULL_PAGE
        render_box = box
        suppress: list[str] = []
        formula_crop_info: dict[str, Any] | None = None
        if (
            planned.strategy == "preserve-formula-region"
            and box is not None
        ):
            # 画出来的图用扩展框：盖住求和号的上下标和行末编号。
            source_page = (source_pages or {}).get(page)
            if source_page is not None:
                # 三步法：内容并集 → 方向边距 → 边缘墨迹检查。
                from academic_pdf_translation.render.formula_crop import (
                    compute_formula_crop,
                    formula_render_box,
                )

                crop = compute_formula_crop(source_page, box)
                formula_crop_info = crop.as_dict()
                render_box = tuple(formula_render_box(source_page, box))
            else:
                # 老作业没有页对象时的兼容路径：固定边距。
                render_box = tuple(
                    _expand_formula_box(box, (page_sizes or {}).get(page))
                )
            # 坐标吞只用紧框（原框加碎片垫，不到页缘）——同一竖向带里
            # 可能有真正文（原版式公式与句子同行），页缘一刀切会误吞。
            width_height = (page_sizes or {}).get(page)
            box = (
                max(0.0, box[0] - FORMULA_PAD_X),
                max(0.0, box[1] - FORMULA_PAD_Y),
                box[2] + FORMULA_PAD_X,
                box[3] + FORMULA_PAD_Y,
            )
            if width_height:
                box = (
                    box[0],
                    box[1],
                    min(width_height[0], box[2]),
                    min(width_height[1], box[3]),
                )
            # 扩展框内、语义上属于公式的碎片行，按文字删除。
            rx0, ry0, rx1, ry1 = render_box
            for unit in units or []:
                if unit.get("page") != page:
                    continue
                ubox = unit.get("source_bbox")
                if not isinstance(ubox, list) or len(ubox) != 4:
                    continue
                cx = (ubox[0] + ubox[2]) / 2
                cy = (ubox[1] + ubox[3]) / 2
                if not (rx0 <= cx <= rx1 and ry0 <= cy <= ry1):
                    continue
                # 抑制优先看结构：绑定到这个公式元素的单元必是它的碎片。
                # 文本启发式只给没有绑定信息的旧作业兜底；
                # 有中文译文的完整句子在 _is_formula_fragment 里被保住。
                bound_here = (
                    str(unit.get("_element_id") or "")
                    == str(planned.element_id)
                )
                if bound_here or _is_formula_fragment(unit):
                    text = str(
                        unit.get("translation") or unit.get("source") or ""
                    ).strip()
                    if text and not CJK_RE.search(
                        str(unit.get("translation") or "")
                    ):
                        suppress.append(text)
        caption = caption_text_for(element, by_id, texts)
        labels: list[dict[str, Any]] = []
        if planned.strategy in (
            "preserve-geometry-with-label-overlay",
            "preserve-geometry-with-numbered-legend",
        ):
            # 图内有中文译文的标签，坐标齐全就交给渲染层覆盖成中文；
            # 数字尺寸、通道数没有译文，原样留在图里。
            for label_id in (element.get("relations") or {}).get(
                EMBEDDED_LABEL_RELATION, []
            ):
                label_element = by_id.get(str(label_id))
                if label_element is None:
                    continue
                label_box = normalize_bbox(label_element.get("bbox"))
                translation = texts.get(str(label_id), "").strip()
                if label_box and CJK_TEXT_RE.search(translation):
                    labels.append(
                        {
                            "bbox": list(label_box),
                            "translation": translation,
                            "source": str(
                                label_element.get("text_excerpt") or ""
                            ),
                        }
                    )
        result.items.append(
            {
                "id": f"plan-{planned.element_id}",
                "page": page,
                "kind": KIND_PRESERVED,
                # 生成器只认这两个保留方法；按类型定的保留策略统一落到
                # 区域保留执行，原始策略记在 plan_strategy 里备查。
                "method": (
                    FALLBACK_PRESERVE_FULL_PAGE
                    if full_page
                    else FALLBACK_PRESERVE_ELEMENT_REGION
                ),
                "plan_strategy": planned.strategy,
                "status": STATUS_READY,
                "source_element_id": planned.element_id,
                # source_evidence 是一串给人核对的字符串，不是结构体。
                # 生成器要求每条复杂内容都能被人拿着原文对回去。
                "source_evidence": [
                    f"原文第 {page} 页元素 {planned.element_id}"
                    f"（{element.get('type') or '未知类型'}）",
                    f"渲染计划定为 {planned.strategy}",
                ],
                "payload": {
                    "render_policy": RENDER_POLICY,
                    # 公式裁切的最终框与扩展原因，供人核对（无则为 None）。
                    "formula_crop": formula_crop_info,
                    "suppress_texts": suppress,
                    "regions": [
                        {
                            "page": page,
                            "bbox": (
                                None
                                if full_page
                                else list(render_box or box or ())
                            ),
                            # 生成器的坐标替换机制认的键是 source_bbox：
                            # 落在这块区域里的正文单元会被移出正文流，
                            # 不写它，保留的区域和压平的流水文字会同时出现。
                            "source_bbox": (
                                None if full_page else list(box or ())
                            ),
                            "full_page": full_page,
                            "labels": labels,
                            "source_element_id": planned.element_id,
                            # 位图的 xref。已有条目按 xref 渲染同一张图时，
                            # 靠它认出"这张已经有人画了"，避免画两遍。
                            "xref": (element.get("detail") or {}).get("xref"),
                            # 生成器认这个键当图题：它会把图题和图锁成一块，
                            # 并把正文里重复的那一份抑制掉。
                            "translation": caption,
                        }
                    ],
                },
                "notes": (
                    "渲染计划把它定到保留级：重建不可靠，原样搬原文那一块"
                ),
            }
        )
    return result


def _region_overlap_ratio(first: list, second: list) -> float:
    """两个 bbox 的交叠占较小者面积的比例。"""

    x0 = max(float(first[0]), float(second[0]))
    y0 = max(float(first[1]), float(second[1]))
    x1 = min(float(first[2]), float(second[2]))
    y1 = min(float(first[3]), float(second[3]))
    if x1 <= x0 or y1 <= y0:
        return 0.0
    overlap = (x1 - x0) * (y1 - y0)
    area = min(
        max((first[2] - first[0]) * (first[3] - first[1]), 1e-6),
        max((second[2] - second[0]) * (second[3] - second[1]), 1e-6),
    )
    return overlap / area


def _covered_by_existing(
    candidate: dict[str, Any], items: list[dict[str, Any]]
) -> bool:
    """同页已有条目的区域是否已经盖住了这个元素。

    盖住了还再保留一次，同一块内容会在候选里出现两遍。
    只有带坐标的区域才能判交叠；没坐标的条目不当作覆盖。
    """

    region = (candidate.get("payload") or {}).get("regions", [{}])[0]
    xref = region.get("xref")
    if isinstance(xref, int):
        for item in items:
            if item.get("status") != "ready":
                continue
            if xref in _item_xrefs(item):
                return True
    box = region.get("bbox")
    if not isinstance(box, list) or len(box) != 4:
        return False
    page = candidate.get("page")
    for item in items:
        if item.get("page") != page or item.get("status") != "ready":
            continue
        for other in (item.get("payload") or {}).get("regions", []):
            other_box = other.get("bbox") if isinstance(other, dict) else None
            if (
                isinstance(other_box, list)
                and len(other_box) == 4
                and _region_overlap_ratio(box, other_box) >= 0.5
            ):
                return True
    return False


def merge_into_complex_content(
    complex_content: dict[str, Any], bridged: BridgeResult
) -> dict[str, Any]:
    """把翻译出来的条目并进复杂内容。

    同一个元素已经有条目的，**不覆盖**——那是别处按自己的判断安排好的，
    这里只补计划里定了、生成器却没有安排的那些。
    """

    merged = dict(complex_content or {})
    items = [item for item in merged.get("items", []) if isinstance(item, dict)]
    existing_ids = {str(item.get("id") or "") for item in items}
    existing_elements = {
        str(item.get("source_element_id") or "")
        for item in items
        if item.get("source_element_id")
    }

    added = 0
    for item in bridged.items:
        if item["id"] in existing_ids:
            continue
        if item["source_element_id"] in existing_elements:
            continue
        if _covered_by_existing(item, items):
            bridged.skipped.append(
                {
                    "element_id": item["source_element_id"],
                    "reason": "同页已有复杂条目的区域盖住了它，不重复保留",
                }
            )
            continue
        items.append(item)
        added += 1

    merged["items"] = items
    merged["plan_bridge"] = {
        "schema_version": SCHEMA_VERSION,
        "added": added,
        "skipped": list(bridged.skipped),
    }
    return merged


#: 复杂条目里挂图级图题用的键。
FIGURE_CAPTION_KEY = "figure_caption"


def _item_xrefs(item: dict[str, Any]) -> set[int]:
    payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
    found: set[int] = set()
    for region in payload.get("regions", []):
        if not isinstance(region, dict):
            continue
        xref = region.get("xref")
        if isinstance(xref, int):
            found.add(xref)
    return found


def attach_figure_captions(
    complex_content: dict[str, Any],
    elements: list[dict[str, Any]],
    unit_texts_by_element: dict[str, str],
) -> tuple[dict[str, Any], list[str]]:
    """把图级图题挂到它那个复杂条目上。

    四联子图里每一格自己的 (a)(b)(c)(d) 说明本来就内嵌在条目里，跟着图走。
    但整张图的图题（"图 3. ……"）是一条独立的译文单元，排在正文流里，
    随时可能被分到上一页或下一页去。

    挂上之后，生成器会把它和图锁成一块，并把正文里重复的那一份抑制掉。

    按图像 xref 对应。矢量图没有 xref，这里认不出来——如实返回，
    不按页码猜，猜错会把图题挂到别的图上。
    """

    merged = dict(complex_content or {})
    items = [item for item in merged.get("items", []) if isinstance(item, dict)]
    by_id = {
        str(element.get("id") or ""): element
        for element in elements
        if isinstance(element, dict)
    }

    caption_by_xref: dict[int, str] = {}
    for element in elements:
        if not isinstance(element, dict):
            continue
        xref = (element.get("detail") or {}).get("xref")
        if not isinstance(xref, int):
            continue
        text = caption_text_for(element, by_id, unit_texts_by_element)
        if text:
            caption_by_xref[xref] = text

    attached: list[str] = []
    for item in items:
        payload = item.get("payload")
        if not isinstance(payload, dict) or payload.get(FIGURE_CAPTION_KEY):
            continue
        for xref in sorted(_item_xrefs(item)):
            caption = caption_by_xref.get(xref)
            if caption:
                payload[FIGURE_CAPTION_KEY] = caption
                attached.append(str(item.get("id") or ""))
                break

    merged["items"] = items
    return (merged, attached)
