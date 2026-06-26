from app.catalog.loader import get_indicator
from app.services.akshare_runner import build_akshare_params


def test_build_akshare_params_normalizes_dates_and_defaults():
    indicator = get_indicator("stock_a_hist")
    assert indicator is not None

    params = build_akshare_params(
        indicator,
        {
            "symbol": "600000",
            "period": "daily",
            "start_date": "2024-02-01",
            "end_date": "2024-02-29",
        },
    )

    assert params["symbol"] == "600000"
    assert params["start_date"] == "20240201"
    assert params["end_date"] == "20240229"
    assert params["adjust"] == ""
