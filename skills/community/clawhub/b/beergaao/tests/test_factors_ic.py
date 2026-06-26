"""P1: 因子 IC 计算测试 - IC 分析、显著性判断、因子换手率"""
import pytest
import numpy as np
import pandas as pd


def make_factor_test_df(n=100):
    """创建因子测试数据"""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    close = 10 + np.cumsum(np.random.randn(n) * 0.3)
    close = np.maximum(close, 1)
    high = close * 1.01
    low = close * 0.99
    opn = close
    volume = np.random.randint(100000, 1000000, n).astype(float)
    return pd.DataFrame({
        "date": dates.strftime("%Y%m%d"),
        "open": opn, "high": high, "low": low, "close": close,
        "volume": volume, "amount": volume * close
    })


class TestEnhancedFactorAnalyzer:
    """增强因子分析器测试"""

    def test_analyze_factor(self):
        """因子分析"""
        try:
            from stock_skill.factors.enhanced_ic import EnhancedFactorAnalyzer
            df = make_factor_test_df(100)
            analyzer = EnhancedFactorAnalyzer()
            factor_values = pd.Series(np.random.randn(100), index=df.index)
            result = analyzer.analyze_factor(factor_values, df, "test_factor")
            assert hasattr(result, "ic_mean")
            assert hasattr(result, "ic_ir")
        except ImportError:
            pytest.skip("因子分析模块不可用")

    def test_ic_calculation(self):
        """IC 计算正确性"""
        try:
            from stock_skill.factors.enhanced_ic import EnhancedFactorAnalyzer
            df = make_factor_test_df(100)
            analyzer = EnhancedFactorAnalyzer()
            # 创建一个与未来收益正相关的因子
            future_returns = df["close"].pct_change(5).shift(-5)
            factor_values = future_returns + np.random.randn(100) * 0.1
            result = analyzer.analyze_factor(factor_values, df, "correlated_factor")
            # 正相关因子 IC 应 > 0
            assert result.ic_mean > 0
        except ImportError:
            pytest.skip("因子分析模块不可用")

    def test_factor_turnover(self):
        """因子换手率"""
        try:
            from stock_skill.factors.enhanced_ic import EnhancedFactorAnalyzer
            analyzer = EnhancedFactorAnalyzer()
            # 稳定因子
            stable_factor = pd.Series([1, 1, 1, 2, 2, 2, 3, 3, 3])
            turnover = analyzer.calculate_factor_turnover(stable_factor)
            assert 0 <= turnover <= 1
        except ImportError:
            pytest.skip("因子分析模块不可用")

    def test_factor_turnover_high(self):
        """高换手率因子"""
        try:
            from stock_skill.factors.enhanced_ic import EnhancedFactorAnalyzer
            analyzer = EnhancedFactorAnalyzer()
            # 高换手因子
            volatile_factor = pd.Series([1, 10, 2, 9, 3, 8, 4, 7, 5])
            turnover = analyzer.calculate_factor_turnover(volatile_factor)
            assert turnover > 0.5
        except ImportError:
            pytest.skip("因子分析模块不可用")


class TestFactorResult:
    """因子结果测试"""

    def test_factor_result_attributes(self):
        """因子结果属性"""
        try:
            from stock_skill.factors.base import FactorResult
            result = FactorResult(
                name="test_factor",
                category="test",
                description="测试因子",
                values={"A": 1.0, "B": 2.0, "C": 3.0}
            )
            assert result.name == "test_factor"
            assert result.category == "test"
            assert result.values["A"] == 1.0
        except ImportError:
            pytest.skip("因子模块不可用")


class TestFactorCombiner:
    """因子合成测试"""

    def test_equal_weight(self):
        """等权重合成"""
        try:
            from stock_skill.factors.base import FactorResult, FactorCombiner
            f1 = FactorResult(name="f1", category="test", description="",
                            values={"A": 1, "B": 2, "C": 3})
            f2 = FactorResult(name="f2", category="test", description="",
                            values={"A": 3, "B": 1, "C": 2})
            scores = FactorCombiner.equal_weight([f1, f2])
            assert "A" in scores
            assert "B" in scores
            assert "C" in scores
        except ImportError:
            pytest.skip("因子模块不可用")

    def test_equal_weight_values(self):
        """等权重合成值正确"""
        try:
            from stock_skill.factors.base import FactorResult, FactorCombiner
            f1 = FactorResult(name="f1", category="test", description="",
                            values={"A": 0.6, "B": 0.4})
            f2 = FactorResult(name="f2", category="test", description="",
                            values={"A": 0.4, "B": 0.6})
            scores = FactorCombiner.equal_weight([f1, f2])
            # 等权重平均
            assert scores["A"] == pytest.approx(0.5, abs=0.01)
            assert scores["B"] == pytest.approx(0.5, abs=0.01)
        except ImportError:
            pytest.skip("因子模块不可用")


class TestFactorRegistry:
    """因子注册表测试"""

    def test_get_all_factors(self):
        """获取所有因子"""
        try:
            from stock_skill.factors.base import get_all_factors
            factors = get_all_factors()
            assert len(factors) > 0
        except ImportError:
            pytest.skip("因子模块不可用")

    def test_get_factors_by_category(self):
        """按类别获取因子"""
        try:
            from stock_skill.factors.base import get_factors_by_category
            factors = get_factors_by_category()
            assert isinstance(factors, dict)
        except ImportError:
            pytest.skip("因子模块不可用")


class TestFundamentalFactors:
    """基本面因子测试"""

    def test_fundamental_factor_set(self):
        """基本面因子集"""
        try:
            from stock_skill.factors.fundamental import FundamentalFactorSet
            factors = FundamentalFactorSet.get_factors()
            assert len(factors) > 0
        except ImportError:
            pytest.skip("因子模块不可用")


class TestSentimentFactors:
    """情绪因子测试"""

    def test_sentiment_factor_set(self):
        """情绪因子集"""
        try:
            from stock_skill.factors.sentiment import SentimentFactorSet
            factors = SentimentFactorSet.get_factors()
            assert len(factors) > 0
        except ImportError:
            pytest.skip("因子模块不可用")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
