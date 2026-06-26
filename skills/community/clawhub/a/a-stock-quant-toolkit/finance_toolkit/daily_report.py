#!/usr/bin/env python3
"""
每日A股市场分析报告
输出: 热门板块、个股信号、技术指标分析
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import traceback

from astock_data import AStockDataFetcher
from astock_strategies import AStockStrategies

def generate_daily_report():
    """生成A股每日分析报告"""
    fetcher = AStockDataFetcher()
    strategies = AStockStrategies()
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=120)).strftime("%Y%m%d")

    report = {
        'report_time': report_time,
        'market_overview': {},
        'hot_stocks': [],
        'watch_list': [],
        'strategy_signals': [],
        'technical_analysis': []
    }

    try:
        # 1. 市场概览 - 大盘指数
        print("📊 获取市场概览...")
        indexes = {
            '上证指数': 'sh000001',
            '深证成指': 'sz399001',
            '创业板指': 'sz399006',
            '沪深300': 'sh000300'
        }
        for name, code in indexes.items():
            df = fetcher.get_index_data(code, start_date="20260101")
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                prev = df.iloc[-2] if len(df) > 1 else latest
                change = (latest['close'] - prev['close']) / prev['close'] * 100
                report['market_overview'][name] = {
                    'latest': round(float(latest['close']), 2),
                    'change_pct': round(float(change), 2)
                }
                print(f"  {name}: {latest['close']:.2f} ({change:+.2f}%)")

        # 2. 热门股票Top20
        print("📈 获取热门股票...")
        hot = fetcher.get_hot_stocks(20)
        if hot is not None:
            for _, row in hot.iterrows():
                report['hot_stocks'].append({
                    'code': row.get('代码',''),
                    'name': row.get('名称',''),
                    'price': float(row.get('最新价',0)),
                    'change_pct': float(row.get('涨跌幅',0)),
                    'volume': float(row.get('成交额',0)),
                    'turnover': float(row.get('换手率',0))
                })

        # 3. 概念板块Top10
        print("🏷️ 获取概念板块...")
        board = fetcher.get_concept_board()
        if board is not None:
            top_boards = board.sort_values('涨跌幅', ascending=False).head(10)
            report['hot_concepts'] = top_boards[['板块名称','涨跌幅','上涨家数','下跌家数']].to_dict('records')

        # 4. 策略信号 - 对热门股票做技术分析
        print("🔍 分析策略信号...")
        for stock in report['hot_stocks'][:10]:
            code = str(stock['code'])
            hist = fetcher.get_history(code, start_date=start_date)
            if hist is not None and len(hist) > 30:
                # 重命名列
                hist = hist.rename(columns={
                    '日期': 'date', '开盘': 'open', '收盘': 'close',
                    '最高': 'high', '最低': 'low', '成交量': 'volume'
                })
                hist['收盘'] = pd.to_numeric(hist['close'], errors='coerce')
                hist['成交量'] = pd.to_numeric(hist['volume'], errors='coerce')

                signals = []
                # MACD
                macd_df = strategies.macd_strategy(hist)
                if macd_df is not None and len(macd_df) > 1:
                    macd_signal = macd_df['signal'].iloc[-1]
                    signals.append(f"MACD={'📈多头' if macd_signal > 0 else '📉空头'}")

                # RSI
                rsi_df = strategies.rsi_strategy(hist)
                if rsi_df is not None and 'RSI' in rsi_df.columns:
                    rsi_val = rsi_df['RSI'].iloc[-1]
                    signals.append(f"RSI={rsi_val:.0f}")
                    if rsi_val < 30:
                        signals.append("⚡超卖")
                    elif rsi_val > 70:
                        signals.append("⚠️超买")

                # Bollinger
                boll_df = strategies.bollinger_strategy(hist)
                if boll_df is not None:
                    pos = boll_df['signal'].iloc[-1]
                    if pos > 0:
                        signals.append("📉触下轨")
                    elif pos < 0:
                        signals.append("📈触上轨")

                report['strategy_signals'].append({
                    'code': code,
                    'name': stock['name'],
                    'price': stock['price'],
                    'signals': ' | '.join(signals)
                })

        return report

    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        traceback.print_exc()
        return report

def format_report_for_fei(report):
    """格式化为飞书消息格式"""
    lines = []
    lines.append(f"📊 **A股市场日报**")
    lines.append(f"🕐 {report['report_time']}\n")

    if report['market_overview']:
        lines.append("**📈 大盘指数**")
        for name, data in report['market_overview'].items():
            arrow = '🟢' if data['change_pct'] >= 0 else '🔴'
            lines.append(f"{arrow} {name}: {data['latest']} ({data['change_pct']:+.2f}%)")

    if report.get('hot_concepts'):
        lines.append("\n**🏷️ 热门概念**")
        for board in report['hot_concepts'][:5]:
            arrow = '🟢' if float(board['涨跌幅']) >= 0 else '🔴'
            lines.append(f"{arrow} {board['板块名称']}: {board['涨涨幅']}%")

    if report['hot_stocks']:
        lines.append("\n**🔥 热门个股 Top10**")
        for stock in report['hot_stocks'][:10]:
            arrow = '🟢' if stock['change_pct'] >= 0 else '🔴'
            lines.append(f"{arrow} {stock['name']}({stock['code']}): {stock['price']:.2f} ({stock['change_pct']:+.2f}%)")

    if report['strategy_signals']:
        lines.append("\n**🔍 技术信号**")
        for s in report['strategy_signals'][:10]:
            lines.append(f"📌 {s['name']}({s['code']}): {s['price']:.2f}")
            lines.append(f"   {s['signals']}")

    return "\n".join(lines)

if __name__ == "__main__":
    print("=" * 40)
    print("📊 A股每日分析报告生成器")
    print("=" * 40)

    report = generate_daily_report()
    formatted = format_report_for_fei(report)
    print("\n" + formatted)

    # 保存报告
    os.makedirs("reports", exist_ok=True)
    report_file = f"reports/daily_report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📄 报告已保存: {report_file}")
