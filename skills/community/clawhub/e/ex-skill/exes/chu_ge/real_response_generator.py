#!/usr/bin/env python3
"""
基于真实聊天记录的楚哥响应生成器
"""

import json
import re

class ChuGeRealResponse:
    """基于真实对话模式的楚哥响应生成器"""
    
    def __init__(self):
        # 加载真实对话规则
        with open('training_rules.json', 'r', encoding='utf-8') as f:
            self.training_rules = json.load(f)
        
        # 加载真实对话数据
        with open('real_conversations.json', 'r', encoding='utf-8') as f:
            self.real_conversations = json.load(f)
        
        # 构建响应映射
        self.response_map = self._build_response_map()
        
        # 高频词统计（从之前的分析）
        self.high_freq_words = {
            '庆哥': 2181,
            '张庆': 1379,
            '呵呵': 2048,
            '哈哈': 1109,
            '拜拜': 222,
            '晚安': 133,
            '我服了': 242,
            '笑死我了': 637,
            '什么意思': 207
        }
    
    def _build_response_map(self):
        """构建用户输入到楚哥响应的映射"""
        response_map = {}
        
        for rule in self.training_rules:
            user_input = rule['user_input'].strip().lower()
            chu_response = rule['chu_response']
            
            if user_input not in response_map:
                response_map[user_input] = []
            
            if chu_response not in response_map[user_input]:
                response_map[user_input].append(chu_response)
        
        return response_map
    
    def find_similar_input(self, user_input):
        """找到最相似的用户输入"""
        user_input_lower = user_input.strip().lower()
        
        # 完全匹配
        if user_input_lower in self.response_map:
            return user_input_lower
        
        # 部分匹配
        for stored_input in self.response_map.keys():
            if stored_input in user_input_lower or user_input_lower in stored_input:
                return stored_input
        
        # 关键词匹配
        keywords = ['庆哥', '呵呵', '哈哈', '生气', '吃饭', '睡觉', '晚安', '拜拜']
        for keyword in keywords:
            if keyword in user_input_lower:
                # 返回包含该关键词的输入
                for stored_input in self.response_map.keys():
                    if keyword in stored_input:
                        return stored_input
        
        return None
    
    def generate_response(self, user_input):
        """生成楚哥的响应"""
        if not user_input or len(user_input.strip()) == 0:
            return "庆哥"
        
        user_input_lower = user_input.strip().lower()
        
        # 1. 尝试基于真实规则匹配
        similar_input = self.find_similar_input(user_input)
        if similar_input and similar_input in self.response_map:
            responses = self.response_map[similar_input]
            # 返回最常见的响应
            return responses[0] if responses else "呵呵"
        
        # 2. 基于高频词的模式匹配
        # 检查是否包含"庆哥"
        if '庆哥' in user_input:
            if user_input.strip() == '庆哥':
                return '庆哥'
            else:
                return '呵呵'
        
        # 检查是否包含问候
        if any(word in user_input_lower for word in ['早安', '早上好', '早']):
            return '庆哥'
        
        if any(word in user_input_lower for word in ['晚安', '睡了', '休息']):
            return '拜拜'
        
        # 检查是否包含关心
        if any(word in user_input_lower for word in ['累', '饿', '困', '忙', '辛苦']):
            return '吃饭了吗'
        
        # 检查是否包含道歉
        if any(word in user_input_lower for word in ['错了', '对不起', '抱歉']):
            return '我生气了'
        
        # 检查是否包含询问
        if any(word in user_input_lower for word in ['为什么', '原因', '怎么']):
            return '什么意思'
        
        # 检查是否分享有趣的事
        if any(word in user_input_lower for word in ['好笑', '有趣', '八卦', '视频']):
            return '笑死我了'
        
        # 3. 基于消息长度和内容的默认响应
        if len(user_input) < 10:
            # 短消息，用高频词回应
            return '呵呵'
        else:
            # 长消息，根据内容选择
            if '?' in user_input or '？' in user_input:
                return '什么意思'
            elif '!' in user_input or '！' in user_input:
                return '哈哈'
            else:
                return '呵呵'
    
    def get_conversation_examples(self, count=5):
        """获取真实的对话示例"""
        examples = []
        for i, dialogue in enumerate(self.real_conversations[:count]):
            example = []
            for turn in dialogue:
                role = '你' if turn['role'] == 'user' else '楚哥'
                content = turn['content']
                if len(content) > 50:
                    content = content[:50] + '...'
                example.append(f'{role}: {content}')
            examples.append('\\n'.join(example))
        return examples

def test_real_responses():
    """测试真实响应生成"""
    generator = ChuGeRealResponse()
    
    test_cases = [
        # 基于真实规则
        ('怎么坐船了', '偷渡回去'),
        ('注意点 别被警察叔叔逮住了', '知道这是哪里吗'),
        ('这是在河里呀，你好傻', '[疑问]'),
        ('我去找找那里可以放孔明灯', '呵呵'),
        ('你怎么一天到晚王者荣耀啊', '你还不是天天打游戏'),
        ('开始咯', '怎么回事'),
        
        # 基于高频词
        ('庆哥', '庆哥'),
        ('庆哥 在干嘛', '呵呵'),
        ('早安', '庆哥'),
        ('晚安', '拜拜'),
        ('我错了', '我生气了'),
        ('为什么生气', '什么意思'),
        ('今天好累', '吃饭了吗'),
        ('分享个好笑的事', '笑死我了'),
    ]
    
    print('=== 基于真实聊天记录的楚哥响应测试 ===')
    print('高频词统计:')
    for word, count in generator.high_freq_words.items():
        if count > 200:
            print(f'  {word}: {count}次')
    print()
    
    print('测试结果:')
    print('-' * 50)
    
    correct = 0
    total = len(test_cases)
    
    for user_input, expected in test_cases:
        response = generator.generate_response(user_input)
        status = '✅' if response == expected else '❌'
        
        print(f'{status} 你: {user_input}')
        print(f'   楚哥: {response}')
        
        if response != expected:
            print(f'   期望: {expected}')
        
        print()
        
        if response == expected:
            correct += 1
    
    print(f'准确率: {correct}/{total} ({correct/total*100:.1f}%)')
    
    # 显示真实对话示例
    print('\\n=== 真实对话示例 ===')
    examples = generator.get_conversation_examples(3)
    for i, example in enumerate(examples, 1):
        print(f'\\n示例 {i}:')
        print('-' * 30)
        print(example)

if __name__ == '__main__':
    test_real_responses()