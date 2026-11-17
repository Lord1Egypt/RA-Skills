from scripts.models import OffsetResult

DIVIDEND_RATE = 0.20
TRANSFER_RATE = 0.20


def estimate_tax(offset: OffsetResult) -> OffsetResult:
    return OffsetResult(
        transfer_net=offset.transfer_net,
        dividend_net=offset.dividend_net,
        interest_net=offset.interest_net,
        dividend_tax=round((offset.dividend_net + offset.interest_net) * DIVIDEND_RATE, 2),
        transfer_tax=round(offset.transfer_net * TRANSFER_RATE, 2),
    )
