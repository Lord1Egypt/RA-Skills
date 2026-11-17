"""一次预检里共用的候选 PDF 分析。

同一次注册前预检要连着做指纹、注册、QA、作业校验和完整性审查。
以前每一步都自己 `fitz.open()` 一遍候选 PDF，再各自重新抽一遍文字：
同一份文件被完整解析五次，而性能计数器只统计了其中一部分。

这个模块把候选 PDF 的打开与文字抽取集中到一个对象上：

- 同一路径在同一次预检里只打开一次，靠引用计数决定谁负责关闭；
- 每页的纯文本、块和结构化字典各抽一次，之后命中缓存；
- 打开与抽取都计数，缓存命中单独计数，账目可以被测试验证。

它只做缓存，不改变任何判定结果：拿到的 document 就是 PyMuPDF 的对象。
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import perf_trace
from _common import SkillError, open_pdf

COUNTER_CANDIDATE_TEXT_EXTRACT = "candidate_text_extract"
COUNTER_CANDIDATE_ANALYSIS_REUSE = "candidate_analysis_reuse"

_ACTIVE: dict[str, CandidateAnalysis] = {}


def _key(path: Path) -> str:
    return str(Path(path).resolve())


class CandidateAnalysis:
    """一份候选 PDF 的共享分析句柄。"""

    def __init__(self, path: Path, *, role: str = "candidate") -> None:
        self.path = Path(path).resolve()
        self.role = role
        self._document = open_pdf(self.path, role=role)
        self._refs = 0
        self._text: dict[int, str] = {}
        self._blocks: dict[int, list[Any]] = {}
        self._dict: dict[int, dict[str, Any]] = {}

    @property
    def document(self) -> Any:
        if self._document is None:
            raise SkillError("候选分析已经关闭，不能再使用")
        return self._document

    @property
    def page_count(self) -> int:
        return int(self.document.page_count)

    def page(self, page_number: int) -> Any:
        """按 1 起的页码取页面对象。"""

        if not 1 <= page_number <= self.page_count:
            raise SkillError(
                f"候选页码越界: {page_number}，共 {self.page_count} 页"
            )
        return self.document[page_number - 1]

    def page_text(self, page_number: int) -> str:
        cached = self._text.get(page_number)
        if cached is not None:
            perf_trace.count(COUNTER_CANDIDATE_ANALYSIS_REUSE)
            return cached
        perf_trace.count(COUNTER_CANDIDATE_TEXT_EXTRACT)
        perf_trace.count(perf_trace.COUNTER_TEXT_PLAIN)
        value = str(self.page(page_number).get_text() or "")
        self._text[page_number] = value
        return value

    def page_blocks(self, page_number: int) -> list[Any]:
        cached = self._blocks.get(page_number)
        if cached is not None:
            perf_trace.count(COUNTER_CANDIDATE_ANALYSIS_REUSE)
            return cached
        perf_trace.count(perf_trace.COUNTER_TEXT_BLOCKS)
        value = list(self.page(page_number).get_text("blocks") or [])
        self._blocks[page_number] = value
        return value

    def page_dict(self, page_number: int) -> dict[str, Any]:
        cached = self._dict.get(page_number)
        if cached is not None:
            perf_trace.count(perf_trace.COUNTER_ANALYSIS_CACHE_HIT)
            return cached
        perf_trace.count(perf_trace.COUNTER_TEXT_DICT)
        value = dict(self.page(page_number).get_text("dict") or {})
        self._dict[page_number] = value
        return value

    def document_text(self) -> str:
        return "\n".join(
            self.page_text(number)
            for number in range(1, self.page_count + 1)
        )

    def _acquire(self) -> CandidateAnalysis:
        self._refs += 1
        return self

    def release(self) -> None:
        """归还一次引用；最后一个使用者负责真正关闭。"""

        self._refs -= 1
        if self._refs > 0:
            return
        _ACTIVE.pop(_key(self.path), None)
        if self._document is not None:
            self._document.close()
            self._document = None


def open_candidate_analysis(
    path: Path,
    *,
    role: str = "candidate",
) -> CandidateAnalysis:
    """取得候选分析；同一路径已经打开时直接复用，不重复解析。"""

    key = _key(path)
    existing = _ACTIVE.get(key)
    if existing is not None and existing._document is not None:
        perf_trace.count(COUNTER_CANDIDATE_ANALYSIS_REUSE)
        return existing._acquire()
    analysis = CandidateAnalysis(Path(path), role=role)
    _ACTIVE[key] = analysis
    return analysis._acquire()


@contextmanager
def candidate_analysis(
    path: Path,
    *,
    role: str = "candidate",
) -> Iterator[CandidateAnalysis]:
    analysis = open_candidate_analysis(path, role=role)
    try:
        yield analysis
    finally:
        analysis.release()


@contextmanager
def shared_candidate_analysis(
    path: Path,
    *,
    role: str = "candidate",
) -> Iterator[CandidateAnalysis]:
    """在一次预检的全程持有一份分析，让内层各步复用同一次打开。"""

    with candidate_analysis(path, role=role) as analysis:
        yield analysis


def active_paths() -> list[str]:
    """当前仍被持有的候选分析路径；测试用。"""

    return sorted(_ACTIVE)
