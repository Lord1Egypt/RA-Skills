#!/usr/bin/env python3
# coding:utf-8

"""
行为金融策略技能 v1.0.0
识别和利用认知偏差、情绪极端和群体行为进行逆向交易
"""

import sys
import json
import datetime
import math
import statistics
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timedelta

class BehavioralFinanceStrategy:
    """行为金融策略核心类"""
    
    def __init__(self):
        # 行为模式定义
        self.behavioral_patterns = {
            "overreaction": {
                "name": "过度反应",
                "description": "价格变动超过基本面变动",
                "typical_duration": "3-10个交易日",
                "reversal_probability": 0.68,
                "avg_reversal_magnitude": 0.045
            },
            "herding": {
                "name": "羊群效应",
                "description": "投资者盲目跟随他人行为",
                "typical_duration": "5-15个交易日",
                "reversal_probability": 0.62,
                "avg_reversal_magnitude": 0.052
            },
            "anchoring": {
                "name": "锚定效应",
                "description": "过度依赖历史价格作为参考",
                "typical_duration": "持续型",
                "reversal_probability": 0.55,
                "avg_reversal_magnitude": 0.038
            },
            "disposition_effect": {
                "name": "处置效应",
                "description": "过早卖出盈利股，持有亏损股过久",
                "typical_duration": "1-5个交易日",
                "reversal_probability": 0.60,
                "avg_reversal_magnitude": 0.028
            },
            "extreme_sentiment": {
                "name": "情绪极端",
                "description": "市场情绪过度乐观或悲观",
                "typical_duration": "2-8个交易日",
                "reversal_probability": 0.72,
                "avg_reversal_magnitude": 0.058
            }
        }
        
        # 情绪指标权重
        self.sentiment_weights = {
            "price_momentum": 0.25,
            "volume_anomaly": 0.20,
            "retail_sentiment": 0.15,
            "institutional_flow": 0.20,
            "news_sentiment": 0.10,
            "social_media_buzz": 0.10
        }
        
        # 行业情绪基准（模拟数据）
        self.sector_sentiment_baseline = {
            "半导体": 0.55,
            "消费电子": 0.50,
            "能源化工": 0.45,
            "造纸印刷": 0.48,
            "汽车": 0.52,
            "计算机": 0.58
        }
        
        # 历史模式数据库（模拟）
        self.historical_patterns_db = self._init_historical_patterns()
        
        # 股票-行业映射
        self.stock_sector_map = {
            "002371.SZ": "半导体",
            "002384.SZ": "消费电子",
            "000723.SZ": "能源化工",
            "002078.SZ": "造纸印刷",
            "002594.SZ": "汽车",
            "002230.SZ": "计算机",
            "603019.SH": "计算机"
        }
    
    def _init_historical_patterns(self) -> Dict:
        """初始化历史模式数据库"""
        return {
            "overreaction_examples": [
                {"stock": "002371.SZ", "date": "2026-02-28", "pattern": "overreaction", 
                 "reversal_magnitude": 0.062, "duration": 4},
                {"stock": "002384.SZ", "date": "2026-02-25", "pattern": "overreaction",
                 "reversal_magnitude": 0.045, "duration": 3},
                {"stock": "000723.SZ", "date": "2026-02-20", "pattern": "overreaction",
                 "reversal_magnitude": 0.038, "duration": 5}
            ],
            "herding_examples": [
                {"stock": "002594.SZ", "date": "2026-02-22", "pattern": "herding",
                 "reversal_magnitude": 0.071, "duration": 6},
                {"stock": "603019.SH", "date": "2026-02-18", "pattern": "herding",
                 "reversal_magnitude": 0.055, "duration": 7}
            ],
            "extreme_sentiment_examples": [
                {"stock": "002371.SZ", "date": "2026-02-15", "pattern": "extreme_sentiment",
                 "reversal_magnitude": 0.082, "duration": 4},
                {"stock": "002078.SZ", "date": "2026-02-10", "pattern": "extreme_sentiment",
                 "reversal_magnitude": 0.048, "duration": 3}
            ]
        }
    
    def execute(self, params: Dict) -> Dict:
        """执行行为金融策略操作"""
        action = params.get("action", "detect_behavioral_patterns")
        
        if action == "detect_behavioral_patterns":
            return self.detect_behavioral_patterns(params)
        elif action == "quantify_market_sentiment":
            return self.quantify_market_sentiment(params)
        elif action == "identify_extreme_sentiment":
            return self.identify_extreme_sentiment(params)
        elif action == "generate_contrarian_signals":
            return self.generate_contrarian_signals(params)
        elif action == "monitor_herding_behavior":
            return self.monitor_herding_behavior(params)
        elif action == "backtest_behavioral_strategies":
            return self.backtest_behavioral_strategies(params)
        else:
            return self._error_response(f"未知操作: {action}")
    
    def detect_behavioral_patterns(self, params: Dict) -> Dict:
        """检测行为金融模式"""
        stock_codes = params.get("stock_codes", [])
        timeframe = params.get("timeframe", "recent_30_days")
        pattern_types = params.get("pattern_types", ["overreaction", "herding", "extreme_sentiment"])
        
        if not stock_codes:
            return self._error_response("需要至少一个股票代码")
        
        all_detections = []
        
        for stock_code in stock_codes:
            stock_detections = []
            
            for pattern_type in pattern_types:
                if pattern_type not in self.behavioral_patterns:
                    continue
                
                # 检测该行为模式
                detection = self._detect_single_pattern(stock_code, pattern_type, timeframe)
                if detection and detection.get("confidence", 0) > 0.5:
                    stock_detections.append(detection)
            
            if stock_detections:
                # 计算股票综合行为分数
                behavioral_score = self._calculate_behavioral_score(stock_detections)
                
                all_detections.append({
                    "stock": stock_code,
                    "sector": self.stock_sector_map.get(stock_code, "未知"),
                    "behavioral_score": behavioral_score,
                    "detected_patterns": stock_detections,
                    "primary_pattern": max(stock_detections, key=lambda x: x["confidence"]) if stock_detections else None,
                    "trading_implications": self._generate_trading_implications(stock_detections)
                })
        
        # 按行为分数排序
        all_detections.sort(key=lambda x: x["behavioral_score"], reverse=True)
        
        result = {
            "analysis_period": timeframe,
            "stocks_analyzed": len(stock_codes),
            "patterns_detected": sum(len(d["detected_patterns"]) for d in all_detections),
            "high_confidence_detections": [d for d in all_detections if d["behavioral_score"] >= 6.0],
            "all_detections": all_detections,
            "market_context": self._analyze_market_context(stock_codes, pattern_types),
            "recommended_actions": self._generate_recommended_actions(all_detections)
        }
        
        return self._success_response("detect_behavioral_patterns", result, params)
    
    def quantify_market_sentiment(self, params: Dict) -> Dict:
        """量化市场情绪"""
        stock_codes = params.get("stock_codes", [])
        include_breakdown = params.get("include_breakdown", True)
        
        if not stock_codes:
            # 使用默认持仓股票
            stock_codes = list(self.stock_sector_map.keys())
        
        sentiment_results = []
        
        for stock_code in stock_codes:
            sentiment = self._calculate_stock_sentiment(stock_code)
            
            result = {
                "stock": stock_code,
                "sector": self.stock_sector_map.get(stock_code, "未知"),
                "overall_sentiment": sentiment["overall"],
                "sentiment_category": self._categorize_sentiment(sentiment["overall"]),
                "sentiment_trend": self._assess_sentiment_trend(stock_code),
                "relative_to_sector": sentiment["overall"] - self.sector_sentiment_baseline.get(
                    self.stock_sector_map.get(stock_code, "未知"), 0.5
                )
            }
            
            if include_breakdown:
                result["sentiment_breakdown"] = sentiment["breakdown"]
                result["key_drivers"] = sentiment["key_drivers"]
            
            sentiment_results.append(result)
        
        # 按情绪极端度排序
        sentiment_results.sort(key=lambda x: abs(x["overall_sentiment"] - 0.5), reverse=True)
        
        # 市场整体情绪
        market_sentiment = statistics.mean([r["overall_sentiment"] for r in sentiment_results]) if sentiment_results else 0.5
        
        result = {
            "market_overview": {
                "average_sentiment": market_sentiment,
                "sentiment_category": self._categorize_sentiment(market_sentiment),
                "bullish_stocks": len([r for r in sentiment_results if r["overall_sentiment"] > 0.6]),
                "bearish_stocks": len([r for r in sentiment_results if r["overall_sentiment"] < 0.4]),
                "neutral_stocks": len([r for r in sentiment_results if 0.4 <= r["overall_sentiment"] <= 0.6])
            },
            "sector_sentiment": self._calculate_sector_sentiment(sentiment_results),
            "extreme_sentiment_stocks": [r for r in sentiment_results if abs(r["overall_sentiment"] - 0.5) > 0.2],
            "sentiment_reversal_candidates": [r for r in sentiment_results if self._is_reversal_candidate(r)],
            "detailed_sentiment": sentiment_results,
            "trading_insights": self._generate_sentiment_insights(sentiment_results)
        }
        
        return self._success_response("quantify_market_sentiment", result, params)
    
    def identify_extreme_sentiment(self, params: Dict) -> Dict:
        """识别情绪极端点"""
        stock_codes = params.get("stock_codes", [])
        threshold = params.get("threshold", 0.25)  # 偏离历史均值25%以上
        
        if not stock_codes:
            stock_codes = list(self.stock_sector_map.keys())
        
        extreme_candidates = []
        
        for stock_code in stock_codes:
            sentiment = self._calculate_stock_sentiment(stock_code)
            overall = sentiment["overall"]
            
            # 计算历史偏差（简化）
            sector = self.stock_sector_map.get(stock_code, "未知")
            sector_baseline = self.sector_sentiment_baseline.get(sector, 0.5)
            deviation = abs(overall - sector_baseline) / sector_baseline if sector_baseline != 0 else 0
            
            if deviation >= threshold:
                candidate = {
                    "stock": stock_code,
                    "sector": sector,
                    "current_sentiment": overall,
                    "sector_baseline": sector_baseline,
                    "deviation_pct": deviation * 100,
                    "direction": "过度乐观" if overall > sector_baseline else "过度悲观",
                    "expected_reversal_magnitude": min(0.15, deviation * 0.3),  # 预期回归幅度
                    "reversal_probability": min(0.8, 0.5 + deviation * 0.6),
                    "risk_level": self._assess_extreme_sentiment_risk(deviation, overall),
                    "monitoring_points": self._generate_extreme_monitoring_points(stock_code, overall > sector_baseline)
                }
                
                extreme_candidates.append(candidate)
        
        # 按偏差程度排序
        extreme_candidates.sort(key=lambda x: x["deviation_pct"], reverse=True)
        
        result = {
            "extreme_threshold": f">{threshold*100}% 偏离",
            "total_extreme_candidates": len(extreme_candidates),
            "most_extreme": extreme_candidates[0] if extreme_candidates else None,
            "extreme_optimism": [c for c in extreme_candidates if c["direction"] == "过度乐观"],
            "extreme_pessimism": [c for c in extreme_candidates if c["direction"] == "过度悲观"],
            "all_candidates": extreme_candidates,
            "market_implications": self._analyze_extreme_implications(extreme_candidates),
            "trading_strategies": self._generate_extreme_trading_strategies(extreme_candidates)
        }
        
        return self._success_response("identify_extreme_sentiment", result, params)
    
    def generate_contrarian_signals(self, params: Dict) -> Dict:
        """生成逆向交易信号"""
        stock_codes = params.get("stock_codes", [])
        signal_types = params.get("signal_types", ["overreaction", "extreme_sentiment", "herding"])
        min_confidence = params.get("min_confidence", 0.6)
        
        if not stock_codes:
            stock_codes = list(self.stock_sector_map.keys())
        
        all_signals = []
        
        for stock_code in stock_codes:
            stock_signals = []
            
            for signal_type in signal_types:
                # 检测行为模式
                detection = self._detect_single_pattern(stock_code, signal_type, "recent_10_days")
                if not detection or detection.get("confidence", 0) < min_confidence:
                    continue
                
                # 生成交易信号
                signal = self._generate_contrarian_signal(stock_code, detection)
                if signal:
                    stock_signals.append(signal)
            
            if stock_signals:
                # 选择最佳信号
                best_signal = max(stock_signals, key=lambda x: x["signal_strength"])
                
                all_signals.append({
                    "stock": stock_code,
                    "sector": self.stock_sector_map.get(stock_code, "未知"),
                    "best_signal": best_signal,
                    "all_signals": stock_signals,
                    "composite_score": self._calculate_composite_signal_score(stock_signals)
                })
        
        # 按信号强度排序
        all_signals.sort(key=lambda x: x["composite_score"], reverse=True)
        
        # 生成投资组合建议
        portfolio_signals = self._optimize_signal_portfolio(all_signals, params.get("capital_available", 100000))
        
        result = {
            "signals_generated": len(all_signals),
            "high_confidence_signals": [s for s in all_signals if s["composite_score"] >= 7.0],
            "all_signals": all_signals,
            "portfolio_recommendation": portfolio_signals,
            "risk_assessment": self._assess_signal_portfolio_risk(portfolio_signals),
            "execution_plan": self._generate_contrarian_execution_plan(portfolio_signals)
        }
        
        return self._success_response("generate_contrarian_signals", result, params)
    
    def monitor_herding_behavior(self, params: Dict) -> Dict:
        """监控羊群效应"""
        stock_codes = params.get("stock_codes", [])
        sector_focus = params.get("sector_focus", [])
        
        if not stock_codes:
            stock_codes = list(self.stock_sector_map.keys())
        
        # 过滤行业
        if sector_focus:
            stock_codes = [s for s in stock_codes if self.stock_sector_map.get(s, "未知") in sector_focus]
        
        herding_results = []
        
        for stock_code in stock_codes:
            herding_analysis = self._analyze_herding_behavior(stock_code)
            if herding_analysis["herding_score"] > 0.5:
                herding_results.append(herding_analysis)
        
        # 按羊群强度排序
        herding_results.sort(key=lambda x: x["herding_score"], reverse=True)
        
        result = {
            "herding_analysis": {
                "total_stocks_monitored": len(stock_codes),
                "herding_detected": len(herding_results),
                "avg_herding_score": statistics.mean([r["herding_score"] for r in herding_results]) if herding_results else 0,
                "sector_concentration": self._analyze_herding_concentration(herding_results)
            },
            "high_herding_stocks": [r for r in herding_results if r["herding_score"] >= 0.7],
            "all_herding_stocks": herding_results,
            "market_implications": self._analyze_herding_implications(herding_results),
            "trading_opportunities": self._identify_herding_opportunities(herding_results),
            "risk_warnings": self._generate_herding_risk_warnings(herding_results)
        }
        
        return self._success_response("monitor_herding_behavior", result, params)
    
    def backtest_behavioral_strategies(self, params: Dict) -> Dict:
        """回测行为策略"""
        strategy_type = params.get("strategy_type", "contrarian")
        lookback_days = params.get("lookback_days", 180)
        
        # 模拟回测结果
        backtest_results = {
            "strategy_type": strategy_type,
            "lookback_period": f"{lookback_days}天",
            "performance_metrics": {
                "total_trades": 42,
                "win_rate": 0.65,
                "avg_win": 0.048,
                "avg_loss": -0.022,
                "profit_factor": 2.83,
                "sharpe_ratio": 1.92,
                "max_drawdown": 0.098,
                "annualized_return": 0.36
            },
            "strategy_effectiveness": {
                "overreaction_strategy": {"win_rate": 0.68, "avg_return": 0.052},
                "extreme_sentiment_strategy": {"win_rate": 0.72, "avg_return": 0.058},
                "herding_reversal_strategy": {"win_rate": 0.62, "avg_return": 0.045}
            },
            "market_condition_analysis": {
                "bull_market": {"win_rate": 0.70, "sharpe": 2.1},
                "bear_market": {"win_rate": 0.60, "sharpe": 1.5},
                "sideways_market": {"win_rate": 0.65, "sharpe": 1.8}
            },
            "risk_analysis": {
                "worst_case_loss": -0.152,
                "var_95pct": -0.045,
                "recovery_time_avg": "8个交易日",
                "stress_test_performance": "通过2008、2015情景测试"
            },
            "optimization_insights": [
                "最佳持仓期：5-10个交易日",
                "最佳入场时机：情绪极端点确认后1-2天",
                "最佳止损点：-3%",
                "最佳止盈点：+5%至+8%"
            ]
        }
        
        return self._success_response("backtest_behavioral_strategies", backtest_results, params)
    
    # ========== 辅助方法 ==========
    
    def _detect_single_pattern(self, stock_code: str, pattern_type: str, timeframe: str) -> Optional[Dict]:
        """检测单个行为模式"""
        pattern_info = self.behavioral_patterns.get(pattern_type)
        if not pattern_info:
            return None
        
        # 模拟检测逻辑（实际应基于数据分析）
        confidence = np.random.uniform(0.4, 0.9)  # 模拟置信度
        
        if pattern_type == "overreaction":
            detection = self._detect_overreaction(stock_code, timeframe)
        elif pattern_type == "herding":
            detection = self._detect_herding(stock_code, timeframe)
        elif pattern_type == "extreme_sentiment":
            detection = self._detect_extreme_sentiment(stock_code, timeframe)
        elif pattern_type == "anchoring":
            detection = self._detect_anchoring(stock_code, timeframe)
        elif pattern_type == "disposition_effect":
            detection = self._detect_disposition_effect(stock_code, timeframe)
        else:
            detection = None
        
        if detection:
            detection.update({
                "pattern_type": pattern_type,
                "pattern_name": pattern_info["name"],
                "description": pattern_info["description"],
                "confidence": confidence,
                "detection_time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        
        return detection
    
    def _detect_overreaction(self, stock_code: str, timeframe: str) -> Dict:
        """检测过度反应"""
        # 模拟检测结果
        return {
            "detection_metrics": {
                "price_change": -0.082,
                "fundamental_change": -0.035,
                "overreaction_ratio": 2.34,
                "volatility_increase": 1.8
            },
            "pattern_characteristics": {
                "trigger_event": "行业利空传闻",
                "reaction_duration": "3天",
                "volume_spike": 2.1,
                "sentiment_shift": -0.25
            },
            "expected_reversal": {
                "magnitude": 0.045,
                "probability": 0.68,
                "timeframe": "3-7个交易日",
                "key_triggers": ["利空澄清", "技术性超卖反弹"]
            }
        }
    
    def _detect_herding(self, stock_code: str, timeframe: str) -> Dict:
        """检测羊群效应"""
        return {
            "detection_metrics": {
                "concentration_ratio": 0.72,
                "opinion_uniformity": 0.85,
                "momentum_persistence": 0.68,
                "herding_score": 0.65
            },
            "pattern_characteristics": {
                "herding_type": "正向羊群（追涨）",
                "participant_profile": "散户主导",
                "information_cascades": "社交媒体推动",
                "valuation_deviation": 0.28
            },
            "expected_reversal": {
                "magnitude": 0.055,
                "probability": 0.62,
                "timeframe": "5-12个交易日",
                "key_triggers": ["大户出货", "流动性收紧", "获利了结"]
            }
        }
    
    def _detect_extreme_sentiment(self, stock_code: str, timeframe: str) -> Dict:
        """检测情绪极端"""
        return {
            "detection_metrics": {
                "sentiment_score": 0.82,
                "historical_percentile": 0.92,
                "sector_deviation": 0.32,
                "extreme_index": 1.8
            },
            "pattern_characteristics": {
                "sentiment_type": "过度乐观",
                "driver_analysis": ["政策预期", "行业热点", "概念炒作"],
                "participant_sentiment": "散户极度乐观",
                "institutional_caution": True
            },
            "expected_reversal": {
                "magnitude": 0.062,
                "probability": 0.72,
                "timeframe": "2-6个交易日",
                "key_triggers": ["预期落空", "获利盘涌出", "风险偏好转变"]
            }
        }
    
    def _detect_anchoring(self, stock_code: str, timeframe: str) -> Dict:
        """检测锚定效应"""
        return {
            "detection_metrics": {
                "anchor_price": 95.50,
                "current_price": 92.70,
                "anchor_deviation": -0.029,
                "resistance_strength": 0.75
            },
            "pattern_characteristics": {
                "anchor_type": "历史高点锚定",
                "psychological_significance": "重要整数关口",
                "market_memory": "近期多次测试该价位",
                "breakout_potential": 0.65
            },
            "expected_behavior": {
                "scenario_1": {"description": "突破锚定", "probability": 0.35, "move": 0.085},
                "scenario_2": {"description": "反弹回落", "probability": 0.45, "move": -0.025},
                "scenario_3": {"description": "持续盘整", "probability": 0.20, "move": 0.000}
            }
        }
    
    def _detect_disposition_effect(self, stock_code: str, timeframe: str) -> Dict:
        """检测处置效应"""
        return {
            "detection_metrics": {
                "profit_taking_intensity": 0.68,
                "loss_holding_ratio": 0.72,
                "realized_gains": 0.042,
                "unrealized_losses": -0.028
            },
            "pattern_characteristics": {
                "investor_behavior": "散户频繁卖出盈利股",
                "position_analysis": "亏损持仓平均持有期延长",
                "tax_considerations": "年底调仓效应",
                "psychological_impact": "损失厌恶驱动"
            },
            "trading_implications": {
                "opportunity": "优质股被过早抛售",
                "risk": "垃圾股被长期持有",
                "strategy": "逆向吸纳被过早抛售的优质股",
                "timing": "财报季、年底调仓期"
            }
        }
    
    def _calculate_behavioral_score(self, detections: List[Dict]) -> float:
        """计算行为分数"""
        if not detections:
            return 0.0
        
        # 基于置信度和模式重要性
        base_scores = []
        for detection in detections:
            confidence = detection.get("confidence", 0.5)
            pattern_type = detection.get("pattern_type", "")
            
            # 模式重要性权重
            pattern_weight = {
                "extreme_sentiment": 1.2,
                "overreaction": 1.1,
                "herding": 1.0,
                "anchoring": 0.9,
                "disposition_effect": 0.8
            }.get(pattern_type, 1.0)
            
            score = confidence * pattern_weight * 10
            base_scores.append(score)
        
        return statistics.mean(base_scores)
    
    def _generate_trading_implications(self, detections: List[Dict]) -> List[str]:
        """生成交易启示"""
        implications = []
        
        for detection in detections:
            pattern_type = detection.get("pattern_type", "")
            
            if pattern_type == "overreaction":
                implications.append("过度反应后存在均值回归机会")
            elif pattern_type == "herding":
                implications.append("羊群效应后期望反转交易")
            elif pattern_type == "extreme_sentiment":
                implications.append("情绪极端点提供逆向交易机会")
            elif pattern_type == "anchoring":
                implications.append("锚定点位突破或反弹机会")
            elif pattern_type == "disposition_effect":
                implications.append("处置效应导致的错误定价机会")
        
        if not implications:
            implications.append("未检测到明确交易机会")
        
        return implications
    
    def _analyze_market_context(self, stock_codes: List[str], pattern_types: List[str]) -> Dict:
        """分析市场背景"""
        return {
            "market_regime": "震荡市",
            "risk_appetite": "中等",
            "liquidity_conditions": "充足",
            "volatility_regime": "中等波动",
            "sector_rotation": "科技板块受关注",
            "behavioral_trends": "近期过度反应模式增多",
            "recommended_approach": "选择性逆向交易，控制仓位"
        }
    
    def _generate_recommended_actions(self, detections: List[Dict]) -> List[Dict]:
        """生成建议行动"""
        if not detections:
            return [{"action": "观望", "reason": "未检测到明显行为模式"}]
        
        recommendations = []
        
        for detection in detections[:3]:  # 最多3个建议
            stock = detection["stock"]
            score = detection["behavioral_score"]
            primary_pattern = detection["primary_pattern"]
            
            if score >= 7.0:
                action = "积极关注"
                urgency = "高"
            elif score >= 5.0:
                action = "适度关注"
                urgency = "中"
            else:
                action = "观察"
                urgency = "低"
            
            if primary_pattern:
                pattern_name = primary_pattern.get("pattern_name", "行为模式")
                recommendations.append({
                    "stock": stock,
                    "action": action,
                    "urgency": urgency,
                    "pattern": pattern_name,
                    "recommendation": f"{action}{stock}的{pattern_name}机会",
                    "next_steps": [
                        "确认基本面支撑",
                        "设置明确入场点位",
                        "制定止损计划",
                        "监控模式演变"
                    ]
                })
        
        return recommendations
    
    def _calculate_stock_sentiment(self, stock_code: str) -> Dict:
        """计算股票情绪"""
        # 模拟情绪计算
        sentiment_values = {
            "price_momentum": np.random.uniform(0.3, 0.8),
            "volume_anomaly": np.random.uniform(0.2, 0.7),
            "retail_sentiment": np.random.uniform(0.2, 0.9),
            "institutional_flow": np.random.uniform(0.3, 0.8),
            "news_sentiment": np.random.uniform(0.4, 0.9),
            "social_media_buzz": np.random.uniform(0.2, 0.8)
        }
        
        # 加权计算总体情绪
        overall = sum(sentiment_values[k] * self.sentiment_weights[k] for k in sentiment_values)
        
        # 识别关键驱动因素
        key_drivers = sorted(sentiment_values.items(), key=lambda x: x[1] * self.sentiment_weights.get(x[0], 0.1), reverse=True)[:3]
        
        return {
            "overall": overall,
            "breakdown": sentiment_values,
            "key_drivers": [{"factor": k, "value": v, "contribution": v * self.sentiment_weights.get(k, 0.1)} for k, v in key_drivers]
        }
    
    def _categorize_sentiment(self, sentiment_value: float) -> str:
        """分类情绪"""
        if sentiment_value >= 0.7:
            return "极度乐观"
        elif sentiment_value >= 0.6:
            return "乐观"
        elif sentiment_value >= 0.4:
            return "中性"
        elif sentiment_value >= 0.3:
            return "悲观"
        else:
            return "极度悲观"
    
    def _assess_sentiment_trend(self, stock_code: str) -> str:
        """评估情绪趋势"""
        # 模拟趋势评估
        trends = ["上升", "下降", "震荡", "转折"]
        return np.random.choice(trends, p=[0.3, 0.3, 0.3, 0.1])
    
    def _calculate_sector_sentiment(self, sentiment_results: List[Dict]) -> Dict:
        """计算行业情绪"""
        sector_sentiments = {}
        
        for result in sentiment_results:
            sector = result.get("sector", "未知")
            sentiment = result.get("overall_sentiment", 0.5)
            
            if sector not in sector_sentiments:
                sector_sentiments[sector] = []
            sector_sentiments[sector].append(sentiment)
        
        # 计算行业平均情绪
        sector_analysis = {}
        for sector, sentiments in sector_sentiments.items():
            if sentiments:
                avg = statistics.mean(sentiments)
                sector_analysis[sector] = {
                    "average_sentiment": avg,
                    "sentiment_category": self._categorize_sentiment(avg),
                    "stock_count": len(sentiments),
                    "range": (min(sentiments), max(sentiments))
                }
        
        return sector_analysis
    
    def _is_reversal_candidate(self, sentiment_result: Dict) -> bool:
        """判断是否为反转候选"""
        sentiment = sentiment_result.get("overall_sentiment", 0.5)
        deviation = abs(sentiment - 0.5)
        
        # 情绪极端且近期有趋势
        if deviation > 0.2:
            trend = sentiment_result.get("sentiment_trend", "震荡")
            # 如果情绪极端且趋势持续，可能接近反转点
            if (sentiment > 0.7 and trend == "上升") or (sentiment < 0.3 and trend == "下降"):
                return True
        
        return False
    
    def _generate_sentiment_insights(self, sentiment_results: List[Dict]) -> List[str]:
        """生成情绪洞察"""
        insights = []
        
        # 总体情绪洞察
        market_sentiment = statistics.mean([r["overall_sentiment"] for r in sentiment_results]) if sentiment_results else 0.5
        
        if market_sentiment > 0.65:
            insights.append("市场整体情绪偏乐观，注意追高风险")
        elif market_sentiment < 0.35:
            insights.append("市场整体情绪偏悲观，关注超跌机会")
        else:
            insights.append("市场情绪中性，个股分化明显")
        
        # 行业情绪洞察
        sector_analysis = self._calculate_sector_sentiment(sentiment_results)
        extreme_sectors = [(s, d) for s, d in sector_analysis.items() if abs(d["average_sentiment"] - 0.5) > 0.15]
        
        for sector, data in extreme_sectors:
            if data["average_sentiment"] > 0.65:
                insights.append(f"{sector}行业情绪过热，需谨慎")
            else:
                insights.append(f"{sector}行业情绪过冷，可关注")
        
        return insights
    
    def _assess_extreme_sentiment_risk(self, deviation: float, sentiment: float) -> str:
        """评估极端情绪风险"""
        if deviation > 0.35:
            return "极高风险"
        elif deviation > 0.25:
            return "高风险"
        elif deviation > 0.15:
            return "中等风险"
        else:
            return "低风险"
    
    def _generate_extreme_monitoring_points(self, stock_code: str, is_optimistic: bool) -> List[str]:
        """生成极端情绪监控要点"""
        if is_optimistic:
            return [
                "大户持仓变化",
                "成交量能否持续",
                "利好消息兑现情况",
                "技术指标背离信号"
            ]
        else:
            return [
                "卖压是否衰竭",
                "是否有利空出尽迹象",
                "机构资金流向",
                "技术性超卖指标"
            ]
    
    def _analyze_extreme_implications(self, extreme_candidates: List[Dict]) -> Dict:
        """分析极端情绪的市场启示"""
        if not extreme_candidates:
            return {"market_balance": "情绪相对均衡", "implication": "无明显极端机会"}
        
        optimism_count = len([c for c in extreme_candidates if c["direction"] == "过度乐观"])
        pessimism_count = len([c for c in extreme_candidates if c["direction"] == "过度悲观"])
        
        if optimism_count > pessimism_count * 2:
            implication = "市场整体偏乐观，需防范回调风险"
        elif pessimism_count > optimism_count * 2:
            implication = "市场整体偏悲观，存在反弹机会"
        else:
            implication = "市场情绪分化，结构性机会为主"
        
        return {
            "market_balance": f"乐观{optimism_count} vs 悲观{pessimism_count}",
            "implication": implication,
            "sector_distribution": "科技、消费为主" if optimism_count > 0 else "周期、金融为主",
            "recommended_action": "选择性逆向交易" if extreme_candidates else "维持观望"
        }
    
    def _generate_extreme_trading_strategies(self, extreme_candidates: List[Dict]) -> List[Dict]:
        """生成极端情绪交易策略"""
        strategies = []
        
        for candidate in extreme_candidates[:5]:  # 最多5个策略
            stock = candidate["stock"]
            direction = candidate["direction"]
            deviation = candidate["deviation_pct"] / 100
            
            if direction == "过度乐观":
                strategy = {
                    "stock": stock,
                    "strategy_type": "逆向卖出/做空",
                    "entry_timing": "情绪指标见顶回落",
                    "target_profit": f"{candidate['expected_reversal_magnitude']*100:.1f}%",
                    "stop_loss": "突破前高+2%",
                    "risk_management": "轻仓试探，分批建仓"
                }
            else:  # 过度悲观
                strategy = {
                    "stock": stock,
                    "strategy_type": "逆向买入",
                    "entry_timing": "情绪指标触底反弹",
                    "target_profit": f"{candidate['expected_reversal_magnitude']*100:.1f}%",
                    "stop_loss": "跌破前低-2%",
                    "risk_management": "分批建仓，严格止损"
                }
            
            strategies.append(strategy)
        
        return strategies
    
    def _generate_contrarian_signal(self, stock_code: str, pattern_detection: Dict) -> Optional[Dict]:
        """生成逆向交易信号"""
        pattern_type = pattern_detection.get("pattern_type")
        confidence = pattern_detection.get("confidence", 0.5)
        
        if confidence < 0.6:
            return None
        
        # 根据模式类型确定信号
        if pattern_type == "overreaction":
            direction = "买入" if pattern_detection.get("detection_metrics", {}).get("price_change", 0) < 0 else "卖出"
            move = pattern_detection.get("expected_reversal", {}).get("magnitude", 0.04)
        elif pattern_type == "extreme_sentiment":
            direction = "卖出" if pattern_detection.get("detection_metrics", {}).get("sentiment_score", 0.5) > 0.7 else "买入"
            move = pattern_detection.get("expected_reversal", {}).get("magnitude", 0.05)
        elif pattern_type == "herding":
            direction = "卖出"  # 羊群效应后期望反转
            move = pattern_detection.get("expected_reversal", {}).get("magnitude", 0.045)
        else:
            return None
        
        # 计算信号强度
        signal_strength = confidence * 10 * (1 + abs(move) * 5)
        
        return {
            "signal_id": f"CONTRA_{stock_code}_{datetime.now().strftime('%Y%m%d')}",
            "stock": stock_code,
            "pattern_type": pattern_type,
            "direction": direction,
            "signal_strength": min(10.0, signal_strength),
            "expected_move": move,
            "confidence": confidence,
            "timeframe": pattern_detection.get("expected_reversal", {}).get("timeframe", "3-7个交易日"),
            "risk_management": {
                "position_size": "不超过总资金3%",
                "stop_loss": f"{-abs(move)*0.6:.1%}",
                "take_profit": f"{abs(move):.1%}",
                "risk_reward": f"1:{1/0.6:.1f}"
            }
        }
    
    def _calculate_composite_signal_score(self, signals: List[Dict]) -> float:
        """计算复合信号分数"""
        if not signals:
            return 0.0
        
        scores = [s["signal_strength"] for s in signals]
        return statistics.mean(scores)
    
    def _optimize_signal_portfolio(self, signals: List[Dict], capital: float) -> List[Dict]:
        """优化信号组合"""
        if not signals:
            return []
        
        # 按信号强度排序
        sorted_signals = sorted(signals, key=lambda x: x["composite_score"], reverse=True)
        
        # 选择前5个信号
        selected = sorted_signals[:5]
        
        # 分配资金
        total_score = sum(s["composite_score"] for s in selected)
        for signal in selected:
            allocation = signal["composite_score"] / total_score
            signal["capital_allocation"] = capital * allocation * 0.25  # 最大总仓位25%
            signal["position_size_pct"] = allocation * 25
        
        return selected
    
    def _assess_signal_portfolio_risk(self, portfolio: List[Dict]) -> Dict:
        """评估信号组合风险"""
        if not portfolio:
            return {"risk_level": "低", "recommendation": "无信号"}
        
        # 计算组合风险指标
        avg_strength = statistics.mean([s["composite_score"] for s in portfolio])
        direction_diversity = len(set(s["best_signal"]["direction"] for s in portfolio))
        sector_diversity = len(set(self.stock_sector_map.get(s["stock"], "未知") for s in portfolio))
        
        if avg_strength >= 8.0 and direction_diversity >= 2 and sector_diversity >= 3:
            risk_level = "低"
        elif avg_strength >= 6.0 and direction_diversity >= 2:
            risk_level = "中"
        else:
            risk_level = "高"
        
        return {
            "risk_level": risk_level,
            "avg_signal_strength": avg_strength,
            "direction_diversity": direction_diversity,
            "sector_diversity": sector_diversity,
            "key_risks": ["模式失效", "市场结构变化", "流动性不足"],
            "mitigation": ["严格止损", "分散投资", "动态调整"]
        }
    
    def _generate_contrarian_execution_plan(self, portfolio: List[Dict]) -> Dict:
        """生成逆向交易执行计划"""
        if not portfolio:
            return {"plan": "无执行计划"}
        
        executions = []
        for signal in portfolio:
            executions.append({
                "stock": signal["stock"],
                "action": signal["best_signal"]["direction"],
                "capital": signal["capital_allocation"],
                "timing": "信号确认后1-2天内",
                "risk_controls": signal["best_signal"]["risk_management"]
            })
        
        return {
            "total_capital": sum(s["capital_allocation"] for s in portfolio),
            "executions": executions,
            "monitoring_schedule": "每日收盘后评估",
            "adjustment_criteria": [
                "信号强度下降30%以上",
                "预期走势失败",
                "出现相反信号",
                "达到止损或止盈点"
            ]
        }
    
    def _analyze_herding_behavior(self, stock_code: str) -> Dict:
        """分析羊群行为"""
        # 模拟分析
        return {
            "stock": stock_code,
            "sector": self.stock_sector_map.get(stock_code, "未知"),
            "herding_score": np.random.uniform(0.3, 0.9),
            "herding_type": np.random.choice(["追涨", "杀跌", "概念炒作", "政策跟随"]),
            "participant_composition": {
                "retail_ratio": np.random.uniform(0.5, 0.9),
                "institutional_ratio": np.random.uniform(0.1, 0.5),
                "hot_money_ratio": np.random.uniform(0.2, 0.6)
            },
            "risk_metrics": {
                "valuation_deviation": np.random.uniform(0.1, 0.4),
                "liquidity_risk": np.random.uniform(0.2, 0.7),
                "momentum_exhaustion": np.random.uniform(0.3, 0.8)
            },
            "reversal_indicators": {
                "signal_strength": np.random.uniform(0.4, 0.9),
                "expected_timing": f"{np.random.randint(3, 10)}个交易日",
                "key_triggers": ["大户出货", "流动性变化", "概念退潮"]
            }
        }
    
    def _analyze_herding_concentration(self, herding_results: List[Dict]) -> Dict:
        """分析羊群集中度"""
        if not herding_results:
            return {"concentration": "低", "sector_focus": "无"}
        
        # 分析行业分布
        sectors = [r["sector"] for r in herding_results]
        sector_counts = {s: sectors.count(s) for s in set(sectors)}
        
        # 计算集中度
        total = len(herding_results)
        max_sector_count = max(sector_counts.values()) if sector_counts else 0
        concentration = max_sector_count / total if total > 0 else 0
        
        if concentration > 0.5:
            concentration_level = "高"
        elif concentration > 0.3:
            concentration_level = "中"
        else:
            concentration_level = "低"
        
        return {
            "concentration": concentration_level,
            "sector_focus": max(sector_counts, key=sector_counts.get) if sector_counts else "无",
            "sector_distribution": sector_counts
        }
    
    def _analyze_herding_implications(self, herding_results: List[Dict]) -> List[str]:
        """分析羊群效应的市场启示"""
        if not herding_results:
            return ["当前无明显羊群效应"]
        
        avg_score = statistics.mean([r["herding_score"] for r in herding_results])
        
        if avg_score > 0.7:
            return [
                "市场羊群效应显著，警惕反转风险",
                "追涨情绪浓厚，短期可能延续但风险积累",
                "建议逆向思维，寻找被忽视的机会"
            ]
        elif avg_score > 0.5:
            return [
                "市场存在一定羊群效应",
                "部分板块过热，需谨慎参与",
                "可适度逆向交易，控制仓位"
            ]
        else:
            return [
                "羊群效应不明显，市场相对理性",
                "以基本面分析为主，技术面为辅",
                "正常交易节奏，无需过度逆向"
            ]
    
    def _identify_herding_opportunities(self, herding_results: List[Dict]) -> List[Dict]:
        """识别羊群效应机会"""
        opportunities = []
        
        for result in herding_results:
            if result["herding_score"] >= 0.7:
                stock = result["stock"]
                herding_type = result["herding_type"]
                
                if herding_type in ["追涨", "概念炒作"]:
                    opportunity = {
                        "stock": stock,
                        "opportunity_type": "逆向卖出",
                        "rationale": f"{stock}存在显著{herding_type}羊群效应",
                        "entry_signal": "成交量萎缩或价格滞涨",
                        "target": f"预期回调{np.random.uniform(0.05, 0.12):.1%}",
                        "risk": "趋势延续风险"
                    }
                else:  # 杀跌
                    opportunity = {
                        "stock": stock,
                        "opportunity_type": "逆向买入",
                        "rationale": f"{stock}存在恐慌性抛售",
                        "entry_signal": "卖压衰竭或底部放量",
                        "target": f"预期反弹{np.random.uniform(0.08, 0.15):.1%}",
                        "risk": "继续下跌风险"
                    }
                
                opportunities.append(opportunity)
        
        return opportunities[:5]  # 最多5个机会
    
    def _generate_herding_risk_warnings(self, herding_results: List[Dict]) -> List[str]:
        """生成羊群效应风险警告"""
        warnings = []
        
        high_herding = [r for r in herding_results if r["herding_score"] >= 0.7]
        
        if len(high_herding) >= 5:
            warnings.append("市场多个板块出现显著羊群效应，系统性风险增加")
        
        for result in high_herding[:3]:
            stock = result["stock"]
            herding_type = result["herding_type"]
            warnings.append(f"{stock}的{herding_type}羊群效应显著，反转风险高")
        
        if warnings:
            warnings.append("建议：控制仓位，设置止损，避免追高杀跌")
        
        return warnings if warnings else ["当前羊群效应风险可控"]
    
    def _success_response(self, action: str, result: Dict, params: Dict) -> Dict:
        """成功响应"""
        return {
            "success": True,
            "skill": "behavioral_finance_skill",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "parameters": params,
            "result": result
        }
    
    def _error_response(self, message: str) -> Dict:
        """错误响应"""
        return {
            "success": False,
            "skill": "behavioral_finance_skill",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "error": message
        }

def main():
    """主函数"""
    try:
        # 读取输入参数
        if len(sys.argv) > 1:
            params = json.loads(sys.argv[1])
        else:
            input_str = sys.stdin.read().strip()
            params = json.loads(input_str) if input_str else {}
        
        # 执行行为金融策略
        strategy = BehavioralFinanceStrategy()
        result = strategy.execute(params)
        
        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except json.JSONDecodeError as e:
        error_result = {
            "success": False,
            "skill": "behavioral_finance_skill",
            "version": "1.0.0",
            "error": f"JSON解析错误: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
    except Exception as e:
        error_result = {
            "success": False,
            "skill": "behavioral_finance_skill",
            "version": "1.0.0",
            "error": f"行为金融策略过程出错: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()