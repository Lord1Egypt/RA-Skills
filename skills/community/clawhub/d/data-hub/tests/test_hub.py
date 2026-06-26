import json
import time

import pytest

from data_hub import DataHub
from data_hub.constants import EXPIRED_PLACEHOLDER


class TestPushData:
    @pytest.mark.asyncio
    async def test_push_market_state(self, hub):
        result = await hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
            "last_price": 65000.5,
            "volume_24h": 1000.0,
        })
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_push_indicators(self, hub):
        result = await hub.push_data("Default_Orchestrator", "indicators", "BTC_USDT", {
            "rsi": [45.2, 48.1],
        })
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_push_intelligence(self, hub):
        result = await hub.push_data("Analyst_Officer", "intelligence", "BTC_USDT", {
            "author": "Analyst_Officer",
            "content": "BTC看涨",
        })
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_push_risk_audit(self, hub):
        result = await hub.push_data("Guard_Agent", "risk_audit", "global_state", {
            "max_position_allowance": 10000.0,
        })
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_permission_denied(self, hub):
        result = await hub.push_data("Analyst_Officer", "market_state", "BTC_USDT", {
            "last_price": 100.0,
        })
        assert result["success"] is False
        assert "[PERMISSION_DENIED]" in result["error"]

    @pytest.mark.asyncio
    async def test_invalid_namespace(self, hub):
        result = await hub.push_data("Default_Orchestrator", "bad_ns", "key", {})
        assert result["success"] is False
        assert "[INVALID_NAMESPACE]" in result["error"]

    @pytest.mark.asyncio
    async def test_validation_error(self, hub):
        result = await hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
            "last_price": "bad",
        })
        assert result["success"] is False
        assert "[VALIDATION_ERROR]" in result["error"]


class TestGetData:
    @pytest.mark.asyncio
    async def test_get_existing(self, hub):
        await hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
            "last_price": 65000.5,
        })
        result = await hub.get_data("market_state", "BTC_USDT")
        assert result["success"] is True
        assert result["data"]["last_price"] == 65000.5

    @pytest.mark.asyncio
    async def test_get_missing(self, hub):
        result = await hub.get_data("market_state", "ETH_USDT")
        assert result["success"] is False
        assert "[NOT_FOUND]" in result["error"]

    @pytest.mark.asyncio
    async def test_get_invalid_namespace(self, hub):
        result = await hub.get_data("bad_ns", "key")
        assert result["success"] is False
        assert "[INVALID_NAMESPACE]" in result["error"]


class TestGetSummary:
    @pytest.mark.asyncio
    async def test_empty_summary(self, hub):
        result = await hub.get_summary()
        assert result["success"] is True
        assert result["data"]["market_state"] == {}

    @pytest.mark.asyncio
    async def test_stale_market_data(self, hub):
        await hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
            "last_price": 100.0,
            "timestamp": time.time() - 20,
        })
        result = await hub.get_summary()
        assert result["data"]["market_state"]["BTC_USDT"]["is_stale"] is True

    @pytest.mark.asyncio
    async def test_fresh_market_data(self, hub):
        await hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
            "last_price": 100.0,
        })
        result = await hub.get_summary()
        assert result["data"]["market_state"]["BTC_USDT"]["is_stale"] is False

    @pytest.mark.asyncio
    async def test_expired_intelligence(self, hub):
        await hub.push_data("Analyst_Officer", "intelligence", "BTC_USDT", {
            "author": "A",
            "content": "BTC看涨",
            "ttl_seconds": 1,
            "created_at": time.time() - 10,
        })
        result = await hub.get_summary()
        assert result["data"]["intelligence"]["BTC_USDT"]["content"] == EXPIRED_PLACEHOLDER


class TestSnapshot:
    @pytest.mark.asyncio
    async def test_snapshot_saved_on_push(self, hub_with_snapshot):
        hub, path = hub_with_snapshot
        await hub.push_data("Guard_Agent", "risk_audit", "global_state", {
            "max_position_allowance": 5000.0,
        })
        with open(path) as f:
            data = json.load(f)
        assert data["max_position_allowance"] == 5000.0
