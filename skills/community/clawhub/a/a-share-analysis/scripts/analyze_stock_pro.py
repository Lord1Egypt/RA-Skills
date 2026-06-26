#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股专业分析系统 - 主入口（优化版）
修复编码问题、添加批量分析、优化输出
"""

import sys
import os
import json
import codecs
from datetime import datetime
from typing import Dict, List, Optional

# Windows 编码处理
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from fetch_realtime_data import AShareRealTimeFetcher
from fetch_technical_indicators_free import AShareTechnicalAnalyzer
from fetch_news_sentiment import AShareNewsSentimentAnalyzer
from memory_store import AShareMemoryStore
from generate_report_pro import AShareProfessionalReport
from generate_report_detailed import AShareDetailedReport
from generate_report_commercial import AShareCommercialReport
from generate_pdf_report import AShareDetailedPDFReport


def print_box(text: str, width: int = 70):
    """打印边框文本"""
    print("=" * width)
    print(text)
    print("=" * width)


def print_status(status: str, message: str, indent: int = 0):
    """打印状态信息"""
    icons = {
        "OK": "[OK]",
        "WARN": "[!]",
        "FAIL": "[X]",
        "INFO": "[*]"
    }
    icon = icons.get(status, "[ ]")
    prefix = " " * indent
    print(f"{prefix}{icon} {message}")


def analyze_single_stock(stock_code: str, stock_name: str = None, verbose: bool = True) -> Optional[Dict]:
    """分析单只股票"""
    
    analysis_data = {
        "stock_code": stock_code,
        "stock_name": stock_name or "未知",
        "analysis_timestamp": datetime.now().isoformat()
    }

    # 1. 获取实时行情
    if verbose:
        print("\n[1/6] 获取实时行情...")
    try:
        fetcher = AShareRealTimeFetcher()
        stock_data = fetcher.fetch_stock_data(stock_code)
        
        if stock_data:
            analysis_data.update(stock_data)
            if verbose:
                print_status("OK", f"{stock_data.get('name', stock_code)}: {stock_data.get('price', 0):.2f} ({stock_data.get('change_percent', 0):+.2f}%)")
        else:
            if verbose:
                print_status("WARN", "无法获取实时行情数据")
            analysis_data["price"] = 0
            analysis_data["change_percent"] = 0
    except Exception as e:
        if verbose:
            print_status("FAIL", f"实时行情获取失败：{e}")
        analysis_data["price"] = 0
        analysis_data["change_percent"] = 0

    # 2. 技术分析（免费数据源）
    if verbose:
        print("\n[2/6] 技术分析（东方财富免费 API）...")
    try:
        analyzer = AShareTechnicalAnalyzer()
        if stock_code.startswith(('6', '5')):
            tech_code = f"1.{stock_code}"
        else:
            tech_code = f"0.{stock_code}"
        
        technical = analyzer.analyze_technical_indicators(tech_code)
        
        if technical:
            analysis_data["technical"] = technical
            if verbose:
                print_status("OK", f"信号：{technical.get('signal', 'N/A')} | 趋势：{technical.get('trend', 'N/A')}")
                print_status("OK", f"支撑：{technical.get('support', 'N/A')} | 阻力：{technical.get('resistance', 'N/A')}", indent=0)
        else:
            if verbose:
                print_status("WARN", "无法获取技术指标")
            analysis_data["technical"] = {"signal": "unknown", "trend": "unknown"}
    except Exception as e:
        if verbose:
            print_status("FAIL", f"技术分析失败：{e}")
        analysis_data["technical"] = {"signal": "unknown", "trend": "unknown"}

    # 3. 新闻情绪分析
    if verbose:
        print("\n[3/6] 新闻情绪分析 (Firecrawl)...")
    try:
        sentiment_analyzer = AShareNewsSentimentAnalyzer()
        
        if not sentiment_analyzer.firecrawl_available:
            if verbose:
                print_status("WARN", "Firecrawl 未认证，使用简化分析")
            analysis_data["news_sentiment"] = {
                "overall_sentiment": "UNKNOWN",
                "avg_sentiment_score": 0.5,
                "news_count": 0
            }
        else:
            name = stock_data.get('name', stock_name) if stock_data else stock_name
            news_sentiment = sentiment_analyzer.analyze_stock_news(stock_code, name)
            analysis_data["news_sentiment"] = news_sentiment
            
            if verbose:
                print_status("OK", f"新闻数量：{news_sentiment.get('news_count', 0)}")
                print_status("OK", f"情绪评分：{news_sentiment.get('avg_sentiment_score', 0):.3f}")
    except Exception as e:
        if verbose:
            print_status("FAIL", f"新闻情绪分析失败：{e}")
        analysis_data["news_sentiment"] = {"overall_sentiment": "ERROR", "avg_sentiment_score": 0.5}

    # 4. 历史分析回顾
    if verbose:
        print("\n[4/6] 历史分析回顾 (Elite Memory)...")
    try:
        memory_store = AShareMemoryStore()
        memory_history = memory_store.get_analysis_summary(stock_code)
        
        if memory_history and memory_history.get('analysis_count', 0) > 0:
            analysis_data["memory_history"] = memory_history
            if verbose:
                print_status("OK", f"历史分析次数：{memory_history.get('analysis_count', 0)}")
                print_status("OK", f"主要建议：{memory_history.get('most_common_recommendation', 'N/A')}")
        else:
            if verbose:
                print_status("INFO", "无历史分析记录（首次分析）")
            analysis_data["memory_history"] = {
                "analysis_count": 0,
                "most_common_recommendation": "N/A"
            }
    except Exception as e:
        if verbose:
            print_status("FAIL", f"历史回顾失败：{e}")
        analysis_data["memory_history"] = {"analysis_count": 0}

    # 5. 生成专业报告（Markdown + PDF）
    if verbose:
        print("\n[5/7] 生成专业报告...")
    try:
        # 根据参数选择报告类型
        if args.commercial:
            generator = AShareCommercialReport()
            report_type = "商业版"
        elif args.detailed:
            generator = AShareDetailedReport()
            report_type = "详细版"
        else:
            generator = AShareProfessionalReport()
            report_type = "专业版"
        
        report = generator.generate_report(analysis_data)
        
        name = stock_data.get('name', stock_name) if stock_data else stock_name
        filepath = generator.save_report(report, stock_code, name or "unknown")
        
        if verbose:
            print_status("OK", f"{report_type}报告：{filepath}")
        
        analysis_data["report_path"] = filepath
        analysis_data["report"] = report
        
        # 生成 PDF 版本（详细版）
        print_status("INFO", "正在生成详细 PDF 报告...")
        try:
            pdf_generator = AShareDetailedPDFReport()
            pdf_filepath = pdf_generator.generate_pdf(analysis_data)
            if verbose:
                print_status("OK", f"详细 PDF 报告：{pdf_filepath}")
            analysis_data["pdf_report_path"] = pdf_filepath
        except Exception as pdf_e:
            if verbose:
                print_status("WARN", f"PDF 生成失败：{pdf_e}")
    except Exception as e:
        if verbose:
            print_status("FAIL", f"报告生成失败：{e}")

    # 6. 存储分析记录
    if verbose:
        print("\n[6/7] 存储分析记录...")
    try:
        memory_store = AShareMemoryStore()
        
        score = 0.5
        if analysis_data.get('technical', {}).get('signal') in ['bullish', 'bearish']:
            score += 0.2
        if analysis_data.get('news_sentiment', {}).get('overall_sentiment') in ['BULLISH', 'BEARISH']:
            score += 0.2
        if abs(analysis_data.get('change_percent', 0)) > 3:
            score += 0.1
        
        store_data = {
            "stock_code": stock_code,
            "stock_name": analysis_data.get('name', stock_name),
            "price": analysis_data.get('price', 0),
            "change_percent": analysis_data.get('change_percent', 0),
            "technical": analysis_data.get('technical', {}),
            "sentiment": analysis_data.get('news_sentiment', {}),
            "recommendation": _get_recommendation(analysis_data),
            "key_points": _get_key_points(analysis_data),
            "importance": min(1.0, score)
        }
        
        memory_store.store_analysis(store_data)
        if verbose:
            print_status("OK", "分析记录已存储")
    except Exception as e:
        if verbose:
            print_status("FAIL", f"存储失败：{e}")

    return analysis_data


def analyze_stock(stock_code: str, stock_name: str = None, verbose: bool = True) -> Optional[Dict]:
    """分析股票的公共接口"""
    print_box("A 股专业分析系统")
    print(f"分析标的：{stock_name or '未知'} ({stock_code})")
    print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_box("")
    
    result = analyze_single_stock(stock_code, stock_name, verbose)
    
    if result and verbose:
        print("\n" + "=" * 70)
        print("分析摘要")
        print("=" * 70)
        print(f"股票：{result.get('name', stock_name)} ({stock_code})")
        print(f"价格：{result.get('price', 0):.2f} ({result.get('change_percent', 0):+.2f}%)")
        print(f"技术信号：{result.get('technical', {}).get('signal', 'N/A')}")
        print(f"综合建议：{_get_recommendation(result)}")
        print("=" * 70)
    
    return result


def batch_analyze(stocks: List[tuple], output_summary: bool = True) -> List[Dict]:
    """
    批量分析股票
    
    Args:
        stocks: 股票列表 [(code, name), ...]
        output_summary: 是否输出摘要
    
    Returns:
        分析结果列表
    """
    print_box(f"A 股批量分析系统 - 共 {len(stocks)} 只股票")
    
    results = []
    summary_data = []
    
    for i, (code, name) in enumerate(stocks, 1):
        print(f"\n{'='*70}")
        print(f"[{i}/{len(stocks)}] {name} ({code})")
        print(f"{'='*70}")
        
        result = analyze_single_stock(code, name, verbose=True)
        if result:
            results.append(result)
            summary_data.append({
                "code": code,
                "name": name,
                "price": result.get('price', 0),
                "change": result.get('change_percent', 0),
                "signal": result.get('technical', {}).get('signal', 'N/A'),
                "recommendation": _get_recommendation(result)
            })
    
    # 输出汇总
    if output_summary and summary_data:
        print("\n" + "=" * 80)
        print(" " * 30 + "批量分析汇总")
        print("=" * 80)
        print(f"{'股票代码':<12} {'股票名称':<12} {'价格':>10} {'涨跌%':>10} {'信号':>10} {'建议':>10}")
        print("-" * 80)
        
        for item in summary_data:
            print(f"{item['code']:<12} {item['name']:<12} {item['price']:>10.2f} {item['change']:>10.2f} {item['signal']:>10} {item['recommendation']:>10}")
        
        print("=" * 80)
    
    return results


def _get_recommendation(data: Dict) -> str:
    """根据分析数据获取投资建议"""
    score = 5.0
    
    tech_signal = data.get('technical', {}).get('signal', '')
    if tech_signal == 'bullish':
        score += 1.5
    elif tech_signal == 'bearish':
        score -= 1.5
    
    sentiment_score = data.get('news_sentiment', {}).get('avg_sentiment_score', 0.5)
    score += (sentiment_score - 0.5) * 3
    
    change = data.get('change_percent', 0)
    if change > 3:
        score += 0.5
    elif change < -3:
        score -= 0.5
    
    if score >= 8:
        return "强烈推荐"
    elif score >= 6:
        return "推荐"
    elif score >= 4:
        return "观望"
    elif score >= 2:
        return "谨慎"
    else:
        return "回避"


def _get_key_points(data: Dict) -> list:
    """提取关键点"""
    points = []
    
    tech = data.get('technical', {})
    if tech.get('signal') == 'bullish':
        points.append("技术面看多")
    if tech.get('trend') == 'bullish':
        points.append("趋势向上")
    
    sentiment = data.get('news_sentiment', {})
    if sentiment.get('overall_sentiment') == 'BULLISH':
        points.append("新闻情绪积极")
    
    change = data.get('change_percent', 0)
    if change > 3:
        points.append(f"大涨{change:.1f}%")
    elif change < -3:
        points.append(f"大跌{change:.1f}%")
    
    return points


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="A 股专业分析系统")
    parser.add_argument("code", nargs="?", help="股票代码")
    parser.add_argument("name", nargs="?", help="股票名称")
    parser.add_argument("--batch", "-b", action="store_true", help="批量分析模式")
    parser.add_argument("--file", "-f", help="股票列表文件（每行：代码 名称）")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")
    parser.add_argument("--commercial", "-c", action="store_true", help="商业版报告")
    parser.add_argument("--detailed", "-d", action="store_true", help="详细版报告")
    
    args = parser.parse_args()
    
    # 批量分析模式
    if args.batch or args.file:
        stocks = []
        
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        stocks.append((parts[0], parts[1]))
        else:
            # 默认测试股票
            stocks = [
                ("600519", "贵州茅台"),
                ("000858", "五粮液"),
                ("603258", "电魂网络")
            ]
        
        results = batch_analyze(stocks, output_summary=not args.quiet)
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
    
    # 单股分析模式
    elif args.code:
        result = analyze_stock(args.code, args.name, verbose=not args.quiet)
        
        if args.json and result:
            output = {k: v for k, v in result.items() if k != 'report'}
            print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    
    # 无参数，显示帮助
    else:
        print("A 股专业分析系统")
        print("\n用法:")
        print("  python analyze_stock_pro.py 600519 贵州茅台     # 分析单只股票")
        print("  python analyze_stock_pro.py --batch             # 批量分析（默认股票）")
        print("  python analyze_stock_pro.py -f stocks.txt       # 从文件批量分析")
        print("  python analyze_stock_pro.py 600519 --json       # JSON 输出")
        print("\n示例:")
        print("  python analyze_stock_pro.py 600519 贵州茅台")
        print("  python analyze_stock_pro.py --batch --json")
