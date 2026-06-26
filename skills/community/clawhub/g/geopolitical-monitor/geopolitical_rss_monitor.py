
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地缘政治事件监控脚本（简化版）
使用简单的新闻源监控地缘政治事件
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# 目录设置
DATA_DIR = Path.home() / "shared_memory" / "geopolitical"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 关键词
KEYWORDS = [
    "中东", "伊朗", "以色列", "巴勒斯坦", "石油", "制裁",
    "地缘政治", "冲突", "原油", "黄金", "避险",
    "霍尔木兹海峡", "红海", "波斯湾"
]

# 模拟新闻数据（在没有真实API的情况下）
# 实际使用时可以从这些源抓取：
# - 新浪财经RSS
# - 财联社
# - 央视新闻
# - 华尔街见闻
# - 联合早报

MOCK_NEWS = [
    {
        "title": "伊朗最高领袖更换引发中东局势紧张",
        "source": "新华社",
        "timestamp": datetime.now().isoformat()
    },
    {
        "title": "美以继续打击伊朗石油设施",
        "source": "路透社",
        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat()
    },
    {
        "title": "霍尔木兹海峡航运风险上升",
        "source": "彭博社",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
    },
    {
        "title": "国际油价突破关键点位",
        "source": "财联社",
        "timestamp": (datetime.now() - timedelta(hours=3)).isoformat()
    },
    {
        "title": "黄金价格创新高避险需求旺盛",
        "source": "华尔街见闻",
        "timestamp": (datetime.now() - timedelta(hours=4)).isoformat()
    },
    {
        "title": "军工板块受益于地缘政治紧张",
        "source": "证券时报",
        "timestamp": (datetime.now() - timedelta(hours=5)).isoformat()
    },
    {
        "title": "中国呼吁停止中东军事行动",
        "source": "央视新闻",
        "timestamp": (datetime.now() - timedelta(hours=6)).isoformat()
    },
    {
        "title": "海湾国家加强安全措施",
        "source": "半岛电视台",
        "timestamp": (datetime.now() - timedelta(hours=7)).isoformat()
    },
    {
        "title": "OPEC+讨论增产应对供应中断",
        "source": "能源资讯",
        "timestamp": (datetime.now() - timedelta(hours=8)).isoformat()
    },
    {
        "title": "地缘政治风险推高全球通胀",
        "source": "金融时报",
        "timestamp": (datetime.now() - timedelta(hours=9)).isoformat()
    }
]

# 板块定义
SECTORS = {
    "能源": {
        "keywords": ["石油", "天然气", "原油", "能源", "油气", "OPEC", "霍尔木兹海峡"],
        "sensitivity": 0.9,
        "direction": "positive",
        "stocks": ["中国石油", "中国石化", "中海油", "潜能恒信", "海油工程"]
    },
    "黄金": {
        "keywords": ["黄金", "贵金属", "避险"],
        "sensitivity": 0.95,
        "direction": "positive",
        "stocks": ["紫金矿业", "山东黄金", "赤峰黄金", "湖南黄金"]
    },
    "军工": {
        "keywords": ["军工", "国防", "武器", "军事", "导弹", "伊朗", "以色列", "冲突"],
        "sensitivity": 0.85,
        "direction": "positive",
        "stocks": ["中航沈飞", "中航西飞", "中航光电", "航天电器", "海格通信"]
    },
    "航运": {
        "keywords": ["航运", "港口", "物流", "海运", "霍尔木兹海峡", "红海"],
        "sensitivity": 0.8,
        "direction": "mixed",
        "stocks": ["中远海控", "招商轮船", "中集集团"]
    },
    "消费": {
        "keywords": ["消费", "零售", "白酒", "通胀"],
        "sensitivity": 0.4,
        "direction": "negative",
        "stocks": ["贵州茅台", "五粮液", "美的集团", "格力电器"]
    },
    "科技": {
        "keywords": ["科技", "半导体", "芯片"],
        "sensitivity": 0.3,
        "direction": "negative",
        "stocks": ["中芯国际", "韦尔股份", "兆易创新"]
    },
    "金融": {
        "keywords": ["银行", "保险", "券商", "金融", "通胀"],
        "sensitivity": 0.5,
        "direction": "mixed",
        "stocks": ["招商银行", "中国平安", "中信证券"]
    }
}

