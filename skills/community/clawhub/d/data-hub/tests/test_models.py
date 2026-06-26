import time

import pytest
from pydantic import ValidationError

from data_hub.models import IntelligenceModel, MarketDataModel, RiskAuditModel


class TestMarketDataModel:
    def test_valid(self):
        m = MarketDataModel(last_price=65000.5, volume_24h=1000.0)
        assert m.last_price == 65000.5
        assert m.volume_24h == 1000.0
        assert m.timestamp <= time.time()

    def test_defaults(self):
        m = MarketDataModel(last_price=1.0)
        assert m.volume_24h == 0.0

    def test_price_must_be_positive(self):
        with pytest.raises(ValidationError):
            MarketDataModel(last_price=0)

    def test_price_must_be_float(self):
        with pytest.raises(ValidationError):
            MarketDataModel(last_price="六万")

    def test_volume_must_be_non_negative(self):
        with pytest.raises(ValidationError):
            MarketDataModel(last_price=1.0, volume_24h=-1)


class TestIntelligenceModel:
    def test_valid(self):
        m = IntelligenceModel(author="Analyst_Officer", content="BTC看涨")
        assert m.author == "Analyst_Officer"
        assert m.ttl_seconds == 1800

    def test_custom_ttl(self):
        m = IntelligenceModel(author="A", content="X", ttl_seconds=60)
        assert m.ttl_seconds == 60

    def test_missing_author(self):
        with pytest.raises(ValidationError):
            IntelligenceModel(content="X")

    def test_missing_content(self):
        with pytest.raises(ValidationError):
            IntelligenceModel(author="A")


class TestRiskAuditModel:
    def test_valid(self):
        m = RiskAuditModel(max_position_allowance=10000.0)
        assert m.global_lock is False
        assert m.current_drawdown == 0.0

    def test_global_lock(self):
        m = RiskAuditModel(global_lock=True, max_position_allowance=0)
        assert m.global_lock is True

    def test_negative_allowance(self):
        with pytest.raises(ValidationError):
            RiskAuditModel(max_position_allowance=-1)

    def test_missing_allowance(self):
        with pytest.raises(ValidationError):
            RiskAuditModel()
