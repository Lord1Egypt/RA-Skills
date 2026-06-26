"""Unit tests for webhook secret startup warning logging.

Validates Requirements 3.1 and 3.2: the Bridge logs a WARNING when
WEBHOOK_SECRET is not configured and an INFO when it is configured.
"""

from __future__ import annotations

import asyncio
import logging

import pytest

import app as app_module
import memory as memory_module


@pytest.fixture()
def tmp_data_dir(tmp_path, monkeypatch):
    """Redirect DATA_DIR so lifespan's ensure_data_dir() doesn't touch the real filesystem."""
    monkeypatch.setattr(memory_module, "DATA_DIR", tmp_path)
    monkeypatch.setattr(app_module, "DATA_DIR", str(tmp_path))
    return tmp_path


async def _run_lifespan_startup():
    """Enter the lifespan context manager (startup phase only)."""
    ctx = app_module.lifespan(app_module.app)
    await ctx.__aenter__()
    # Run shutdown as well to be clean
    await ctx.__aexit__(None, None, None)


def test_warning_when_webhook_secret_not_set(tmp_data_dir, monkeypatch, caplog):  # noqa: ARG001
    """Requirement 3.1: WARNING logged when WEBHOOK_SECRET is not configured."""
    monkeypatch.setattr(app_module, "WEBHOOK_SECRET", "")

    with caplog.at_level(logging.DEBUG, logger="app"):
        asyncio.get_event_loop().run_until_complete(_run_lifespan_startup())

    assert any(
        "WEBHOOK_SECRET is not configured" in rec.message
        and rec.levelno == logging.WARNING
        for rec in caplog.records
    ), "Expected a WARNING about WEBHOOK_SECRET not being configured"


def test_info_when_webhook_secret_is_set(tmp_data_dir, monkeypatch, caplog):  # noqa: ARG001
    """Requirement 3.2: INFO logged when WEBHOOK_SECRET is configured."""
    monkeypatch.setattr(app_module, "WEBHOOK_SECRET", "some-secret-value")

    with caplog.at_level(logging.DEBUG, logger="app"):
        asyncio.get_event_loop().run_until_complete(_run_lifespan_startup())

    assert any(
        "Webhook signature verification is enabled" in rec.message
        and rec.levelno == logging.INFO
        for rec in caplog.records
    ), "Expected an INFO message about webhook verification being enabled"
