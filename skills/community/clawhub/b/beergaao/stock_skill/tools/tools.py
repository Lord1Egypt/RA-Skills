"""Agent 工具层 - 15 个标准化工具 + 集成引擎 + ML + 因子分析 + 参数校准"""
from __future__ import annotations
import json, logging
from datetime import date, timedelta
from typing import Any, Dict, List, Optional
import pandas as pd, numpy as np

from ..config import get_config
from ..models import (BacktestResult, DragonTiger, MarketAnalysis, MarketTrend, MoneyFlow, ReviewReport, SectorFlow, SignalType, StockAnalysis, StockInfo, TradeSignal)
from ..providers.providers import DataGateway
from ..indicators import compute_all, latest_indicators, support_resistance
from ..strategies.strategies import get_all_strategies, RawSignal, StrategyCalibrator
from ..strategies.ensemble import EnsembleStrategyEngine, MarketRegime
from ..risk import RiskManager
from ..state import StateStore
from ..factors.base import FactorCombiner, get_factors_by_category, FactorResult
from ..factors.fundamental import FundamentalFactorSet
from ..factors.sentiment import SentimentFactorSet
from ..factors.enhanced_ic import EnhancedFactorAnalyzer

logger = logging.getLogger(__name__)

# 策略相关性分组：同组策略高度相关，计票时只取代表
_STRATEGY_FAMILIES = {
    "ma_family": {"ma_breakout", "double_ma", "volume_shrink"},
    "macd_family": {"macd_cross"},
    "boll_family": {"boll_squeeze"},
    "rsi_family": {"rsi_oversold"},
    "kdj_family": {"kdj_cross"},
    "vol_family": {"vol_price_divergence", "obv_trend"},
    "support_family": {"support_bounce"},
}


