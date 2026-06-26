import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
"""
Pytest configuration for private network tests.

Network tests (marked with @pytest.mark.network) are skipped by default.
Use --test-api to enable them.
"""

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "network: mark test as requiring network access (real API calls)"
    )


def pytest_addoption(parser):
    """Add command line options for network tests."""
    parser.addoption(
        "--test-api",
        action="store_true",
        default=False,
        help="Enable tests marked as 'network' (real API calls)"
    )


def pytest_collection_modifyitems(config, items):
    """Skip network tests unless --test-api is given."""
    if not config.getoption("--test-api"):
        skip_network = pytest.mark.skip(reason="Network tests require --test-api flag")
        for item in items:
            if "network" in item.keywords:
                item.add_marker(skip_network)