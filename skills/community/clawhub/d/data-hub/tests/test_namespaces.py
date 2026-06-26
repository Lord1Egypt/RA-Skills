import json
import time

from data_hub.constants import INDICATOR_WINDOW_SIZE
from data_hub.namespaces import indicators, intelligence, market_state, risk_audit


class TestMarketStateNamespace:
    def setup_method(self):
        self.memory = {"market_state": {}, "indicators": {}, "intelligence": {}, "risk_audit": {}}

    def test_push_valid(self):
        new_mem, err = market_state.push(self.memory, "BTC_USDT", {"last_price": 65000.5})
        assert err is None
        assert new_mem["market_state"]["BTC_USDT"]["last_price"] == 65000.5

    def test_push_invalid(self):
        new_mem, err = market_state.push(self.memory, "BTC_USDT", {"last_price": "bad"})
        assert err is not None
        assert "[VALIDATION_ERROR]" in err
        assert new_mem is self.memory  # 原数据不变

    def test_get_existing(self):
        new_mem, _ = market_state.push(self.memory, "BTC_USDT", {"last_price": 100.0})
        result = market_state.get(new_mem, "BTC_USDT")
        assert result["last_price"] == 100.0

    def test_get_missing(self):
        assert market_state.get(self.memory, "ETH_USDT") is None

    def test_overwrite(self):
        mem1, _ = market_state.push(self.memory, "BTC_USDT", {"last_price": 100.0})
        mem2, _ = market_state.push(mem1, "BTC_USDT", {"last_price": 200.0})
        assert mem2["market_state"]["BTC_USDT"]["last_price"] == 200.0


class TestIndicatorsNamespace:
    def setup_method(self):
        self.memory = {"market_state": {}, "indicators": {}, "intelligence": {}, "risk_audit": {}}

    def test_push_valid(self):
        data = {"rsi": [45.2, 48.1], "ma20": [64800.0]}
        new_mem, err = indicators.push(self.memory, "BTC_USDT", data)
        assert err is None
        assert new_mem["indicators"]["BTC_USDT"]["rsi"] == [45.2, 48.1]

    def test_push_invalid_type(self):
        _, err = indicators.push(self.memory, "BTC_USDT", {"rsi": "bad"})
        assert err is not None
        assert "[VALIDATION_ERROR]" in err

    def test_push_invalid_value_type(self):
        _, err = indicators.push(self.memory, "BTC_USDT", {"rsi": ["not_float"]})
        assert err is not None

    def test_sliding_window(self):
        big_data = {"rsi": list(range(60))}
        new_mem, _ = indicators.push(self.memory, "BTC_USDT", big_data)
        assert len(new_mem["indicators"]["BTC_USDT"]["rsi"]) == INDICATOR_WINDOW_SIZE
        assert new_mem["indicators"]["BTC_USDT"]["rsi"][0] == 10  # 前 10 条被丢弃

    def test_append_merge(self):
        mem1, _ = indicators.push(self.memory, "BTC_USDT", {"rsi": [1.0, 2.0]})
        mem2, _ = indicators.push(mem1, "BTC_USDT", {"rsi": [3.0]})
        assert mem2["indicators"]["BTC_USDT"]["rsi"] == [1.0, 2.0, 3.0]

    def test_get_missing(self):
        assert indicators.get(self.memory, "ETH_USDT") is None


class TestIntelligenceNamespace:
    def setup_method(self):
        self.memory = {"market_state": {}, "indicators": {}, "intelligence": {}, "risk_audit": {}}

    def test_push_valid(self):
        data = {"author": "Analyst_Officer", "content": "BTC看涨"}
        new_mem, err = intelligence.push(self.memory, "BTC_USDT", data)
        assert err is None
        assert new_mem["intelligence"]["BTC_USDT"]["author"] == "Analyst_Officer"

    def test_push_invalid(self):
        _, err = intelligence.push(self.memory, "BTC_USDT", {"author": "A"})
        assert err is not None
        assert "[VALIDATION_ERROR]" in err

    def test_get_missing(self):
        assert intelligence.get(self.memory, "ETH_USDT") is None


class TestRiskAuditNamespace:
    def setup_method(self):
        self.memory = {"market_state": {}, "indicators": {}, "intelligence": {}, "risk_audit": {}}

    def test_push_valid(self):
        data = {"max_position_allowance": 10000.0, "current_drawdown": 0.05}
        new_mem, err = risk_audit.push(self.memory, data)
        assert err is None
        assert new_mem["risk_audit"]["global_state"]["max_position_allowance"] == 10000.0

    def test_push_invalid(self):
        _, err = risk_audit.push(self.memory, {"max_position_allowance": -1})
        assert err is not None

    def test_get_empty(self):
        assert risk_audit.get(self.memory) is None

    def test_snapshot_save_load(self, tmp_path):
        data = {"global_lock": False, "max_position_allowance": 5000.0}
        path = str(tmp_path / "snapshot.json")

        err = risk_audit.save_snapshot(data, path)
        assert err is None

        loaded, load_err = risk_audit.load_snapshot(path)
        assert load_err is None
        assert loaded["max_position_allowance"] == 5000.0

    def test_snapshot_load_missing_file(self):
        _, err = risk_audit.load_snapshot("/nonexistent/path.json")
        assert "[SNAPSHOT_ERROR]" in err

    def test_snapshot_load_corrupt_file(self, tmp_path):
        path = str(tmp_path / "bad.json")
        with open(path, "w") as f:
            f.write("{corrupt")
        _, err = risk_audit.load_snapshot(path)
        assert "[SNAPSHOT_ERROR]" in err