class StockTools:
    def __init__(self):
        self.cfg = get_config()
        self.gw = DataGateway()
        self.risk = RiskManager()
        self.state = StateStore()
        self.ensemble = EnsembleStrategyEngine()
        self._strategy_perf_weights: Dict[str, float] = {}
        self._ml_ensemble = None
        self._ml_trained = False
        self._calibrated = False
        self._last_perf_check = None
        self._ic_analyzer = EnhancedFactorAnalyzer()

    def get_quote(self, code: str) -> Dict[str, Any]:
        try:
            q = self.gw.get_realtime_quote(code)
            return {"tool":"get_quote","status":"success","data":q} if q else {"tool":"get_quote","status":"error","error":f"无法获取{code}"}
        except Exception as e: return {"tool":"get_quote","status":"error","error":str(e)}

    def analyze_stock(self, code: str) -> Dict[str, Any]:
        try:
            info = self.gw.get_stock_info(code)
            df = self.gw.get_kline(code, self.cfg.backtest_days)
            if df.empty:
                return {"tool": "analyze_stock", "status": "error", "error": f"{code} 数据为空"}

            df = compute_all(df)
            indicators = latest_indicators(df)
            support, resistance = support_resistance(df)

            # 0. 参数校准（首次运行时自动校准，结果缓存）
            cal_info = None
            if not self._calibrated:
                try:
                    cal_results = StrategyCalibrator.apply_calibrated(df)
                    if cal_results:
                        cal_info = {k: v["best_params"] for k, v in cal_results.items()}
                        logger.info(f"参数校准完成: {list(cal_info.keys())}")
                except Exception as e:
                    logger.debug(f"参数校准跳过: {e}")
                self._calibrated = True

            backtest = self._run_backtest(df)

            # 1. 传统策略信号（已校准参数）
            strategies = get_all_strategies()
            raw_signals = []
            for s in strategies:
                sig = s.evaluate(df)
                if sig is not None:
                    raw_signals.append(sig)

            # 2. 集成引擎信号（含市场状态检测 + 动态权重）
            ensemble_signal = self.ensemble.evaluate(df)

            # 3. ML策略信号
            ml_signal = self._get_ml_signal(df)

            # 4. 增强IC分析（评估因子质量）
            ic_report = self._analyze_factors_ic(df)

            # 5. 信号去冗余：同族策略只取最高置信度代表
            deduped_buy, deduped_sell = self._deduplicate_signals(raw_signals)

            # 6. 融合所有信号源，确定最终信号
            trade_signal = self._build_trade_signal(
                code=code, name=info.name, df=df,
                deduped_buy=deduped_buy, deduped_sell=deduped_sell,
                ensemble_signal=ensemble_signal, ml_signal=ml_signal,
                backtest=backtest, support=support, resistance=resistance,
                ic_report=ic_report,
            )

            if trade_signal:
                self.state.save_signal(trade_signal)
                # 自动触发绩效回填（每日最多一次）
                self._auto_performance_feedback()

            # 7. 构造返回数据
            ensemble_info = None
            if ensemble_signal:
                ensemble_info = {
                    "direction": ensemble_signal.direction,
                    "confidence": ensemble_signal.confidence,
                    "consensus": ensemble_signal.consensus_score,
                    "regime": ensemble_signal.regime.value,
                    "strategies_agreed": f"{ensemble_signal.strategies_agreed}/{ensemble_signal.total_strategies}",
                }

            ml_info = None
            if ml_signal:
                ml_info = {
                    "direction": ml_signal.direction,
                    "confidence": ml_signal.confidence,
                    "model": ml_signal.model_name,
                }

            return {"tool": "analyze_stock", "status": "success", "data": {
                "info": {"code": code, "name": info.name, "industry": info.industry},
                "indicators": indicators, "support": support, "resistance": resistance,
                "backtest": backtest.__dict__ if backtest else None,
                "raw_signals": [
                    {"strategy": s.strategy_name, "direction": s.direction,
                     "confidence": s.confidence, "reason": s.reason}
                    for s in raw_signals
                ],
                "ensemble": ensemble_info,
                "ml_signal": ml_info,
                "factor_ic": ic_report,
                "calibration": cal_info,
                "signal": trade_signal.to_dict() if trade_signal else None,
            }}
        except Exception as e:
            logger.error(f"analyze_stock失败: {e}", exc_info=True)
            return {"tool": "analyze_stock", "status": "error", "error": str(e)}

    def _deduplicate_signals(self, signals: List[RawSignal]):
        """信号去冗余：同族策略只保留置信度最高的一个"""
        buy_by_family: Dict[str, RawSignal] = {}
        sell_by_family: Dict[str, RawSignal] = {}

        family_lookup = {}
        for fam_name, members in _STRATEGY_FAMILIES.items():
            for m in members:
                family_lookup[m] = fam_name

        for sig in signals:
            family = family_lookup.get(sig.strategy_name, sig.strategy_name)
            if sig.direction == "BUY":
                if family not in buy_by_family or sig.confidence > buy_by_family[family].confidence:
                    buy_by_family[family] = sig
            elif sig.direction == "SELL":
                if family not in sell_by_family or sig.confidence > sell_by_family[family].confidence:
                    sell_by_family[family] = sig

        return list(buy_by_family.values()), list(sell_by_family.values())

    def _build_trade_signal(self, code, name, df, deduped_buy, deduped_sell,
                            ensemble_signal, ml_signal, backtest, support, resistance,
                            ic_report=None):
        """融合传统策略(去重后) + 集成引擎 + ML策略 + IC过滤，生成最终 TradeSignal"""
        last_price = float(df.iloc[-1]["close"])
        atr = float(df.iloc[-1].get("atr", 0))

        # 加载历史策略胜率用于动态调权
        perf_weights = self.state.get_signal_win_rate_by_strategy(days=90)

        # IC过滤：将因子质量映射为策略置信度调整系数
        ic_penalty = self._compute_ic_penalty(ic_report) if ic_report else {}

        # 计算加权买/卖分数（含IC惩罚）
        buy_score = 0.0
        sell_score = 0.0
        for sig in deduped_buy:
            w = perf_weights.get(sig.strategy_name, 0.5)
            ic_factor = ic_penalty.get(sig.strategy_name, 1.0)
            buy_score += sig.confidence * (0.5 + w) * ic_factor
        for sig in deduped_sell:
            w = perf_weights.get(sig.strategy_name, 0.5)
            ic_factor = ic_penalty.get(sig.strategy_name, 1.0)
            sell_score += sig.confidence * (0.5 + w) * ic_factor

        # 集成引擎信号作为独立投票源（权重 0.3）
        ensemble_buy = 0.0
        ensemble_sell = 0.0
        if ensemble_signal:
            ew = 0.3
            if ensemble_signal.direction == "BUY":
                ensemble_buy = ensemble_signal.confidence * ew
            elif ensemble_signal.direction == "SELL":
                ensemble_sell = ensemble_signal.confidence * ew

        # ML策略信号（权重 0.25）
        ml_buy = 0.0
        ml_sell = 0.0
        if ml_signal:
            mw = 0.25
            if ml_signal.direction == "BUY":
                ml_buy = ml_signal.confidence * mw
            elif ml_signal.direction == "SELL":
                ml_sell = ml_signal.confidence * mw

        total_buy = buy_score + ensemble_buy + ml_buy
        total_sell = sell_score + ensemble_sell + ml_sell

        # 无任何信号
        if total_buy == 0 and total_sell == 0:
            return None

        # 确定信号类型
        if total_sell > total_buy and total_sell > 0.3:
            adj_conf = min(total_sell / max(len(deduped_sell) + 1, 1), 0.95)
            sig_type = SignalType.SELL if adj_conf >= 0.5 else SignalType.HOLD
        elif total_buy > 0:
            adj_conf = min(total_buy / max(len(deduped_buy) + 1, 1), 0.95)
            bt_factor = backtest.win_rate / 0.5 if backtest and backtest.win_rate > 0 else 0.8
            adj_conf = round(max(0.0, min(1.0, adj_conf * bt_factor)), 2)
            sig_type = SignalType.BUY if adj_conf >= 0.6 else SignalType.WATCH if adj_conf >= 0.4 else SignalType.HOLD
        else:
            adj_conf = 0.0
            sig_type = SignalType.HOLD

        sl = self.risk.calculate_stop_loss(last_price, atr, support)
        tgt = self.risk.calculate_target(last_price, resistance, atr)
        pos = self.risk.calculate_position(adj_conf, 5.0, 1, atr, last_price)

        all_reasons = []
        if deduped_buy:
            all_reasons.append("[买入] " + " | ".join(s.reason for s in deduped_buy))
        if deduped_sell:
            all_reasons.append("[卖出] " + " | ".join(s.reason for s in deduped_sell))
        if ensemble_signal:
            all_reasons.append(f"[集成] {ensemble_signal.summary()}")
        if ml_signal:
            all_reasons.append(f"[ML] {ml_signal.model_name} {ml_signal.direction} conf={ml_signal.confidence:.2f}")

        all_strategy_names = [s.strategy_name for s in deduped_buy + deduped_sell]
        if ensemble_signal:
            all_strategy_names.append("ensemble")
        if ml_signal:
            all_strategy_names.append(ml_signal.model_name)

        return TradeSignal(
            code=code, name=name, signal_type=sig_type, price=round(last_price, 2),
            support=support, resistance=resistance, stop_loss=sl, target_price=tgt,
            position_pct=pos.position_pct if sig_type == SignalType.BUY else 0,
            confidence=adj_conf, reason=" | ".join(all_reasons),
            strategy_name="+".join(all_strategy_names),
            backtest_win_rate=backtest.win_rate if backtest else 0,
            atr=round(atr, 4),
        )

    def _get_ml_signal(self, df: pd.DataFrame):
        """获取ML策略信号（懒加载+持久化+增量训练）"""
        try:
            from ..strategies.ml_strategies import EnsembleMLStrategy
            if self._ml_ensemble is None:
                self._ml_ensemble = EnsembleMLStrategy()
                # 尝试加载已保存的模型
                if self._ml_ensemble.load_all():
                    self._ml_trained = True
                    logger.info("ML模型已从磁盘加载")
            if not self._ml_trained:
                if len(df) >= 200:
                    self._ml_ensemble.train(df, forward_periods=5, threshold=0.02)
                    self._ml_trained = True
                    self._ml_ensemble.save_all()
                    logger.info("ML策略训练完成并已保存")
                else:
                    return None
            return self._ml_ensemble.predict(df)
        except Exception as e:
            logger.debug(f"ML策略跳过: {e}")
            return None

    def _analyze_factors_ic(self, df: pd.DataFrame) -> Dict[str, Any]:
        """增强IC分析 - 评估各因子预测能力"""
        try:
            if len(df) < 60:
                return None

            close = df["close"].astype(float)
            forward_returns = close.shift(-5) / close - 1

            factor_candidates = {}
            for col in ["ma5", "ma10", "ma20", "rsi", "dif", "dea", "macd",
                         "k", "d", "boll_mid", "atr"]:
                if col in df.columns:
                    factor_candidates[col] = df[col].astype(float)

            if not factor_candidates:
                return None

            ic_results = {}
            for factor_name, factor_values in factor_candidates.items():
                aligned = pd.DataFrame({
                    "factor": factor_values,
                    "returns": forward_returns,
                }).dropna()

                if len(aligned) < 30:
                    continue

                ic_values = []
                for i in range(60, len(aligned)):
                    window = aligned.iloc[i - 60:i]
                    ic = window["factor"].corr(window["returns"], method="spearman")
                    if np.isfinite(ic):
                        ic_values.append(ic)

                if len(ic_values) >= 5:
                    ic_mean = float(np.mean(ic_values))
                    ic_std = float(np.std(ic_values))
                    ic_ir = ic_mean / ic_std if ic_std > 0 else 0
                    ic_results[factor_name] = {
                        "ic": round(ic_mean, 4),
                        "ic_ir": round(ic_ir, 2),
                        "significant": abs(ic_mean) > 0.02 and abs(ic_ir) > 0.3,
                    }

            return ic_results if ic_results else None
        except Exception as e:
            logger.debug(f"IC分析跳过: {e}")
            return None

    def _auto_performance_feedback(self):
        """自动绩效回填（每日最多一次）"""
        try:
            today = date.today().isoformat()
            if self._last_perf_check == today:
                return
            result = self.evaluate_signal_performance()
            self._last_perf_check = today
            updated = result.get("data", {}).get("updated", 0)
            if updated > 0:
                logger.info(f"自动绩效回填: {updated}条信号")
        except Exception as e:
            logger.debug(f"自动绩效回填跳过: {e}")

    # 策略→因子映射，用于IC质量惩罚
    _STRATEGY_FACTOR_MAP = {
        "ma_breakout": ["ma20", "ma5", "ma10"],
        "macd_cross": ["dif", "dea", "macd"],
        "boll_squeeze": ["boll_mid"],
        "rsi_oversold": ["rsi"],
        "kdj_cross": ["k", "d"],
        "volume_shrink": ["ma20", "ma5"],
        "vol_price_divergence": [],
        "obv_trend": [],
        "double_ma": ["ma5", "ma20"],
        "support_bounce": ["ma60"],
    }

    def _compute_ic_penalty(self, ic_report: Dict[str, Any]) -> Dict[str, float]:
        """根据IC分析结果计算策略置信度惩罚系数

        如果策略依赖的因子IC不显著，该策略的置信度乘以惩罚系数(0.6-1.0)
        """
        if not ic_report:
            return {}

        penalty = {}
        for strategy_name, factors in self._STRATEGY_FACTOR_MAP.items():
            if not factors:
                penalty[strategy_name] = 1.0
                continue

            significant_count = 0
            total_count = 0
            for factor in factors:
                if factor in ic_report:
                    total_count += 1
                    if ic_report[factor].get("significant", False):
                        significant_count += 1

            if total_count == 0:
                penalty[strategy_name] = 1.0
            elif significant_count == 0:
                penalty[strategy_name] = 0.6
            elif significant_count < total_count:
                penalty[strategy_name] = 0.8
            else:
                penalty[strategy_name] = 1.0

        return penalty

    def strategy_attribution(self, code: str = None, days: int = 30) -> Dict[str, Any]:
        """策略归因分析 - 追踪收益来源到具体策略/因子"""
        try:
            perf = self.state.get_strategy_performance(days=days)
            if not perf:
                return {"tool": "strategy_attribution", "status": "success",
                        "data": {"message": "暂无足够绩效数据"}}

            attributions = []
            for p in perf:
                total = p.get("total", 0)
                if total < 3:
                    continue
                wins = p.get("wins", 0)
                avg_ret = p.get("avg_ret_5d", 0) or 0
                target_hits = p.get("target_hits", 0)
                stop_hits = p.get("stop_hits", 0)

                win_rate = wins / total if total > 0 else 0
                profit_factor = (target_hits / stop_hits) if stop_hits > 0 else (
                    target_hits * 1.0 if target_hits > 0 else 0)

                attributions.append({
                    "strategy": p["strategy_name"],
                    "signals": total,
                    "win_rate": round(win_rate, 3),
                    "avg_return_5d": round(avg_ret, 4),
                    "target_hits": target_hits,
                    "stop_hits": stop_hits,
                    "profit_factor": round(profit_factor, 2),
                    "contribution": round(win_rate * avg_ret * total, 4),
                })

            attributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)

            return {"tool": "strategy_attribution", "status": "success",
                    "data": {"attributions": attributions, "period_days": days}}
        except Exception as e:
            return {"tool": "strategy_attribution", "status": "error", "error": str(e)}

    def evaluate_signal_performance(self) -> Dict[str, Any]:
        """回填历史信号的实际收益，用于策略权重反馈"""
        pending = self.state.get_pending_performance_checks(days_back=10)
        updated = 0
        for record in pending:
            try:
                code = record["code"]
                entry_price = record["entry_price"]
                signal_date = record["signal_date"]
                df = self.gw.get_kline(code, 20)
                if df.empty:
                    continue

                # 找到信号日期对应的行
                df["date_str"] = df["date"].astype(str)
                signal_idx = df[df["date_str"] == signal_date].index
                if len(signal_idx) == 0:
                    continue
                idx = signal_idx[0]

                returns = {}
                for period, label in [(1, "1d"), (3, "3d"), (5, "5d"), (10, "10d")]:
                    if idx + period < len(df):
                        close_after = float(df.iloc[idx + period]["close"])
                        returns[label] = (close_after - entry_price) / entry_price
                    else:
                        returns[label] = 0.0

                # 判断是否触发止损/止盈
                hit_stop = False
                hit_target = False
                for j in range(1, min(11, len(df) - idx)):
                    day_low = float(df.iloc[idx + j]["low"])
                    day_high = float(df.iloc[idx + j]["high"])
                    if (day_low - entry_price) / entry_price <= self.cfg.stop_loss_rate:
                        hit_stop = True
                    if (day_high - entry_price) / entry_price >= self.cfg.target_rate:
                        hit_target = True

                self.state.save_signal_performance(
                    signal_id=record["id"], code=code, signal_date=signal_date,
                    signal_type=record["signal_type"], entry_price=entry_price,
                    strategy_name=record["strategy_name"], returns=returns,
                    hit_target=hit_target, hit_stop=hit_stop,
                )
                updated += 1
            except Exception as e:
                logger.debug(f"回填信号绩效失败 {record}: {e}")

        # 刷新集成引擎的策略权重
        perf_weights = self.state.get_signal_win_rate_by_strategy(days=90)
        for strat_name, win_rate in perf_weights.items():
            self.ensemble.weight_optimizer.update_performance(strat_name, win_rate - 0.5)
        self._strategy_perf_weights = perf_weights

        return {"tool": "evaluate_signal_performance", "status": "success",
                "data": {"updated": updated, "total_pending": len(pending),
                         "strategy_weights": perf_weights}}

    def get_money_flow(self, code):
        try:
            f = self.gw.get_money_flow(code)
            if f:
                return {"tool": "get_money_flow", "status": "success", "data": f.to_dict()}
            return {"tool": "get_money_flow", "status": "error", "error": "无数据"}
        except Exception as e:
            return {"tool": "get_money_flow", "status": "error", "error": str(e)}

    def analyze_market(self):
        try:
            today = date.today().strftime("%Y%m%d")
            df = self.gw.get_market_snapshot(today)
            if df.empty:
                return {"tool": "analyze_market", "status": "error", "error": "无数据"}

            up = int((df["change"] > 0).sum())
            down = int((df["change"] < 0).sum())
            total = len(df)
            limit_up = int((df["pct_chg"] >= 9.5).sum())
            limit_down = int((df["pct_chg"] <= -9.5).sum())

            score = round(up / total * 10, 1) if total > 0 else 5.0
            if limit_up > 10:
                score = min(10, score + 0.5)
            if limit_down > 10:
                score = max(0, score - 0.5)

            if score >= 8:
                trend = MarketTrend.STRONG_UP
            elif score >= 6:
                trend = MarketTrend.WEAK_UP
            elif score >= 4:
                trend = MarketTrend.SIDEWAYS
            elif score >= 2:
                trend = MarketTrend.WEAK_DOWN
            else:
                trend = MarketTrend.STRONG_DOWN

            advice_map = {
                MarketTrend.STRONG_UP: "强势，可加仓",
                MarketTrend.WEAK_UP: "偏强，可低吸",
                MarketTrend.SIDEWAYS: "震荡，轻仓观望",
                MarketTrend.WEAK_DOWN: "偏弱，控制仓位",
                MarketTrend.STRONG_DOWN: "弱势，空仓观望",
            }

            market = MarketAnalysis(
                trend=trend, score=score,
                up_count=up, down_count=down, total_count=total,
                limit_up=limit_up, limit_down=limit_down,
                advice=advice_map[trend],
            )
            return {"tool": "analyze_market", "status": "success", "data": market.to_dict()}
        except Exception as e:
            return {"tool": "analyze_market", "status": "error", "error": str(e)}

    def get_sector_flow(self, limit=10):
        try:
            sectors = self.gw.get_sector_flow(limit)
            data = [
                {"name": s.sector_name, "change_pct": s.change_pct, "main_net_inflow": s.main_net_inflow}
                for s in sectors
            ]
            return {"tool": "get_sector_flow", "status": "success", "data": data}
        except Exception as e:
            return {"tool": "get_sector_flow", "status": "error", "error": str(e)}

    def get_dragon_tiger(self):
        try:
            items = self.gw.get_dragon_tiger()
            data = [
                {"code": d.code, "name": d.name, "close": d.close,
                 "pct_change": d.pct_change, "net_amount": d.net_amount,
                 "buy_amount": d.buy_amount, "sell_amount": d.sell_amount,
                 "reason": d.reason}
                for d in items
            ]
            return {"tool": "get_dragon_tiger", "status": "success", "data": data}
        except Exception as e:
            return {"tool": "get_dragon_tiger", "status": "error", "error": str(e)}

    def get_positions(self):
        return {"tool":"get_positions","status":"success","data":self.state.get_open_positions()}

    def add_position(self, code, price, shares, stop_loss, target):
        info = self.gw.get_stock_info(code)
        self.state.save_position(code, info.name, price, shares, stop_loss, target)
        return {"tool":"add_position","status":"success","message":f"已记录 {info.name} 持仓"}

    def close_position(self, code):
        self.state.close_position(code)
        return {"tool":"close_position","status":"success","message":f"{code} 已平仓"}

    def get_signal_history(self, code=None, days=30):
        start = (date.today() - timedelta(days=days)).isoformat()
        signals = self.state.get_signals(code=code, start_date=start)
        stats = self.state.get_signal_stats(days)
        return {"tool": "get_signal_history", "status": "success", "data": {"signals": signals, "stats": stats}}

    def get_market_breadth(self):
        try:
            today = date.today().strftime("%Y%m%d")
            df = self.gw.get_market_snapshot(today)
            if df.empty:
                return {"tool": "get_market_breadth", "status": "error", "error": "无数据"}

            up = int((df["change"] > 0).sum())
            down = int((df["change"] < 0).sum())
            flat = int((df["change"] == 0).sum())
            limit_up = int((df["pct_chg"] >= 9.5).sum())
            limit_down = int((df["pct_chg"] <= -9.5).sum())

            ad_ratio = round(up / down, 2) if down > 0 else 99.9
            profit_effect = round(up / (up + down) * 100, 1) if (up + down) > 0 else 50

            if ad_ratio > 2:
                breadth_signal = "强"
            elif ad_ratio < 0.5:
                breadth_signal = "弱"
            else:
                breadth_signal = "中性"

            return {"tool": "get_market_breadth", "status": "success", "data": {
                "up": up, "down": down, "flat": flat,
                "limit_up": limit_up, "limit_down": limit_down,
                "ad_ratio": ad_ratio, "profit_effect": profit_effect,
                "breadth_signal": breadth_signal,
            }}
        except Exception as e:
            return {"tool": "get_market_breadth", "status": "error", "error": str(e)}

    def check_correlation(self, codes):
        try:
            returns = {}
            for code in codes:
                df = self.gw.get_kline(code, 60)
                if not df.empty and "close" in df.columns:
                    returns[code] = df["close"].pct_change().dropna().values
            if len(returns) < 2:
                return {"tool": "check_correlation", "status": "error", "error": "数据不足"}

            min_len = min(len(v) for v in returns.values())
            aligned = np.array([returns[c][-min_len:] for c in returns])
            corr = np.corrcoef(aligned)
            code_list = list(returns.keys())

            warnings = []
            for i in range(len(code_list)):
                for j in range(i + 1, len(code_list)):
                    if corr[i][j] > self.cfg.correlation_threshold:
                        warnings.append(f"{code_list[i]} 与 {code_list[j]} 相关性 {corr[i][j]:.2f}")

            return {"tool": "check_correlation", "status": "success", "data": {
                "codes": code_list, "correlation_matrix": corr.tolist(), "warnings": warnings,
            }}
        except Exception as e:
            return {"tool": "check_correlation", "status": "error", "error": str(e)}

    def circuit_breaker_check(self):
        try:
            m = self.analyze_market()
            if m.get("status") != "success":
                return {"tool": "circuit_breaker_check", "status": "error", "error": "无数据"}

            d = m["data"]
            market = MarketAnalysis(
                trend=MarketTrend(d["trend"]), score=d["score"],
                up_count=d["up_count"], down_count=d["down_count"],
                total_count=d["total_count"], limit_up=d["limit_up"], limit_down=d["limit_down"],
            )
            triggered, triggers = self.risk.circuit_breaker(market)

            return {"tool": "circuit_breaker_check", "status": "success", "data": {
                "triggered": triggered, "triggers": triggers,
                "advice": "熔断触发！建议清仓" if triggered else "市场正常",
            }}
        except Exception as e:
            return {"tool": "circuit_breaker_check", "status": "error", "error": str(e)}

    def full_review(self, watchlist=None):
        codes = watchlist or self.cfg.default_watchlist
        today = date.today().isoformat()
        market_result = self.analyze_market()
        md = market_result.get("data", {})
        stock_analyses = []

        for code in codes:
            result = self.analyze_stock(code)
            if result.get("status") != "success":
                continue

            data = result["data"]
            info = StockInfo(**data["info"])

            sig = None
            if data.get("signal"):
                d = data["signal"]
                sig = TradeSignal(
                    code=d["code"], name=d["name"],
                    signal_type=SignalType(d["signal_type"]), price=d["price"],
                    support=d["support"], resistance=d["resistance"],
                    stop_loss=d["stop_loss"], target_price=d["target_price"],
                    position_pct=d["position_pct"], confidence=d["confidence"],
                    reason=d["reason"], strategy_name=d.get("strategy_name", ""),
                    backtest_win_rate=d.get("backtest_win_rate", 0), atr=d.get("atr", 0),
                )

            mf = None
            fr = self.get_money_flow(code)
            if fr.get("status") == "success":
                mf = MoneyFlow(**fr["data"])

            bt = BacktestResult(**data["backtest"]) if data.get("backtest") else None
            stock_analyses.append(StockAnalysis(
                info=info, signal=sig, money_flow=mf, backtest=bt,
                indicators=data.get("indicators", {}),
            ))

        sectors_data = self.get_sector_flow()
        sectors = [SectorFlow(**s) for s in sectors_data.get("data", [])]
        dt_data = self.get_dragon_tiger()
        dragon_tiger = [DragonTiger(**d) for d in dt_data.get("data", [])]

        market_analysis = MarketAnalysis(
            trend=MarketTrend(md.get("trend", "横盘震荡")),
            score=md.get("score", 5.0),
            up_count=md.get("up_count", 0), down_count=md.get("down_count", 0),
            total_count=md.get("total_count", 0),
            limit_up=md.get("limit_up", 0), limit_down=md.get("limit_down", 0),
            advice=md.get("advice", ""),
        )

        report = ReviewReport(
            date=today, market=market_analysis, stocks=stock_analyses,
            sectors=sectors, dragon_tiger=dragon_tiger,
        )
        self.state.save_report(report.to_json())
        return {"tool": "full_review", "status": "success", "data": report.to_dict(), "summary": report.summary()}

    def _run_backtest(self, df):
        if len(df) < 125:
            return None
        buy_cost = self.cfg.commission_rate + self.cfg.slippage_rate
        sell_cost = self.cfg.commission_rate + self.cfg.stamp_tax_rate + self.cfg.slippage_rate
        total_cost = buy_cost + sell_cost
        trades = []
        strategies = get_all_strategies()
        hold_days = self.cfg.hold_days

        for i in range(120, len(df) - hold_days):
            sub = df.iloc[:i + 1]
            if len(sub) < 25:
                continue
            has_buy = False
            for s in strategies:
                sig = s.evaluate(sub)
                if sig and sig.direction == "BUY":
                    has_buy = True
                    break
            if not has_buy:
                continue

            entry = float(df.iloc[i]["close"])
            prev_close = float(df.iloc[i - 1]["close"])
            if (entry - prev_close) / prev_close >= 0.095:
                continue

            ret = 0.0
            for d in range(1, hold_days + 1):
                if i + d >= len(df):
                    break
                day_high = float(df.iloc[i + d]["high"])
                day_low = float(df.iloc[i + d]["low"])
                day_close = float(df.iloc[i + d]["close"])

                if d == 1 and (day_low - prev_close) / prev_close <= -0.095:
                    break

                if (day_low - entry) / entry <= self.cfg.stop_loss_rate:
                    ret = self.cfg.stop_loss_rate - total_cost
                    break
                if (day_high - entry) / entry >= self.cfg.target_rate:
                    ret = self.cfg.target_rate - total_cost
                    break
                if d == hold_days:
                    ret = (day_close - entry) / entry - total_cost
            trades.append(ret)

        if not trades:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        wins = sum(1 for r in trades if r > 0)
        losses = sum(1 for r in trades if r < 0)
        total = len(trades)
        avg_ret = float(np.mean(trades))
        cum = np.cumprod(1 + np.array(trades))
        peak = np.maximum.accumulate(cum)
        dd = (peak - cum) / peak
        max_dd = float(np.max(dd)) if len(dd) > 0 else 0
        sharpe = avg_ret / float(np.std(trades)) * np.sqrt(252 / hold_days) if np.std(trades) > 0 else 0
        gross_profit = sum(r for r in trades if r > 0)
        gross_loss = abs(sum(r for r in trades if r < 0))
        pf = gross_profit / gross_loss if gross_loss > 0 else float("inf")
        return BacktestResult(total, wins, losses, total - wins - losses, round(wins / total, 2),
                              round(losses / total, 2), round(avg_ret, 4), round(max_dd, 4),
                              round(sharpe, 2), round(pf, 2))

    def backtest_bt(self, code: str, strategy_name: str = 'MAStrategy',
                    start_date: str = '', end_date: str = '',
                    cash: float = 100000.0) -> Dict[str, Any]:
        """使用 Backtrader 引擎进行回测

        Args:
            code: 股票代码，如 "600036.SH"
            strategy_name: 策略名称，如 "MAStrategy", "MACDStrategy", "RSIMeanReversionStrategy"
            start_date: 开始日期 "YYYY-MM-DD"，默认为 1 年前
            end_date: 结束日期 "YYYY-MM-DD"，默认为今天
            cash: 初始资金

        Returns:
            回测结果字典
        """
        try:
            from ..backtest.backtrader_engine import BacktraderBacktest, BacktraderConfig
            from ..strategies.backtrader_adapters import get_bt_strategy, list_bt_strategies

            # 获取策略类
            strategy_cls = get_bt_strategy(strategy_name)
            if not strategy_cls:
                available = list_bt_strategies()
                return {
                    "tool": "backtest_bt",
                    "status": "error",
                    "error": f"未知策略: {strategy_name}，可用策略: {available}"
                }

            # 设置日期范围
            if not end_date:
                end_date = date.today().strftime("%Y-%m-%d")
            if not start_date:
                start_date = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")

            # 获取数据
            days = (date.today() - date.fromisoformat(start_date)).days + 30
            df = self.gw.get_kline(code, days=days)
            if df.empty:
                return {"tool": "backtest_bt", "status": "error", "error": f"{code} 数据为空"}

            # 过滤日期范围
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

            if df.empty:
                return {"tool": "backtest_bt", "status": "error", "error": "指定日期范围内无数据"}

            # 配置回测引擎
            config = BacktraderConfig(
                initial_capital=cash,
                commission=self.cfg.commission_rate,
                stop_loss_pct=abs(self.cfg.stop_loss_rate),
                take_profit_pct=self.cfg.target_rate,
                max_position_pct=self.cfg.max_single_position,
            )

            # 运行回测
            engine = BacktraderBacktest(config)
            engine.load_data(df, name=code)
            engine.add_strategy(strategy_cls)
            engine.add_default_analyzers()
            results = engine.run()

            return {
                "tool": "backtest_bt",
                "status": "success",
                "data": {
                    "code": code,
                    "strategy": strategy_name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "initial_capital": results['initial_capital'],
                    "final_capital": round(results['final_capital'], 2),
                    "total_return": round(results['total_return'] * 100, 2),
                    "annual_return": round(results['annual_return'] * 100, 2),
                    "max_drawdown": round(results['max_drawdown'] * 100, 2),
                    "sharpe_ratio": round(results['sharpe_ratio'], 2),
                    "win_rate": round(results['win_rate'] * 100, 2),
                    "profit_factor": round(results['profit_factor'], 2),
                    "total_trades": results['total_trades'],
                    "won_trades": results['won_trades'],
                    "lost_trades": results['lost_trades'],
                }
            }

        except Exception as e:
            logger.error(f"Backtrader 回测失败: {e}")
            return {"tool": "backtest_bt", "status": "error", "error": str(e)}


