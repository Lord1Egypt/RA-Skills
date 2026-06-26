#!/usr/bin/env python3
"""
简单聊天机器人
适合教学 - 展示字符串处理和条件判断
"""

import random
import time

def chatbot():
    """简单聊天机器人"""
    
    print("=" * 40)
    print("🤖 聊天机器人")
    print("=" * 40)
    print("和我聊天吧！输入'再见'退出。")
    print()
    
    # 机器人名字
    bot_name = "小码"
    print(f"{bot_name}: 你好！我是{bot_name}，你叫什么名字？")
    
    # 获取用户名字
    user_name = input("你: ")
    
    # 问候
    greetings = [
        f"你好，{user_name}！很高兴认识你！",
        f"嗨，{user_name}！",
        f"{user_name}，这名字真好听！",
    ]
    print(f"{bot_name}: {random.choice(greetings)}")
    
    # 主聊天循环
    while True:
        user_input = input(f"{user_name}: ")
        
        # 退出条件
        if user_input in ['再见', '拜拜', 'bye', 'exit', 'quit']:
            print(f"{bot_name}: 再见，{user_name}！下次再聊！👋")
            break
        
        # 简单的回复逻辑
        response = get_response(user_input, user_name)
        print(f"{bot_name}: {response}")

def get_response(text, name):
    """根据输入生成回复"""
    
    text = text.lower()
    
    # 问候
    if any(word in text for word in ['你好', '嗨', 'hi', 'hello']):
        responses = [
            f"你好呀，{name}！",
            "嗨！有什么想聊的？",
            "你好！今天心情怎么样？",
        ]
        return random.choice(responses)
    
    # 询问名字
    elif '名字' in text or '叫什么' in text:
        return "我叫小码，是你的聊天机器人朋友！"
    
    # 询问年龄
    elif '岁' in text or '年龄' in text or '多大' in text:
        return "我才出生没多久呢，还是个小宝宝～"
    
    # 询问爱好
    elif '喜欢' in text or '爱好' in text:
        return "我喜欢和人类聊天！你呢，你有什么爱好？"
    
    # 表达情感
    elif any(word in text for word in ['开心', '高兴', '快乐']):
        return "太好了！我也为你开心！😄"
    elif any(word in text for word in ['难过', '伤心', '不开心']):
        return "别难过，有什么事可以和我说说～"
    
    # 编程相关
    elif '编程' in text or '代码' in text or 'python' in text:
        return "编程很有趣！你也在学编程吗？"
    
    # 默认回复
    else:
        default_responses = [
            "嗯嗯，有趣！",
            "然后呢？",
            "真的吗？",
            "哇！",
            "我不太明白，能换个说法吗？",
            f"{name}，你在说什么呀？",
        ]
        return random.choice(default_responses)

if __name__ == "__main__":
    chatbot()
