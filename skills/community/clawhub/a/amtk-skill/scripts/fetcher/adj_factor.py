import pandas as pd

from fetcher.common import tushare_request
from transforms import normalize_trade_date


ADJ_FACTOR_FIELDS = "ts_code,trade_date,adj_factor"
ADJ_FACTOR_COLUMNS = ["ts_code", "trade_date", "adj_factor"]


def fetch_adj_factor_with_pro(pro, config: dict[str, str | None]) -> pd.DataFrame:
    data = tushare_request(
        "adj_factor",
        lambda: pro.adj_factor(
            trade_date=config["trade_date"],
            ts_code=config["ts_code"],
            start_date=config["start_date"],
            end_date=config["end_date"],
            fields=ADJ_FACTOR_FIELDS,
        ),
    )

    data = normalize_trade_date(data)
    return data.reindex(columns=ADJ_FACTOR_COLUMNS)
