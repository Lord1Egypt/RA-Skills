#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析器 - 统一分析接口
功能：整合所有股票分析能力，提供统一的分析接口
"""

import sys
sys.path.insert(0, '.')

from a_stock_watcher import get_stock_realtime, get_technical_analysis
from historical_data import get_stock_history
from technical_analysis import analyze_technical, format_analysis_report
from stock_cache import StockCache
from health_check import DataSourceHealth
from datetime import datetime
from typing import Dict, List, Optional

class StockAnalyzer:
    """股票分析器 - 统一分析接口"""
    
    def __init__(self):
        """初始化分析器"""
        self.cache = StockCache()
        self.health_checker = DataSourceHealth()
    
    def get_price(self, stock_code: str, use_cache: bool = True) -> Dict:
        """
        获取实时行情
        
        Args:
            stock_code: 股票代码
            use_cache: 是否使用缓存
        
        Returns:
            行情数据字典
        """
        # 检查缓存
        if use_cache:
            cached = self.cache.get(stock_code)
            if cached:
                return cached
        
        # 获取健康数据源
        best_source = self.health_checker.get_best_source()
        
        # 获取实时数据
        data = get_stock_realtime(stock_code, prefer_source=best_source)
        
        # 保存到缓存
        if data.get('success'):
            self.cache.set(stock_code, data)
        
        return data
    
    def get_technical(self, stock_code: str) -> str:
        """
        获取技术分析
        
        Args:
            stock_code: 股票代码
        
        Returns:
            技术分析报告字符串
        """
        return get_technical_analysis(stock_code)
    
    def get_finance(self, stock_code: str) -> Dict:
        """
        获取财务数据（简化版）
        
        Args:
            stock_code: 股票代码
        
        Returns:
            财务数据字典
        """
        # TODO: 集成 Tushare API
        return {
            'success': True,
            'code': stock_code,
            'message': '财务数据功能开发中',
            'data': {}
        }
    
    def get_history(self, stock_code: str, days: int = 60) -> Dict:
        """
        获取历史数据
        
        Args:
            stock_code: 股票代码
            days: 天数
        
        Returns:
            历史数据字典
        """
        return get_stock_history(stock_code, days=days)
    
    def full_analysis(self, stock_code: str) -> str:
        """
        完整分析（一键获取）
        
        Args:
            stock_code: 股票代码
        
        Returns:
            完整分析报告字符串
        """
        print(f"正在分析 {stock_code}...")
        
        # 获取实时行情
        price_data = self.get_price(stock_code)
        
        # 获取技术分析
        technical_report = self.get_technical(stock_code)
        
        # 组合报告
        report = []
        report.append("=" * 70)
        report.append(f"{price_data.get('name', stock_code)} ({stock_code}) 完整分析报告")
        report.append(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 70)
        
        if price_data.get('success'):
            report.append("\n【实时行情】")
            report.append(f"现价：¥{price_data['current_price']:.2f}")
            report.append(f"涨跌：{price_data['change']:+.2f} ({price_data['change_pct']:+.2f}%)")
            report.append(f"成交：{price_data.get('volume', 0):,}手")
        
        report.append("\n" + technical_report)
        
        return "\n".join(report)
    
    def compare(self, stock_codes: List[str]) -> str:
        """
        股票对比分析
        
        Args:
            stock_codes: 股票代码列表
        
        Returns:
            对比报告字符串
        """
        if len(stock_codes) < 2:
            return "❌ 至少需要两只股票进行对比"
        
        print(f"正在对比：{', '.join(stock_codes)}")
        
        # 获取所有股票数据
        stocks_data = []
        for code in stock_codes:
            data = self.get_price(code)
            if data.get('success'):
                stocks_data.append(data)
        
        if len(stocks_data) < 2:
            return "❌ 获取股票数据失败"
        
        # 生成对比报告
        report = []
        report.append("=" * 80)
        report.append("股票对比分析报告")
        report.append(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"对比股票：{len(stocks_data)}只")
        report.append("=" * 80)
        
        # 基本信息对比表
        report.append("\n【基本信息对比】")
        report.append("-" * 80)
        header = f"{'股票':<15} {'现价':<10} {'涨跌':<12} {'涨幅':<10} {'成交 (万手)':<12} {'成交额 (亿)':<10}"
        report.append(header)
        report.append("-" * 80)
        
        for stock in stocks_data:
            name = f"{stock['name']} ({stock['code']})"
            price = f"¥{stock['current_price']:.2f}"
            change = f"{stock['change']:+.2f}"
            change_pct = f"{stock['change_pct']:+.2f}%"
            volume = f"{stock.get('volume', 0)/10000:.1f}"
            amount = f"{stock.get('amount', 0)/100000000:.2f}"
            
            report.append(f"{name:<15} {price:<10} {change:<12} {change_pct:<10} {volume:<12} {amount:<10}")
        
        # 涨跌幅排名
        report.append("\n【涨跌幅排名】")
        report.append("-" * 80)
        sorted_stocks = sorted(stocks_data, key=lambda x: x['change_pct'], reverse=True)
        
        for i, stock in enumerate(sorted_stocks, 1):
            icon = "📈" if stock['change_pct'] > 0 else "📉" if stock['change_pct'] < 0 else "➖"
            report.append(f"{i}. {icon} {stock['name']} ({stock['code']}): {stock['change_pct']:+.2f}%")
        
        # 估值对比
        report.append("\n【估值对比】")
        report.append("-" * 80)
        report.append("注：以下数据为示例，实际数据需要接入 Tushare API")
        
        for stock in stocks_data:
            report.append(f"\n{stock['name']} ({stock['code']}):")
            report.append(f"  PE(市盈率): N/A (待接入)")
            report.append(f"  PB(市净率): N/A (待接入)")
            report.append(f"  ROE: N/A (待接入)")
        
        # 技术面对比
        report.append("\n【技术面对比】")
        report.append("-" * 80)
        
        for stock in stocks_data:
            report.append(f"\n{stock['name']} ({stock['code']}):")
            # 简化技术分析
            if stock['change_pct'] > 2:
                report.append(f"  趋势：📈 强势上涨")
            elif stock['change_pct'] > 0:
                report.append(f"  趋势：📈 温和上涨")
            elif stock['change_pct'] > -2:
                report.append(f"  趋势：➖ 震荡整理")
            else:
                report.append(f"  趋势：📉 下跌")
        
        # 投资建议
        report.append("\n【投资建议】")
        report.append("-" * 80)
        
        best = sorted_stocks[0]
        worst = sorted_stocks[-1]
        
        report.append(f"🏆 最强股票：{best['name']} ({best['change_pct']:+.2f}%)")
        report.append(f"📉 最弱股票：{worst['name']} ({worst['change_pct']:+.2f}%)")
        report.append("\n建议：")
        report.append(f"• 关注强势股：{best['name']}")
        report.append(f"• 谨慎对待弱势股：{worst['name']}")
        report.append(f"• 分散投资，降低风险")
        
        report.append("\n" + "=" * 80)
        report.append("⚠️ 风险提示：以上分析仅供参考，不构成投资建议")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def risk_assessment(self, stock_code: str) -> Dict:
        """
        风险评估
        
        Args:
            stock_code: 股票代码
        
        Returns:
            风险评估字典
        """
        data = self.get_price(stock_code)
        
        if not data.get('success'):
            return {'success': False, 'error': '获取数据失败'}
        
        change_pct = abs(data['change_pct'])
        
        # 风险等级判断
        if change_pct > 7:
            risk_level = 'high'
            risk_desc = '高风险 - 大幅波动'
        elif change_pct > 3:
            risk_level = 'medium'
            risk_desc = '中风险 - 正常波动'
        else:
            risk_level = 'low'
            risk_desc = '低风险 - 波动较小'
        
        return {
            'success': True,
            'code': stock_code,
            'risk_level': risk_level,
            'risk_desc': risk_desc,
            'volatility': change_pct,
            'suggestion': '建议设置止损位' if risk_level == 'high' else '正常持有'
        }


# 测试
if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    
    analyzer = StockAnalyzer()
    
    print("=" * 70)
    print("股票分析器测试")
    print("=" * 70)
    
    # 测试 1：获取行情
    print("\n[测试 1] 获取实时行情")
    print("-" * 70)
    data = analyzer.get_price('002892')
    if data.get('success'):
        print(f"✅ {data['name']} ({data['code']})")
        print(f"   现价：¥{data['current_price']:.2f}")
        print(f"   涨跌：{data['change']:+.2f} ({data['change_pct']:+.2f}%)")
    
    # 测试 2：股票对比
    print("\n[测试 2] 股票对比分析")
    print("-" * 70)
    report = analyzer.compare(['002892', '600036', '300059'])
    print(report)
    
    # 测试 3：风险评估
    print("\n[测试 3] 风险评估")
    print("-" * 70)
    risk = analyzer.risk_assessment('002892')
    if risk.get('success'):
        print(f"风险等级：{risk['risk_level']}")
        print(f"风险描述：{risk['risk_desc']}")
        print(f"波动率：{risk['volatility']:.2f}%")
        print(f"建议：{risk['suggestion']}")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
