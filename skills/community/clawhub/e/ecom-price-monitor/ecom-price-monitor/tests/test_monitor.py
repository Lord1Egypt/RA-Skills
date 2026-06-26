#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电商价格监控测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import PriceMonitor

def test_monitor():
    """测试监控器功能"""
    print("💰 测试跨境电商价格监控...\n")
    
    monitor = PriceMonitor()
    
    # 测试1: 添加产品
    print("✅ 测试1: 添加监控产品")
    product = monitor.add_product(
        name="Test Earbuds",
        platform="amazon",
        url="https://amazon.com/dp/B08N5WRWNW",
        target_price=40.0
    )
    assert product.id in monitor.products, "添加失败"
    assert len(monitor.alerts) == 1, "未自动创建提醒"
    print(f"   添加成功: {product.name} (ID: {product.id})")
    
    # 测试2: 抓取Amazon
    print("✅ 测试2: 抓取Amazon价格")
    product = monitor.scrape_amazon("B08N5WRWNW")
    assert product is not None, "抓取失败"
    assert product.current_price > 0, "价格异常"
    print(f"   价格: ${product.current_price}")
    
    # 测试3: 更新价格
    print("✅ 测试3: 更新价格")
    monitor.products[product.id] = product
    updated = monitor.update_price(product.id)
    assert updated is not None, "更新失败"
    print(f"   更新成功: ${updated.current_price}")
    
    # 测试4: 价格提醒
    print("✅ 测试4: 价格提醒")
    monitor.add_alert(product.id, "below", 50.0)
    alerts = monitor.check_alerts()
    # 注意: 实际触发取决于当前价格是否低于阈值
    print(f"   提醒数量: {len(alerts)}")
    
    # 测试5: 套利机会
    print("✅ 测试5: 套利机会发现")
    opportunities = monitor.find_arbitrage("electronics")
    assert len(opportunities) > 0, "未找到套利机会"
    for opp in opportunities[:1]:
        print(f"   发现: {opp['product_name']} ({opp['profit_margin']*100:.0f}%利润率)")
    
    # 测试6: 价格趋势
    print("✅ 测试6: 价格趋势")
    # 添加一些历史数据
    product.price_history = [
        {"price": 55.0, "timestamp": "2026-03-20T10:00:00"},
        {"price": 52.0, "timestamp": "2026-03-21T10:00:00"},
        {"price": 49.99, "timestamp": "2026-03-22T10:00:00"}
    ]
    monitor.products[product.id] = product
    
    trend = monitor.get_price_trend(product.id)
    assert 'trend' in trend, "趋势分析失败"
    print(f"   趋势: {trend['trend']}")
    print(f"   最低: ${trend['min_price']}, 最高: ${trend['max_price']}")
    
    # 测试7: 导出
    print("✅ 测试7: 导出数据")
    filepath = monitor.export_data("json", "test_export")
    assert os.path.exists(filepath), "导出失败"
    print(f"   导出成功: {filepath}")
    os.remove(filepath)
    
    print("\n" + "="*50)
    print("🎉 所有测试通过！")
    return 0

if __name__ == "__main__":
    exit(test_monitor())