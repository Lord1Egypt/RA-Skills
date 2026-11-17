"""B 级文本修复层 V5（plan.md Phase 2 / T2.2）。

修复对象是我们可控的文本（OCR 重建层、修复统计、报告），以及
span 级图层去重（repair_pdf_dedup，作用于 PDF 副本，只做零排版风险的
"完全同文+近位置"冗余删除）。

粘连拆分策略（自包含，wordninja 可选增强）：
  - 医学刊名/缩写保护表先行（按最长纯字母段匹配，防标点击穿）；
  - camelCase 边界与字母-数字边界始终用规则拆分；
  - 全大写 >10 / 混合 >15 候选：有 wordninja 时词典拆分（大小写映射回原串），
    缺失时保守不拆（宁可保留也不哑切误伤）——selfcheck 显示当前模式。
"""

from __future__ import annotations

import re

try:
    import wordninja  # type: ignore
    _HAS_WORDNINJA = True
except Exception:  # pragma: no cover
    wordninja = None
    _HAS_WORDNINJA = False

# 全大写粘连拆分阈值（plan T2.2：>10 全大写 / >15 混合）
UPPER_SPLIT_MIN = 10
MIXED_SPLIT_MIN = 15

# 中文之间不应有空格（排版/OCR 引入的伪空格）
CJK_SPACE_RE = re.compile(r"([\u4e00-\u9fff]) +(?=[\u4e00-\u9fff])")

# 医学刊名/术语缩写保护表（命中则整 token 不拆）
ABBREV_PROTECT = {
    "chinjepidemiol", "chinjpediatr", "intjcardiol", "amjrespircritcaremed",
    "nejm", "jama", "bmj", "lancet", "lancetoncol", "lancetinfdis",
    "annrheumdis", "ard", "arthritisrheumatol", "jrheumatol", "clinexpimmunol",
    "immuno", "immunol", "institut of medicine", "who", "nih", "cdc",
    "ecmo", "crispr", "hla", "il6", "tnf", "igm", "igg", "ige", "iga",
}


def _has_wordninja() -> bool:
    return _HAS_WORDNINJA


def fix_cjk_spaces(text: str) -> tuple:
    """删除汉字之间的伪空格。返回 (fixed, removed_count)。"""
    fixed, n = CJK_SPACE_RE.subn(r"\1", text)
    return fixed, n


def _is_protected(token: str) -> bool:
    """保护判定查 token 内最长纯字母段（评审 P1：防标点后缀击穿）。"""
    low = token.lower()
    if low in ABBREV_PROTECT:
        return True
    segments = re.findall(r"[a-z]+", low)
    if not segments:
        return False
    longest = max(segments, key=len)
    if longest in ABBREV_PROTECT:
        return True
    # 前缀匹配：ChinJEpidemiol2019 → chinjepidemiol
    for abbr in ABBREV_PROTECT:
        if len(abbr) >= 6 and longest.startswith(abbr):
            return True
    return False


def _split_candidate(token: str) -> bool:
    """是否为粘连拆分候选（阈值见模块头）。"""
    letters = [c for c in token if c.isalpha()]
    if len(letters) < 6:
        return False
    if token.isupper():
        return len(token) > UPPER_SPLIT_MIN
    if any(c.islower() for c in token) and any(c.isupper() for c in token):
        return len(token) > MIXED_SPLIT_MIN or _has_camel_boundary(token)
    return False


def _has_camel_boundary(token: str) -> bool:
    return bool(re.search(r"[a-z][A-Z]", token))


def split_glued_token(token: str) -> str:
    """拆分单个粘连 token；无法可靠拆分时原样返回。"""
    if not _split_candidate(token) or _is_protected(token):
        return token
    if _HAS_WORDNINJA:
        parts = wordninja.split(token)
        if len(parts) > 1 and all(p for p in parts):
            if token.isupper():
                parts = [p.upper() for p in parts]   # wordninja 返回小写，映射回原大小写
            return " ".join(parts)
    # 无 wordninja 的规则拆分：camelCase 边界 + 字母/数字边界
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", token)
    s = re.sub(r"([A-Za-z])(\d)", r"\1 \2", s)
    s = re.sub(r"(\d)([A-Za-z])", r"\1 \2", s)
    # 全大写长串按 3-4 字符哑切仅当无从下手时避免误伤——直接返回 camel 结果
    if s != token:
        return s
    return token


def fix_glued_words(text: str) -> tuple:
    """对文本中的粘连 token 做拆分。返回 (fixed, split_count)。"""
    out_lines = []
    split_count = 0
    for line in text.splitlines():
        tokens = line.split(" ")
        new_tokens = []
        for tok in tokens:
            if not tok.isascii():
                new_tokens.append(tok)   # wordninja 丢非 ASCII（评审实测），含中文 token 一律保留
                continue
            core = tok.strip(",")
            if _split_candidate(core) and not _is_protected(core):
                fixed = split_glued_token(core)
                if fixed != core:
                    split_count += 1
                    new_tokens.append(tok.replace(core, fixed))
                    continue
            new_tokens.append(tok)
        out_lines.append(" ".join(new_tokens))
    return "\n".join(out_lines), split_count


def repair_text(text: str) -> tuple:
    """文本修复总入口：中文空格 + 粘连拆分 + 控制字符/噪声清洗。

    返回 (fixed_text, stats_dict)。
    """
    from . import skip_rules

    stats = {"cjk_spaces_removed": 0, "glued_split": 0,
             "control_chars": 0, "noise_lines_dropped": 0}
    fixed, stats["cjk_spaces_removed"] = fix_cjk_spaces(text)
    fixed, stats["glued_split"] = fix_glued_words(fixed)
    cleaned, hits = skip_rules.clean_text(fixed)
    # 口径修正（评审 P2）：按实际行数差计，避免一行多规则重复计数
    stats["noise_lines_dropped"] = len(text.splitlines()) - len(cleaned.splitlines())
    stats["control_chars"] = len(skip_rules.CONTROL_RE.findall(text))
    return cleaned, stats
