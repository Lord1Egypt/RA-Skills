from scripts.estimate import estimate_tax
from scripts.matching import match_trades
from scripts.models import IncomeItem, Trade
from scripts.offset import offset_year
from scripts.report import ClientReport, build_client_report


def run_pipeline(trades: list[Trade], income_items: list[IncomeItem]) -> ClientReport:
    matched, unmatched = match_trades(trades)
    offset = offset_year(matched, income_items)
    taxed = estimate_tax(offset)
    report = build_client_report(taxed, unmatched)
    report.unmatched = unmatched
    report.tax_due_inputs = taxed
    return report
