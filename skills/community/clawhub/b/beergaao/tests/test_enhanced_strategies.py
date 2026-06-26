"""增强策略模块测试"""
import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def create_test_data(n_days: int = 100) -> pd.DataFrame:
    """创建测试数据"""
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=n_days, freq="D")

    base_price = 100
    returns = np.random.normal(0.001, 0.02, n_days)
    prices = base_price * np.cumprod(1 + returns)

    df = pd.DataFrame({
        "date": dates,
        "open": prices * (1 + np.random.uniform(-0.01, 0.01, n_days)),
        "high": prices * (1 + np.random.uniform(0, 0.03, n_days)),
        "low": prices * (1 - np.random.uniform(0, 0.03, n_days)),
        "close": prices,
        "volume": np.random.randint(1000000, 10000000, n_days),
    })

    df["ma5"] = df["close"].rolling(5).mean()
    df["ma10"] = df["close"].rolling(10).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["ma60"] = df["close"].rolling(60).mean()
    df["vol_ma5"] = df["volume"].rolling(5).mean()

    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()
    df["dif"] = exp1 - exp2
    df["dea"] = df["dif"].ewm(span=9, adjust=False).mean()
    df["macd"] = (df["dif"] - df["dea"]) * 2

    df["boll_mid"] = df["close"].rolling(20).mean()
    df["boll_std"] = df["close"].rolling(20).std()
    df["boll_upper"] = df["boll_mid"] + 2 * df["boll_std"]
    df["boll_lower"] = df["boll_mid"] - 2 * df["boll_std"]

    low_min = df["low"].rolling(9).min()
    high_max = df["high"].rolling(9).max()
    rsv = (df["close"] - low_min) / (high_max - low_min) * 100
    df["k"] = rsv.ewm(com=2, adjust=False).mean()
    df["d"] = df["k"].ewm(com=2, adjust=False).mean()
    df["j"] = 3 * df["k"] - 2 * df["d"]

    return df


class TestStrategyParams:
    """测试策略参数化"""

    def test_strategy_params_default(self):
        from stock_skill.strategies.strategies import StrategyParams
        params = StrategyParams()
        assert params.vol_multiplier == 1.8
        assert params.rsi_threshold == 30
        assert params.ma_period == 20

    def test_strategy_params_custom(self):
        from stock_skill.strategies.strategies import StrategyParams
        params = StrategyParams(vol_multiplier=2.0, rsi_threshold=25)
        assert params.vol_multiplier == 2.0
        assert params.rsi_threshold == 25

    def test_strategy_set_params(self):
        from stock_skill.strategies.strategies import MABreakoutStrategy
        strategy = MABreakoutStrategy()
        strategy.set_params(vol_multiplier=2.5)
        assert strategy.params.vol_multiplier == 2.5


class TestMAStrategies:
    """测试传统策略"""

    def test_ma_breakout_strategy(self):
        from stock_skill.strategies.strategies import MABreakoutStrategy
        df = create_test_data(50)
        strategy = MABreakoutStrategy()
        result = strategy.evaluate(df)
        assert result is None or hasattr(result, "direction")

    def test_macd_cross_strategy(self):
        from stock_skill.strategies.strategies import MACDCrossStrategy
        df = create_test_data(50)
        strategy = MACDCrossStrategy()
        result = strategy.evaluate(df)
        assert result is None or hasattr(result, "confidence")

    def test_rsi_oversold_strategy(self):
        from stock_skill.strategies.strategies import RSIOversoldStrategy
        df = create_test_data(50)
        strategy = RSIOversoldStrategy()
        result = strategy.evaluate(df)
        assert result is None or result.direction in ["BUY", "SELL"]


class TestStrategyOptimizer:
    """测试策略优化器"""

    def test_param_space(self):
        from stock_skill.strategies.optimizer import ParamSpace
        space = ParamSpace("test", "float", low=1.0, high=3.0)
        sample = space.sample()
        assert 1.0 <= sample <= 3.0

    def test_param_space_int(self):
        from stock_skill.strategies.optimizer import ParamSpace
        space = ParamSpace("test", "int", low=5, high=20)
        sample = space.sample()
        assert 5 <= sample <= 20

    def test_grid_search(self):
        from stock_skill.strategies.optimizer import StrategyOptimizer
        from stock_skill.strategies.strategies import RSIOversoldStrategy

        df = create_test_data(100)
        optimizer = StrategyOptimizer(RSIOversoldStrategy)
        optimizer.add_param("rsi_threshold", "int", low=25, high=35)
        result = optimizer.grid_search(df)
        assert result.best_score >= 0
        assert "rsi_threshold" in result.best_params


class TestMLEnhancements:
    """测试机器学习增强"""

    def test_feature_engineer(self):
        from stock_skill.strategies.ml_strategies import FeatureEngineer
        df = create_test_data(100)
        features = FeatureEngineer.create_features(df)
        assert len(features) == len(df)
        assert "momentum_5" in features.columns
        assert "volatility_10" in features.columns

    def test_random_forest_strategy(self):
        from stock_skill.strategies.ml_strategies import RandomForestStrategy
        df = create_test_data(200)
        strategy = RandomForestStrategy()
        metrics = strategy.train(df, forward_periods=5, threshold=0.02)
        assert "accuracy" in metrics
        assert "samples" in metrics


class TestEnsembleStrategy:
    """测试集成策略"""

    def test_market_regime_detector(self):
        from stock_skill.strategies.ensemble import MarketRegimeDetector, MarketRegime
        df = create_test_data(100)
        detector = MarketRegimeDetector()
        regime = detector.detect(df)
        assert isinstance(regime, MarketRegime)

    def test_ensemble_engine(self):
        from stock_skill.strategies.ensemble import EnsembleStrategyEngine
        df = create_test_data(100)
        engine = EnsembleStrategyEngine()
        signal = engine.evaluate(df, min_consensus=0.1)
        assert signal is None or hasattr(signal, "consensus_score")


class TestFactorAnalysis:
    """测试因子分析"""

    def test_enhanced_factor_analyzer(self):
        from stock_skill.factors.enhanced_ic import EnhancedFactorAnalyzer
        df = create_test_data(100)
        analyzer = EnhancedFactorAnalyzer()

        factor_values = pd.Series(np.random.randn(100), index=df.index)
        result = analyzer.analyze_factor(factor_values, df, "test_factor")
        assert hasattr(result, "ic_mean")
        assert hasattr(result, "ic_ir")

    def test_factor_turnover(self):
        from stock_skill.factors.enhanced_ic import EnhancedFactorAnalyzer
        analyzer = EnhancedFactorAnalyzer()
        factor_values = pd.Series(np.random.randn(100))
        turnover = analyzer.calculate_factor_turnover(factor_values)
        assert 0 <= turnover <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
