"""单元测试"""
import json, sys, os, unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import numpy as np
import pandas as pd

def make_sample_df(n=200):
    np.random.seed(42)
    dates = pd.date_range("2025-01-01", periods=n, freq="B")
    close = 10+np.cumsum(np.random.randn(n)*0.3)
    close = np.maximum(close, 1)
    high = close*(1+np.abs(np.random.randn(n)*0.01))
    low = close*(1-np.abs(np.random.randn(n)*0.01))
    opn = close*(1+np.random.randn(n)*0.005)
    volume = np.random.randint(100000,1000000,n).astype(float)
    return pd.DataFrame({"date":dates.strftime("%Y%m%d"),"open":opn,"high":high,"low":low,"close":close,"volume":volume,"amount":volume*close})

class TestConfig(unittest.TestCase):
    @patch.dict(os.environ,{"TUSHARE_TOKEN":"test123","VOL_MULTI":"2.0"})
    def test_config_from_env(self):
        from stock_skill.config import reload_config
        cfg = reload_config()
        self.assertEqual(cfg.tushare_token,"test123")
        self.assertEqual(cfg.vol_multi,2.0)

class TestIndicators(unittest.TestCase):
    def test_compute_all(self):
        from stock_skill.indicators import compute_all, latest_indicators
        df = make_sample_df()
        result = compute_all(df)
        for col in ["ma5","ma20","ma60","dif","dea","macd","rsi","k","d","j","boll_mid","atr"]:
            self.assertIn(col, result.columns)
        ind = latest_indicators(result)
        self.assertGreater(len(ind), 10)

    def test_support_resistance(self):
        from stock_skill.indicators import compute_all, support_resistance
        df = compute_all(make_sample_df())
        s, r = support_resistance(df)
        self.assertLess(s, float(df.iloc[-1]["close"]))
        self.assertGreater(r, float(df.iloc[-1]["close"]))

class TestStrategies(unittest.TestCase):
    def test_registry(self):
        from stock_skill.strategies.strategies import get_all_strategies
        names = [s.name for s in get_all_strategies()]
        self.assertIn("ma_breakout", names)
        self.assertIn("macd_cross", names)
        self.assertIn("boll_squeeze", names)
        self.assertIn("vol_price_divergence", names)
        self.assertIn("obv_trend", names)
        self.assertIn("double_ma", names)
        self.assertIn("support_bounce", names)
        self.assertGreaterEqual(len(names), 10)

    def test_no_crash(self):
        from stock_skill.strategies.strategies import get_all_strategies
        from stock_skill.indicators import compute_all
        df = compute_all(make_sample_df(200))
        for s in get_all_strategies():
            result = s.evaluate(df)
            self.assertTrue(result is None or hasattr(result,"confidence"))

class TestRisk(unittest.TestCase):
    def test_position(self):
        from stock_skill.risk import RiskManager
        rm = RiskManager()
        pos = rm.calculate_position(0.7, 7.0, 2, 0.5, 10.0)
        self.assertGreater(pos.position_pct, 0)
        self.assertLessEqual(pos.position_pct, rm.max_single)

    def test_circuit_breaker(self):
        from stock_skill.risk import RiskManager
        from stock_skill.models import MarketAnalysis, MarketTrend
        rm = RiskManager()
        crash = MarketAnalysis(trend=MarketTrend.STRONG_DOWN,score=1.0,up_count=100,down_count=1900,total_count=2000,limit_up=0,limit_down=50)
        triggered, reasons = rm.circuit_breaker(crash)
        self.assertTrue(triggered)
        self.assertGreater(len(reasons), 0)

    def test_trailing_stop(self):
        from stock_skill.risk import RiskManager
        rm = RiskManager()
        ts = rm.init_trailing_stop("TEST.SH", 10.0, 0.3)
        rm.update_trailing_stop("TEST.SH", 11.0)
        self.assertEqual(ts.highest_price, 11.0)
        self.assertGreater(ts.current_stop, 9.0)

class TestModels(unittest.TestCase):
    def test_signal_json(self):
        from stock_skill.models import TradeSignal, SignalType
        sig = TradeSignal(code="600036.SH",name="招商银行",signal_type=SignalType.BUY,price=35.0,
            support=33.0,resistance=38.0,stop_loss=33.6,target_price=37.1,position_pct=0.2,confidence=0.75,reason="test")
        j = sig.to_dict()
        self.assertEqual(j["code"],"600036.SH")
        self.assertEqual(j["signal_type"],"买入")

