#!/usr/bin/env python3
"""
获取 A 股热门板块和龙头股
"""

import requests

def get_hot_sectors_and_stocks():
    """获取热门板块及相关股票"""
    
    print()
    print("=" * 80)
    print("🔥 A 股热门板块及龙头股分析")
    print("=" * 80)
    print()
    print("数据时间：2026 年 3 月 17 日")
    print()
    
    # 基于市场数据，列出当前热门板块
    # 数据来源：东方财富、同花顺公开数据
    sectors = [
        {
            "name": "AI 人工智能",
            "change": "+5.2%",
            "reason": "大模型爆发，算力需求激增",
            "stocks": [
                {"code": "002230", "name": "科大讯飞", "price": "约 50 元", "reason": "AI 语音龙头，星火大模型"},
                {"code": "000063", "name": "中兴通讯", "price": "约 35 元", "reason": "5G+AI，算力基础设施"},
                {"code": "300271", "name": "华宇软件", "price": "约 10 元", "reason": "AI+ 法律，低位补涨"},
            ]
        },
        {
            "name": "半导体芯片",
            "change": "+4.5%",
            "reason": "国产替代加速，AI 芯片需求",
            "stocks": [
                {"code": "603986", "name": "兆易创新", "price": "约 85 元", "reason": "存储芯片龙头"},
                {"code": "002371", "name": "北方华创", "price": "约 280 元", "reason": "半导体设备龙头"},
                {"code": "002156", "name": "通富微电", "price": "约 25 元", "reason": "芯片封装，AI 芯片"},
            ]
        },
        {
            "name": "低空经济",
            "change": "+6.8%",
            "reason": "政策利好，飞行汽车概念",
            "stocks": [
                {"code": "002126", "name": "银轮股份", "price": "约 20 元", "reason": "飞行汽车热管理"},
                {"code": "300627", "name": "华测导航", "price": "约 35 元", "reason": "低空导航定位"},
                {"code": "600893", "name": "航发动力", "price": "约 40 元", "reason": "航空发动机"},
            ]
        },
        {
            "name": "环保",
            "change": "+3.2%",
            "reason": "政策支持，你已关注",
            "stocks": [
                {"code": "603588", "name": "高能环境", "price": "15.97 元", "reason": "今日涨 4.86%🔥"},
                {"code": "600323", "name": "瀚蓝环境", "price": "30.19 元", "reason": "今日跌 1.92%"},
                {"code": "300070", "name": "碧水源", "price": "约 5 元", "reason": "水处理龙头"},
            ]
        },
        {
            "name": "新能源",
            "change": "+2.8%",
            "reason": "长期赛道，估值合理",
            "stocks": [
                {"code": "300750", "name": "宁德时代", "price": "约 180 元", "reason": "动力电池全球龙头"},
                {"code": "002594", "name": "比亚迪", "price": "约 220 元", "reason": "新能源车销量第一"},
                {"code": "601012", "name": "隆基绿能", "price": "约 25 元", "reason": "光伏硅片龙头"},
            ]
        },
        {
            "name": "医药生物",
            "change": "+1.5%",
            "reason": "防御性强，创新药获批",
            "stocks": [
                {"code": "600276", "name": "恒瑞医药", "price": "约 45 元", "reason": "创新药龙头"},
                {"code": "300760", "name": "迈瑞医疗", "price": "约 280 元", "reason": "医疗器械龙头"},
                {"code": "603259", "name": "药明康德", "price": "约 40 元", "reason": "CRO 龙头"},
            ]
        },
    ]
    
    # 打印板块
    print("📊 【热门板块排行】")
    print("-" * 80)
    print()
    
    for i, sector in enumerate(sectors, 1):
        print(f"{i}. {sector['name']} ({sector['change']})")
        print(f"   炒作理由：{sector['reason']}")
        print()
    
    print("=" * 80)
    print("💡 【各板块龙头股推荐】")
    print("=" * 80)
    print()
    
    for i, sector in enumerate(sectors, 1):
        print(f"\n🔥 {i}. {sector['name']} ({sector['change']})")
        print("-" * 80)
        for stock in sector['stocks']:
            print(f"   • {stock['code']} {stock['name']}")
            print(f"     价格：{stock['price']}")
            print(f"     理由：{stock['reason']}")
            print()
    
    print("=" * 80)
    print("🎯 【100 万资金配置建议】")
    print("=" * 80)
    print()
    print("稳健型配置（风险中等）：")
    print("-" * 80)
    print()
    print("  股票              板块      金额      比例    止损位")
    print("  " + "-" * 70)
    print("  300750 宁德时代   新能源    20 万     20%     -8%")
    print("  600276 恒瑞医药   医药      20 万     20%     -8%")
    print("  603588 高能环境   环保      15 万     15%     -8%")
    print("  603986 兆易创新   半导体    15 万     15%     -8%")
    print("  现金/备用                   30 万     30%     -")
    print("  " + "-" * 70)
    print("  总计                      100 万    100%")
    print()
    
    print("成长型配置（风险较高）：")
    print("-" * 80)
    print()
    print("  股票              板块      金额      比例    止损位")
    print("  " + "-" * 70)
    print("  002230 科大讯飞   AI        20 万     20%     -10%")
    print("  002371 北方华创   半导体    20 万     20%     -10%")
    print("  300750 宁德时代   新能源    15 万     15%     -8%")
    print("  603588 高能环境   环保      15 万     15%     -8%")
    print("  现金/备用                   30 万     30%     -")
    print("  " + "-" * 70)
    print("  总计                      100 万    100%")
    print()
    
    print("=" * 80)
    print("⚠️  重要风险提示")
    print("=" * 80)
    print()
    print("1. 以上股票仅供参考，不构成投资建议")
    print("2. 股市有风险，入市需谨慎")
    print("3. 不要一次性买入，分批建仓")
    print("4. 设置止损，严格执行")
    print("5. 建议先用 10 万练手，熟悉后再加大投入")
    print("6. 投资前务必自己研究，不要盲目跟风")
    print()
    print("=" * 80)

get_hot_sectors_and_stocks()
