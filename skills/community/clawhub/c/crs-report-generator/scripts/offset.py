from .models import IncomeItem, MatchedSale, OffsetResult


def offset_year(
    matched_sales: list[MatchedSale], income_items: list[IncomeItem]
) -> OffsetResult:
    transfer_net = max(sum(sale.gain for sale in matched_sales), 0)
    dividend_net = sum(
        item.amount for item in income_items if item.kind == "dividend"
    )
    interest_net = sum(
        item.amount for item in income_items if item.kind == "interest"
    )
    return OffsetResult(
        transfer_net=transfer_net,
        dividend_net=dividend_net,
        interest_net=interest_net,
    )
