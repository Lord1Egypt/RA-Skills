"""Pytest configuration for boss-cli."""

from __future__ import annotations

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip smoke tests unless they were explicitly selected with -m smoke."""
    markexpr = (config.option.markexpr or "").strip()
    if "smoke" in markexpr:
        return

    skip_smoke = pytest.mark.skip(reason="smoke tests require explicit selection via `-m smoke`")
    for item in items:
        if "smoke" in item.keywords:
            item.add_marker(skip_smoke)
