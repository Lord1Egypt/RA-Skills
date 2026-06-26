import asyncio

import pytest

from data_hub import DataHub


class TestConcurrency:
    @pytest.mark.asyncio
    async def test_concurrent_push_same_symbol(self):
        hub = DataHub()
        tasks = [
            hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
                "last_price": float(i + 1),
            })
            for i in range(50)
        ]
        results = await asyncio.gather(*tasks)
        assert all(r["success"] for r in results)

        final = await hub.get_data("market_state", "BTC_USDT")
        assert final["success"] is True
        assert final["data"]["last_price"] > 0

    @pytest.mark.asyncio
    async def test_concurrent_push_different_namespaces(self):
        hub = DataHub()
        tasks = [
            hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
                "last_price": 100.0,
            }),
            hub.push_data("Default_Orchestrator", "indicators", "BTC_USDT", {
                "rsi": [45.0],
            }),
            hub.push_data("Analyst_Officer", "intelligence", "BTC_USDT", {
                "author": "A",
                "content": "test",
            }),
            hub.push_data("Guard_Agent", "risk_audit", "global_state", {
                "max_position_allowance": 1000.0,
            }),
        ]
        results = await asyncio.gather(*tasks)
        assert all(r["success"] for r in results)

    @pytest.mark.asyncio
    async def test_concurrent_push_and_summary(self):
        hub = DataHub()

        async def push_loop():
            for i in range(20):
                await hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
                    "last_price": float(i + 1),
                })

        async def summary_loop():
            for _ in range(10):
                result = await hub.get_summary()
                assert result["success"] is True

        await asyncio.gather(push_loop(), summary_loop())

    @pytest.mark.asyncio
    async def test_concurrent_indicators_no_data_loss(self):
        hub = DataHub()
        tasks = [
            hub.push_data("Default_Orchestrator", "indicators", "BTC_USDT", {
                "rsi": [float(i)],
            })
            for i in range(30)
        ]
        results = await asyncio.gather(*tasks)
        assert all(r["success"] for r in results)

        data = await hub.get_data("indicators", "BTC_USDT")
        assert data["success"] is True
        assert len(data["data"]["rsi"]) >= 1
