from data_hub.constants import EXPIRED_PLACEHOLDER, STALE_THRESHOLD_SECONDS
from data_hub.janitor import expire_intelligence, mark_stale_market_data


class TestMarkStaleMarketData:
    def test_fresh_data(self):
        now = 1000.0
        data = {"last_price": 65000, "timestamp": 999.0}
        result = mark_stale_market_data(data, now=now)
        assert result["is_stale"] is False
        assert data.get("is_stale") is None  # 原数据未被修改

    def test_stale_data(self):
        now = 1000.0
        data = {"last_price": 65000, "timestamp": 989.0}
        result = mark_stale_market_data(data, now=now)
        assert result["is_stale"] is True

    def test_exactly_at_threshold(self):
        now = 1000.0
        data = {"last_price": 65000, "timestamp": now - STALE_THRESHOLD_SECONDS}
        result = mark_stale_market_data(data, now=now)
        assert result["is_stale"] is False

    def test_preserves_original_fields(self):
        data = {"last_price": 65000, "timestamp": 0.0, "volume_24h": 100}
        result = mark_stale_market_data(data, now=100.0)
        assert result["last_price"] == 65000
        assert result["volume_24h"] == 100


class TestExpireIntelligence:
    def test_valid_report(self):
        now = 1000.0
        data = {"content": "BTC看涨", "created_at": 999.0, "ttl_seconds": 1800}
        result = expire_intelligence(data, now=now)
        assert result["content"] == "BTC看涨"

    def test_expired_report(self):
        now = 3000.0
        data = {"content": "BTC看涨", "created_at": 1000.0, "ttl_seconds": 1800}
        result = expire_intelligence(data, now=now)
        assert result["content"] == EXPIRED_PLACEHOLDER

    def test_exactly_at_ttl(self):
        now = 2800.0
        data = {"content": "BTC看涨", "created_at": 1000.0, "ttl_seconds": 1800}
        result = expire_intelligence(data, now=now)
        assert result["content"] == "BTC看涨"

    def test_does_not_mutate_original(self):
        data = {"content": "BTC看涨", "created_at": 0.0, "ttl_seconds": 10}
        expire_intelligence(data, now=100.0)
        assert data["content"] == "BTC看涨"
