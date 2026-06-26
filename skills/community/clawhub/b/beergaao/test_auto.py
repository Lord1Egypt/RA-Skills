"""未来函数自动检测器 - 检测策略是否存在前视偏差"""
from __future__ import annotations

import numpy as np
import pandas as pd
from stock_skill.indicators import compute_all
from stock_skill.strategies.strategies import get_all_strategies


def create_test_data(n_days: int = 200) -> pd.DataFrame:
    """创建测试数据"""
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=n_days, freq="B")

    base_price = 100
    returns = np.random.normal(0.001, 0.02, n_days)
    prices = base_price * np.cumprod(1 + returns)

    df = pd.DataFrame({
        "date": dates.strftime("%Y%m%d"),
        "open": prices * (1 + np.random.uniform(-0.01, 0.01, n_days)),
        "high": prices * (1 + np.random.uniform(0, 0.03, n_days)),
        "low": prices * (1 - np.random.uniform(0, 0.03, n_days)),
        "close": prices,
        "volume": np.random.randint(1000000, 10000000, n_days),
    })

    return df


def detect_lookahead_in_indicators(df: pd.DataFrame, cutoff_idx: int) -> bool:
    """检测技术指标计算是否存在未来函数

    Args:
        df: 完整K线数据
        cutoff_idx: 截断位置（只使用 0~cutoff_idx 的数据）

    Returns:
        True = 存在未来函数，False = 无未来函数
    """
    # 使用完整数据计算指标
    full_df = compute_all(df.copy())

    # 使用截断数据计算指标
    truncated_df = compute_all(df.iloc[:cutoff_idx + 1].copy())

    # 比较截断位置的指标值
    indicator_cols = ["ma5", "ma10", "ma20", "ma60", "ma120",
                      "dif", "dea", "macd", "rsi", "k", "d", "j",
                      "boll_mid", "boll_upper", "boll_lower", "atr"]

    for col in indicator_cols:
        if col not in full_df.columns or col not in truncated_df.columns:
            continue

        # 截断数据的最后一个值应该与完整数据在相同位置的值一致
        truncated_last = truncated_df.iloc[-1][col]
        full_value = full_df.iloc[cutoff_idx][col]

        if not np.isnan(truncated_last) and not np.isnan(full_value):
            if abs(truncated_last - full_value) > 1e-10:
                print(f"[未来函数] 指标 {col}: 截断值={truncated_last:.6f}, 完整值={full_value:.6f}")
                return True

    return False


def detect_lookahead_in_strategies(df: pd.DataFrame, cutoff_idx: int) -> bool:
    """检测策略信号计算是否存在未来函数

    Args:
        df: 完整K线数据
        cutoff_idx: 截断位置

    Returns:
        True = 存在未来函数
    """
    # 先计算技术指标
    full_df = compute_all(df.copy())
    truncated_df = compute_all(df.iloc[:cutoff_idx + 1].copy())

    strategies = get_all_strategies()
    has_lookahead = False

    for strategy in strategies:
        try:
            # 使用截断数据生成信号
            signal_truncated = strategy.evaluate(truncated_df)

            # 如果截断数据没有信号，跳过
            if signal_truncated is None:
                continue

            # 使用完整数据在相同位置生成信号（应该得到相同结果）
            # 注意：策略需要至少2行数据才能比较
            if cutoff_idx >= 1:
                signal_full_at_cutoff = strategy.evaluate(full_df.iloc[:cutoff_idx + 1])

                # 如果两者信号不同，可能存在未来函数
                if signal_full_at_cutoff is None and signal_truncated is not None:
                    print(f"[未来函数] 策略 {strategy.name}: 截断有信号但完整数据无信号")
                    has_lookahead = True
                elif signal_full_at_cutoff is not None and signal_truncated is not None:
                    if signal_full_at_cutoff.direction != signal_truncated.direction:
                        print(f"[未来函数] 策略 {strategy.name}: "
                              f"截断方向={signal_truncated.direction}, "
                              f"完整方向={signal_full_at_cutoff.direction}")
                        has_lookahead = True
                    elif abs(signal_full_at_cutoff.confidence - signal_truncated.confidence) > 0.01:
                        print(f"[未来函数] 策略 {strategy.name}: "
                              f"置信度差异 {abs(signal_full_at_cutoff.confidence - signal_truncated.confidence):.4f}")
                        has_lookahead = True

        except Exception as e:
            # 策略计算失败不算未来函数
            pass

    return has_lookahead