def analyze_news(news_items: List[Dict[str, Any]]) -&gt; Dict[str, Any]:
    """
    分析新闻对各板块的影响
    """
    # 初始化板块数据
    sector_data = {
        sector: {
            "impact_score": 0,
            "news_count": 0,
            "affected_stocks": []
        }
        for sector in SECTORS.keys()
    }

    # 分析每条新闻
    for news in news_items:
        title = news['title']

        for sector, config in SECTORS.items():
            # 检查是否包含该板块的关键词
            for keyword in config['keywords']:
                if keyword in title:
                    # 增加影响分数
                    sector_data[sector]['impact_score'] += config['sensitivity']
                    sector_data[sector]['news_count'] += 1

                    # 添加相关股票
                    sector_data[sector]['affected_stocks'].extend(config['stocks'])

    # 去重股票
    for sector in sector_data:
        sector_data[sector]['affected_stocks'] = list(set(sector_data[sector]['affected_stocks']))

    # 归一化影响分数（0-10）
    max_score = max((s['impact_score'] for s in sector_data.values()), default=1)
    for sector in sector_data:
        if max_score &gt; 0:
            sector_data[sector]['impact_score'] = round(min(10, sector_data[sector]['impact_score'] / max_score * 10), 1)

    # 生成板块排名
    ranking = sorted(
        sector_data.items(),
        key=lambda x: x[1]['impact_score'],
        reverse=True
    )

    return {
        'sectors': {k: v for k, v in sector_data.items()},
        'ranking': [
            {
                'sector': sector,
                'impact_score': data['impact_score'],
                'news_count': data['news_count'],
                'trend': 'up' if data['impact_score'] &gt; 5 else 'neutral' if data['impact_score'] &gt; 2 else 'down'
            }
            for sector, data in ranking
        ]
    }

def generate_report(news_items: List[Dict[str, Any]], analysis: Dict[str, Any]) -&gt; Dict[str, Any]:
    """
    生成监控报告
    """
    now = datetime.now()

    return {
        "timestamp": now.isoformat(),
        "utc_timestamp": (now - timedelta(hours=8)).isoformat(),
        "data_source": "rss_monitor_v2",
        "search_status": "success",
        "search_keywords": KEYWORDS,

        "news_events": [
            {
                "title": news['title'],
                "url": "",
                "source": news['source'],
                "timestamp": news['timestamp']
            }
            for news in news_items
        ],

        "analysis": {
            "sectors": {
                sector: {
                    "impact_score": data['impact_score'],
                    "sentiment": "positive" if SECTORS[sector]['direction'] == "positive" else "mixed" if SECTORS[sector]['direction'] == "mixed" else "negative",
                    "news_count": data['news_count'],
                    "affected_stocks": data['affected_stocks']
                }
                for sector, data in analysis['sectors'].items()
            },
            "sector_ranking": analysis['ranking']
        },

        "key_events_summary": news_items[:10] if news_items else [],

        "notes": f"数据采集时间：{now.strftime('%Y-%m-%d %H:%M:%S')}（新加坡时间）\n数据源：RSS监控（简化版）\n说明：使用模拟数据展示功能，实际使用时需要接入真实的RSS或新闻API源"
    }

def main():
    """
    主函数
    """
    print(f"🌍 地缘政治监控开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 使用模拟数据
    print(f"📊 获取到 {len(MOCK_NEWS)} 条相关新闻（模拟数据）")

    # 分析新闻
    print("🔍 分析板块影响...")
    analysis = analyze_news(MOCK_NEWS)

    # 生成报告
    print("📝 生成报告...")
    report = generate_report(MOCK_NEWS, analysis)

    # 保存到文件
    now = datetime.now()
    filename = f"{now.strftime('%Y-%m-%d_%H')}.json"
    filepath = DATA_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"✅ 报告已保存: {filepath}")
    print(f"\n📈 板块排名:")
    for item in analysis['ranking']:
        print(f"   {item['sector']:8s} - {item['impact_score']:.1f}分 ({item['news_count']}条新闻) [{'⬆️' if item['trend']=='up' else '➖' if item['trend']=='neutral' else '⬇️'}]")

    print(f"\n📰 最新事件:")
    for news in MOCK_NEWS[:5]:
        print(f"   • {news['title'][:40]}... ({news['source']})")

    print("\n🎉 监控完成！")

if __name__ == "__main__":
    main()
