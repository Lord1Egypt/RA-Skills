import pandas as pd

from fetcher.common import tushare_request
from transforms import normalize_trade_date


DAILY_BASIC_FIELDS = "ts_code,trade_date,turnover_rate,pe,pe_ttm,pb,total_mv,circ_mv"
DAILY_BASIC_COLUMNS = ["ts_code", "trade_date", "turnover_rate", "pe", "pe_ttm", "pb", "total_mv", "circ_mv"]


def fetch_daily_basic_with_pro(pro, config: dict[str, str | None]) -> pd.DataFrame:
    data = tushare_request(
        "daily_basic",
        lambda: pro.daily_basic(
            trade_date=config["trade_date"],
            ts_code=config["ts_code"],
            start_date=config["start_date"],
            end_date=config["end_date"],
            fields=DAILY_BASIC_FIELDS,
        ),
    )

    data = normalize_trade_date(data)
    return data.reindex(columns=DAILY_BASIC_COLUMNS)