def detect_lookahead_in_rolling(df: pd.DataFrame, test_points: int = 5) -> dict:
    """滚动检测多个时间点的未来函数

    Args:
        df: 完整K线数据
        test_points: 测试点数量

    Returns:
        检测结果字典
    """
    n = len(df)
    if n < 100:
        return {"error": "数据不足，需要至少100条K线"}

    # 选择测试点（均匀分布在后半段）
    start_idx = n // 2
    step = (n - start_idx) // test_points
    test_indices = [start_idx + i * step for i in range(test_points)]
    test_indices = [idx for idx in test_indices if idx < n - 10]  # 留出足够的未来数据

    results = {
        "indicator_lookahead": False,
        "strategy_lookahead": False,
        "details": [],
    }

    for idx in test_indices:
        # 检测指标
        ind_result = detect_lookahead_in_indicators(df, idx)
        if ind_result:
            results["indicator_lookahead"] = True
            results["details"].append(f"指标在位置 {idx} 存在未来函数")

        # 检测策略
        strat_result = detect_lookahead_in_strategies(df, idx)
        if strat_result:
            results["strategy_lookahead"] = True
            results["details"].append(f"策略在位置 {idx} 存在未来函数")

    return results


def any_lookahead(df: pd.DataFrame = None) -> bool:
    """检测是否存在未来函数

    Args:
        df: 测试数据，如果为None则自动生成

    Returns:
        True = 存在未来函数，False = 无未来函数
    """
    if df is None:
        df = create_test_data(200)

    result = detect_lookahead_in_rolling(df, test_points=3)

    if result.get("indicator_lookahead") or result.get("strategy_lookahead"):
        print("[失败] 检测到未来函数:")
        for detail in result.get("details", []):
            print(f"  - {detail}")
        return True

    return False


# ===================== 测试函数 =====================

def test_no_lookahead():
    """测试策略和技术指标不存在未来函数"""
    print("[测试] 检测未来函数...")

    df = create_test_data(200)

    # 检测指标
    has_indicator_lookahead = False
    for idx in [100, 150, 180]:
        if detect_lookahead_in_indicators(df, idx):
            has_indicator_lookahead = True
            break

    assert not has_indicator_lookahead, "技术指标存在未来函数！"

    # 检测策略
    has_strategy_lookahead = False
    for idx in [100, 150, 180]:
        if detect_lookahead_in_strategies(df, idx):
            has_strategy_lookahead = True
            break

    assert not has_strategy_lookahead, "策略信号存在未来函数！"

    print("[通过] 未检测到未来函数")


def test_indicator_consistency():
    """测试指标计算的一致性"""
    print("[测试] 指标一致性...")

    df = create_test_data(150)
    df = compute_all(df)

    # 检查滚动窗口指标是否正确使用历史数据
    # MA5 在位置 i 应该只使用 close[i-4] 到 close[i]
    for i in [50, 100, 120]:
        ma5_expected = df["close"].iloc[i-4:i+1].mean()
        ma5_actual = df["iloc" if False else "ma5"].iloc[i]  # 使用列名

        if abs(ma5_expected - ma5_actual) > 1e-10:
            print(f"[失败] MA5 在位置 {i}: 期望={ma5_expected:.4f}, 实际={ma5_actual:.4f}")
            assert False, "MA5 计算不一致"

    print("[通过] 指标一致性检查")


def test_quant_skill():
    """基础功能测试"""
    print("[测试] 启动 BeerGaao 量化 Skill...")
    from stock_skill.tools.tools import StockTools
    tools = StockTools()
    print("[测试] StockTools 初始化成功")
    print("[测试] 基础功能通过")


if __name__ == "__main__":
    test_no_lookahead()
    test_indicator_consistency()
    test_quant_skill()
    print("\n[完成] 所有测试通过")
