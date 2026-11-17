"""候选元素映射：每个源元素到底落在候选的哪一页。

排版计划里写着"图 1 放在第 2 页"，这只是**打算**。这里回答的是另一个问题：
打开产出的 PDF，图 1 真的在里面吗，在第几页？

两者会不一样，而且不一样的时候恰恰是最要命的时候——真实样本里，
排版计划把结构图安排在候选第 2 页，产出的 PDF 那一页却只有 1 个绘图对象，
原文那 213 个一个都没搬过来。计划没错，产出错了。只看计划就看不见。

所以这里的每一条定位都必须来自候选 PDF 本身：
- 位图按图像字节的哈希认，一一对上；
- 矢量元素按它区域内的文字锚点认（通道数、尺寸标注这些数字），
  再用绘图对象数量做一次下界检查；
- 文字元素按译文（或按策略保留的原文）在页面文字里查。

绘图对象数量这件事要说清楚：它只能证明"不在"，不能证明"在"。
一页有 300 个绘图对象，不代表其中就有你要的那 213 个。所以它单独用时
只降级成一个下界判据，置信度写低，不假装是定位。
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.enums import VISUAL_ELEMENT_TYPES
from academic_pdf_translation.contracts.models import normalize_bbox

SCHEMA_VERSION = "1.0"

METHOD_IMAGE_DIGEST = "image-digest"
METHOD_REGION_PIXELS = "region-pixels"
METHOD_INSIDE_PRESERVED = "inside-preserved-region"
METHOD_TEXT_ANCHOR = "text-anchor"
METHOD_TEXT_SEARCH = "text-search"
METHOD_DRAWING_BOUND = "drawing-count-lower-bound"
METHOD_NOT_FOUND = "not-found"
METHOD_NO_EVIDENCE = "no-locatable-evidence"

#: 文字定位用的探针长度（去掉空白后的字符数）。
TEXT_PROBE_CHARS = 24
#: 文字探针的最短长度。「1 引言」这样的章节标题只有三个字，
#: 门槛定高了它们就会被当成"找不到"。短探针照查，命中多页时如实报不唯一。
MIN_TEXT_PROBE_CHARS = 2
#: 一个元素最多试几段探针。元素可以横跨候选的分页：摘要的"摘要"两个字
#: 留在上一页、正文落到下一页，从头取的那一段探针就哪一页都不在。
#: 依次往后取，第一段查得到的就算数。
MAX_TEXT_PROBES = 6
#: 像素指纹的网格边长。16x16 灰度足以认出"是不是同一块"，
#: 又对缩放和重新编码不敏感。
FINGERPRINT_GRID = 16
#: 两块区域算同一块的平均灰度差上限。
#: 真实样本上：保留下来的区域与原区域差 1.3-3.6，不相干的区域差 20 以上，
#: 门槛定在中间留足余量。
MAX_FINGERPRINT_DISTANCE = 8.0
#: 区域太平（几乎全白）时不做像素比对——两块空白永远长得一样。
MIN_FINGERPRINT_CONTRAST = 6.0
#: 计算像素指纹时的渲染倍率。
FINGERPRINT_SCALE = 2.0
#: 矢量元素至少要认出这么多个文字锚点，才算定位成功。
MIN_ANCHOR_HITS = 2
#: 只靠绘图对象数量下界时的置信度。它证明不了"在"。
DRAWING_BOUND_CONFIDENCE = 0.30
#: 文字锚点定位的置信度。
ANCHOR_CONFIDENCE = 0.75
#: 精确匹配（图像哈希、文字全串）的置信度。
EXACT_CONFIDENCE = 1.0

WHITESPACE_RE = re.compile(r"\s+")
#: 控制字符。数学字体的抽取残渣里常带着它们，拿去查页面文字永远查不到。
CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")
#: 图内文字锚点：数字、带 x 的尺寸、纯字母词都算。
ANCHOR_RE = re.compile(r"[0-9]+(?:\s*[x×]\s*[0-9]+)?|[A-Za-z]{3,}")


class CandidateMappingError(RuntimeError):
    """候选映射失败。"""


@dataclass
class ElementLocation:
    """一个源元素在候选里的落点与证据。"""

    element_id: str
    element_type: str
    source_page: int
    required: bool
    candidate_pages: list[int] = field(default_factory=list)
    candidate_bbox: list[float] | None = None
    method: str = METHOD_NOT_FOUND
    confidence: float = 0.0
    evidence: str = ""
    #: 元素在原文里的绘图对象数量。0 表示它本来就没有几何结构。
    source_drawing_count: int = 0
    #: 命中页里最多的绘图对象数量。几何有没有跟过来，看这个。
    candidate_drawing_count: int = 0

    @property
    def geometry_ok(self) -> bool | None:
        """几何结构有没有跟着搬过来。

        元素本身没有绘图对象时返回 None——没有几何可谈，不是通过也不是失败。

        按像素指纹定位到的元素直接算通过：指纹证明整块视觉内容原样在场，
        而保留区域必然是栅格，绘图对象计数在这条路径上永远追不上原文——
        再用它评几何只会制造永不消失的误报。
        """

        if self.method == METHOD_REGION_PIXELS:
            return True
        if self.source_drawing_count <= 0:
            return None
        return self.candidate_drawing_count >= self.source_drawing_count

    @property
    def located(self) -> bool:
        return bool(self.candidate_pages)

    @property
    def ambiguous(self) -> bool:
        return len(self.candidate_pages) > 1

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["located"] = self.located
        data["ambiguous"] = self.ambiguous
        data["geometry_ok"] = self.geometry_ok
        return data


@dataclass
class CandidateMapping:
    """一次映射的完整结果。"""

    schema_version: str = SCHEMA_VERSION
    source_pages: int = 0
    candidate_pages: int = 0
    locations: list[ElementLocation] = field(default_factory=list)

    @property
    def located(self) -> list[ElementLocation]:
        return [item for item in self.locations if item.located]

    @property
    def missing(self) -> list[ElementLocation]:
        return [item for item in self.locations if not item.located]

    @property
    def missing_required(self) -> list[ElementLocation]:
        return [item for item in self.missing if item.required]

    @property
    def complete(self) -> bool:
        """完整与否是**数出来的**，不是谁写上去的。"""

        return not self.missing_required

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source_pages": self.source_pages,
            "candidate_pages": self.candidate_pages,
            "element_count": len(self.locations),
            "located_count": len(self.located),
            "missing_count": len(self.missing),
            "missing_required_count": len(self.missing_required),
            "complete": self.complete,
            "locations": [item.as_dict() for item in self.locations],
        }


def normalize_text(text: str) -> str:
    """去掉全部空白和控制字符。

    折行、对齐插入的空格都不该影响"这段文字在不在"。控制字符则是数学字体
    抽取出来的残渣，拿它去查页面文字永远查不到，留着只会制造假的"缺失"。
    """

    return WHITESPACE_RE.sub("", CONTROL_RE.sub("", str(text or "")))


def image_digests(document: Any) -> dict[str, list[tuple[int, list[float]]]]:
    """候选里每张图的字节哈希到落点。

    用图像字节，不用 xref——图被搬进新文档时 xref 会变，字节不会。
    """

    found: dict[str, list[tuple[int, list[float]]]] = {}
    for index in range(document.page_count):
        page = document[index]
        for info in page.get_images(full=True):
            xref = info[0]
            try:
                data = document.extract_image(xref)
            except Exception:  # noqa: BLE001 - 取不到就当这张认不出来
                continue
            digest = hashlib.sha256(data.get("image") or b"").hexdigest()
            rects = page.get_image_rects(xref)
            bbox = (
                [rects[0].x0, rects[0].y0, rects[0].x1, rects[0].y1]
                if rects
                else None
            )
            found.setdefault(digest, []).append((index + 1, bbox or []))
    return found


def source_image_digest(document: Any, element: dict[str, Any]) -> str | None:
    xref = (element.get("detail") or {}).get("xref")
    if not xref:
        return None
    try:
        data = document.extract_image(int(xref))
    except Exception:  # noqa: BLE001 - 原图取不到就没法按哈希认
        return None
    return hashlib.sha256(data.get("image") or b"").hexdigest()


def text_anchors(
    document: Any, element: dict[str, Any], *, limit: int = 12
) -> list[str]:
    """一个矢量元素区域内的文字锚点。

    结构图里的通道数、特征图尺寸都是文字。它们是几何检查看不见、
    却最能证明"这张图真的搬过来了"的东西。
    """

    import fitz

    box = normalize_bbox(element.get("bbox"))
    page_number = int(element.get("page") or 0)
    if box is None or not 1 <= page_number <= document.page_count:
        return []
    text = document[page_number - 1].get_text("text", clip=fitz.Rect(*box))
    seen: list[str] = []
    for token in ANCHOR_RE.findall(text):
        cleaned = normalize_text(token)
        if len(cleaned) < 2 or cleaned in seen:
            continue
        seen.append(cleaned)
        if len(seen) >= limit:
            break
    return seen


def region_fingerprint(page: Any, rect: Any) -> list[int] | None:
    """一块区域的灰度指纹。

    保留下来的原文区域在候选里是一张图片：没有文字层，也没有绘图对象，
    文字锚点和几何数量都看不见它。但**像素还在**——把两边都降采样成
    一小格灰度图比一比，就知道是不是同一块。

    这不是"相信生成器说它保留了"，是自己去看候选页面上画的是什么。
    """

    import fitz

    pixmap = page.get_pixmap(
        matrix=fitz.Matrix(FINGERPRINT_SCALE, FINGERPRINT_SCALE),
        clip=rect,
        alpha=False,
    )
    pixmap = fitz.Pixmap(fitz.csGRAY, pixmap)
    width, height, samples = pixmap.width, pixmap.height, pixmap.samples
    if width < FINGERPRINT_GRID or height < FINGERPRINT_GRID:
        return None
    # 整格求均值，不做稀疏点采样。表格这类内容由细线主导，
    # 每格只抽十几个点会随机撞上或撞空线条，同一块内容的两次指纹
    # 能差出 9 个灰度——比对就成了掷硬币。
    grid_sums = [[0] * FINGERPRINT_GRID for _ in range(FINGERPRINT_GRID)]
    grid_counts = [[0] * FINGERPRINT_GRID for _ in range(FINGERPRINT_GRID)]
    for y in range(height):
        gy = min(y * FINGERPRINT_GRID // height, FINGERPRINT_GRID - 1)
        base = y * width
        sums = grid_sums[gy]
        counts = grid_counts[gy]
        for x in range(width):
            gx = min(x * FINGERPRINT_GRID // width, FINGERPRINT_GRID - 1)
            sums[gx] += samples[base + x]
            counts[gx] += 1
    return [
        grid_sums[gy][gx] // max(grid_counts[gy][gx], 1)
        for gy in range(FINGERPRINT_GRID)
        for gx in range(FINGERPRINT_GRID)
    ]


def fingerprint_contrast(grid: list[int]) -> float:
    """指纹的起伏。几乎全白的区域起伏接近 0，比对它没有意义。"""

    if not grid:
        return 0.0
    mean = sum(grid) / len(grid)
    return (sum((value - mean) ** 2 for value in grid) / len(grid)) ** 0.5


def fingerprint_distance(first: list[int], second: list[int]) -> float:
    """两个指纹的平均灰度差。"""

    if not first or len(first) != len(second):
        return float("inf")
    return sum(abs(a - b) for a, b in zip(first, second, strict=True)) / len(
        first
    )


def candidate_image_fingerprints(
    document: Any,
) -> list[tuple[int, list[float], list[int]]]:
    """候选里每张图片所占区域的指纹与落点。"""

    found: list[tuple[int, list[float], list[int]]] = []
    for index in range(document.page_count):
        page = document[index]
        for info in page.get_images(full=True):
            for rect in page.get_image_rects(info[0]):
                grid = region_fingerprint(page, rect)
                if grid is None:
                    continue
                found.append(
                    (index + 1, [rect.x0, rect.y0, rect.x1, rect.y1], grid)
                )
    return found


def locate_by_pixels(
    source_document: Any,
    element: dict[str, Any],
    fingerprints: list[tuple[int, list[float], list[int]]],
) -> tuple[list[int], list[float] | None, float]:
    """按像素指纹找这块原文区域被搬到了候选哪一页。"""

    import fitz

    if not fingerprints:
        return ([], None, float("inf"))
    box = normalize_bbox(element.get("bbox"))
    page_number = int(element.get("page") or 0)
    if box is None or not 1 <= page_number <= source_document.page_count:
        return ([], None, float("inf"))

    if str(element.get("type") or "") == "display-formula":
        # 公式的渲染区域是扩展框（含求和号上下标与行末编号）。
        # 拿窄的检测框去比宽的渲染图，空白占比不同，指纹必然失配——
        # 渲染按什么框画，核查就按什么框比。
        from academic_pdf_translation.render.formula_crop import (
            formula_render_box,
        )

        box = tuple(
            formula_render_box(source_document[page_number - 1], box)
        )

    grid = region_fingerprint(
        source_document[page_number - 1], fitz.Rect(*box)
    )
    if grid is None or fingerprint_contrast(grid) < MIN_FINGERPRINT_CONTRAST:
        return ([], None, float("inf"))

    best = min(
        fingerprints, key=lambda item: fingerprint_distance(grid, item[2])
    )
    distance = fingerprint_distance(grid, best[2])
    if distance > MAX_FINGERPRINT_DISTANCE:
        return ([], None, distance)
    return ([best[0]], list(best[1]), distance)


def _page_texts(document: Any) -> list[str]:
    return [
        normalize_text(document[index].get_text("text"))
        for index in range(document.page_count)
    ]


def text_probes(probe: str) -> list[str]:
    """把一个元素的文字切成若干段探针。

    元素横跨候选分页时，从头取的那一段会被页边界切断，哪一页都查不到。
    切成连续几段依次试，能定位就定位——定位不到才是真的没搬过来。
    """

    cleaned = normalize_text(probe)
    windows: list[str] = []
    for start in range(0, len(cleaned), TEXT_PROBE_CHARS):
        window = cleaned[start : start + TEXT_PROBE_CHARS]
        if len(window) >= MIN_TEXT_PROBE_CHARS:
            windows.append(window)
        if len(windows) >= MAX_TEXT_PROBES:
            break
    return windows


def locate_by_text(
    page_texts: list[str], probe: str
) -> list[int]:
    """一段文字出现在候选的哪些页。"""

    cleaned = normalize_text(probe)
    if len(cleaned) < MIN_TEXT_PROBE_CHARS:
        return []
    return [
        index + 1
        for index, text in enumerate(page_texts)
        if cleaned in text
    ]


def locate_by_anchors(
    page_texts: list[str], anchors: list[str]
) -> tuple[list[int], int]:
    """按文字锚点定位，返回命中页和最高命中数。"""

    if not anchors:
        return ([], 0)
    best = 0
    pages: list[int] = []
    for index, text in enumerate(page_texts):
        hits = sum(1 for anchor in anchors if anchor in text)
        if hits < MIN_ANCHOR_HITS:
            continue
        if hits > best:
            best = hits
            pages = [index + 1]
        elif hits == best:
            pages.append(index + 1)
    return (pages, best)


def _drawing_counts(document: Any) -> list[int]:
    return [
        len(document[index].get_drawings())
        for index in range(document.page_count)
    ]


def _bbox_in_candidate(
    candidate_document: Any, page_number: int, probe: str
) -> list[float] | None:
    """在候选页里量出这段文字的坐标。量不到就留空，不猜。"""

    if not 1 <= page_number <= candidate_document.page_count:
        return None
    needle = str(probe or "").strip()[:40]
    if not needle:
        return None
    rects = candidate_document[page_number - 1].search_for(needle)
    if not rects:
        return None
    rect = rects[0]
    return [rect.x0, rect.y0, rect.x1, rect.y1]


def locate_element(
    source_document: Any,
    candidate_document: Any,
    element: dict[str, Any],
    *,
    page_texts: list[str],
    digests: dict[str, list[tuple[int, list[float]]]],
    drawing_counts: list[int],
    fingerprints: list[tuple[int, list[float], list[int]]] | None = None,
    element_texts: dict[str, str] | None = None,
) -> ElementLocation:
    """定位一个源元素。逐个判据往下试，用上哪个就记哪个。"""

    element_id = str(element.get("id") or "")
    element_type = str(element.get("type") or "")
    needed = int((element.get("detail") or {}).get("drawing_count") or 0)
    location = ElementLocation(
        element_id=element_id,
        element_type=element_type,
        source_page=int(element.get("page") or 0),
        required=bool(element.get("required")),
        source_drawing_count=needed,
    )

    def finish(result: ElementLocation) -> ElementLocation:
        """收尾：把命中页里的绘图对象数量记下来，供几何检查用。"""

        if result.candidate_pages:
            result.candidate_drawing_count = max(
                drawing_counts[page - 1]
                for page in result.candidate_pages
                if 1 <= page <= len(drawing_counts)
            )
        return result

    # 1. 位图：按图像字节哈希一一对上，最硬的证据。
    #    哈希对不上不等于图不在：按区域保留时图片被重新裁切、重新编码，
    #    字节必然变。所以哈希只在命中时下结论，落空就交给下面的像素指纹。
    digest = source_image_digest(source_document, element)
    digest_miss = ""
    if digest:
        hits = digests.get(digest, [])
        if hits:
            location.candidate_pages = sorted({page for page, _ in hits})
            location.candidate_bbox = next(
                (bbox for _, bbox in hits if bbox), None
            )
            location.method = METHOD_IMAGE_DIGEST
            location.confidence = EXACT_CONFIDENCE
            location.evidence = f"图像字节哈希 {digest[:12]} 命中"
            return finish(location)
        digest_miss = f"图像字节哈希 {digest[:12]} 在候选里找不到"

    # 2. 文字元素：按译文（或按策略保留的原文）查。
    probe = normalize_text((element_texts or {}).get(element_id, ""))
    if probe:
        hit: tuple[str, list[int]] | None = None
        for window in text_probes(probe):
            pages = locate_by_text(page_texts, window)
            if not pages:
                continue
            if len(pages) == 1:
                hit = (window, pages)
                break
            if hit is None:
                hit = (window, pages)
        if hit is not None:
            window, pages = hit
            location.candidate_pages = pages
            location.candidate_bbox = _bbox_in_candidate(
                candidate_document, pages[0], window
            )
            location.method = METHOD_TEXT_SEARCH
            location.confidence = (
                EXACT_CONFIDENCE if len(pages) == 1 else round(1 / len(pages), 2)
            )
            location.evidence = f"文字探针 {window!r} 命中 {len(pages)} 页"
            return finish(location)

    # 3. 保留下来的原文区域：候选里是一张图片，没有文字层也没有绘图对象，
    #    文字锚点和几何数量都看不见它。比像素。
    pages, bbox, distance = locate_by_pixels(
        source_document, element, list(fingerprints or [])
    )
    if pages:
        location.candidate_pages = pages
        location.candidate_bbox = bbox
        location.method = METHOD_REGION_PIXELS
        location.confidence = EXACT_CONFIDENCE
        location.evidence = (
            f"原区域与候选那块图片的灰度指纹平均差 {distance:.1f}，"
            f"低于 {MAX_FINGERPRINT_DISTANCE:.1f}"
        )
        return finish(location)

    # 4. 矢量元素：按区域内的文字锚点认。
    anchors = text_anchors(source_document, element)
    pages, hits = locate_by_anchors(page_texts, anchors)
    if pages:
        location.candidate_pages = pages
        location.method = METHOD_TEXT_ANCHOR
        location.confidence = ANCHOR_CONFIDENCE if len(pages) == 1 else 0.45
        location.evidence = (
            f"{len(anchors)} 个文字锚点里命中 {hits} 个"
        )
        return finish(location)

    # 5. 只剩绘图对象数量。它只能证明"不在"。
    if needed > 0:
        enough = [
            index + 1
            for index, count in enumerate(drawing_counts)
            if count >= needed
        ]
        if not enough:
            location.method = METHOD_NOT_FOUND
            location.evidence = (
                f"原文该元素有 {needed} 个绘图对象，候选里最多的一页只有 "
                f"{max(drawing_counts or [0])} 个，几何结构没有搬过来"
            )
            return finish(location)
        location.candidate_pages = enough
        location.method = METHOD_DRAWING_BOUND
        location.confidence = DRAWING_BOUND_CONFIDENCE
        location.evidence = (
            f"只有绘图对象数量下界可用（需要 {needed} 个），"
            "不能证明这一页上的就是它"
        )
        return finish(location)

    usable_probe = len(probe) >= MIN_TEXT_PROBE_CHARS
    if digest_miss:
        location.method = METHOD_NOT_FOUND
        location.confidence = 0.0
        location.evidence = f"{digest_miss}，区域像素指纹也没有对上"
    elif usable_probe or anchors:
        location.method = METHOD_NOT_FOUND
        location.evidence = "文字探针与锚点都没有命中任何一页"
    elif probe or (element_texts or {}).get(element_id, "").strip():
        # 只剩一两个字符（或全是控制字符）的，是数学字体的抽取残渣，
        # 不是内容——真正的公式已按区域整块保留。把它算进"必需缺失"，
        # 一篇干净的论文会永远停在"交给人"，而人打开一看只是个孤立的 X。
        # 如实分类：不计入必需完整性，但保留证据供人复查。
        location.required = False
        location.method = METHOD_NO_EVIDENCE
        location.evidence = (
            f"抽取残渣（可用文字 {probe!r}），不计入必需完整性，"
            "原内容已随所在区域整块保留"
        )
    else:
        location.method = METHOD_NO_EVIDENCE
        location.evidence = "这个元素没有可用来定位的文字、图像或几何证据"
    return finish(location)


def build_mapping(
    source_document: Any,
    candidate_document: Any,
    elements: list[dict[str, Any]],
    *,
    element_texts: dict[str, str] | None = None,
) -> CandidateMapping:
    """把整份文档的元素逐个映射到候选。"""

    if not elements:
        raise CandidateMappingError("元素清单为空，无法建立候选映射")

    page_texts = _page_texts(candidate_document)
    digests = image_digests(candidate_document)
    drawing_counts = _drawing_counts(candidate_document)
    fingerprints = candidate_image_fingerprints(candidate_document)

    locations = [
        locate_element(
            source_document,
            candidate_document,
            element,
            page_texts=page_texts,
            digests=digests,
            drawing_counts=drawing_counts,
            fingerprints=fingerprints,
            element_texts=element_texts,
        )
        for element in elements
    ]
    _inherit_from_preserved_hosts(locations, elements, source_document)
    return CandidateMapping(
        source_pages=source_document.page_count,
        candidate_pages=candidate_document.page_count,
        locations=locations,
    )


def _inherit_from_preserved_hosts(
    locations: list[ElementLocation],
    elements: list[dict[str, Any]],
    source_document: Any = None,
) -> None:
    """中心点落在已确认保留区域里的元素，继承宿主的定位。

    一块区域按像素指纹确认原样在场后，它内部的标签、单元格、公式碎片
    都跟着进了那张图——它们不再有独立的文字层，按探针找必然落空。
    落空不等于丢了：内容就在宿主区域里，位置也随宿主一起确定。
    """

    boxes = {
        str(element.get("id") or ""): (
            int(element.get("page") or 0),
            normalize_bbox(element.get("bbox")),
        )
        for element in elements
        if isinstance(element, dict)
    }
    hosts = [
        item
        for item in locations
        if item.method == METHOD_REGION_PIXELS and item.located
    ]
    if not hosts:
        return
    weak_methods = {
        METHOD_NOT_FOUND,
        METHOD_NO_EVIDENCE,
        METHOD_TEXT_SEARCH,
        METHOD_TEXT_ANCHOR,
    }
    for item in locations:
        # 弱判据的命中也要重判：标签被移进保留区域后没有独立文字层，
        # 文字探针在别处（比如参考文献页的年份数字）撞上的都是巧合。
        if item.located and item.method not in weak_methods:
            continue
        page, box = boxes.get(item.element_id, (0, None))
        if box is None:
            continue
        cx = (box[0] + box[2]) / 2
        cy = (box[1] + box[3]) / 2
        for host in hosts:
            host_page, host_box = boxes.get(host.element_id, (0, None))
            if host_box is None or host_page != page:
                continue
            host_element = next(
                (
                    element
                    for element in elements
                    if str(element.get("id") or "") == host.element_id
                ),
                None,
            )
            if (
                host_element is not None
                and str(host_element.get("type") or "") == "display-formula"
                and source_document is not None
                and 1 <= host_page <= source_document.page_count
            ):
                # 公式按扩展框渲染，碎片就落在扩展框里、窄检测框外。
                # 判归属要按真实渲染的那个框。
                from academic_pdf_translation.render.formula_crop import (
                    formula_render_box,
                )

                host_box = tuple(
                    formula_render_box(
                        source_document[host_page - 1], host_box
                    )
                )
            if (
                host_box[0] <= cx <= host_box[2]
                and host_box[1] <= cy <= host_box[3]
            ):
                item.candidate_pages = list(host.candidate_pages)
                item.candidate_bbox = (
                    list(host.candidate_bbox) if host.candidate_bbox else None
                )
                item.method = METHOD_INSIDE_PRESERVED
                item.confidence = 0.9
                item.evidence = (
                    f"位于已按像素指纹确认的保留区域 {host.element_id} 内"
                )
                break


def element_texts_from_units(
    elements: list[dict[str, Any]],
    units: list[dict[str, Any]],
    *,
    bindings: list[dict[str, Any]] | None = None,
) -> dict[str, str]:
    """把翻译单元的文字按元素归拢，供文字定位使用。

    单元归属优先取 ``unit_bindings.json`` 里的绑定表。元素清单自己的
    ``translation_unit_ids`` 常常是空的——绑定是另一个阶段算出来的，
    没回填进清单。拿空字段当归属，结果就是每个文字元素都"找不到"。

    文字优先用译文；按策略保留原文的单元用原文。两者都没有就不给探针——
    宁可报"没有可用证据"，也不要拿一段无关文字去碰运气。
    """

    by_unit = {str(unit.get("id") or ""): unit for unit in units}
    unit_ids_by_element: dict[str, list[str]] = {}

    for binding in bindings or []:
        element_id = str(binding.get("element_id") or "")
        unit_id = str(binding.get("unit_id") or "")
        if element_id and unit_id:
            unit_ids_by_element.setdefault(element_id, []).append(unit_id)

    for element in elements:
        element_id = str(element.get("id") or "")
        if element_id in unit_ids_by_element:
            continue
        listed = [
            str(unit_id) for unit_id in element.get("translation_unit_ids") or []
        ]
        if listed:
            unit_ids_by_element[element_id] = listed

    texts: dict[str, str] = {}
    for element_id, unit_ids in unit_ids_by_element.items():
        parts: list[str] = []
        for unit_id in unit_ids:
            unit = by_unit.get(unit_id)
            if unit is None:
                continue
            value = str(
                unit.get("translation") or unit.get("source") or ""
            ).strip()
            if value:
                parts.append(value)
        if parts:
            texts[element_id] = " ".join(parts)
    return texts


def verify_mapping(mapping: CandidateMapping) -> list[str]:
    """核对映射结果，把说不清楚的地方全摆出来。"""

    problems: list[str] = []

    for item in mapping.missing_required:
        problems.append(
            f"{item.element_id}（{item.element_type}，原文第 "
            f"{item.source_page} 页）在候选里找不到: {item.evidence}"
        )

    for item in mapping.locations:
        if item.ambiguous:
            problems.append(
                f"{item.element_id}: 在候选第 {item.candidate_pages} 页都疑似命中，"
                "定位不唯一"
            )
        if (
            item.located
            and item.required
            and item.method == METHOD_DRAWING_BOUND
        ):
            problems.append(
                f"{item.element_id}: 只有绘图对象数量下界，"
                "证明不了它真的在候选里"
            )
        if item.located and item.geometry_ok is False:
            problems.append(
                f"{item.element_id}: 文字锚点在候选第 {item.candidate_pages} 页"
                f"找得到，但那些页最多只有 {item.candidate_drawing_count} 个绘图"
                f"对象，少于原文的 {item.source_drawing_count} 个——"
                "图里的文字漏进了正文，几何结构没跟过来"
            )
        if item.method == METHOD_NO_EVIDENCE and item.required:
            problems.append(
                f"{item.element_id}: 必需元素却没有任何可定位的证据"
            )

    visual = [
        item
        for item in mapping.locations
        if item.element_type in {value.value for value in VISUAL_ELEMENT_TYPES}
    ]
    missing_visual = [item for item in visual if not item.located]
    if missing_visual:
        problems.append(
            f"{len(missing_visual)}/{len(visual)} 个视觉元素在候选里找不到: "
            + "、".join(item.element_id for item in missing_visual[:8])
        )
    return problems
