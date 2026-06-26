"""P1: ML 策略测试 - 特征工程、模型训练/推理、数据不足降级"""
import pytest
import numpy as np
import pandas as pd


def make_ml_test_df(n=200):
    """创建 ML 测试数据"""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    close = 10 + np.cumsum(np.random.randn(n) * 0.3)
    close = np.maximum(close, 1)
    high = close * (1 + np.abs(np.random.randn(n) * 0.01))
    low = close * (1 - np.abs(np.random.randn(n) * 0.01))
    opn = close * (1 + np.random.randn(n) * 0.005)
    volume = np.random.randint(100000, 1000000, n).astype(float)
    return pd.DataFrame({
        "date": dates.strftime("%Y%m%d"),
        "open": opn, "high": high, "low": low, "close": close,
        "volume": volume, "amount": volume * close
    })


class TestFeatureEngineer:
    """特征工程测试"""

    def test_create_features(self):
        """特征生成"""
        try:
            from stock_skill.strategies.ml_strategies import FeatureEngineer
            df = make_ml_test_df(100)
            features = FeatureEngineer.create_features(df)
            assert len(features) == len(df)
            assert "momentum_5" in features.columns
            assert "volatility_10" in features.columns
        except ImportError:
            pytest.skip("ML 模块不可用")

    def test_features_no_nan(self):
        """特征无 NaN（或 NaN 在合理范围内）"""
        try:
            from stock_skill.strategies.ml_strategies import FeatureEngineer
            df = make_ml_test_df(100)
            features = FeatureEngineer.create_features(df)
            # 前几行可能有 NaN（滚动窗口）
            nan_ratio = features.isnull().sum().sum() / (features.shape[0] * features.shape[1])
            assert nan_ratio < 0.1  # NaN 比例 < 10%
        except ImportError:
            pytest.skip("ML 模块不可用")


class TestMLStrategy:
    """ML 策略测试"""

    def test_random_forest_train(self):
        """随机森林训练"""
        try:
            from stock_skill.strategies.ml_strategies import RandomForestStrategy
            df = make_ml_test_df(200)
            strategy = RandomForestStrategy()
            metrics = strategy.train(df, forward_periods=5, threshold=0.02)
            assert "accuracy" in metrics
            assert "samples" in metrics
            assert metrics["samples"] > 0
        except ImportError:
            pytest.skip("ML 模块不可用")

    def test_random_forest_predict(self):
        """随机森林预测"""
        try:
            from stock_skill.strategies.ml_strategies import RandomForestStrategy
            df = make_ml_test_df(200)
            strategy = RandomForestStrategy()
            strategy.train(df, forward_periods=5, threshold=0.02)
            signal = strategy.evaluate(df)
            assert signal is None or hasattr(signal, "confidence")
        except ImportError:
            pytest.skip("ML 模块不可用")

    def test_insufficient_data(self):
        """数据不足 -> 降级"""
        try:
            from stock_skill.strategies.ml_strategies import RandomForestStrategy
            df = make_ml_test_df(50)  # 不足 200 行
            strategy = RandomForestStrategy()
            result = strategy.evaluate(df)
            # 数据不足时应返回 None 或降级处理
            assert result is None or hasattr(result, "confidence")
        except ImportError:
            pytest.skip("ML 模块不可用")


class TestEnsembleMLStrategy:
    """集成 ML 策略测试"""

    def test_ensemble_ml_evaluate(self):
        """集成 ML 策略评估"""
        try:
            from stock_skill.strategies.ml_strategies import EnsembleMLStrategy
            df = make_ml_test_df(200)
            strategy = EnsembleMLStrategy()
            signal = strategy.evaluate(df)
            assert signal is None or hasattr(signal, "confidence")
        except ImportError:
            pytest.skip("ML 模块不可用")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
