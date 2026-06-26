#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的摘要生成 - 不依赖Chrome
使用RSS中的描述和关键词匹配来生成更好的摘要
"""

import re
import json

def generate_summary_from_rss(title, description, url, source):
    """
    从RSS内容生成更好的摘要
    """
    summary = ""
    
    # 1. 优先使用meta描述
    if description and len(description) > 20:
        summary = description.strip()
        # 清理HTML标签
        summary = re.sub(r'<[^>]+>', '', summary)
        summary = summary.strip()
    
    # 2. 如果没有描述，从标题提取关键信息
    if not summary or len(summary) < 30:
        # 标题通常包含核心信息
        summary = title
    
    # 3. 清理
    summary = re.sub(r'\s+', ' ', summary)
    summary = summary[:350]
    
    return summary


def extract_key_points(title, content, source):
    """
    从内容中提取关键点
    """
    if not content:
        return []
    
    # 合并标题和内容
    text = title + " " + content
    
    # 关键词模式 - 包含这些词往往是重点
    patterns = [
        r'(\d+[亿万千百])',  # 数字
        r'(发布|推出|上线|公布|宣布)',  # 动作
        r'(首次|首个|第一|首次|首次)',  # 最高级
        r'(增长|下降|突破|超过|领先)',  # 变化
        r'(融资|投资|收购|上市|估值)',  # 商业
        r'(新模型|新产品|新功能|新版)',  # 新产品
        r'(免费|限时|优惠|特价)',  # 促销
        r'(AI|人工智能|模型|算法)',  # AI相关
    ]
    
    key_points = []
    
    # 分割成句子
    sentences = re.split(r'[。！？\n\r]+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 15 or len(sentence) > 150:
            continue
        
        # 检查是否包含数字（往往是重点）
        has_number = any(p in sentence for p in ['亿', '万', '千', '%', '年', '月', '日'])
        
        # 检查是否是重点句子
        is_important = any(re.search(p, sentence) for p in patterns)
        
        if has_number or is_important:
            if sentence not in key_points:
                key_points.append(sentence)
        
        if len(key_points) >= 4:
            break
    
    return key_points[:3]


def enhance_summary(article):
    """
    增强摘要 - 组合多个来源的信息
    """
    title = article.get('title', '')
    url = article.get('url', '')
    source = article.get('source', '')
    
    # 原始摘要
    original_summary = article.get('summary', '')
    
    # 尝试从URL获取更多信息（简化版）
    # 在实际环境中，这里可以调用更详细的内容获取
    
    # 生成更好的摘要
    better_summary = generate_summary_from_rss(
        title, 
        original_summary, 
        url, 
        source
    )
    
    # 提取关键点
    key_points = extract_key_points(title, original_summary, source)
    
    return {
        'title': title,
        'url': url,
        'source': source,
        'summary': better_summary,
        'key_points': key_points,
        'method': article.get('method', 'unknown'),
        'credibility': article.get('credibility', {})
    }


def main():
    """测试"""
    # 测试数据
    test_articles = [
        {
            'title': 'OpenAI新模型不是GPTX！全新预训练"土豆"曝光，Sora成弃子的原因找到了',
            'url': 'https://www.qbitai.com/2026/04/396535.html',
            'source': '量子位',
            'summary': '首页 资讯 智能车 智库 活动 MEET大会 AIGC OpenAI新模型不是GPTX！全新预训练"土豆"曝光，Sora成弃子的原因找到了 henry 2026-04-05 17:06:59 来源：量子位 正面回应了和Anthropic的竞争 一水 发自 凹非寺 量子位',
            'method': 'rss'
        },
        {
            'title': '神州数码2025年营收超1400亿，AI相关业务增长近五成',
            'url': 'https://www.36kr.com/p/3751046517129735',
            'source': '36kr',
            'summary': '作者｜黄楠编辑｜袁斯来神州数码（000034.SZ）2025年全年业绩报告近日发布。财报显示，公司全年实现营业收入1438亿元，同比增长12%，营收规模连续三年稳步攀升。其中，AI相关业务成为核心增长引擎，全年收入达330亿元，同比增长了48%',
            'method': 'rss'
        },
        {
            'title': 'NVIDIA发布新一代GPU，性能提升3倍',
            'url': 'https://example.com/nvidia-gpu',
            'source': '驱动之家',
            'summary': '刚刚发布的Blackwell架构GPU将在2026年上市，预计性能提升3倍，功耗降低30%',
            'method': 'chrome'
        }
    ]
    
    print("=" * 60)
    print("摘要增强测试")
    print("=" * 60)
    
    for article in test_articles:
        enhanced = enhance_summary(article)
        
        print(f"\n标题: {enhanced['title'][:60]}")
        print(f"来源: {enhanced['source']}")
        print(f"摘要: {enhanced['summary'][:200]}...")
        
        if enhanced['key_points']:
            print("关键点:")
            for i, kp in enumerate(enhanced['key_points'], 1):
                print(f"  {i}. {kp[:80]}")
        else:
            print("关键点: 无")


if __name__ == "__main__":
    main()