from collections import defaultdict, deque

from scripts.models import MatchedSale, Trade, UnmatchedSale


def match_trades(trades: list[Trade]) -> tuple[list[MatchedSale], list[UnmatchedSale]]:
    buys: dict[tuple[str, str | None], deque[list[float | Trade]]] = defaultdict(deque)
    matched: list[MatchedSale] = []
    unmatched: list[UnmatchedSale] = []

    for trade in sorted(trades, key=lambda item: item.date):
        key = (trade.symbol, trade.account)
        if trade.side == "buy":
            buys[key].append([trade, trade.qty])
            continue
        if trade.side != "sell":
            continue

        remaining_qty = trade.qty
        while remaining_qty > 0 and buys[key]:
            buy, available_qty = buys[key][0]
            match_qty = min(remaining_qty, available_qty)
            proceeds = trade.amount * match_qty / trade.qty
            cost = buy.amount * match_qty / buy.qty
            matched.append(
                MatchedSale(
                    sale=trade,
                    buy=buy,
                    qty=match_qty,
                    proceeds=proceeds,
                    cost=cost,
                    gain=proceeds - cost,
                )
            )
            remaining_qty -= match_qty
            available_qty -= match_qty
            if available_qty == 0:
                buys[key].popleft()
            else:
                buys[key][0][1] = available_qty

        if remaining_qty > 0:
            unmatched.append(
                UnmatchedSale(
                    sale=trade,
                    qty=remaining_qty,
                    proceeds=trade.amount * remaining_qty / trade.qty,
                )
            )

    return matched, unmatched
