"""
tests/test_server_boots.py — Smoke test: FastMCP server registers all expected tools.
"""

from __future__ import annotations

import asyncio
import importlib

import pytest


@pytest.fixture(scope="module")
def tool_names() -> list[str]:
    """Import server.main and return the list of registered tool names."""
    mod = importlib.import_module("server.main")
    mcp = mod.mcp
    tools = asyncio.run(mcp.list_tools())
    return [t.name for t in tools]


# ---------------------------------------------------------------------------
# Core tool name assertions
# ---------------------------------------------------------------------------

EXPECTED_TOOLS = [
    # Setup
    "setup_status",
    "apply_initial_setup",
    # Banks
    "start_link",
    "complete_link",
    "list_connections",
    "refresh_connection",
    "disconnect",
    # Ledgers
    "list_ledgers",
    "add_line_item",
    "add_ledger",
    "remove_line_item",
    # Transactions
    "sync",
    "list",
    "get_needs_review",
    "route",
    "add_hint",
    # Reports
    "summary",
    "export_excel",
]


@pytest.mark.parametrize("name", EXPECTED_TOOLS)
def test_tool_registered(tool_names: list[str], name: str) -> None:
    assert name in tool_names, f"Expected tool '{name}' not found in registered tools: {tool_names}"


def test_all_tools_count(tool_names: list[str]) -> None:
    """Sanity check: at least as many tools as our expected list."""
    assert len(tool_names) >= len(
        EXPECTED_TOOLS
    ), f"Expected at least {len(EXPECTED_TOOLS)} tools, found {len(tool_names)}: {tool_names}"
