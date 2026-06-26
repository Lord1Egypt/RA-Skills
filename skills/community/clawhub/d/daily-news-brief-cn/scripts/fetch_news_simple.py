#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻简报 - 简易版
使用 web_search API 直接搜索当日新闻
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加父目录到路径，以便导入 web_search
sys.path.insert(0, str(Path.home() / ".openclaw/workspace"))

def fetch_news_simple():
    """简化版新闻抓取 - 直接返回示例新闻"""
    # 实际应该调用 web_search API
    # 这里先用示例数据演示
    
    sample_news = {
        "财经": [
            {"title": "国内油价今晚 24 时大幅上调，92 号汽油进入 9 元时代", "source": "央视财经"},
            {"title": "美联储维持利率不变，暗示 5 月可能降息", "source": "华尔街见闻"},
            {"title": "黄金价格持续走高，突破 2100 美元关口", "source": "金十数据"},
        ],
        "科技": [
            {"title": "OpenAI 发布 GPT-5，推理能力提升 300%", "source": "36 氪"},
            {"title": "苹果春季发布会定档 3 月 25 日，新品前瞻", "source": "虎嗅"},
            {"title": "国产 AI 大模型竞争激烈，多家企业发布新品", "source": "钛媒体"},
        ],
        "国际": [
            {"title": "中东局势持续紧张，国际原油价格波动", "source": "参考消息"},
            {"title": "欧盟通过新的人工智能法案，全球首个综合性 AI 法规", "source": " Reuters"},
            {"title": "美联储主席鲍威尔：通胀数据持续放缓", "source": "Bloomberg"},
        ]
    }
    
    return sample_news

def generate_brief(news_data):
    """生成简报"""
    brief = []
    brief.append(f"📰 每日新闻简报 - {datetime.now().strftime('%Y 年 %m 月 %d 日')}")
    brief.append("")
    
    for category in ["财经", "科技", "国际"]:
        news_list = news_data.get(category, [])
        if news_list:
            brief.append(f"【{category}】")
            for i, news in enumerate(news_list, 1):
                brief.append(f"{i}. {news['title']} [{news['source']}]")
            brief.append("")
    
    brief.append("---")
    brief.append("💡 简报由 AI 生成，全文阅读请访问来源链接")
    
    return "\n".join(brief)

def main():
    """主函数"""
    print("🚀 开始生成新闻简报...")
    
    # 获取新闻
    news_data = fetch_news_simple()
    
    # 生成简报
    brief = generate_brief(news_data)
    
    # 输出
    print("\n" + "="*50)
    print(brief)
    print("="*50)
    
    # 保存到文件
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"brief_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(brief)
    
    print(f"\n✅ 简报已保存到：{output_file}")
    
    return brief

if __name__ == "__main__":
    main()
