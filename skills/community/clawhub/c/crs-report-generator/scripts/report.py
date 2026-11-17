from dataclasses import dataclass, field

from scripts.estimate import estimate_tax
from scripts.models import OffsetResult, UnmatchedSale


SECTIONS = ["大概要补多少钱", "这钱是怎么来的", "还缺哪些单子", "给税局准备什么"]


@dataclass
class ClientReport:
    tax_due: float
    missing_docs: str
    requested_uploads: list[str] = field(default_factory=list)
    tax_bureau_notes: str = ""
    sections: list[str] = field(default_factory=lambda: list(SECTIONS))
    unmatched: list[UnmatchedSale] = field(default_factory=list)
    tax_due_inputs: OffsetResult | None = None


def build_client_report(result: OffsetResult, unmatched: list[UnmatchedSale]) -> ClientReport:
    taxed = result if result.dividend_tax or result.transfer_tax else estimate_tax(result)
    symbols = ", ".join(item.sale.symbol if hasattr(item, "sale") else getattr(item, "symbol", "") for item in unmatched)
    missing = f"{symbols} 还缺买入记录，这些笔暂时不算。" if unmatched else "单子齐了，已匹配的买卖都算进去了。"
    notes = "给税局准备：这一年的境外结单、测算表、缺材料说明。身份证请自己带去税局或交给中介，不要上传到这里。"
    return ClientReport(
        tax_due=taxed.dividend_tax + taxed.transfer_tax,
        missing_docs=missing,
        requested_uploads=[],
        tax_bureau_notes=notes,
        unmatched=unmatched,
        tax_due_inputs=taxed,
    )
