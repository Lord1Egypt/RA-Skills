#!/usr/bin/env python3
# coding:utf-8

"""
事件驱动策略技能 v1.0.0
捕捉财报、并购、政策等事件带来的超额收益机会
"""

import sys
import json
import datetime
import re
import math
import statistics
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timedelta

class EventDrivenStrategy:
    """事件驱动策略核心类"""
    
    def __init__(self):
        # 事件类型定义
        self.event_types = {
            "earnings": {
                "name": "财报发布",
                "importance": 5,
                "prep_days": 3,
                "reaction_days": 3,
                "avg_impact": 0.04  # 平均4%波动
            },
            "merger": {
                "name": "并购公告",
                "importance": 5,
                "prep_days": 1,
                "reaction_days": 5,
                "avg_impact": 0.08  # 平均8%波动
            },
            "policy": {
                "name": "政策发布",
                "importance": 4,
                "prep_days": 0,
                "reaction_days": 2,
                "avg_impact": 0.06  # 平均6%波动
            },
            "fda_approval": {
                "name": "FDA/NMPA审批",
                "importance": 4,
                "prep_days": 2,
                "reaction_days": 3,
                "avg_impact": 0.12  # 平均12%波动
            },
            "management_change": {
                "name": "管理层变动",
                "importance": 3,
                "prep_days": 0,
                "reaction_days": 2,
                "avg_impact": 0.03  # 平均3%波动
            },
            "product_launch": {
                "name": "产品发布会",
                "importance": 3,
                "prep_days": 1,
                "reaction_days": 2,
                "avg_impact": 0.05  # 平均5%波动
            }
        }
        
        # 模拟事件数据库（实际应连接数据库）
        self.event_database = self._init_event_database()
        
        # 历史事件模式（简化版本）
        self.historical_patterns = self._init_historical_patterns()
        
        # 行业映射
        self.sector_mapping = {
            "002371.SZ": "半导体",
            "002384.SZ": "消费电子",
            "000723.SZ": "能源化工",
            "002078.SZ": "造纸印刷",
            "002594.SZ": "汽车",
            "002230.SZ": "计算机",
            "603019.SH": "计算机"
        }
    
    def _init_event_database(self) -> Dict:
        """初始化事件数据库（模拟数据）"""
        today = datetime.now()
        
        # 模拟未来事件
        return [
            {
                "id": "EVT202603001",
                "stock": "002371.SZ",
                "event_type": "earnings",
                "event_date": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
                "title": "2026年第一季度财报",
                "market_consensus_eps": 1.20,
                "internal_estimate": 1.25,
                "analyst_count": 15,
                "expected_revenue_growth": 0.25,
                "catalyst_strength": 4,
                "notes": "半导体行业复苏，预期超预期"
            },
            {
                "id": "EVT202603002",
                "stock": "002384.SZ",
                "event_type": "product_launch",
                "event_date": (today + timedelta(days=3)).strftime("%Y-%m-%d"),
                "title": "新一代折叠屏手机发布会",
                "market_consensus_eps": None,
                "internal_estimate": None,
                "analyst_count": 8,
                "expected_revenue_growth": 0.15,
                "catalyst_strength": 3,
                "notes": "消费电子创新产品，市场关注度高"
            },
            {
                "id": "EVT202603003",
                "stock": "603019.SH",
                "event_type": "policy",
                "event_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
                "title": "人工智能产业政策细则发布",
                "market_consensus_eps": None,
                "internal_estimate": None,
                "analyst_count": 12,
                "expected_revenue_growth": 0.30,
                "catalyst_strength": 5,
                "notes": "两会后AI产业政策落地，受益明显"
            },
            {
                "id": "EVT202603004",
                "stock": "002594.SZ",
                "event_type": "earnings",
                "event_date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
                "title": "2026年第一季度财报",
                "market_consensus_eps": 8.50,
                "internal_estimate": 9.20,
                "analyst_count": 22,
                "expected_revenue_growth": 0.35,
                "catalyst_strength": 4,
                "notes": "新能源汽车销量超预期"
            }
        ]
    
    def _init_historical_patterns(self) -> Dict:
        """初始化历史事件模式"""
        return {
            "earnings": {
                "beat_rate": 0.65,  # 65%概率超预期
                "avg_positive_move": 0.045,  # 超预期平均涨幅4.5%
                "avg_negative_move": -0.032,  # 不及预期平均跌幅3.2%
                "volatility_increase": 2.5,  # 波动率增加150%
                "reaction_complete_days": 3  # 3天完成反应
            },
            "merger": {
                "beat_rate": 0.55,
                "avg_positive_move": 0.12,
                "avg_negative_move": -0.08,
                "volatility_increase": 3.0,
                "reaction_complete_days": 5
            },
            "policy": {
                "beat_rate": 0.60,
                "avg_positive_move": 0.07,
                "avg_negative_move": -0.05,
                "volatility_increase": 2.0,
                "reaction_complete_days": 2
            }
        }
    
    def execute(self, params: Dict) -> Dict:
        """执行事件驱动策略操作"""
        action = params.get("action", "analyze_event")
        
        if action == "analyze_event":
            return self.analyze_single_event(params)
        elif action == "scan_upcoming_events":
            return self.scan_upcoming_events(params)
        elif action == "backtest_event_pattern":
            return self.backtest_event_pattern(params)
        elif action == "monitor_event_reaction":
            return self.monitor_event_reaction(params)
        elif action == "generate_trading_signals":
            return self.generate_trading_signals(params)
        else:
            return self._error_response(f"未知操作: {action}")
    
    def analyze_single_event(self, params: Dict) -> Dict:
        """分析单个事件机会"""
        stock_code = params.get("stock_code", "")
        event_type = params.get("event_type", "")
        event_date = params.get("event_date", "")
        
        if not stock_code or not event_type:
            return self._error_response("缺少必要参数: stock_code, event_type")
        
        # 获取事件信息（模拟）
        event_info = self._get_event_info(stock_code, event_type, event_date)
        
        # 计算预期差
        expectation_gap = self._calculate_expectation_gap(event_info)
        
        # 评估催化剂强度
        catalyst_strength = self._assess_catalyst_strength(event_info)
        
        # 预测价格变动
        price_move_prediction = self._predict_price_move(event_info, expectation_gap, catalyst_strength)
        
        # 生成交易建议
        trading_recommendation = self._generate_trading_recommendation(
            event_info, expectation_gap, price_move_prediction
        )
        
        result = {
            "event_analysis": {
                "event_id": event_info.get("id", "N/A"),
                "stock": stock_code,
                "event_type": event_type,
                "event_name": self.event_types.get(event_type, {}).get("name", event_type),
                "event_date": event_info.get("event_date", event_date),
                "title": event_info.get("title", ""),
                "importance_level": self.event_types.get(event_type, {}).get("importance", 3),
                "time_to_event": self._calculate_time_to_event(event_info.get("event_date", event_date))
            },
            "expectation_analysis": expectation_gap,
            "catalyst_analysis": catalyst_strength,
            "price_prediction": price_move_prediction,
            "trading_recommendation": trading_recommendation,
            "risk_assessment": self._assess_event_risk(event_info, expectation_gap),
            "historical_context": self._get_historical_context(stock_code, event_type)
        }
        
        return self._success_response("analyze_event", result, params)
    
    def scan_upcoming_events(self, params: Dict) -> Dict:
        """扫描即将发生的事件"""
        days_ahead = params.get("days_ahead", 7)
        min_importance = params.get("min_importance", 3)
        sectors = params.get("sectors", [])
        
        upcoming_events = []
        today = datetime.now()
        end_date = today + timedelta(days=days_ahead)
        
        for event in self.event_database:
            event_date = datetime.strptime(event["event_date"], "%Y-%m-%d")
            event_type_info = self.event_types.get(event["event_type"], {})
            
            # 过滤条件
            if event_date > end_date:
                continue
            
            importance = event_type_info.get("importance", 3)
            if importance < min_importance:
                continue
            
            if sectors:
                sector = self.sector_mapping.get(event["stock"], "其他")
                if sector not in sectors:
                    continue
            
            # 计算优先级分数
            priority_score = self._calculate_event_priority(event)
            
            upcoming_events.append({
                "event_id": event["id"],
                "stock": event["stock"],
                "event_type": event["event_type"],
                "event_name": event_type_info.get("name", event["event_type"]),
                "event_date": event["event_date"],
                "title": event["title"],
                "importance": importance,
                "days_to_event": (event_date - today).days,
                "priority_score": priority_score,
                "expected_impact": event_type_info.get("avg_impact", 0.05),
                "catalyst_strength": event.get("catalyst_strength", 3),
                "quick_analysis": self._generate_quick_analysis(event)
            })
        
        # 按优先级排序
        upcoming_events.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # 分组统计
        event_stats = self._generate_event_statistics(upcoming_events)
        
        result = {
            "scan_period": f"{today.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}",
            "total_events": len(upcoming_events),
            "event_statistics": event_stats,
            "high_priority_events": [e for e in upcoming_events if e["priority_score"] >= 7.5],
            "all_events": upcoming_events,
            "recommended_focus": self._recommend_focus_areas(upcoming_events)
        }
        
        return self._success_response("scan_upcoming_events", result, params)
    
    def backtest_event_pattern(self, params: Dict) -> Dict:
        """回测历史事件模式"""
        event_type = params.get("event_type", "earnings")
        lookback_days = params.get("lookback_days", 365)
        
        if event_type not in self.historical_patterns:
            return self._error_response(f"不支持的事件类型: {event_type}")
        
        pattern = self.historical_patterns[event_type]
        
        # 模拟回测结果（实际应基于历史数据）
        backtest_results = {
            "event_type": event_type,
            "lookback_period": lookback_days,
            "total_events_simulated": 42,
            "performance_metrics": {
                "win_rate": pattern["beat_rate"],
                "average_win": pattern["avg_positive_move"],
                "average_loss": pattern["avg_negative_move"],
                "profit_factor": pattern["beat_rate"] * abs(pattern["avg_positive_move"]) / 
                               ((1 - pattern["beat_rate"]) * abs(pattern["avg_negative_move"])),
                "sharpe_ratio": 1.8,
                "max_drawdown": 0.12
            },
            "timing_analysis": {
                "best_entry_day": -2,  # 事件前2天
                "best_exit_day": 1,    # 事件后1天
                "avg_holding_period": 3.2,
                "overnight_risk_adjustment": 0.85
            },
            "market_conditions_impact": {
                "bull_market": {"win_rate": 0.72, "avg_return": 0.058},
                "bear_market": {"win_rate": 0.58, "avg_return": 0.032},
                "sideways_market": {"win_rate": 0.65, "avg_return": 0.042}
            },
            "lessons_learned": self._generate_lessons_learned(event_type)
        }
        
        return self._success_response("backtest_event_pattern", backtest_results, params)
    
    def monitor_event_reaction(self, params: Dict) -> Dict:
        """监控事件后的市场反应"""
        event_id = params.get("event_id", "")
        stock_code = params.get("stock_code", "")
        event_date = params.get("event_date", "")
        
        if not event_id and not (stock_code and event_date):
            return self._error_response("需要event_id或stock_code+event_date")
        
        # 模拟监控结果（实际应连接实时数据）
        today = datetime.now()
        event_date_obj = datetime.strptime(event_date if event_date else "2026-03-01", "%Y-%m-%d")
        days_since_event = (today - event_date_obj).days
        
        # 模拟价格反应
        price_reaction = self._simulate_price_reaction(days_since_event)
        
        result = {
            "monitoring_summary": {
                "event_id": event_id or f"EVT_{stock_code}_{event_date}",
                "stock": stock_code,
                "event_date": event_date,
                "days_since_event": days_since_event,
                "reaction_stage": self._determine_reaction_stage(days_since_event),
                "reaction_completion": min(1.0, days_since_event / 3.0)  # 假设3天完成反应
            },
            "price_reaction_analysis": price_reaction,
            "volume_analysis": {
                "volume_spike": 2.5,  # 交易量放大倍数
                "volume_persistence": 0.7,  # 交易量持续性
                "institutional_participation": 0.65  # 机构参与度
            },
            "sentiment_analysis": {
                "news_sentiment": 0.75,  # 新闻情绪正面度
                "social_media_buzz": 1.8,  # 社交媒体热度
                "analyst_reactions": ["买入", "增持", "持有"]  # 分析师反应
            },
            "trading_implications": self._generate_trading_implications(days_since_event, price_reaction),
            "next_monitoring_check": (today + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")
        }
        
        return self._success_response("monitor_event_reaction", result, params)
    
    def generate_trading_signals(self, params: Dict) -> Dict:
        """生成交易信号"""
        portfolio_context = params.get("portfolio_context", {})
        risk_tolerance = params.get("risk_tolerance", 3)
        capital_available = params.get("capital_available", 100000)
        
        # 扫描即将发生的事件
        upcoming_events = []
        for event in self.event_database:
            event_date = datetime.strptime(event["event_date"], "%Y-%m-%d")
            days_to_event = (event_date - datetime.now()).days
            
            if 0 <= days_to_event <= 7:  # 未来7天内的事件
                priority_score = self._calculate_event_priority(event)
                if priority_score >= 6.0:
                    upcoming_events.append(event)
        
        # 为每个事件生成交易信号
        trading_signals = []
        for event in upcoming_events:
            signal = self._generate_single_signal(event, portfolio_context, risk_tolerance, capital_available)
            if signal:
                trading_signals.append(signal)
        
        # 风险控制和组合优化
        optimized_signals = self._optimize_signal_portfolio(trading_signals, capital_available, risk_tolerance)
        
        result = {
            "generated_signals": trading_signals,
            "optimized_portfolio": optimized_signals,
            "risk_metrics": {
                "total_position_suggested": sum(s.get("position_size", 0) for s in optimized_signals),
                "max_single_position": max((s.get("position_size", 0) for s in optimized_signals), default=0),
                "portfolio_var": 0.085,  # 简化计算
                "correlation_score": 0.65  # 分散化评分
            },
            "execution_plan": self._generate_execution_plan(optimized_signals),
            "monitoring_requirements": self._generate_monitoring_requirements(optimized_signals)
        }
        
        return self._success_response("generate_trading_signals", result, params)
    
    # ========== 辅助方法 ==========
    
    def _get_event_info(self, stock_code: str, event_type: str, event_date: str) -> Dict:
        """获取事件信息（模拟）"""
        # 首先检查数据库
        for event in self.event_database:
            if event["stock"] == stock_code and event["event_type"] == event_type:
                if not event_date or event["event_date"] == event_date:
                    return event
        
        # 如果未找到，创建模拟事件
        return {
            "id": f"EVT_{stock_code}_{datetime.now().strftime('%Y%m%d')}",
            "stock": stock_code,
            "event_type": event_type,
            "event_date": event_date or (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "title": f"{stock_code} {self.event_types.get(event_type, {}).get('name', event_type)}",
            "market_consensus_eps": 1.0,
            "internal_estimate": 1.05,
            "analyst_count": 10,
            "expected_revenue_growth": 0.15,
            "catalyst_strength": 3,
            "notes": "模拟事件数据"
        }
    
    def _calculate_expectation_gap(self, event_info: Dict) -> Dict:
        """计算预期差"""
        market_consensus = event_info.get("market_consensus_eps")
        internal_estimate = event_info.get("internal_estimate")
        
        if market_consensus is None or internal_estimate is None:
            return {
                "expectation_gap_pct": 0.0,
                "expectation_gap_direction": "neutral",
                "confidence_level": 0.5,
                "analyst_coverage": event_info.get("analyst_count", 5),
                "notes": "缺乏具体预期数据"
            }
        
        gap_pct = (internal_estimate - market_consensus) / market_consensus if market_consensus != 0 else 0
        
        if gap_pct > 0.02:
            direction = "positive"
            confidence = min(0.9, 0.6 + abs(gap_pct) * 2)
        elif gap_pct < -0.02:
            direction = "negative"
            confidence = min(0.9, 0.6 + abs(gap_pct) * 2)
        else:
            direction = "neutral"
            confidence = 0.5
        
        return {
            "market_consensus": market_consensus,
            "internal_estimate": internal_estimate,
            "expectation_gap": internal_estimate - market_consensus,
            "expectation_gap_pct": gap_pct,
            "expectation_gap_direction": direction,
            "confidence_level": confidence,
            "analyst_coverage": event_info.get("analyst_count", 5),
            "interpretation": f"内部预期较市场共识{gap_pct*100:+.1f}%"
        }
    
    def _assess_catalyst_strength(self, event_info: Dict) -> Dict:
        """评估催化剂强度"""
        base_strength = event_info.get("catalyst_strength", 3)
        event_type = event_info.get("event_type", "")
        
        # 事件类型权重
        event_type_weight = self.event_types.get(event_type, {}).get("importance", 3) / 5.0
        
        # 分析师覆盖度调整
        analyst_count = event_info.get("analyst_count", 5)
        analyst_weight = min(1.0, analyst_count / 20.0)
        
        # 预期增长调整
        growth = event_info.get("expected_revenue_growth", 0.1)
        growth_weight = min(1.0, growth / 0.3)
        
        # 计算综合强度
        total_strength = base_strength * (0.4 * event_type_weight + 0.3 * analyst_weight + 0.3 * growth_weight)
        
        # 强度评级
        if total_strength >= 4.5:
            rating = "极高"
            color = "red"
        elif total_strength >= 3.5:
            rating = "高"
            color = "orange"
        elif total_strength >= 2.5:
            rating = "中等"
            color = "yellow"
        else:
            rating = "低"
            color = "green"
        
        return {
            "base_strength": base_strength,
            "event_type_weight": event_type_weight,
            "analyst_coverage_weight": analyst_weight,
            "growth_weight": growth_weight,
            "total_strength": total_strength,
            "strength_rating": rating,
            "color_code": color,
            "comparison": f"高于{int((total_strength/5.0)*100)}%的类似事件"
        }
    
    def _predict_price_move(self, event_info: Dict, expectation_gap: Dict, catalyst_strength: Dict) -> Dict:
        """预测价格变动"""
        event_type = event_info.get("event_type", "")
        pattern = self.historical_patterns.get(event_type, self.historical_patterns.get("earnings", {}))
        
        base_move = pattern.get("avg_positive_move", 0.04)
        gap_pct = expectation_gap.get("expectation_gap_pct", 0)
        strength = catalyst_strength.get("total_strength", 3)
        
        # 调整因子
        gap_adjustment = 1.0 + abs(gap_pct) * 10  # 预期差影响
        strength_adjustment = strength / 3.0  # 催化剂强度影响
        
        # 预测变动范围
        predicted_move = base_move * gap_adjustment * strength_adjustment
        
        # 波动范围（置信区间）
        volatility = pattern.get("volatility_increase", 2.0)
        lower_bound = predicted_move * 0.6
        upper_bound = predicted_move * 1.4
        
        # 方向判断
        direction = "positive" if gap_pct > 0 else ("negative" if gap_pct < 0 else "neutral")
        
        return {
            "predicted_move_pct": predicted_move,
            "direction": direction,
            "confidence_interval": {
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "probability_68pct": f"{lower_bound*100:.1f}% 至 {upper_bound*100:.1f}%"
            },
            "volatility_impact": volatility,
            "timeframe": f"事件后{pattern.get('reaction_complete_days', 3)}个交易日",
            "key_drivers": [
                f"预期差: {gap_pct*100:+.1f}%",
                f"催化剂强度: {strength:.1f}/5.0",
                f"历史模式: {event_type}"
            ]
        }
    
    def _generate_trading_recommendation(self, event_info: Dict, expectation_gap: Dict, price_prediction: Dict) -> Dict:
        """生成交易建议"""
        event_type = event_info.get("event_type", "")
        event_type_info = self.event_types.get(event_type, {})
        
        prep_days = event_type_info.get("prep_days", 2)
        reaction_days = event_type_info.get("reaction_days", 3)
        
        direction = expectation_gap.get("expectation_gap_direction", "neutral")
        predicted_move = price_prediction.get("predicted_move_pct", 0)
        
        if direction == "positive" and predicted_move > 0.02:
            action = "买入"
            reasoning = "预期差正面，催化剂强度足够"
            timing = f"事件前{prep_days}天内入场"
            exit_timing = f"事件后{reaction_days}天内出场"
        elif direction == "negative" and predicted_move < -0.02:
            action = "卖出"
            reasoning = "预期差负面，存在下行风险"
            timing = "事件前立即入场"
            exit_timing = "事件后1-2天内出场"
        else:
            action = "观望"
            reasoning = "预期差不足或方向不明确"
            timing = "不参与"
            exit_timing = "N/A"
        
        # 风险控制
        stop_loss = abs(predicted_move) * 0.6  # 止损为预期收益的60%
        take_profit = abs(predicted_move) * 1.2  # 止盈为预期收益的120%
        
        risk_reward = take_profit / stop_loss if stop_loss > 0 else 0
        
        return {
            "recommended_action": action,
            "reasoning": reasoning,
            "timing_recommendation": {
                "entry": timing,
                "exit": exit_timing,
                "holding_period": f"{prep_days + reaction_days}天"
            },
            "risk_management": {
                "stop_loss_pct": -stop_loss,
                "take_profit_pct": take_profit,
                "risk_reward_ratio": risk_reward,
                "position_size_suggestion": "单事件不超过总资金5%"
            },
            "monitoring_points": [
                "事件前1天市场情绪",
                "事件当天公告内容",
                "事件后市场初始反应",
                "交易量变化"
            ]
        }
    
    def _calculate_event_priority(self, event: Dict) -> float:
        """计算事件优先级分数"""
        # 基础分数
        base_score = 5.0
        
        # 事件类型加分
        event_type = event.get("event_type", "")
        importance = self.event_types.get(event_type, {}).get("importance", 3)
        type_score = importance * 0.5
        
        # 催化剂强度加分
        catalyst = event.get("catalyst_strength", 3)
        catalyst_score = catalyst * 0.3
        
        # 分析师覆盖度加分
        analysts = event.get("analyst_count", 5)
        analyst_score = min(2.0, analysts / 10.0)
        
        # 时间紧迫性（越近越高）
        event_date = datetime.strptime(event["event_date"], "%Y-%m-%d")
        days_to_event = (event_date - datetime.now()).days
        time_score = max(0, 3.0 - days_to_event * 0.3)
        
        return base_score + type_score + catalyst_score + analyst_score + time_score
    
    def _generate_quick_analysis(self, event: Dict) -> str:
        """生成快速分析"""
        event_type = event.get("event_type", "")
        stock = event.get("stock", "")
        catalyst = event.get("catalyst_strength", 3)
        
        if event_type == "earnings":
            return f"{stock}财报，催化剂强度{catalyst}/5，关注预期差"
        elif event_type == "policy":
            return f"{stock}政策受益，催化剂强度{catalyst}/5，关注细则内容"
        elif event_type == "product_launch":
            return f"{stock}新品发布，催化剂强度{catalyst}/5，关注市场反响"
        else:
            return f"{stock}{event_type}事件，催化剂强度{catalyst}/5"
    
    def _generate_event_statistics(self, events: List) -> Dict:
        """生成事件统计"""
        if not events:
            return {}
        
        by_type = {}
        by_sector = {}
        
        for event in events:
            # 按类型统计
            e_type = event["event_type"]
            by_type[e_type] = by_type.get(e_type, 0) + 1
            
            # 按行业统计
            stock = event["stock"]
            sector = self.sector_mapping.get(stock, "其他")
            by_sector[sector] = by_sector.get(sector, 0) + 1
        
        return {
            "by_event_type": by_type,
            "by_sector": by_sector,
            "avg_priority_score": statistics.mean(e["priority_score"] for e in events) if events else 0,
            "high_impact_count": sum(1 for e in events if e["importance"] >= 4),
            "time_distribution": {
                "within_3_days": sum(1 for e in events if e["days_to_event"] <= 3),
                "4_7_days": sum(1 for e in events if 4 <= e["days_to_event"] <= 7)
            }
        }
    
    def _recommend_focus_areas(self, events: List) -> List[str]:
        """推荐关注领域"""
        if not events:
            return ["近期无重要事件"]
        
        # 按优先级排序
        top_events = sorted(events, key=lambda x: x["priority_score"], reverse=True)[:3]
        
        recommendations = []
        for event in top_events:
            rec = f"{event['stock']}的{event['event_name']}（{event['event_date']}）"
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_lessons_learned(self, event_type: str) -> List[str]:
        """生成经验教训"""
        lessons = {
            "earnings": [
                "财报前股价往往反映预期，入场时机关键",
                "关注营收增长而不仅是EPS",
                "管理层电话会议内容比财报数字更重要",
                "同行业公司财报具有预示作用"
            ],
            "merger": [
                "公告后第一个小时反应最强烈",
                "关注并购溢价率和协同效应",
                "监管审批风险是主要不确定性",
                "套利空间随时间递减"
            ],
            "policy": [
                "政策细则比框架更重要",
                "关注地方政府配套政策",
                "受益公司需有实质业务支撑",
                "避免追高政策概念股"
            ]
        }
        
        return lessons.get(event_type, [
            "事件驱动交易需严格控制仓位",
            "设置明确止损点",
            "关注事件后的持续反应",
            "避免过度交易"
        ])
    
    def _simulate_price_reaction(self, days_since_event: int) -> Dict:
        """模拟价格反应"""
        # 简化的价格反应曲线
        if days_since_event < 0:
            return {"stage": "pre_event", "price_change": 0.0, "volatility": 1.0}
        elif days_since_event == 0:
            return {"stage": "event_day", "price_change": 0.03, "volatility": 2.5}
        elif days_since_event == 1:
            return {"stage": "day_1", "price_change": 0.015, "volatility": 1.8}
        elif days_since_event == 2:
            return {"stage": "day_2", "price_change": 0.005, "volatility": 1.3}
        elif days_since_event >= 3:
            return {"stage": "post_event", "price_change": 0.002, "volatility": 1.1}
        else:
            return {"stage": "unknown", "price_change": 0.0, "volatility": 1.0}
    
    def _determine_reaction_stage(self, days_since_event: int) -> str:
        """确定反应阶段"""
        if days_since_event < 0:
            return "事件前"
        elif days_since_event == 0:
            return "事件当日"
        elif 1 <= days_since_event <= 2:
            return "即时反应期"
        elif 3 <= days_since_event <= 5:
            return "消化调整期"
        else:
            return "后事件期"
    
    def _generate_trading_implications(self, days_since_event: int, price_reaction: Dict) -> List[str]:
        """生成交易启示"""
        if days_since_event < 0:
            return ["等待事件发生", "观察市场预期变化", "准备交易计划"]
        elif days_since_event == 0:
            return ["关注公告细节", "评估初始市场反应", "决定是否入场"]
        elif days_since_event == 1:
            return ["评估持续反应", "调整仓位", "设置止损"]
        elif days_since_event >= 2:
            return ["考虑获利了结", "评估后续催化剂", "转向下一个事件"]
        else:
            return ["持续监控", "记录经验教训"]
    
    def _generate_single_signal(self, event: Dict, portfolio_context: Dict, risk_tolerance: int, capital: float) -> Optional[Dict]:
        """生成单个交易信号"""
        # 计算信号强度
        priority = self._calculate_event_priority(event)
        if priority < 6.0:
            return None
        
        # 确定交易方向
        event_type = event.get("event_type", "")
        if event_type in ["earnings", "policy", "fda_approval", "product_launch"]:
            direction = "买入"
        elif event_type == "merger":
            direction = "套利"  # 并购套利
        else:
            direction = "观察"
        
        # 计算仓位大小
        position_size_pct = min(0.05, 0.02 + (priority - 6.0) * 0.005)  # 最大5%
        position_size = capital * position_size_pct
        
        # 风险调整
        if risk_tolerance <= 2:
            position_size *= 0.5
        elif risk_tolerance >= 4:
            position_size *= 1.2
        
        return {
            "signal_id": f"SIG_{event['id']}",
            "event_id": event["id"],
            "stock": event["stock"],
            "event_type": event_type,
            "event_name": self.event_types.get(event_type, {}).get("name", event_type),
            "event_date": event["event_date"],
            "direction": direction,
            "signal_strength": priority / 10.0,
            "position_size": position_size,
            "position_size_pct": position_size_pct,
            "entry_timing": f"事件前{self.event_types.get(event_type, {}).get('prep_days', 2)}天",
            "exit_timing": f"事件后{self.event_types.get(event_type, {}).get('reaction_days', 3)}天",
            "stop_loss_pct": -0.025,
            "take_profit_pct": 0.05,
            "risk_reward_ratio": 2.0
        }
    
    def _optimize_signal_portfolio(self, signals: List[Dict], capital: float, risk_tolerance: int) -> List[Dict]:
        """优化信号组合"""
        if not signals:
            return []
        
        # 按信号强度排序
        sorted_signals = sorted(signals, key=lambda x: x["signal_strength"], reverse=True)
        
        # 根据风险容忍度选择信号数量
        max_signals = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6}.get(risk_tolerance, 4)
        selected_signals = sorted_signals[:max_signals]
        
        # 检查行业集中度
        sector_counts = {}
        optimized_signals = []
        
        for signal in selected_signals:
            stock = signal["stock"]
            sector = self.sector_mapping.get(stock, "其他")
            
            # 限制单一行业暴露
            if sector_counts.get(sector, 0) >= 2 and len(selected_signals) > 2:
                # 跳过，添加替代信号
                continue
            
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
            optimized_signals.append(signal)
        
        # 调整仓位大小以确保总仓位不超过限制
        total_position = sum(s["position_size"] for s in optimized_signals)
        if total_position > capital * 0.25:  # 最大总仓位25%
            scale_factor = capital * 0.25 / total_position
            for signal in optimized_signals:
                signal["position_size"] *= scale_factor
                signal["position_size_pct"] *= scale_factor
        
        return optimized_signals
    
    def _generate_execution_plan(self, signals: List[Dict]) -> Dict:
        """生成执行计划"""
        if not signals:
            return {"plan": "无信号", "timeline": []}
        
        # 按事件日期排序
        signals_by_date = sorted(signals, key=lambda x: x["event_date"])
        
        timeline = []
        for signal in signals_by_date:
            event_date = datetime.strptime(signal["event_date"], "%Y-%m-%d")
            prep_days = self.event_types.get(signal["event_type"], {}).get("prep_days", 2)
            entry_date = event_date - timedelta(days=prep_days)
            
            timeline.append({
                "date": entry_date.strftime("%Y-%m-%d"),
                "action": f"{signal['direction']} {signal['stock']}",
                "position_size": signal["position_size"],
                "event_date": signal["event_date"],
                "notes": signal["event_name"]
            })
        
        return {
            "total_signals": len(signals),
            "total_capital_allocated": sum(s["position_size"] for s in signals),
            "capital_allocation_pct": sum(s["position_size_pct"] for s in signals) * 100,
            "execution_timeline": timeline,
            "risk_controls": [
                "单个信号最大损失2.5%",
                "总仓位不超过25%",
                "事件后3天内必须评估",
                "严格执行止损纪律"
            ]
        }
    
    def _generate_monitoring_requirements(self, signals: List[Dict]) -> List[str]:
        """生成监控要求"""
        requirements = []
        
        for signal in signals:
            req = f"{signal['stock']} ({signal['event_date']}): 监控{signal['event_name']}反应"
            requirements.append(req)
        
        if requirements:
            requirements.append("每日收盘后评估信号表现")
            requirements.append("事件发生后立即调整策略")
        
        return requirements
    
    def _calculate_time_to_event(self, event_date_str: str) -> str:
        """计算距离事件时间"""
        try:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
            today = datetime.now()
            
            if event_date < today:
                days_passed = (today - event_date).days
                return f"已过去{days_passed}天"
            else:
                days_to_event = (event_date - today).days
                return f"还有{days_to_event}天"
        except:
            return "日期格式错误"
    
    def _assess_event_risk(self, event_info: Dict, expectation_gap: Dict) -> Dict:
        """评估事件风险"""
        event_type = event_info.get("event_type", "")
        
        base_risk = {
            "earnings": 0.6,
            "merger": 0.7,
            "policy": 0.5,
            "fda_approval": 0.8,
            "management_change": 0.4,
            "product_launch": 0.5
        }.get(event_type, 0.5)
        
        # 预期差调整
        gap_pct = expectation_gap.get("expectation_gap_pct", 0)
        if abs(gap_pct) > 0.05:
            risk_adjustment = 1.2
        elif abs(gap_pct) > 0.02:
            risk_adjustment = 1.0
        else:
            risk_adjustment = 0.8
        
        total_risk = base_risk * risk_adjustment
        
        # 风险评级
        if total_risk >= 0.8:
            rating = "高风险"
            color = "red"
        elif total_risk >= 0.6:
            rating = "中高风险"
            color = "orange"
        elif total_risk >= 0.4:
            rating = "中等风险"
            color = "yellow"
        else:
            rating = "低风险"
            color = "green"
        
        return {
            "base_risk": base_risk,
            "adjustment_factor": risk_adjustment,
            "total_risk": total_risk,
            "risk_rating": rating,
            "color_code": color,
            "key_risk_factors": self._identify_key_risk_factors(event_info),
            "mitigation_strategies": [
                "严格仓位控制",
                "设置止损点",
                "分散事件类型",
                "准备应急计划"
            ]
        }
    
    def _identify_key_risk_factors(self, event_info: Dict) -> List[str]:
        """识别关键风险因素"""
        event_type = event_info.get("event_type", "")
        
        risk_factors = []
        
        if event_type == "earnings":
            risk_factors.extend(["营收不及预期", "毛利率下降", "指引下调"])
        elif event_type == "merger":
            risk_factors.extend(["监管否决", "融资困难", "协同效应不足"])
        elif event_type == "policy":
            risk_factors.extend(["细则不及预期", "执行力度弱", "受益范围小"])
        
        risk_factors.append("市场整体风险")
        risk_factors.append("流动性风险")
        
        return risk_factors
    
    def _get_historical_context(self, stock_code: str, event_type: str) -> Dict:
        """获取历史背景"""
        # 简化历史背景
        return {
            "historical_performance": {
                "last_3_events": {"avg_return": 0.042, "win_rate": 0.67},
                "same_event_type_history": {"avg_return": 0.038, "win_rate": 0.65},
                "seasonality_pattern": "Q1财报通常表现较好"
            },
            "market_context": {
                "current_environment": "震荡上行",
                "sector_trend": self.sector_mapping.get(stock_code, "未知"),
                "volatility_regime": "中等"
            },
            "comparative_analysis": f"{stock_code}在同类事件中表现优于{65}%的同行"
        }
    
    def _success_response(self, action: str, result: Dict, params: Dict) -> Dict:
        """成功响应"""
        return {
            "success": True,
            "skill": "event_driven_strategy_skill",
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
            "skill": "event_driven_strategy_skill",
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
        
        # 执行事件驱动策略
        strategy = EventDrivenStrategy()
        result = strategy.execute(params)
        
        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except json.JSONDecodeError as e:
        error_result = {
            "success": False,
            "skill": "event_driven_strategy_skill",
            "version": "1.0.0",
            "error": f"JSON解析错误: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
    except Exception as e:
        error_result = {
            "success": False,
            "skill": "event_driven_strategy_skill",
            "version": "1.0.0",
            "error": f"事件驱动策略过程出错: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()