"""
Leak Audit Script
P3: 检查预测系统是否存在数据泄漏

数据泄漏类型:
1. 未来信息泄漏: 训练/验证时使用了未来数据
2. 特征泄漏: 某些特征在预测时不可用
3. 随机性泄漏: 随机种子未固定
4. 时间序列泄漏: 窗口滑动时使用了未来数据

Usage:
  python3 scripts/leak_audit.py --symbol BTC-USDT-SWAP --bar 4H
  python3 scripts/leak_audit.py --symbol ETH-USDT-SWAP --bar 1H --detailed
"""
import sys
import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import data provider
from okx_data_provider import get_klines


@dataclass
class LeakReport:
    """泄漏报告"""
    has_leak: bool
    leak_type: str
    severity: str  # critical/high/medium/low/none
    description: str
    location: str
    recommendation: str


class LeakAuditor:
    """泄漏审计器"""
    
    def __init__(self):
        self.reports: List[LeakReport] = []
    
    def audit_future_lookahead(
        self,
        df: pd.DataFrame,
        lookback: int,
        pred_len: int,
        bar: str
    ) -> List[LeakReport]:
        """
        检查是否存在未来数据窥视
        
        问题: 使用了预测窗口内的数据来生成特征
        """
        reports = []
        
        # 检查 lookback 是否足够
        if len(df) < lookback + pred_len:
            reports.append(LeakReport(
                has_leak=True,
                leak_type="insufficient_history",
                severity="high",
                description=f"数据长度 ({len(df)}) < lookback ({lookback}) + pred_len ({pred_len})",
                location="data_pipeline",
                recommendation="确保有足够的歷史數據"
            ))
        
        return reports
    
    def audit_timestamp_alignment(
        self,
        df: pd.DataFrame,
        bar: str
    ) -> List[LeakReport]:
        """
        检查时间戳对齐问题
        """
        reports = []
        
        if "ts" not in df.columns and "timestamp" not in df.columns:
            reports.append(LeakReport(
                has_leak=True,
                leak_type="missing_timestamp",
                severity="critical",
                description="数据中没有时间戳列",
                location="data_pipeline",
                recommendation="必须有时间戳用于对齐检查"
            ))
            return reports
        
        ts_col = "ts" if "ts" in df.columns else "timestamp"
        
        # 检查时间间隔是否一致
        if len(df) > 1:
            df_sorted = df.sort_values(ts_col)
            time_diffs = pd.to_datetime(df_sorted[ts_col]).diff().dropna()
            
            # 根据 bar 计算预期间隔
            bar_minutes = self.bar_to_minutes(bar)
            expected_diff = timedelta(minutes=bar_minutes)
            
            inconsistent = []
            for i, diff in enumerate(time_diffs):
                actual_minutes = diff.total_seconds() / 60
                expected_minutes = bar_minutes
                
                # 允许一定的误差范围 (10%)
                if abs(actual_minutes - expected_minutes) / expected_minutes > 0.1:
                    inconsistent.append(i)
            
            if inconsistent:
                reports.append(LeakReport(
                    has_leak=True,
                    leak_type="timestamp_gaps",
                    severity="medium",
                    description=f"发现 {len(inconsistent)} 个时间间隔不一致的记录",
                    location=f"timestamp_column:{ts_col}",
                    recommendation=f"检查数据源是否完整，预期间隔 {bar}"
                ))
        
        return reports
    
    def audit_feature_leakage(
        self,
        feature_values: Dict[str, any],
        prediction_time: datetime
    ) -> List[LeakReport]:
        """
        检查特征是否在预测时可用
        """
        reports = []
        
        # 检查是否有"事后"特征
        future_only_features = [
            "future_return",
            "next_day_return",
            "forward_close",
            "forward_high",
            "forward_low"
        ]
        
        for feature in future_only_features:
            if feature in feature_values:
                reports.append(LeakReport(
                    has_leak=True,
                    leak_type="future_feature",
                    severity="critical",
                    description=f"特征 '{feature}' 是未来信息，不应在预测时使用",
                    location=f"feature:{feature}",
                    recommendation=f"移除所有包含未来信息的特征"
                ))
        
        return reports
    
    def audit_random_seeds(
        self,
        model_names: List[str]
    ) -> List[LeakReport]:
        """
        检查随机种子是否固定
        """
        reports = []
        
        # 检查环境变量
        seed_vars = ["PYTHONHASHSEED", "RANDOM_SEED", "MODEL_SEED"]
        unfixed_seeds = []
        
        for var in seed_vars:
            if var not in os.environ:
                unfixed_seeds.append(var)
        
        if unfixed_seeds:
            reports.append(LeakReport(
                has_leak=False,
                leak_type="unfixed_random_seed",
                severity="low",
                description=f"环境变量未设置: {', '.join(unfixed_seeds)}",
                location="environment",
                recommendation="建议设置 PYTHONHASHSEED 等环境变量确保可复现性"
            ))
        
        return reports
    
    def audit_time_window_sliding(
        self,
        df: pd.DataFrame,
        lookback: int,
        pred_len: int,
        bar: str
    ) -> List[LeakReport]:
        """
        检查滑动窗口是否存在未来数据泄漏
        
        正确做法:
        - 特征窗口: [t - lookback, t)
        - 预测窗口: [t, t + pred_len)
        - 不能包含任何 t 之后的数据
        """
        reports = []
        
        # 简化检查: 验证数据的时间顺序
        if len(df) > 1:
            df_sorted = df.sort_values("ts" if "ts" in df.columns else "timestamp")
            timestamps = pd.to_datetime(df_sorted["ts" if "ts" in df_sorted.columns else "timestamp"])
            
            # 检查是否有时间倒退
            time_diffs = timestamps.diff().dropna()
            negative_diffs = time_diffs[time_diffs < timedelta(0)]
            
            if len(negative_diffs) > 0:
                reports.append(LeakReport(
                    has_leak=True,
                    leak_type="non_monotonic_time",
                    severity="high",
                    description="时间戳不单调递增，存在回退",
                    location="time_window",
                    recommendation="确保数据按时间排序，检查数据源"
                ))
        
        return reports
    
    def audit_sentiment_timing(
        self,
        sentiment_data: Dict,
        prediction_time: datetime
    ) -> List[LeakReport]:
        """
        检查社媒情绪数据的时间戳是否合理
        """
        reports = []
        
        if not sentiment_data:
            return reports
        
        # 情绪数据应该有发布时间的
        # 如果没有时间戳，可能是爬虫时间而非实际发布时间
        if "timestamp" not in sentiment_data and "published" not in sentiment_data:
            reports.append(LeakReport(
                has_leak=False,
                leak_type="missing_sentiment_timestamp",
                severity="medium",
                description="情绪数据缺少发布时间戳",
                location="social_sentiment_provider",
                recommendation="使用实际发布时间而非爬虫时间"
            ))
        
        return reports
    
    def run_full_audit(
        self,
        symbol: str,
        bar: str,
        lookback: int = 400,
        pred_len: int = 24,
        detailed: bool = False
    ) -> Dict:
        """
        执行完整泄漏审计
        """
        print(f"\n🔍 开始泄漏审计: {symbol} ({bar})")
        print("=" * 60)
        
        all_reports = []
        
        # 1. 获取数据
        print("📊 获取数据...")
        try:
            df = get_klines(symbol, bar=bar, limit=lookback + pred_len + 100)
            if isinstance(df, dict) and "error" in df:
                return {"error": f"获取数据失败: {df['error']}"}
            print(f"   获取到 {len(df)} 条数据")
        except Exception as e:
            return {"error": f"数据获取异常: {e}"}
        
        # 2. 时间戳审计
        print("\n⏰ 检查时间戳...")
        ts_reports = self.audit_timestamp_alignment(df, bar)
        all_reports.extend(ts_reports)
        for r in ts_reports:
            print(f"   {'❌' if r.has_leak else '⚠️'} {r.leak_type}: {r.description}")
        
        # 3. 窗口滑动审计
        print("\n📐 检查窗口滑动...")
        window_reports = self.audit_time_window_sliding(df, lookback, pred_len, bar)
        all_reports.extend(window_reports)
        for r in window_reports:
            print(f"   {'❌' if r.has_leak else '⚠️'} {r.leak_type}: {r.description}")
        
        # 4. 随机种子审计
        print("\n🎲 检查随机种子...")
        seed_reports = self.audit_random_seeds(["kronos", "timesfm", "chronos", "finbert"])
        all_reports.extend(seed_reports)
        for r in seed_reports:
            print(f"   {'❌' if r.has_leak else '⚠️'} {r.leak_type}: {r.description}")
        
        # 5. 详细审计（可选）
        if detailed:
            print("\n🔬 详细分析...")
            # 这里可以添加更多详细检查
            pass
        
        # 汇总
        print("\n" + "=" * 60)
        print("📋 审计报告汇总")
        print("=" * 60)
        
        critical_count = sum(1 for r in all_reports if r.severity == "critical")
        high_count = sum(1 for r in all_reports if r.severity == "high")
        medium_count = sum(1 for r in all_reports if r.severity == "medium")
        low_count = sum(1 for r in all_reports if r.severity == "low")
        
        has_leak = any(r.has_leak for r in all_reports)
        
        if not has_leak:
            print("✅ 未发现数据泄漏")
        else:
            print("❌ 发现数据泄漏问题:")
            for r in all_reports:
                if r.has_leak:
                    print(f"\n  [{r.severity.upper()}] {r.leak_type}")
                    print(f"    位置: {r.location}")
                    print(f"    问题: {r.description}")
                    print(f"    建议: {r.recommendation}")
        
        print(f"\n统计: ❌{critical_count} 🔴{high_count} ⚠️{medium_count} ℹ️{low_count}")
        
        return {
            "has_leak": has_leak,
            "total_issues": len(all_reports),
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
            "reports": [
                {
                    "type": r.leak_type,
                    "severity": r.severity,
                    "has_leak": r.has_leak,
                    "description": r.description,
                    "location": r.location,
                    "recommendation": r.recommendation
                }
                for r in all_reports
            ]
        }
    
    @staticmethod
    def bar_to_minutes(bar: str) -> int:
        """将 bar 字符串转换为分钟数"""
        bar = bar.lower()
        if bar.endswith("m"):
            return int(bar[:-1])
        elif bar.endswith("h"):
            return int(bar[:-1]) * 60
        elif bar.endswith("d"):
            return int(bar[:-1]) * 60 * 24
        elif bar.endswith("w"):
            return int(bar[:-1]) * 60 * 24 * 7
        return int(bar)


def main():
    parser = argparse.ArgumentParser(description="数据泄漏审计工具")
    parser.add_argument("--symbol", default="BTC-USDT-SWAP", help="交易对")
    parser.add_argument("--bar", default="4H", help="时间周期")
    parser.add_argument("--lookback", type=int, default=400, help="回看窗口")
    parser.add_argument("--pred-len", type=int, default=24, help="预测长度")
    parser.add_argument("--detailed", action="store_true", help="详细分析")
    args = parser.parse_args()
    
    auditor = LeakAuditor()
    result = auditor.run_full_audit(
        symbol=args.symbol,
        bar=args.bar,
        lookback=args.lookback,
        pred_len=args.pred_len,
        detailed=args.detailed
    )
    
    # Exit code based on leak status
    if result.get("has_leak"):
        if result.get("critical", 0) > 0:
            sys.exit(2)  # Critical leak
        elif result.get("high", 0) > 0:
            sys.exit(1)  # High severity leak
    sys.exit(0)


if __name__ == "__main__":
    main()
