# 本文件定义 5 组舆情关键词，并提供确定性的 OR/AND 匹配逻辑。

from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class KeywordGroup:
    id: str
    name: str
    expression: str
    term_groups: Sequence[Sequence[str]]


KEYWORD_GROUPS = [
    KeywordGroup(
        id="avenir_group",
        name="Avenir Group舆情相关",
        expression='"Avenir Group" OR "Avenir" OR "Avenir集团" OR "未来资本"',
        term_groups=[("Avenir Group", "Avenir", "Avenir集团", "未来资本")],
    ),
    KeywordGroup(
        id="li_lin",
        name="李林相关",
        expression='"Li Lin" OR "Leon Li" OR "李林" OR "Huobi founder" OR "Founder of Huobi" OR "火币创始人"',
        term_groups=[("Li Lin", "Leon Li", "李林", "Huobi founder", "Founder of Huobi", "火币创始人")],
    ),
    KeywordGroup(
        id="binance_us_stocks",
        name="币安上美股专项监测",
        expression='("Binance" OR "币安") AND ("US stocks" OR "stocks" OR "equities" OR "美股" OR "股票" OR "tokenized stocks" OR "股票代币")',
        term_groups=[
            ("Binance", "币安"),
            ("US stocks", "stocks", "equities", "美股", "股票", "tokenized stocks", "股票代币"),
        ],
    ),
    KeywordGroup(
        id="crypto_exchange_us_stocks",
        name="加密平台美股交易舆情",
        expression='("crypto exchange" OR "加密平台" OR "交易所") AND ("US stocks" OR "stocks" OR "美股" OR "股票" OR "美股交易")',
        term_groups=[
            ("crypto exchange", "加密平台", "交易所"),
            ("US stocks", "stocks", "美股", "股票", "美股交易"),
        ],
    ),
    KeywordGroup(
        id="crypto_stock_connect",
        name="币股互通市场舆情",
        expression='("crypto" OR "加密资产" OR "币") AND ("stocks" OR "US stocks" OR "美股" OR "股票") AND ("one account" OR "cross-asset" OR "capital efficiency" OR "一个账户" OR "跨资产" OR "资金效率" OR "币股互通")',
        term_groups=[
            ("crypto", "加密资产", "币"),
            ("stocks", "US stocks", "美股", "股票"),
            ("one account", "cross-asset", "capital efficiency", "一个账户", "跨资产", "资金效率", "币股互通"),
        ],
    ),
]


def _contains(text: str, term: str) -> bool:
    """英文按小写匹配，中文按原文包含匹配。"""
    if not text or not term:
        return False
    return term.lower() in text.lower()


def match_group(text: str, group: KeywordGroup) -> List[str]:
    """每个 term_group 内是 OR，多个 term_group 之间是 AND。"""
    matched_terms = []
    for terms in group.term_groups:
        group_matches = [term for term in terms if _contains(text, term)]
        if not group_matches:
            return []
        matched_terms.extend(group_matches)
    return matched_terms


def match_groups(text: str, groups: Iterable[KeywordGroup] = KEYWORD_GROUPS):
    """返回所有命中的关键词组和对应命中词。"""
    results = []
    for group in groups:
        terms = match_group(text, group)
        if terms:
            results.append((group, terms))
    return results


def item_text(item: dict) -> str:
    """把标题、摘要、正文合并为用于匹配的文本。"""
    return "\n".join(
        str(item.get(key) or "")
        for key in ("title", "abstract", "content")
    )