class TestSemantic(unittest.TestCase):
    def test_resolve(self):
        from stock_skill.semantic import _resolve_code, _detect_intent
        self.assertEqual(_resolve_code("招商银行怎么样"),"600036.SH")
        self.assertEqual(_detect_intent("今天复盘"),"full_review")
        self.assertEqual(_detect_intent("大盘怎么样"),"analyze_market")

class TestState(unittest.TestCase):
    def setUp(self):
        from stock_skill.state import StateStore
        self.store = StateStore(":memory:")
    def test_signal(self):
        from stock_skill.models import TradeSignal, SignalType
        sig = TradeSignal(code="600036.SH",name="招商银行",signal_type=SignalType.BUY,price=35.0,
            support=33.0,resistance=38.0,stop_loss=33.6,target_price=37.1,position_pct=0.2,confidence=0.75,reason="test")
        self.store.save_signal(sig)
        self.assertEqual(len(self.store.get_signals(code="600036.SH")),1)

class TestFactors(unittest.TestCase):
    def test_factor_registry(self):
        from stock_skill.factors.base import get_all_factors
        factors = get_all_factors()
        self.assertGreater(len(factors), 5)

    def test_fundamental_factors(self):
        from stock_skill.factors.fundamental import FundamentalFactorSet
        factors = FundamentalFactorSet.get_factors()
        self.assertGreater(len(factors), 5)

    def test_sentiment_factors(self):
        from stock_skill.factors.sentiment import SentimentFactorSet
        factors = SentimentFactorSet.get_factors()
        self.assertGreater(len(factors), 4)

    def test_factor_combiner(self):
        from stock_skill.factors.base import FactorResult, FactorCombiner
        f1 = FactorResult(name="test1",category="test",description="",values={"A":1,"B":2,"C":3})
        f2 = FactorResult(name="test2",category="test",description="",values={"A":3,"B":1,"C":2})
        scores = FactorCombiner.equal_weight([f1,f2])
        self.assertIn("A", scores)
        self.assertIn("B", scores)

class TestBacktest(unittest.TestCase):
    def test_backtest_engine(self):
        from stock_skill.backtest.engine import BacktestEngine, BacktestConfig, CostModel
        config = BacktestConfig(initial_capital=100000, cost_model=CostModel())
        engine = BacktestEngine(config)
        self.assertEqual(engine.portfolio.cash, 100000)

    def test_cost_model(self):
        from stock_skill.backtest.engine import CostModel
        cm = CostModel()
        buy = cm.buy_cost(10.0, 1000)
        self.assertGreater(buy, 10000)
        sell = cm.sell_cost(10.0, 1000)
        self.assertLess(sell, 10000)

class TestExecution(unittest.TestCase):
    def test_simulated_broker(self):
        from stock_skill.execution.order import SimulatedBroker, OrderRequest, OrderSide, OrderType
        broker = SimulatedBroker(100000)
        order = OrderRequest(code="600036.SH",side=OrderSide.BUY,order_type=OrderType.MARKET,quantity=100,price=10.0)
        resp = broker.submit_order(order)
        self.assertEqual(resp.status.value, "filled")
        self.assertIn("600036.SH", broker.positions)

    def test_t1_manager(self):
        from stock_skill.execution.order import T1Manager
        t1 = T1Manager()
        t1.record_buy("600036.SH", "2025-01-01")
        self.assertFalse(t1.can_sell("600036.SH", "2025-01-01"))
        self.assertTrue(t1.can_sell("600036.SH", "2025-01-02"))

class TestAttribution(unittest.TestCase):
    def test_brinson(self):
        from stock_skill.attribution.brinson import BrinsonModel
        pw = {"tech":0.4,"finance":0.3,"health":0.3}
        bw = {"tech":0.3,"finance":0.4,"health":0.3}
        pr = {"tech":0.05,"finance":0.02,"health":-0.01}
        br = {"tech":0.03,"finance":0.04,"health":0.01}
        result = BrinsonModel.single_period(pw,bw,pr,br)
        self.assertIsNotNone(result.total_active_return)

if __name__=="__main__": unittest.main()
