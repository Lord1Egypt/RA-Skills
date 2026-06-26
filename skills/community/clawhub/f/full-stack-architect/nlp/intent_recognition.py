#!/usr/bin/env python3
"""
意图识别模块
负责识别用户的意图
"""

import os
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntentRecognizer:
    def __init__(self):
        self.intents = {
            'generate_prd': {
                'name': 'generate_prd',
                'description': '生成PRD文档',
                'keywords': [
                    '生成PRD', '创建PRD', '写PRD', 'PRD文档', '产品需求文档',
                    'generate PRD', 'create PRD', 'PRD document', 'product requirements document'
                ],
                'examples': [
                    '帮我生成一个电商平台的PRD',
                    '创建一个SaaS系统的产品需求文档',
                    '写一个移动应用的PRD'
                ]
            },
            'recommend_tech': {
                'name': 'recommend_tech',
                'description': '推荐技术栈',
                'keywords': [
                    '推荐技术栈', '技术选型', '技术方案', '技术推荐',
                    'recommend tech stack', 'technology selection', 'tech solution'
                ],
                'examples': [
                    '推荐一个电商平台的技术栈',
                    '帮我做一个技术选型',
                    '推荐适合SaaS系统的技术方案'
                ]
            },
            'generate_code': {
                'name': 'generate_code',
                'description': '生成代码',
                'keywords': [
                    '生成代码', '写代码', '代码实现', '编程',
                    'generate code', 'write code', 'code implementation', 'programming'
                ],
                'examples': [
                    '帮我生成一个Python的阶乘函数',
                    '写一个React组件',
                    '生成一个Go的Web服务器'
                ]
            },
            'explain_code': {
                'name': 'explain_code',
                'description': '解释代码',
                'keywords': [
                    '解释代码', '代码说明', '代码分析', '代码讲解',
                    'explain code', 'code explanation', 'code analysis', 'code walkthrough'
                ],
                'examples': [
                    '帮我解释这段代码',
                    '这段代码是什么意思',
                    '分析一下这段Python代码'
                ]
            },
            'analyze_bug': {
                'name': 'analyze_bug',
                'description': '分析代码中的bug',
                'keywords': [
                    '分析bug', '找bug', 'bug分析', '代码错误',
                    'analyze bug', 'find bug', 'bug analysis', 'code error'
                ],
                'examples': [
                    '帮我分析这段代码中的bug',
                    '找一下这段代码的错误',
                    '分析一下这段JavaScript代码的问题'
                ]
            },
            'generate_documentation': {
                'name': 'generate_documentation',
                'description': '生成文档',
                'keywords': [
                    '生成文档', '写文档', '文档编写', '技术文档',
                    'generate documentation', 'write documentation', 'document writing', 'technical documentation'
                ],
                'examples': [
                    '帮我生成一个API文档',
                    '写一个功能的技术文档',
                    '生成一个组件的使用文档'
                ]
            },
            'summarize_prd': {
                'name': 'summarize_prd',
                'description': '总结PRD文档',
                'keywords': [
                    '总结PRD', 'PRD总结', 'PRD分析', '分析PRD',
                    'summarize PRD', 'PRD summary', 'PRD analysis', 'analyze PRD'
                ],
                'examples': [
                    '帮我总结一下这个PRD',
                    '分析一下这个产品需求文档',
                    '总结这个PRD的核心内容'
                ]
            },
            'ask_question': {
                'name': 'ask_question',
                'description': '回答技术问题',
                'keywords': [
                    '如何', '怎么', '为什么', '什么是', '解释',
                    'how', 'what', 'why', 'explain', 'describe'
                ],
                'examples': [
                    '如何使用React Hooks',
                    '什么是微服务',
                    '解释一下RESTful API'
                ]
            }
        }
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                if 'intents' in config:
                    self.intents = config['intents']
                logger.info(f"加载配置成功，包含 {len(self.intents)} 个意图")
            except Exception as e:
                logger.error(f"加载配置失败: {str(e)}")
        else:
            # 保存默认配置
            self._save_config()
    
    def _save_config(self):
        """保存配置文件"""
        try:
            config = {
                'intents': self.intents
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            logger.info("配置保存成功")
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def add_intent(self, intent_name, intent_config):
        """添加意图
        
        Args:
            intent_name: 意图名称
            intent_config: 意图配置
        """
        self.intents[intent_name] = intent_config
        self._save_config()
        logger.info(f"添加意图成功: {intent_name}")
    
    def remove_intent(self, intent_name):
        """删除意图
        
        Args:
            intent_name: 意图名称
        """
        if intent_name in self.intents:
            del self.intents[intent_name]
            self._save_config()
            logger.info(f"删除意图成功: {intent_name}")
        else:
            logger.warning(f"意图不存在: {intent_name}")
    
    def list_intents(self):
        """列出所有意图
        
        Returns:
            intent_list: 意图列表
        """
        return list(self.intents.items())
    
    def recognize_intent(self, text):
        """识别意图
        
        Args:
            text: 输入文本
            
        Returns:
            intent: 识别结果
        """
        text_lower = text.lower()
        scores = {}
        
        # 计算每个意图的得分
        for intent_name, intent_config in self.intents.items():
            score = 0
            keywords = intent_config.get('keywords', [])
            
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += 1
            
            scores[intent_name] = score
        
        # 找出得分最高的意图
        if scores:
            best_intent = max(scores.items(), key=lambda x: x[1])
            if best_intent[1] > 0:
                return {
                    'intent': best_intent[0],
                    'score': best_intent[1],
                    'confidence': best_intent[1] / len(self.intents[best_intent[0]].get('keywords', [])),
                    'description': self.intents[best_intent[0]].get('description', '')
                }
        
        # 默认意图
        return {
            'intent': 'ask_question',
            'score': 0,
            'confidence': 0.5,
            'description': '回答技术问题'
        }
    
    def get_intent_config(self, intent_name):
        """获取意图配置
        
        Args:
            intent_name: 意图名称
            
        Returns:
            config: 意图配置
        """
        return self.intents.get(intent_name, None)
    
    def update_intent(self, intent_name, updates):
        """更新意图配置
        
        Args:
            intent_name: 意图名称
            updates: 更新内容
        """
        if intent_name in self.intents:
            self.intents[intent_name].update(updates)
            self._save_config()
            logger.info(f"更新意图成功: {intent_name}")
        else:
            logger.warning(f"意图不存在: {intent_name}")

if __name__ == "__main__":
    # 测试意图识别器
    recognizer = IntentRecognizer()
    
    # 测试意图列表
    print("当前意图列表:")
    for name, config in recognizer.list_intents():
        print(f"- {name}: {config['description']}")
    print()
    
    # 测试意图识别
    test_texts = [
        '帮我生成一个电商平台的PRD',
        '推荐一个SaaS系统的技术栈',
        '帮我写一个Python的阶乘函数',
        '解释一下这段代码',
        '分析一下这段代码中的bug',
        '帮我生成一个API文档',
        '总结一下这个PRD',
        '如何使用React Hooks'
    ]
    
    for text in test_texts:
        result = recognizer.recognize_intent(text)
        print(f"输入: {text}")
        print(f"意图: {result['intent']} (得分: {result['score']}, 置信度: {result['confidence']:.2f})")
        print(f"描述: {result['description']}")
        print()
