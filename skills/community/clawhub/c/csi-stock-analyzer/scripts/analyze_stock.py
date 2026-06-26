#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析命令行工具
"""

import os
import sys
import argparse

# 添加核心模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../core'))

from stock_analyzer import AdvancedStockAnalyzer

def main():
    parser = argparse.ArgumentParser(description='CSI 2000 股票分析工具')
    parser.add_argument('stock', help='股票代码或公司名称')
    parser.add_argument('--days', '-d', type=int, default=120, help='分析天数，默认120天')
    parser.add_argument('--no-news', action='store_true', help='不包含新闻分析')
    parser.add_argument('--no-financial', action='store_true', help='不包含财务分析')
    parser.add_argument('--no-technical', action='store_true', help='不包含技术分析')
    parser.add_argument('--output', '-o', help='输出报告文件路径')
    
    args = parser.parse_args()
    
    print(f"🚀 开始分析 {args.stock}...")
    print(f"📅 分析周期：{args.days}天")
    
    analyzer = AdvancedStockAnalyzer()
    
    try:
        result = analyzer.comprehensive_analysis(
            args.stock,
            days=args.days,
            include_news=not args.no_news,
            include_financial=not args.no_financial,
            include_technical=not args.no_technical
        )
        
        report = analyzer.generate_analysis_report(result)
        
        # 输出报告
        print("\n" + "="*60)
        print(report)
        print("="*60 + "\n")
        
        # 保存到文件
        if args.output:
            output_path = args.output
        else:
            from datetime import datetime
            output_path = f"{args.stock}_分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 分析完成！报告已保存到：{output_path}")
        
    except Exception as e:
        print(f"❌ 分析失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
