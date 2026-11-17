"""标题与正文渲染器。

独立复审 R-007 的病根只有一句话：**渲染器自己判断了什么是标题**。
它看到一行短、字号略大、上下有空白，就把它排成章节标题——于是作者单位
「德国弗莱堡大学」、arXiv 版本戳、图内标签「复制并裁剪」全都成了标题，
连正文句子中段「其中 ak(x) 表示」都被切出来当成页首标题。

这里换一条规矩：**角色只来自 source_elements.json**。渲染器不看字号、
不看行长、不看空白，只看这个翻译单元绑到了哪个元素、那个元素是什么类型。
绑不上元素的单元一律按正文处理——宁可漏掉一个标题，也不要凭空造出一个。

R-008 是另一回事：标题译文尾部多出一段重复（「……的卷积网络图像分割」）。
这个不靠语义判断，靠数：译文尾巴上的一段在译文里重复出现，而原文没有
对应的重复，就报出来。这项检查**只对标题生效**——长段落里中英语序不同，
中文常把宾语挪到句尾，尾部检查在那里会大量误报。
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.analysis.unit_binding import (
    ROLE_AFFILIATION,
    ROLE_AUTHOR,
    ROLE_BODY,
    ROLE_DOCUMENT_TITLE,
    ROLE_FIGURE_CAPTION,
    ROLE_FIGURE_LABEL,
    ROLE_FOOTNOTE,
    ROLE_HEADING,
    ROLE_PAGE_FURNITURE,
    ROLE_PUBLICATION_METADATA,
    ROLE_REFERENCE_ENTRY,
    ROLE_TABLE_TITLE,
    ROLE_UNKNOWN,
)

#: 只有这两种角色允许用标题字号。别的一律不行，没有例外。
HEADING_ROLES = frozenset({ROLE_DOCUMENT_TITLE, ROLE_HEADING})

#: 这些角色由各自的专用渲染器处理，不进标题/正文的行流。
DELEGATED_ROLES = frozenset(
    {ROLE_FIGURE_LABEL, ROLE_FOOTNOTE, ROLE_PAGE_FURNITURE}
)

#: 各角色的字号相对正文的倍数。
ROLE_FONT_SCALE = {
    ROLE_DOCUMENT_TITLE: 1.55,
    ROLE_HEADING: 1.25,
    ROLE_AUTHOR: 1.05,
    ROLE_AFFILIATION: 0.95,
    ROLE_PUBLICATION_METADATA: 0.85,
    ROLE_FIGURE_CAPTION: 0.90,
    ROLE_TABLE_TITLE: 0.90,
    ROLE_REFERENCE_ENTRY: 0.90,
    ROLE_BODY: 1.0,
    ROLE_UNKNOWN: 1.0,
}

#: 二级标题相对一级标题再缩一档。
HEADING_LEVEL_STEP = 0.08
#: 译文尾部重复至少这么多词元才算问题，短于它多半是正常的词语呼应。
MIN_TAIL_REPEAT_TOKENS = 3


class HeadingRenderError(RuntimeError):
    """标题与正文渲染失败。"""


@dataclass
class TextRole:
    """一个翻译单元最终拿到的角色与字号。"""

    unit_id: str
    element_id: str
    element_type: str
    role: str
    font_size: float
    is_heading: bool
    level: int = 0
    #: 角色是怎么定下来的。用来证明渲染器没有自己发挥。
    source: str = "source_elements.json"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ResolvedRoles:
    """一次角色解析的结果与证据。"""

    roles: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def heading_unit_ids(self) -> list[str]:
        return [item["unit_id"] for item in self.roles if item["is_heading"]]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["heading_unit_ids"] = self.heading_unit_ids
        return data


def heading_level(element: dict[str, Any] | None) -> int:
    """标题级别只从元素的 detail 里读，读不到就当一级。"""

    if not element:
        return 1
    detail = element.get("detail") or {}
    try:
        level = int(detail.get("heading_level") or detail.get("level") or 1)
    except (TypeError, ValueError):
        return 1
    return max(1, min(level, 4))


def font_size_for(role: str, body_font_size: float, *, level: int = 1) -> float:
    """按角色算字号。

    注意这里的输入只有角色和正文字号——**没有原文字号，也没有行长**。
    一旦让原文字号参与，扫描版里一行偶然大一点的字就又会变成标题。
    """

    if body_font_size <= 0:
        raise HeadingRenderError("正文字号必须为正数")
    scale = ROLE_FONT_SCALE.get(role, 1.0)
    if role == ROLE_HEADING and level > 1:
        scale = max(1.0, scale - HEADING_LEVEL_STEP * (level - 1))
    return round(body_font_size * scale, 2)


def resolve_roles(
    bindings: list[dict[str, Any]],
    *,
    body_font_size: float = 10.0,
    elements_by_id: dict[str, dict[str, Any]] | None = None,
) -> ResolvedRoles:
    """给每个翻译单元定角色。角色只来自绑定，不看排版特征。"""

    elements = elements_by_id or {}
    roles: list[dict[str, Any]] = []
    warnings: list[str] = []
    unbound = 0

    for binding in bindings:
        unit_id = str(binding.get("unit_id") or "").strip()
        if not unit_id:
            raise HeadingRenderError("绑定记录缺少 unit_id，无法定角色")
        element_id = str(binding.get("element_id") or "").strip()
        role = str(binding.get("element_role") or "").strip()
        if not element_id or not role:
            # 绑不上元素就按正文走。造一个标题出来比漏一个标题坏得多。
            unbound += 1
            role = ROLE_UNKNOWN
            element_id = ""
        level = heading_level(elements.get(element_id))
        is_heading = role in HEADING_ROLES
        roles.append(
            TextRole(
                unit_id=unit_id,
                element_id=element_id,
                element_type=str(binding.get("element_type") or ""),
                role=role,
                font_size=font_size_for(
                    role, body_font_size, level=level
                ),
                is_heading=is_heading,
                level=level if is_heading else 0,
                source=(
                    "source_elements.json"
                    if element_id
                    else "unbound-defaults-to-body"
                ),
            ).as_dict()
        )

    if unbound:
        warnings.append(
            f"{unbound} 个翻译单元没有绑定元素，已按正文处理，不得当标题"
        )
    return ResolvedRoles(roles=roles, warnings=warnings)


def _tokens(text: str) -> list[str]:
    """切成词元。中日韩按字，拉丁按词。

    两种语言的重复长得不一样：中文「图像分割」是四个字，英文
    "image segmentation" 是两个词。拿中文子串去英文原文里数出现次数
    永远是零，那样的比较等于没比。
    """

    return re.findall(r"[\u3400-\u9fff]|[A-Za-z0-9]+", str(text or "").lower())


def longest_repeated_tail(text: str) -> list[str]:
    """找出结尾处那一段在前文出现过的词元，没有就返回空。"""

    tokens = _tokens(text)
    longest: list[str] = []
    for length in range(MIN_TAIL_REPEAT_TOKENS, len(tokens) // 2 + 1):
        tail = tokens[-length:]
        head = tokens[:-length]
        if any(head[i:i + length] == tail for i in range(len(head) - length + 1)):
            longest = tail
    return longest


def detect_tail_duplication(source: str, translation: str) -> str | None:
    """找出译文尾部多出来的重复段。

    ``用于生物医学图像分割的卷积网络图像分割`` 里，尾巴上的「图像分割」
    在前面已经出现过一次，而原文的结尾 "Biomedical Image Segmentation"
    在原文里只出现一次——多出来的这一段就是译出来的。

    原文自己也在结尾重复的（比如图题里 (b) 和 (d) 都以「与人工真值
    （黄色边界）」收尾），照搬不算错。

    """

    repeated = longest_repeated_tail(translation)
    if not repeated:
        return None
    if longest_repeated_tail(source):
        return None
    return "".join(repeated) if _is_cjk(repeated) else " ".join(repeated)


def _is_cjk(tokens: list[str]) -> bool:
    return all(len(token) == 1 and ord(token) > 0x3400 for token in tokens)


def verify_text_roles(
    resolved: ResolvedRoles,
    *,
    body_font_size: float = 10.0,
    translations: dict[str, str] | None = None,
    sources: dict[str, str] | None = None,
) -> list[str]:
    """核对没有任何东西被偷偷提成标题。"""

    problems: list[str] = []
    heading_floor = body_font_size * ROLE_FONT_SCALE[ROLE_HEADING]

    for item in resolved.roles:
        role = item["role"]
        if item["is_heading"] and role not in HEADING_ROLES:
            problems.append(
                f"{item['unit_id']}: 角色 {role} 不是标题，却被标成了标题"
            )
        if not item["is_heading"] and item["font_size"] >= heading_floor:
            problems.append(
                f"{item['unit_id']}: 角色 {role} 用了标题字号 "
                f"{item['font_size']}"
            )
        if item["is_heading"] and not item["element_id"]:
            problems.append(
                f"{item['unit_id']}: 没有绑定元素却当了标题"
            )
        if role in DELEGATED_ROLES and item["is_heading"]:
            problems.append(
                f"{item['unit_id']}: {role} 由专用渲染器处理，不得进标题行流"
            )

    texts = translations or {}
    origins = sources or {}
    for item in resolved.roles:
        # 只查标题。长段落里中英语序不同——中文常把「类别标签」挪到句尾——
        # 尾部重复检查在那里会大量误报，而 R-008 本来就是标题上的缺陷。
        if item["role"] not in HEADING_ROLES:
            continue
        translation = texts.get(item["unit_id"], "")
        if not translation:
            continue
        repeated = detect_tail_duplication(
            origins.get(item["unit_id"], ""), translation
        )
        if repeated:
            problems.append(
                f"{item['unit_id']}: 译文尾部重复了 {repeated!r}，"
                "原文没有对应的重复"
            )
    return problems
