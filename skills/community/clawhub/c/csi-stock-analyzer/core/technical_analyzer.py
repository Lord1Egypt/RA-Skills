#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术分析模块 - 分析MACD、KDJ、RSI、EMA等技术指标，给出买卖点建议
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    def __init__(self):
        # 指标权重配置
        self.indicator_weights = {
            'macd': 0.25,
            'kdj': 0.25,
            'rsi': 0.20,
            'ema': 0.30
        }
    
    def analyze_trading_signals(self, indicators: Dict) -> Dict:
        """
        综合分析技术指标，给出买卖点建议
        :param indicators: 技术指标数据（来自data_fetcher.get_technical_indicators）
        :return: 分析结果
        """
        analysis = {}
        
        # 1. MACD分析
        analysis['macd'] = self._analyze_macd(indicators['macd'])
        
        # 2. KDJ分析
        analysis['kdj'] = self._analyze_kdj(indicators['kdj'])
        
        # 3. RSI分析
        analysis['rsi'] = self._analyze_rsi(indicators['rsi'])
        
        # 4. EMA分析
        analysis['ema'] = self._analyze_ema(indicators['ema'])
        
        # 5. 综合评分和建议
        analysis['comprehensive'] = self._comprehensive_analysis(analysis)
        
        return analysis
    
    def _analyze_macd(self, macd_data: Dict) -> Dict:
        """分析MACD指标"""
        dif = macd_data['dif']
        dea = macd_data['dea']
        macd = macd_data['macd']
        golden_cross = macd_data['golden_cross']
        death_cross = macd_data['death_cross']
        trend = macd_data['trend']
        
        score = 50  # 中性
        signal = 'hold'
        details = []
        
        if golden_cross:
            score += 30
            signal = 'buy'
            details.append("MACD出现金叉，看涨信号")
        if death_cross:
            score -= 30
            signal = 'sell'
            details.append("MACD出现死叉，看跌信号")
        
        if macd > 0:
            score += 10
            details.append("MACD柱为正，多头市场")
        else:
            score -= 10
            details.append("MACD柱为负，空头市场")
        
        if dif > 0 and dea > 0:
            score += 10
            details.append("DIF和DEA均在零轴上方，强势市场")
        elif dif < 0 and dea < 0:
            score -= 10
            details.append("DIF和DEA均在零轴下方，弱势市场")
        
        # 背离判断（需要更多历史数据，暂简化）
        if trend == 'up' and macd < 0:
            details.append("潜在底背离信号，关注反弹机会")
        elif trend == 'down' and macd > 0:
            details.append("潜在顶背离信号，注意回调风险")
        
        rating = '强烈看多' if score >= 80 else '看多' if score >= 60 else '中性' if score >= 40 else '看空' if score >= 20 else '强烈看空'
        
        return {
            'score': max(0, min(100, score)),
            'signal': signal,
            'rating': rating,
            'details': details,
            'dif': dif,
            'dea': dea,
            'macd': macd,
            'golden_cross': golden_cross,
            'death_cross': death_cross
        }
    
    def _analyze_kdj(self, kdj_data: Dict) -> Dict:
        """分析KDJ指标"""
        k = kdj_data['k']
        d = kdj_data['d']
        j = kdj_data['j']
        golden_cross = kdj_data['golden_cross']
        death_cross = kdj_data['death_cross']
        oversold = kdj_data['oversold']
        overbought = kdj_data['overbought']
        
        score = 50
        signal = 'hold'
        details = []
        
        if golden_cross:
            score += 25
            signal = 'buy'
            details.append("KDJ出现金叉，短期看涨")
        if death_cross:
            score -= 25
            signal = 'sell'
            details.append("KDJ出现死叉，短期看跌")
        
        if oversold:
            score += 20
            details.append(f"J值{j:.1f}，处于超卖区间，可能反弹")
        if overbought:
            score -= 20
            details.append(f"J值{j:.1f}，处于超买区间，可能回调")
        
        if k > d:
            score += 10
            details.append("K线在D线上方，短期趋势向上")
        else:
            score -= 10
            details.append("K线在D线下方，短期趋势向下")
        
        # KDJ区间判断
        if j < 20:
            score += 10
        elif j > 80:
            score -= 10
        
        rating = '强烈看多' if score >= 80 else '看多' if score >= 60 else '中性' if score >= 40 else '看空' if score >= 20 else '强烈看空'
        
        return {
            'score': max(0, min(100, score)),
            'signal': signal,
            'rating': rating,
            'details': details,
            'k': k,
            'd': d,
            'j': j,
            'golden_cross': golden_cross,
            'death_cross': death_cross,
            'oversold': oversold,
            'overbought': overbought
        }
    
    def _analyze_rsi(self, rsi_data: Dict) -> Dict:
        """分析RSI指标"""
        rsi = rsi_data['rsi14']
        oversold = rsi_data['oversold']
        overbought = rsi_data['overbought']
        trend = rsi_data['trend']
        
        score = 50
        signal = 'hold'
        details = []
        
        if oversold:
            score += 25
            signal = 'buy'
            details.append(f"RSI {rsi:.1f}，处于超卖区间，反弹概率大")
        if overbought:
            score -= 25
            signal = 'sell'
            details.append(f"RSI {rsi:.1f}，处于超买区间，回调概率大")
        
        if rsi > 50:
            score += 10
            details.append("RSI在50以上，多头占优")
        else:
            score -= 10
            details.append("RSI在50以下，空头占优")
        
        if trend == 'up':
            score += 10
            details.append("RSI趋势向上，动量增强")
        else:
            score -= 10
            details.append("RSI趋势向下，动量减弱")
        
        # RSI区间
        if 40 <= rsi <= 60:
            details.append("RSI处于中性区间，方向不明")
        
        rating = '强烈看多' if score >= 80 else '看多' if score >= 60 else '中性' if score >= 40 else '看空' if score >= 20 else '强烈看空'
        
        return {
            'score': max(0, min(100, score)),
            'signal': signal,
            'rating': rating,
            'details': details,
            'rsi14': rsi,
            'oversold': oversold,
            'overbought': overbought,
            'trend': trend
        }
    
    def _analyze_ema(self, ema_data: Dict) -> Dict:
        """分析EMA均线系统"""
        ema5 = ema_data['ema5']
        ema10 = ema_data['ema10']
        ema20 = ema_data['ema20']
        ema60 = ema_data['ema60']
        bullish_arrangement = ema_data['bullish_arrangement']
        bearish_arrangement = ema_data['bearish_arrangement']
        price_above_ema20 = ema_data['price_above_ema20']
        price_above_ema60 = ema_data['price_above_ema60']
        
        score = 50
        signal = 'hold'
        details = []
        
        if bullish_arrangement:
            score += 35
            signal = 'buy'
            details.append("均线多头排列（价格>EMA20>EMA60），强势上涨趋势")
        if bearish_arrangement:
            score -= 35
            signal = 'sell'
            details.append("均线空头排列（价格<EMA20<EMA60），弱势下跌趋势")
        
        if price_above_ema20:
            score += 15
            details.append("价格在EMA20上方，短期趋势向上")
        else:
            score -= 15
            details.append("价格在EMA20下方，短期趋势向下")
        
        if price_above_ema60:
            score += 20
            details.append("价格在EMA60上方，中长期趋势向上")
        else:
            score -= 20
            details.append("价格在EMA60下方，中长期趋势向下")
        
        # 短期均线排列
        if ema5 > ema10 > ema20:
            score += 10
            details.append("短期均线多头排列，短期强势")
        elif ema5 < ema10 < ema20:
            score -= 10
            details.append("短期均线空头排列，短期弱势")
        
        rating = '强烈看多' if score >= 80 else '看多' if score >= 60 else '中性' if score >= 40 else '看空' if score >= 20 else '强烈看空'
        
        return {
            'score': max(0, min(100, score)),
            'signal': signal,
            'rating': rating,
            'details': details,
            'ema5': ema5,
            'ema10': ema10,
            'ema20': ema20,
            'ema60': ema60,
            'bullish_arrangement': bullish_arrangement,
            'bearish_arrangement': bearish_arrangement,
            'price_above_ema20': price_above_ema20,
            'price_above_ema60': price_above_ema60
        }
    
    def _comprehensive_analysis(self, indicator_analysis: Dict) -> Dict:
        """综合所有指标给出建议"""
        total_score = 0
        signals = []
        
        for indicator, weight in self.indicator_weights.items():
            score = indicator_analysis[indicator]['score']
            total_score += score * weight
            signals.append(indicator_analysis[indicator]['signal'])
        
        total_score = round(total_score, 2)
        
        # 统计信号
        buy_count = signals.count('buy')
        sell_count = signals.count('sell')
        hold_count = signals.count('hold')
        
        # 综合建议
        if total_score >= 70:
            recommendation = '买入'
            action = '建议逢低买入，持仓待涨'
        elif total_score >= 55:
            recommendation = '增持'
            action = '建议逐步建仓，持股为主'
        elif total_score >= 45:
            recommendation = '持有'
            action = '建议持有观望，高抛低吸'
        elif total_score >= 30:
            recommendation = '减持'
            action = '建议逢高减持，控制仓位'
        else:
            recommendation = '卖出'
            action = '建议卖出离场，回避风险'
        
        # 风险提示
        risk_level = '低' if total_score >= 70 else '中低' if total_score >= 55 else '中' if total_score >= 45 else '中高' if total_score >= 30 else '高'
        
        return {
            'total_score': total_score,
            'recommendation': recommendation,
            'action': action,
            'risk_level': risk_level,
            'signal_summary': {
                'buy': buy_count,
                'sell': sell_count,
                'hold': hold_count
            },
            'indicator_scores': {
                'macd': indicator_analysis['macd']['score'],
                'kdj': indicator_analysis['kdj']['score'],
                'rsi': indicator_analysis['rsi']['score'],
                'ema': indicator_analysis['ema']['score']
            }
        }
    
    def generate_trading_report(self, analysis_result: Dict) -> str:
        """生成技术分析报告"""
        comp = analysis_result['comprehensive']
        
        report = [
            "📊 技术指标分析报告",
            "=" * 40,
            f"综合评分：{comp['total_score']}/100",
            f"投资建议：{comp['recommendation']}",
            f"操作策略：{comp['action']}",
            f"风险等级：{comp['risk_level']}",
            f"信号分布：买入{comp['signal_summary']['buy']}个，卖出{comp['signal_summary']['sell']}个，中性{comp['signal_summary']['hold']}个",
            "",
            "📈 各指标评分：",
            f"MACD: {comp['indicator_scores']['macd']}分 - {analysis_result['macd']['rating']}",
            f"KDJ: {comp['indicator_scores']['kdj']}分 - {analysis_result['kdj']['rating']}",
            f"RSI: {comp['indicator_scores']['rsi']}分 - {analysis_result['rsi']['rating']}",
            f"EMA: {comp['indicator_scores']['ema']}分 - {analysis_result['ema']['rating']}",
            "",
            "🔍 详细信号："
        ]
        
        for indicator in ['macd', 'kdj', 'rsi', 'ema']:
            report.append(f"\n{indicator.upper()} 信号：")
            for detail in analysis_result[indicator]['details']:
                report.append(f"  • {detail}")
        
        report.append("\n⚠️ 免责声明：技术分析仅供参考，不构成投资建议。")
        
        return "\n".join(report)
