import importlib

from app.catalog.loader import load_indicators, load_sectors


EXPECTED_INDICATOR_COUNT = 134
EXPECTED_SECTOR_IDS = {
    "equity_index",
    "company_financials",
    "bond",
    "fx",
    "rate",
    "futures",
    "fund",
    "macro",
}


def test_catalog_has_one_hundred_indicators_with_unique_ids():
    indicators = load_indicators()
    indicator_ids = [indicator.id for indicator in indicators]

    assert len(indicators) == EXPECTED_INDICATOR_COUNT
    assert len(indicator_ids) == len(set(indicator_ids))


def test_catalog_covers_core_financial_categories():
    level1_values = {indicator.level1 for indicator in load_indicators()}

    assert {"股票与指数", "公司与财报", "债券", "外汇", "利率", "期货", "基金", "宏观"}.issubset(level1_values)


def test_all_ak_functions_exist_in_akshare():
    ak = importlib.import_module("akshare")

    missing: list[str] = []
    for indicator in load_indicators():
        if not hasattr(ak, indicator.ak_function):
            missing.append(f"{indicator.id}->{indicator.ak_function}")
    assert not missing, f"Missing AKShare functions: {missing}"


def test_sectors_have_required_shape():
    sectors = load_sectors()
    indicator_ids = {indicator.id for indicator in load_indicators()}

    sector_ids = {sector.id for sector in sectors}
    assert sector_ids == EXPECTED_SECTOR_IDS

    aggregated: list[str] = []
    for sector in sectors:
        assert sector.indicator_ids, f"Sector {sector.id} has no indicators"
        assert len(sector.snapshot.cards) == 6, (
            f"Sector {sector.id} should have 6 snapshot cards, got {len(sector.snapshot.cards)}"
        )
        for indicator_id in sector.indicator_ids:
            assert indicator_id in indicator_ids, (
                f"Sector {sector.id} references unknown indicator {indicator_id}"
            )
        aggregated.extend(sector.indicator_ids)

    assert len(aggregated) == EXPECTED_INDICATOR_COUNT
    assert len(set(aggregated)) == EXPECTED_INDICATOR_COUNT


def test_snapshot_card_ak_functions_exist_in_akshare():
    ak = importlib.import_module("akshare")

    missing: list[str] = []
    for sector in load_sectors():
        for card in sector.snapshot.cards:
            if not hasattr(ak, card.ak_function):
                missing.append(f"{sector.id}:{card.title}->{card.ak_function}")
    assert not missing, f"Missing AKShare functions: {missing}"
