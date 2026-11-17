"""原文 PDF 的单次扫描结果。

原来 `pdf_profile.profile_pdf()` 和 `extract_source_structure()` 各自打开一次
原文，并各自逐页调用 `get_text("dict")`、`get_drawings()`、`get_image_info()`。
本模块把这些原始读取合并成一次，两个下游模块改为消费同一份结果。

约定：

- 只负责“读”，不做任何路线判断、单元切分或质量结论；
- 返回的原始结构按只读方式共享，调用方不得原地修改；
- 派生结论仍由 `pdf_profile` 和 `extract_source_structure` 各自计算，
  因此输出与旧版逐字段一致。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import perf_trace
from _common import (
    SkillError,
    import_fitz,
    open_pdf,
    sha256_file,
    utc_now,
    write_json,
)


ANALYSIS_SCHEMA_VERSION = "1.0"
ANALYZER_BUILD_VERSION = "source-analysis-1"


@dataclass(frozen=True)
class PageScan:
    """一页原文的原始读取结果。"""

    number: int
    width: float
    height: float
    rotation: int
    text_dict: dict[str, Any]
    text_blocks: tuple[Any, ...]
    plain_text: str
    image_info: tuple[dict[str, Any], ...]
    drawing_bboxes: tuple[tuple[float, float, float, float], ...]
    drawing_count: int
    image_count: int


@dataclass(frozen=True)
class SourceAnalysis:
    """整份原文的一次性扫描结果。"""

    path: Path
    sha256: str
    page_count: int
    pages: tuple[PageScan, ...]
    pymupdf_version: str
    schema_version: str = ANALYSIS_SCHEMA_VERSION
    analyzer_version: str = ANALYZER_BUILD_VERSION
    generated_at: str = field(default_factory=utc_now)

    @property
    def cache_key(self) -> dict[str, str]:
        return {
            "source_sha256": self.sha256,
            "schema_version": self.schema_version,
            "pymupdf_major": self.pymupdf_version.split(".", 1)[0],
            "analyzer_version": self.analyzer_version,
        }

    def all_plain_text(self) -> str:
        return "\n".join(page.plain_text for page in self.pages)


_MEMO: dict[tuple[str, str], SourceAnalysis] = {}


def _pymupdf_version() -> str:
    fitz = import_fitz()
    version = getattr(fitz, "VersionBind", None)
    if not version:
        version = getattr(fitz, "__doc__", "") or ""
    return str(version) or "unknown"


def _scan_page(page: Any, number: int) -> PageScan:
    text_dict = page.get_text("dict")
    perf_trace.count(perf_trace.COUNTER_TEXT_DICT)
    text_blocks = tuple(page.get_text("blocks"))
    perf_trace.count(perf_trace.COUNTER_TEXT_BLOCKS)
    plain_text = page.get_text("text")
    perf_trace.count(perf_trace.COUNTER_TEXT_PLAIN)
    image_info = tuple(page.get_image_info(xrefs=True))
    perf_trace.count(perf_trace.COUNTER_IMAGE_INFO)
    drawings = page.get_drawings()
    perf_trace.count(perf_trace.COUNTER_DRAWINGS)

    boxes: list[tuple[float, float, float, float]] = []
    for drawing in drawings:
        rect = drawing.get("rect")
        if rect is None:
            continue
        boxes.append(
            (
                round(float(rect.x0), 3),
                round(float(rect.y0), 3),
                round(float(rect.x1), 3),
                round(float(rect.y1), 3),
            )
        )

    return PageScan(
        number=number,
        width=float(page.rect.width),
        height=float(page.rect.height),
        rotation=int(page.rotation),
        text_dict=text_dict,
        text_blocks=text_blocks,
        plain_text=plain_text,
        image_info=image_info,
        drawing_bboxes=tuple(boxes),
        drawing_count=len(drawings),
        image_count=len(page.get_images(full=True)),
    )


def analyze_source(
    source: Path,
    *,
    sha256: str | None = None,
    use_memo: bool = True,
) -> SourceAnalysis:
    """一次打开原文，逐页只读取一遍所需的全部原始结构。"""

    source = Path(source).resolve()
    if not source.is_file():
        raise SkillError(f"PDF 不存在: {source}")
    digest = sha256 or sha256_file(source)
    memo_key = (str(source), digest)
    if use_memo:
        cached = _MEMO.get(memo_key)
        if cached is not None:
            perf_trace.count(perf_trace.COUNTER_ANALYSIS_CACHE_HIT)
            return cached

    with perf_trace.stage("source_analysis", source=source.name):
        document = open_pdf(source, role="source")
        try:
            if document.page_count < 1:
                raise SkillError(f"PDF 没有页面: {source}")
            pages = tuple(
                _scan_page(page, number)
                for number, page in enumerate(document, 1)
            )
            page_count = int(document.page_count)
        finally:
            document.close()

    analysis = SourceAnalysis(
        path=source,
        sha256=digest,
        page_count=page_count,
        pages=pages,
        pymupdf_version=_pymupdf_version(),
    )
    if use_memo:
        _MEMO[memo_key] = analysis
    return analysis


def clear_memo() -> None:
    _MEMO.clear()


def analysis_record(analysis: SourceAnalysis) -> dict[str, Any]:
    """写入作业目录的分析凭据。

    只记录缓存键与逐页规模，不落盘 `text_dict` 原文结构：那份数据体积可能
    超过原 PDF，而派生结果已经完整保存在 `source_manifest.json` 与
    `source_structure.json` 中。
    """

    return {
        "schema_version": analysis.schema_version,
        "generated_at": analysis.generated_at,
        "source": str(analysis.path),
        "cache_key": analysis.cache_key,
        "page_count": analysis.page_count,
        "single_pass": True,
        "pages": [
            {
                "page": page.number,
                "width": round(page.width, 3),
                "height": round(page.height, 3),
                "rotation": page.rotation,
                "text_blocks": len(
                    [
                        block
                        for block in page.text_dict.get("blocks", [])
                        if block.get("type") == 0
                    ]
                ),
                "images": page.image_count,
                "drawings": page.drawing_count,
                "text_chars": len(page.plain_text.strip()),
            }
            for page in analysis.pages
        ],
        "note": (
            "本文件是单次扫描的凭据与规模画像；派生结论见 "
            "source_manifest.json 与 source_structure.json。"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="对原文 PDF 执行一次性扫描并写出分析凭据"
    )
    parser.add_argument("source_pdf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        analysis = analyze_source(args.source_pdf)
        output = args.output or args.source_pdf.with_suffix(
            ".source-analysis.json"
        )
        write_json(output.resolve(), analysis_record(analysis))
        print(f"分析凭据已写入: {output.resolve()}")
        print(f"页数: {analysis.page_count}")
        print(
            "原文 PDF 打开次数: "
            f"{perf_trace.counter(perf_trace.COUNTER_SOURCE_PDF_OPEN)}"
        )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
