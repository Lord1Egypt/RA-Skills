from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from app.models import Indicator, IndicatorSummary, Sector, SectorSummary, SourceSummary


CATALOG_DIR = Path(__file__).parent
INDICATORS_PATH = CATALOG_DIR / "indicators.yaml"
SECTORS_PATH = CATALOG_DIR / "sectors.yaml"


@lru_cache
def load_indicators() -> list[Indicator]:
    with INDICATORS_PATH.open("r", encoding="utf-8") as catalog_file:
        payload = yaml.safe_load(catalog_file) or {}

    indicators = [Indicator(**item) for item in payload.get("indicators", [])]
    indicator_ids = [indicator.id for indicator in indicators]
    if len(indicator_ids) != len(set(indicator_ids)):
        raise ValueError("Indicator catalog contains duplicate ids")
    return indicators


@lru_cache
def get_indicator_map() -> dict[str, Indicator]:
    return {indicator.id: indicator for indicator in load_indicators()}


def get_indicator(indicator_id: str) -> Indicator | None:
    return get_indicator_map().get(indicator_id)


def list_indicator_summaries(
    source: str | None = None,
    query: str | None = None,
) -> list[IndicatorSummary]:
    indicators = load_indicators()

    if source:
        indicators = [ind for ind in indicators if ind.source == source]

    if query:
        keyword = query.lower()
        indicators = [
            ind for ind in indicators
            if keyword in ind.name.lower()
            or keyword in ind.description.lower()
            or keyword in ind.ak_function.lower()
            or keyword in ind.source_name.lower()
        ]

    return [
        IndicatorSummary(
            id=indicator.id,
            level1=indicator.level1,
            level2=indicator.level2,
            level3=indicator.level3,
            name=indicator.name,
            source=indicator.source,
            source_name=indicator.source_name,
            update_frequency=indicator.update_frequency,
            description=indicator.description,
            docs_url=indicator.docs_url,
        )
        for indicator in indicators
    ]


def list_source_summaries() -> list[SourceSummary]:
    counts: dict[str, tuple[str, int]] = {}
    for indicator in load_indicators():
        if not indicator.source:
            continue
        source_name = indicator.source_name or indicator.source
        current = counts.get(indicator.source, (source_name, 0))
        counts[indicator.source] = (source_name, current[1] + 1)

    return [
        SourceSummary(source=source, source_name=name, indicator_count=count)
        for source, (name, count) in sorted(counts.items(), key=lambda item: -item[1][1])
    ]


@lru_cache
def load_sectors() -> list[Sector]:
    with SECTORS_PATH.open("r", encoding="utf-8") as catalog_file:
        payload = yaml.safe_load(catalog_file) or {}

    sectors = [Sector(**item) for item in payload.get("sectors", [])]

    indicator_map = get_indicator_map()
    for sector in sectors:
        unknown = [iid for iid in sector.indicator_ids if iid not in indicator_map]
        if unknown:
            raise ValueError(
                f"Sector {sector.id!r} references unknown indicator ids: {unknown}"
            )

    return sectors


@lru_cache
def get_sector_map() -> dict[str, Sector]:
    return {sector.id: sector for sector in load_sectors()}


def get_sector(sector_id: str) -> Sector | None:
    return get_sector_map().get(sector_id)


def list_sector_summaries() -> list[SectorSummary]:
    return [
        SectorSummary(
            id=sector.id,
            name=sector.name,
            short_name=sector.short_name,
            description=sector.description,
            accent=sector.accent,
            indicator_count=len(sector.indicator_ids),
        )
        for sector in load_sectors()
    ]
