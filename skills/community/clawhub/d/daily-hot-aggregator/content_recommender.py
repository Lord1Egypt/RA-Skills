#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题推荐工具 v1.0 - 根据热榜推荐自媒体选题
作者: 小天🦞
"""

import json
import os
import sys
import random
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class ContentRecommender:
    """选题推荐器"""

    # 内容模板库
    TEMPLATES = {
        'bilibili': {
            '知识科普': [
                '{topic}背后的科学原理',
                '深度解析：{topic}',
                '关于{topic}你不知道的10件事',
            ],
            '吐槽娱乐': [
                '笑死！{topic}也太离谱了吧',
                '当{topic}遇上脑洞大开的网友',
                '{topic}名场面合集',
            ],
            '生活记录': [
                '挑战{topic}的24小时',
                '我的{topic}日常vlog',
                '{topic}翻车现场实录',
            ]
        },
        'douyin': {
            '热点追踪': [
                '🔥{topic}最新进展！',
                '关于{topic}，官方回应了！',
                '{topic}后续来了！',
            ],
            '情感共鸣': [
                '看完{topic}我哭了...',
                '{topic}：每个人都能找到共鸣',
                '为什么{topic}能火？答案在这里',
            ],
            '实用技巧': [
                '{topic}的正确打开方式',
                '学会{topic}，你也是大神',
                '{topic}小技巧，一学就会',
            ]
        },
        'weibo': {
            '观点评论': [
                '关于{topic}，我想说...',
                '{topic}背后的真相是什么？',
                '从{topic}看社会现象',
            ],
            '互动话题': [
                '你觉得{topic}怎么样？',
                '{topic}引发热议，你站哪边？',
                '聊聊你对{topic}的看法',
            ],
            '热点解读': [
                '{topic}全解析，看这一篇就够了',
                '5分钟了解{topic}始末',
                '{topic}时间线梳理',
            ]
        },
        'xiaohongshu': {
            '种草安利': [
                '{topic}真的绝了！姐妹们冲！',
                '被{topic}惊艳到的一天',
                '{topic}测评｜真实体验分享',
            ],
            '教程攻略': [
                '手把手教你{topic}',
                '{topic}保姆级教程',
                '新手必看！{topic}全攻略',
            ],
            '生活美学': [
                '把{topic}过成诗',
                '{topic}让生活更有仪式感',
                '我的{topic}美好生活日记',
            ]
        }
    }

    # 平台特性
    PLATFORM_TRAITS = {
        'bilibili': {
            'name': 'B站',
            'best_length': '5-15分钟',
            'content_style': '深度、有趣、有梗',
            'audience': 'Z世代、二次元、知识爱好者'
        },
        'douyin': {
            'name': '抖音',
            'best_length': '15-60秒',
            'content_style': '快节奏、强冲击、反转',
            'audience': '大众、碎片化时间用户'
        },
        'weibo': {
            'name': '微博',
            'best_length': '100-300字',
            'content_style': '观点鲜明、互动性强',
            'audience': '追星族、时事关注者'
        },
        'xiaohongshu': {
            'name': '小红书',
            'best_length': '图文结合',
            'content_style': '精致、实用、种草',
            'audience': '年轻女性、生活方式追求者'
        }
    }

    def __init__(self, data_dir: str = 'hot_reports'):
        self.data_dir = data_dir

    def load_report(self, date_str: str, report_type: str = 'daily') -> Optional[Dict]:
        """加载报告"""
        if report_type == 'daily':
            filepath = os.path.join(self.data_dir, f'daily_report_{date_str}.json')
        elif report_type == 'xiaohongshu':
            filepath = os.path.join(self.data_dir, f'xiaohongshu_report_{date_str}.json')
        else:
            return None
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def extract_topics(self, data: Dict, platform: str, top_n: int = 10) -> List[str]:
        """提取热门话题"""
        items = data.get('data', {}).get(platform, [])
        return [item.get('title', '') for item in items[:top_n] if item.get('title')]

    def generate_title(self, topic: str, platform: str, category: str = None) -> str:
        """生成标题"""
        templates = self.TEMPLATES.get(platform, {})
        
        if category and category in templates:
            template = random.choice(templates[category])
        else:
            # 随机选择类别
            all_templates = []
            for cat_templates in templates.values():
                all_templates.extend(cat_templates)
            template = random.choice(all_templates) if all_templates else '{topic}'
        
        return template.format(topic=topic)

    def recommend_for_platform(self, platform: str, date_str: str, top_n: int = 5) -> List[Dict]:
        """为指定平台推荐选题"""
        data = self.load_report(date_str)
        if not data:
            return []
        
        topics = self.extract_topics(data, platform, top_n * 2)
        templates = self.TEMPLATES.get(platform, {})
        categories = list(templates.keys())
        
        recommendations = []
        for i, topic in enumerate(topics[:top_n]):
            category = categories[i % len(categories)] if categories else '通用'
            title = self.generate_title(topic, platform, category)
            
            recommendations.append({
                'original_topic': topic,
                'suggested_title': title,
                'category': category,
                'platform': platform,
                'platform_name': self.PLATFORM_TRAITS.get(platform, {}).get('name', platform),
                'best_length': self.PLATFORM_TRAITS.get(platform, {}).get('best_length', ''),
                'content_style': self.PLATFORM_TRAITS.get(platform, {}).get('content_style', '')
            })
        
        return recommendations

    def recommend_all_platforms(self, date_str: str, top_n: int = 3) -> Dict[str, List[Dict]]:
        """为所有平台推荐选题"""
        platforms = ['bilibili', 'douyin', 'weibo', 'xiaohongshu']
        result = {}
        
        for platform in platforms:
            result[platform] = self.recommend_for_platform(platform, date_str, top_n)
        
        return result

    def format_recommendation(self, rec: Dict) -> str:
        """格式化推荐结果"""
        return f"""
📌 原话题：{rec['original_topic']}
💡 推荐标题：{rec['suggested_title']}
📂 分类：{rec['category']}
🎯 平台：{rec['platform_name']}
⏱️ 建议时长：{rec['best_length']}
✨ 内容风格：{rec['content_style']}"""


def main():
    import argparse
    parser = argparse.ArgumentParser(description='💡 选题推荐工具 v1.0')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='数据日期')
    parser.add_argument('--platform', type=str, help='指定平台 (bilibili/douyin/weibo/xiaohongshu)')
    parser.add_argument('--top', type=int, default=5, help='推荐数量')
    
    args = parser.parse_args()
    
    recommender = ContentRecommender()
    
    if args.platform:
        # 单平台推荐
        recs = recommender.recommend_for_platform(args.platform, args.date, args.top)
        print(f"\n💡 {args.platform} 选题推荐 ({args.date})：")
        for i, rec in enumerate(recs, 1):
            print(f"\n--- 选题 {i} ---")
            print(recommender.format_recommendation(rec))
    else:
        # 全平台推荐
        all_recs = recommender.recommend_all_platforms(args.date, args.top)
        for platform, recs in all_recs.items():
            if recs:
                print(f"\n{'='*50}")
                print(f"🎯 {platform.upper()} 选题推荐")
                print('='*50)
                for i, rec in enumerate(recs, 1):
                    print(f"\n📌 选题{i}: {rec['suggested_title']}")
                    print(f"   原话题: {rec['original_topic']}")
                    print(f"   分类: {rec['category']} | 时长: {rec['best_length']}")


if __name__ == '__main__':
    main()
