#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晚间预缓存财务数据脚本
每天收盘后运行，预先获取所有股票的财务数据
"""

import sys
import os
import time
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入analyze模块
import importlib.util
spec = importlib.util.spec_from_file_location("analyze", Path(__file__).parent / "analyze.py")
analyze_module = importlib.util.module_from_spec(spec)
sys.modules['analyze'] = analyze_module
spec.loader.exec_module(analyze_module)

AStockAnalyzer = analyze_module.AStockAnalyzer


def prefetch_all_financial_data():
    """预获取所有股票的财务数据"""
    print("=" * 50)
    print("📊 晚间预缓存财务数据")
    print("=" * 50)
    
    analyzer = AStockAnalyzer()
    
    # 获取全部股票列表
    stock_pool = analyzer.get_stock_pool()
    total = len(stock_pool)
    print(f"\n📈 股票总数: {total} 只")
    
    # 预获取每只股票的财务数据
    for i, symbol in enumerate(stock_pool):
        if i % 50 == 0:
            print(f"  进度: {i}/{total} ({i*100//total}%)")
        
        try:
            # 获取财务数据（会自动存入缓存）
            fin = analyzer.check_financial_conditions(symbol)
            time.sleep(0.05)  # 避免请求过快
        except Exception as e:
            pass
    
    # 保存缓存
    print(f"\n  进度: {total}/{total} (100%)")
    analyzer._save_financial_cache()
    
    print("\n✅ 预缓存完成!")
    print(f"   已缓存 {len(analyzer._financial_cache)} 只股票的财务数据")


if __name__ == '__main__':
    prefetch_all_financial_data()
