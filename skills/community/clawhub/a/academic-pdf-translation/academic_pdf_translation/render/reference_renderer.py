"""参考文献渲染器。

独立复审 R-011 报的是两件小事，但它们让参考文献不能用：

1. ``net-\\nworks`` 被原样搬了过去，变成 "net-works"。学术 PDF 的两端对齐
   会在行末插入软连字符，行一合并，这个连字符就该消失。
2. URL 在行末被切断后，合并时被塞进一个空格，链接点不开。

难的是**软连字符和真连字符长得一模一样**。``human-level`` 里的连字符要留，
``net-works`` 里的要删。这里不猜，用文档自己的词表判：合起来的词在文中
别处出现过就合，带连字符的写法在别处出现过就留。两样证据都没有、
而左半截本身又是文中出现过的词时，保留连字符**并标记证据不足**——
宁可让人来看一眼，也不要悄悄拼出一个不存在的词。
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any

#: 行末断词：左右两半都至少两个字母。
LINE_BREAK_HYPHEN_RE = re.compile(r"([A-Za-z]{2,})-\n([A-Za-z]{2,})")
#: URL。词表要把它们剔掉——``codesolorzano.com`` 会让 "com" 冒充英文词。
URL_RE = re.compile(r"(?:https?://|www\.)\S+")
WORD_RE = re.compile(r"[A-Za-z]{2,}")
HYPHENATED_RE = re.compile(r"[A-Za-z]+-[A-Za-z]+")
#: 条目编号：1. / [1] / (1)
ENTRY_NUMBER_RE = re.compile(r"^\s*(?:\[(\d{1,3})\]|\((\d{1,3})\)|(\d{1,3})\.)\s+")
#: URL 在行末被切断时，行尾多半停在这些字符上。
URL_CONTINUES_ON = ("/", "-", "_", "=", "&", "?", ".", "~")
#: 左半截要算"文中出现过的词"，至少这么长。
MIN_STANDALONE_LEN = 3

DECISION_JOIN = "join"
DECISION_KEEP = "keep-hyphen"


class ReferenceRenderError(RuntimeError):
    """参考文献渲染失败。"""


@dataclass
class HyphenDecision:
    """一处行末断词的判定与它的依据。"""

    left: str
    right: str
    decision: str
    evidence: str
    uncertain: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReferenceEntry:
    """一条参考文献。"""

    number: str
    text: str
    translation_unit_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RenderedReferences:
    """参考文献列表的渲染结果与证据。"""

    element_id: str
    entries: list[dict[str, Any]] = field(default_factory=list)
    hyphen_decisions: list[dict[str, Any]] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def numbers(self) -> list[str]:
        return [str(entry["number"]) for entry in self.entries]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["numbers"] = self.numbers
        return data


def build_vocabulary(text: str) -> Counter:
    """从文档全文数出词频，作为断词判定的证据。

    两处必须先剔掉，否则词表会"自己证明自己"：
    行末断词的两个碎片，以及 URL 里的域名片段。
    """

    plain = URL_RE.sub(" ", LINE_BREAK_HYPHEN_RE.sub("\n", str(text or "")))
    return Counter(word.lower() for word in WORD_RE.findall(plain))


def build_hyphenated_forms(text: str) -> set[str]:
    """文中别处出现过的、带连字符的写法。"""

    plain = URL_RE.sub(" ", LINE_BREAK_HYPHEN_RE.sub("\n", str(text or "")))
    return {
        form.lower() for form in HYPHENATED_RE.findall(plain.replace("\n", " "))
    }


def decide_hyphen(
    left: str,
    right: str,
    vocabulary: Counter,
    hyphenated_forms: set[str],
) -> HyphenDecision:
    """判一处行末断词该合还是该留。"""

    lower_left, lower_right = left.lower(), right.lower()
    joined = lower_left + lower_right
    if vocabulary.get(joined):
        return HyphenDecision(
            left, right, DECISION_JOIN, f"合成词 {joined!r} 在文中出现过"
        )
    if f"{lower_left}-{lower_right}" in hyphenated_forms:
        return HyphenDecision(
            left,
            right,
            DECISION_KEEP,
            f"带连字符的写法 {lower_left}-{lower_right!r} 在文中出现过",
        )
    if len(lower_left) >= MIN_STANDALONE_LEN and vocabulary.get(lower_left):
        return HyphenDecision(
            left,
            right,
            DECISION_KEEP,
            f"左半截 {lower_left!r} 本身是文中出现过的词，但合成词没出现过，"
            "无法判定是软连字符还是真连字符",
            uncertain=True,
        )
    return HyphenDecision(
        left,
        right,
        DECISION_JOIN,
        f"左半截 {lower_left!r} 不是文中出现过的词，按行末软连字符处理",
    )


def dehyphenate(
    text: str, vocabulary: Counter, hyphenated_forms: set[str]
) -> tuple[str, list[HyphenDecision]]:
    """合并行末断词，逐处留下判定依据。"""

    decisions: list[HyphenDecision] = []

    def replace(match: re.Match[str]) -> str:
        decision = decide_hyphen(
            match.group(1), match.group(2), vocabulary, hyphenated_forms
        )
        decisions.append(decision)
        if decision.decision == DECISION_JOIN:
            return f"{match.group(1)}{match.group(2)}"
        return f"{match.group(1)}-{match.group(2)}"

    return (LINE_BREAK_HYPHEN_RE.sub(replace, str(text or "")), decisions)


def join_lines(text: str) -> str:
    """合并折行。URL 被行末切断时**不许**补空格。"""

    lines = [line.strip() for line in str(text or "").splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return ""
    out = lines[0]
    for line in lines[1:]:
        if _url_continues(out):
            out += line
        else:
            out += " " + line
    return out


def _url_continues(text: str) -> bool:
    """上一行是不是停在一个没写完的 URL 上。"""

    tail = text.rsplit(" ", 1)[-1] if " " in text else text
    if "://" not in tail and not tail.lower().startswith("www."):
        return False
    return tail.endswith(URL_CONTINUES_ON)


def extract_urls(text: str) -> list[str]:
    return URL_RE.findall(str(text or ""))


def source_urls(raw_text: str) -> list[str]:
    """原文里的完整 URL。

    必须先按同一套规则合行再抽，否则被行末切断的 URL 会连上下一条的编号，
    抽出一个根本不存在的地址——核对就变成了自己吓自己。
    """

    return [
        url
        for line in _entry_chunks(raw_text)
        for url in extract_urls(join_lines(line))
    ]


def _entry_chunks(raw_text: str) -> list[str]:
    """按条目切块。条目之间不许跨着合行。"""

    chunks: list[str] = []
    buffer: list[str] = []
    for raw_line in str(raw_text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ENTRY_NUMBER_RE.match(line) and buffer:
            chunks.append("\n".join(buffer))
            buffer = []
        buffer.append(line)
    if buffer:
        chunks.append("\n".join(buffer))
    return chunks


def split_reference_entries(text: str) -> list[ReferenceEntry]:
    """按编号把参考文献拆成一条一条。"""

    entries: list[ReferenceEntry] = []
    number: str | None = None
    buffer: list[str] = []
    for raw_line in str(text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = ENTRY_NUMBER_RE.match(line)
        if match:
            if number is not None:
                entries.append(
                    ReferenceEntry(number=number, text="\n".join(buffer))
                )
            number = next(group for group in match.groups() if group)
            buffer = [line[match.end():]]
        elif number is not None:
            buffer.append(line)
    if number is not None:
        entries.append(ReferenceEntry(number=number, text="\n".join(buffer)))
    return entries


def normalize_reference_text(
    text: str, vocabulary: Counter, hyphenated_forms: set[str]
) -> tuple[str, list[HyphenDecision]]:
    """一条参考文献的清理：先判断词，再合行。顺序不能反。

    反过来先合行，``net-\\nworks`` 就会变成 ``net- works``，断词的痕迹没了，
    再也判不出来。
    """

    dehyphenated, decisions = dehyphenate(text, vocabulary, hyphenated_forms)
    return (join_lines(dehyphenated), decisions)


def render_references(
    element_id: str,
    raw_text: str,
    *,
    document_text: str,
    translation_unit_ids: dict[str, str] | None = None,
) -> RenderedReferences:
    """整理一份参考文献列表。"""

    if not str(raw_text or "").strip():
        raise ReferenceRenderError(f"{element_id}: 参考文献正文为空")

    vocabulary = build_vocabulary(document_text)
    hyphenated_forms = build_hyphenated_forms(document_text)
    unit_ids = translation_unit_ids or {}

    raw_entries = split_reference_entries(raw_text)
    if not raw_entries:
        raise ReferenceRenderError(
            f"{element_id}: 参考文献里找不到任何编号条目，无法逐条核对"
        )

    entries: list[dict[str, Any]] = []
    all_decisions: list[HyphenDecision] = []
    urls: list[str] = []
    for entry in raw_entries:
        cleaned, decisions = normalize_reference_text(
            entry.text, vocabulary, hyphenated_forms
        )
        all_decisions.extend(decisions)
        found = extract_urls(cleaned)
        urls.extend(found)
        entries.append(
            {
                "number": entry.number,
                "text": cleaned,
                "translation_unit_id": unit_ids.get(entry.number, ""),
                "urls": found,
            }
        )

    warnings: list[str] = []
    uncertain = [item for item in all_decisions if item.uncertain]
    if uncertain:
        warnings.append(
            "以下断词证据不足，已保留连字符待人工确认: "
            + "、".join(f"{item.left}-{item.right}" for item in uncertain)
        )

    numbers = [entry["number"] for entry in entries]
    expected = [str(index) for index in range(1, len(numbers) + 1)]
    if numbers != expected:
        warnings.append(f"参考文献编号不连续: {numbers}")

    return RenderedReferences(
        element_id=element_id,
        entries=entries,
        hyphen_decisions=[item.as_dict() for item in all_decisions],
        urls=urls,
        warnings=warnings,
    )


def verify_reference_output(
    rendered: RenderedReferences,
    candidate_text: str,
    *,
    expected_urls: list[str] | None = None,
) -> list[str]:
    """核对参考文献有没有真的整理干净。"""

    problems: list[str] = []
    text = str(candidate_text or "")

    for entry in rendered.entries:
        for url in entry["urls"]:
            if url not in text:
                problems.append(
                    f"条目 {entry['number']}: URL {url} 在候选里找不到，"
                    "可能被折行时插入了空格"
                )

    for url in expected_urls or []:
        if url in text:
            continue
        if url in text.replace(" ", ""):
            problems.append(f"原文 URL {url} 在候选里被插入了空格，点不开")
        else:
            problems.append(f"原文 URL {url} 在候选里丢失")

    for decision in rendered.hyphen_decisions:
        if decision["decision"] != DECISION_JOIN:
            continue
        broken = f"{decision['left']}-{decision['right']}"
        if broken in text:
            problems.append(
                f"断词 {broken} 判定为合并，但候选里仍带着连字符"
            )

    if len(set(rendered.numbers)) != len(rendered.numbers):
        problems.append(f"参考文献编号重复: {rendered.numbers}")

    return problems


#: 已固化断词的两半都得像个词的样子，才值得送去判定。
BAKED_HYPHEN_RE = re.compile(r"\b([A-Za-z]{2,})-([A-Za-z]{2,})\b")
#: URL 后面跟着的这种碎片才可能是被折行切下来的后半段。
URL_TAIL_RE = re.compile(r"(https?://\S+)\s+([\w./_%#?&=-]+)")


def repair_baked_line_artifacts(
    text: str, vocabulary: Counter, hyphenated_forms: set[str]
) -> str:
    """修复上游已经拼死的行末伪影。

    理想情况是拿到带换行的原文，让 ``normalize_reference_text`` 按 ``-\n``
    判。但有些抽取管线在更早的地方就把换行折掉了：``net-\nworks`` 进来时
    已经是 ``net-works``，URL 断口处留着一个空格。这里做补救——
    断词复用同一套词表判定（证据不足仍保留连字符），URL 只在断口停在
    续行字符上、且后半段长得像路径时才拼。
    """

    def fix_hyphen(match: re.Match[str]) -> str:
        decision = decide_hyphen(
            match.group(1), match.group(2), vocabulary, hyphenated_forms
        )
        if decision.decision == DECISION_JOIN:
            return f"{match.group(1)}{match.group(2)}"
        return match.group(0)

    value = BAKED_HYPHEN_RE.sub(fix_hyphen, str(text or ""))

    def fix_url(match: re.Match[str]) -> str:
        url, tail = match.group(1), match.group(2)
        if not url.endswith(URL_CONTINUES_ON):
            return match.group(0)
        # 「数字.」开头的是下一条题录的编号，不是 URL 的后半段——
        # 拼进去会把两条题录焊在一起。
        if re.match(r"\d{1,3}\.", tail):
            return match.group(0)
        return f"{url}{tail}"

    while True:
        replaced = URL_TAIL_RE.sub(fix_url, value, count=1)
        if replaced == value:
            return value
        value = replaced
