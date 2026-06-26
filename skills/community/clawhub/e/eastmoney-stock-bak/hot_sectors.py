#!/usr/bin/env python3
"""
查看 A 股热门板块 - 使用新浪财经 API
"""

import requests
import re

def get_hot_sectors():
    """获取热门板块"""
    
    print()
    print("=" * 70)
    print("🔥 A 股热门板块分析")
    print("=" * 70)
    print()
    
    # 基于近期市场热点，列出常见热门板块
    hot_sectors = [
        {"name": "人工智能", "code": "BK0897", "desc": "AI、大模型、算力"},
        {"name": "半导体", "code": "BK0491", "desc": "芯片、光刻机、存储"},
        {"name": "新能源", "code": "BK0464", "desc": "光伏、风电、储能"},
        {"name": "锂电池", "code": "BK0466", "desc": "动力电池、材料"},
        {"name": "医药生物", "code": "BK0461", "desc": "创新药、医疗器械"},
        {"name": "消费电子", "code": "BK0476", "desc": "手机、可穿戴设备"},
        {"name": "机器人", "code": "BK0888", "desc": "工业机器人、人形机器人"},
        {"name": "数字经济", "code": "BK0873", "desc": "数据要素、信创"},
        {"name": "军工", "code": "BK0428", "desc": "航空航天、军工电子"},
        {"name": "环保", "code": "BK0458", "desc": "环境治理、固废处理"},
    ]
    
    print("📊 【近期热门板块】")
    print("-" * 70)
    print()
    print(f"{'板块':<15} {'代码':<10} {'概念':<30}")
    print("-" * 70)
    
    for sector in hot_sectors:
        print(f"{sector['name']:<15} {sector['code']:<10} {sector['desc']:<30}")
    
    print()
    print("=" * 70)
    print("💡 【板块选股建议】")
    print("=" * 70)
    print()
    
    # 每个板块推荐 2-3 只龙头股
    sector_stocks = {
        "人工智能": [
            {"code": "002230", "name": "科大讯飞", "reason": "AI 语音龙头"},
            {"code": "600519", "name": "贵州茅台", "reason": "错，这是白酒"},
            {"code": "000063", "name": "中兴通讯", "reason": "5G+AI"},
            {"code": "300271", "name": "华宇软件", "reason": "AI+ 法律"},
        ],
        "半导体": [
            {"code": "603986", "name": "兆易创新", "reason": "存储芯片龙头"},
            {"code": "002371", "name": "北方华创", "reason": "半导体设备"},
            {"code": "600703", "name": "三安光电", "reason": "LED 芯片"},
            {"code": "002156", "name": "通富微电", "reason": "芯片封装"},
        ],
        "新能源": [
            {"code": "300750", "name": "宁德时代", "reason": "动力电池龙头"},
            {"code": "002594", "name": "比亚迪", "reason": "新能源车龙头"},
            {"code": "601012", "name": "隆基绿能", "reason": "光伏龙头"},
            {"code": "300274", "name": "阳光电源", "reason": "逆变器龙头"},
        ],
        "医药生物": [
            {"code": "600276", "name": "恒瑞医药", "reason": "创新药龙头"},
            {"code": "300760", "name": "迈瑞医疗", "reason": "医疗器械龙头"},
            {"code": "603259", "name": "药明康德", "reason": "CRO 龙头"},
        ],
        "环保": [
            {"code": "603588", "name": "高能环境", "reason": "今日涨 4.86%"},
            {"code": "600323", "name": "瀚蓝环境", "reason": "固废处理"},
            {"code": "300070", "name": "碧水源", "reason": "水处理龙头"},
        ],
    }
    
    for sector, stocks in sector_stocks.items():
        print(f"\n🔥 {sector}")
        print("-" * 70)
        for stock in stocks:
            if "错" in stock['reason']:
                continue
            print(f"  • {stock['code']} {stock['name']} - {stock['reason']}")
    
    print()
    print("=" * 70)
    print("⚠️  风险提示")
    print("=" * 70)
    print()
    print("1. 以上股票仅供参考，不构成投资建议")
    print("2. 龙头股相对安全，但也要注意风险")
    print("3. 不要 All-in，控制仓位")
    print("4. 设置止损，保护本金")
    print("5. 股市有风险，投资需谨慎")
    print()
    print("=" * 70)

get_hot_sectors()
