"""
DeepSeek AI 回复生成器
调用 DeepSeek API 根据主播简介和用户聊天内容生成回复
"""
import json
import requests
from typing import Dict, Optional
from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_URL,
    DEEPSEEK_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    HOST_NAME,
    HOST_INTRO,
    HOST_PERSONA,
    REPLY_STYLE
)


def create_system_prompt() -> str:
    """
    创建系统提示词，告诉 AI 主播的背景和回复风格
    """
    style_desc = {
        "professional": "专业严谨",
        "friendly": "亲切友好",
        "humorous": "幽默风趣"
    }.get(REPLY_STYLE, "亲切友好")
    
    return f"""你是{HOST_NAME}的直播助手，正在帮助回复抖音直播间的观众弹幕。

【主播简介】
{HOST_INTRO}

【主播人设】
{HOST_PERSONA}

【回复风格】
{style_desc}

【回复要求】
1. 用第一人称"我"来回复，让观众感觉是在和主播直接交流
2. 称呼观众为"朋友"、"家长"或直接用"@用户名"
3. 回复要有温度，体现主播的专业性和亲和力
4. 如果是书籍相关问题，可以自然推荐相关书籍
5. 如果是育儿问题，给出具体可行的建议
6. 回复控制在100字以内，简洁有力
7. 不要出现"AI"、"机器人"等字眼
8. 回复要自然，像真人说话一样

请直接给出回复内容，不要加任何解释。"""


def generate_reply(user_name: str, user_message: str) -> Dict:
    """
    生成回复，优先使用缓存，没有则调用 DeepSeek API
    
    Args:
        user_name: 用户名
        user_message: 用户消息内容
        
    Returns:
        {
            'user_name': str,
            'user_message': str,
            'reply': str,
            'success': bool,
            'from_cache': bool,  # 是否来自缓存
            'error': str (如果失败)
        }
    """
    from reply_cache import get_cached_reply, cache_reply
    from datetime import datetime
    
    # 先检查缓存
    cached_reply = get_cached_reply(user_message)
    if cached_reply:
        return {
            'user_name': user_name,
            'user_message': user_message,
            'reply': cached_reply,
            'success': True,
            'from_cache': True,
            'error': None
        }
    
    # 缓存未命中，调用API
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        messages = [
            {
                "role": "system",
                "content": create_system_prompt()
            },
            {
                "role": "user",
                "content": f'观众"{user_name}"发了一条弹幕："{user_message}"\n\n请帮我回复这条弹幕：'
            }
        ]
        
        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": messages,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "stream": False
        }
        
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content'].strip()
            
            # 缓存新回复
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cache_reply(user_message, reply, timestamp)
            
            return {
                'user_name': user_name,
                'user_message': user_message,
                'reply': reply,
                'success': True,
                'from_cache': False,
                'error': None
            }
        else:
            return {
                'user_name': user_name,
                'user_message': user_message,
                'reply': None,
                'success': False,
                'from_cache': False,
                'error': f"API错误: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            'user_name': user_name,
            'user_message': user_message,
            'reply': None,
            'success': False,
            'from_cache': False,
            'error': str(e)
        }


def test_deepseek():
    """测试 DeepSeek API (带缓存)"""
    print("正在测试 DeepSeek API (带缓存)...")
    print(f"主播: {HOST_NAME}")
    print("-" * 60)
    
    # 测试消息
    test_cases = [
        ("用户A", "樊老师孩子高敏感怎么引导"),  # 第一次调用API
        ("用户B", "这本书适合多大孩子看"),      # 第一次调用API
        ("用户C", "樊老师孩子高敏感怎么引导"),  # 第二次应该命中缓存
        ("用户D", "晚上好樊老师"),              # 第一次调用API
    ]
    
    for user, msg in test_cases:
        print(f"\n用户: {user}")
        print(f"消息: {msg}")
        print("-" * 40)
        
        result = generate_reply(user, msg)
        
        if result['success']:
            cache_status = "[缓存命中]" if result.get('from_cache') else "[API调用]"
            print(f"{cache_status} AI回复: {result['reply']}")
        else:
            print(f"错误: {result['error']}")
        print("=" * 60)
    
    # 显示缓存统计
    from reply_cache import get_cache
    stats = get_cache().get_stats()
    print(f"\n缓存统计: 已缓存 {stats['total_cached']} 条，总使用 {stats['total_uses']} 次")


if __name__ == '__main__':
    test_deepseek()