TOOL_SCHEMAS = [
    {"name":"get_quote","description":"获取实时行情","parameters":{"type":"object","properties":{"code":{"type":"string"}},"required":["code"]}},
    {"name":"analyze_stock","description":"完整技术分析（含集成引擎+多因子+回测）","parameters":{"type":"object","properties":{"code":{"type":"string"}},"required":["code"]}},
    {"name":"get_money_flow","description":"获取资金流向","parameters":{"type":"object","properties":{"code":{"type":"string"}},"required":["code"]}},
    {"name":"analyze_market","description":"分析大盘环境","parameters":{"type":"object","properties":{}}},
    {"name":"get_sector_flow","description":"板块资金排名","parameters":{"type":"object","properties":{"limit":{"type":"integer","default":10}}}},
    {"name":"get_dragon_tiger","description":"龙虎榜数据","parameters":{"type":"object","properties":{}}},
    {"name":"get_positions","description":"查询持仓","parameters":{"type":"object","properties":{}}},
    {"name":"add_position","description":"添加持仓","parameters":{"type":"object","properties":{"code":{"type":"string"},"price":{"type":"number"},"shares":{"type":"integer"},"stop_loss":{"type":"number"},"target":{"type":"number"}},"required":["code","price","shares","stop_loss","target"]}},
    {"name":"close_position","description":"平仓","parameters":{"type":"object","properties":{"code":{"type":"string"}},"required":["code"]}},
    {"name":"get_signal_history","description":"历史信号","parameters":{"type":"object","properties":{"code":{"type":"string"},"days":{"type":"integer","default":30}}}},
    {"name":"full_review","description":"完整复盘","parameters":{"type":"object","properties":{"watchlist":{"type":"array","items":{"type":"string"}}}}},
    {"name":"get_market_breadth","description":"市场广度指标","parameters":{"type":"object","properties":{}}},
    {"name":"check_correlation","description":"相关性检查","parameters":{"type":"object","properties":{"codes":{"type":"array","items":{"type":"string"}}},"required":["codes"]}},
    {"name":"circuit_breaker_check","description":"熔断检查","parameters":{"type":"object","properties":{}}},
    {"name":"evaluate_signal_performance","description":"回填信号绩效+刷新策略权重","parameters":{"type":"object","properties":{}}},
    {"name":"strategy_attribution","description":"策略归因分析-追踪收益来源","parameters":{"type":"object","properties":{"days":{"type":"integer","default":30}}}},
]
