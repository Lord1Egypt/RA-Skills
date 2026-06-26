#!/usr/bin/env python3
"""
36氪热门获取脚本
36kr Hot News Fetcher
"""

import json
import sys

def get_36kr_hot(limit=10):
    """获取36氪热门（模拟数据）"""
    mock_news = [
        {"id": 1, "title": "OpenAI 发布 GPT-5，性能提升 50%", "category": "AI", "views": 125000, "comments": 234, "source": "36kr"},
        {"id": 2, "title": "小米汽车 SU7 交付量突破 10 万台", "category": "汽车", "views": 98000, "comments": 189, "source": "36kr"},
        {"id": 3, "title": "字节跳动 2026 年营收增长 30%", "category": "公司", "views": 87000, "comments": 156, "source": "36kr"},
        {"id": 4, "title": "红杉中国完成新一期基金募资 200 亿", "category": "创投", "views": 76000, "comments": 134, "source": "36kr"},
        {"id": 5, "title": "苹果中国市场份额下滑至第三", "category": "科技", "views": 65000, "comments": 98, "source": "36kr"},
        {"id": 6, "title": "新能源车企掀起价格战", "category": "汽车", "views": 54000, "comments": 87, "source": "36kr"},
        {"id": 7, "title": "AI 创业公司估值泡沫引关注", "category": "创投", "views": 43000, "comments": 76, "source": "36kr"},
        {"id": 8, "title": "美团外卖测试无人机配送", "category": "科技", "views": 32000, "comments": 65, "source": "36kr"},
        {"id": 9, "title": "SaaS 行业进入整合期", "category": "企业服务", "views": 21000, "comments": 54, "source": "36kr"},
        {"id": 10, "title": "国产大模型竞争白热化", "category": "AI", "views": 15000, "comments": 43, "source": "36kr"},
    ]
    return mock_news[:limit]

def format_output(data):
    output = "📰 36氪今日热门\n\n"
    for item in data:
        views_w = f"{item['views'] / 10000:.1f}万"
        output += f"{item['id']}. {item['title']}\n"
        output += f"   📂 {item['category']} | 👁 {views_w} | 💬 {item['comments']}\n\n"
    return output

def main():
    limit = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
    
    data = get_36kr_hot(limit=limit)
    
    if "--json" in sys.argv or "-j" in sys.argv:
        print(json.dumps({"data": data}, ensure_ascii=False, indent=2))
    else:
        print(format_output(data))

if __name__ == "__main__":
    main()
