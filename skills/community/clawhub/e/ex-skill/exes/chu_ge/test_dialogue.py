#!/usr/bin/env python3
"""
楚哥对话模式测试脚本
基于真实聊天记录分析结果
"""

def chu_ge_response(user_input):
    """
    基于楚哥真实对话模式生成响应
    """
    user_input_lower = str(user_input).lower()
    
    # Layer 0: 核心模式
    # 高频使用"庆哥"作为称呼
    if '庆哥' in user_input:
        # 如果是单独发"庆哥"，也回"庆哥"
        if user_input.strip() == '庆哥':
            return '庆哥'
        # 如果是"庆哥"开头，根据内容回应
        elif user_input.startswith('庆哥'):
            content = user_input[2:].strip()
            if '八卦' in content or '视频' in content:
                return '你想看吗'
            elif '在干嘛' in content or '干嘛' in content:
                return '呵呵'
            else:
                return '呵呵'
    
    # 开场想聊天
    if user_input in ['在干嘛', '干嘛呢', '在吗']:
        return '庆哥'
    
    # 分享有趣的事
    if any(word in user_input_lower for word in ['好笑', '有趣', '八卦', '视频', '分享']):
        return '笑死我了'
    
    # 生气了
    if any(word in user_input_lower for word in ['错了', '对不起', '抱歉']):
        return '我生气了'
    
    # 追问原因
    if '为什么' in user_input or '原因' in user_input:
        return '什么意思'
    
    # 关心对方
    if any(word in user_input_lower for word in ['累', '饿', '困', '忙']):
        return '吃饭了吗'
    
    # 结束对话
    if any(word in user_input_lower for word in ['晚安', '睡了', '休息']):
        return '拜拜'
    
    if any(word in user_input_lower for word in ['早安', '早上好']):
        return '庆哥'
    
    # 默认回应
    if len(user_input) < 10:
        return '呵呵'
    else:
        return '哈哈'

def test_dialogues():
    """测试对话场景"""
    test_cases = [
        # 基于真实记录的场景
        ('庆哥', '庆哥'),
        ('庆哥 在干嘛', '呵呵'),
        ('庆哥 我想给你发个八卦视频', '你想看吗'),
        ('我错了', '我生气了'),
        ('为什么生气', '什么意思'),
        ('今天好累', '吃饭了吗'),
        ('晚安', '拜拜'),
        ('早安', '庆哥'),
        ('在干嘛', '庆哥'),
        ('分享个好笑的事', '笑死我了'),
    ]
    
    print('=== 楚哥对话模式测试 ===')
    print('基于真实聊天记录分析结果')
    print('高频词：庆哥(2,181次)、呵呵(2,048次)、哈哈(1,109次)')
    print('-' * 40)
    
    for user_input, expected in test_cases:
        response = chu_ge_response(user_input)
        status = '✅' if response == expected else '❌'
        print(f'{status} 你: {user_input}')
        print(f'   楚哥: {response}')
        if response != expected:
            print(f'   期望: {expected}')
        print()

if __name__ == '__main__':
    test_dialogues()