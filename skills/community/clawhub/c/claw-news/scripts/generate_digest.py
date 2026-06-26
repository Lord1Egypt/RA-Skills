#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Claw-News 简报生成脚本"""

import os
from openai import OpenAI
from datetime import datetime

def generate_digest():
    client = OpenAI(
        api_key='sk-kimi-mU3OeWaHvOwipfEK2210ao2qcXGWZ0srvv9fMLhZgDOCd0HM8aXiEi9MxhSedm6x',
        base_url='https://api.moonshot.cn/v1'
    )

    interests = [
        ('🤖 人工智能', ['AI', '大模型', 'AGI', '机器学习']),
        ('💻 科技动态', ['科技', '互联网', '初创公司', '融资']),
        ('🚀 马斯克', ['Elon Musk', 'Tesla', 'SpaceX']),
        ('⛓️ 区块链', ['区块链', '加密货币', 'Web3'])
    ]
    
    print('='*70)
    print('📰 Claw-News 每日新闻简报')
    print(f'📅 {datetime.now().strftime("%Y年%m月%d日 %H:%M")}')
    print('='*70)
    print()

    for title, keywords in interests:
        print(f'\n{title}')
        print('-'*70)
        
        try:
            query = ' '.join(keywords[:3])
            response = client.chat.completions.create(
                model='kimi-k2-5',
                messages=[
                    {'role': 'system', 'content': '你是新闻助手，用中文总结最新新闻。每条新闻用"• 标题 - 摘要"格式，简洁明了。'},
                    {'role': 'user', 'content': f'搜索"{query}"的最新新闻（过去24小时），列出3-4条最重要的，格式：标题+一句话摘要。'}
                ],
                tools=[{'type': 'builtin_function', 'function': {'name': 'web_search'}}],
                temperature=0.3,
                timeout=60
            )
            
            content = response.choices[0].message.content
            print(content)
        except Exception as e:
            print(f'  ⚠️ 获取失败: {e}')
        print()

    print('='*70)
    print('🤖 Powered by Claw-News & Kimi AI')
    print('💡 使用 newsman add <关键词> 添加更多关注')
    print('='*70)

if __name__ == '__main__':
    generate_digest()
