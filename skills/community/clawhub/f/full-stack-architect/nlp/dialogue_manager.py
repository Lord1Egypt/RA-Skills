#!/usr/bin/env python3
"""
对话管理模块
负责管理与用户的对话
"""

import os
import json
import logging
from datetime import datetime
from .intent_recognition import IntentRecognizer
from .entity_extraction import EntityExtractor

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DialogueManager:
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.entity_extractor = EntityExtractor()
        self.dialogues = {}
        self.max_dialogue_history = 10
        self.config_path = os.path.join(os.path.dirname(__file__), 'dialogue_config.json')
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                if 'max_dialogue_history' in config:
                    self.max_dialogue_history = config['max_dialogue_history']
                logger.info("加载配置成功")
            except Exception as e:
                logger.error(f"加载配置失败: {str(e)}")
        else:
            # 保存默认配置
            self._save_config()
    
    def _save_config(self):
        """保存配置文件"""
        try:
            config = {
                'max_dialogue_history': self.max_dialogue_history
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            logger.info("配置保存成功")
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def start_dialogue(self, user_id):
        """开始对话
        
        Args:
            user_id: 用户ID
            
        Returns:
            dialogue_id: 对话ID
        """
        dialogue_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.dialogues[dialogue_id] = {
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'messages': [],
            'context': {}
        }
        logger.info(f"开始对话: {dialogue_id}")
        return dialogue_id
    
    def end_dialogue(self, dialogue_id):
        """结束对话
        
        Args:
            dialogue_id: 对话ID
        """
        if dialogue_id in self.dialogues:
            self.dialogues[dialogue_id]['end_time'] = datetime.now().isoformat()
            logger.info(f"结束对话: {dialogue_id}")
        else:
            logger.warning(f"对话不存在: {dialogue_id}")
    
    def add_message(self, dialogue_id, message_type, content):
        """添加消息
        
        Args:
            dialogue_id: 对话ID
            message_type: 消息类型 (user/assistant)
            content: 消息内容
        """
        if dialogue_id in self.dialogues:
            message = {
                'type': message_type,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            self.dialogues[dialogue_id]['messages'].append(message)
            
            # 限制对话历史长度
            if len(self.dialogues[dialogue_id]['messages']) > self.max_dialogue_history:
                self.dialogues[dialogue_id]['messages'] = self.dialogues[dialogue_id]['messages'][-self.max_dialogue_history:]
            
            logger.info(f"添加消息到对话: {dialogue_id}, 类型: {message_type}")
        else:
            logger.warning(f"对话不存在: {dialogue_id}")
    
    def get_dialogue(self, dialogue_id):
        """获取对话
        
        Args:
            dialogue_id: 对话ID
            
        Returns:
            dialogue: 对话信息
        """
        return self.dialogues.get(dialogue_id, None)
    
    def get_dialogue_history(self, dialogue_id):
        """获取对话历史
        
        Args:
            dialogue_id: 对话ID
            
        Returns:
            history: 对话历史
        """
        if dialogue_id in self.dialogues:
            return self.dialogues[dialogue_id]['messages']
        else:
            logger.warning(f"对话不存在: {dialogue_id}")
            return []
    
    def process_message(self, dialogue_id, user_message):
        """处理用户消息
        
        Args:
            dialogue_id: 对话ID
            user_message: 用户消息
            
        Returns:
            response: 处理结果
        """
        # 添加用户消息
        self.add_message(dialogue_id, 'user', user_message)
        
        # 识别意图
        intent_result = self.intent_recognizer.recognize_intent(user_message)
        
        # 提取实体
        entities = self.entity_extractor.extract_entities(user_message)
        
        # 更新对话上下文
        if dialogue_id in self.dialogues:
            self.dialogues[dialogue_id]['context']['last_intent'] = intent_result
            self.dialogues[dialogue_id]['context']['last_entities'] = entities
            self.dialogues[dialogue_id]['context']['last_message'] = user_message
        
        # 生成响应
        response = {
            'intent': intent_result,
            'entities': entities,
            'context': self.dialogues[dialogue_id]['context'] if dialogue_id in self.dialogues else {},
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"处理消息: {dialogue_id}, 意图: {intent_result['intent']}")
        return response
    
    def update_context(self, dialogue_id, context_updates):
        """更新对话上下文
        
        Args:
            dialogue_id: 对话ID
            context_updates: 上下文更新
        """
        if dialogue_id in self.dialogues:
            self.dialogues[dialogue_id]['context'].update(context_updates)
            logger.info(f"更新对话上下文: {dialogue_id}")
        else:
            logger.warning(f"对话不存在: {dialogue_id}")
    
    def get_context(self, dialogue_id):
        """获取对话上下文
        
        Args:
            dialogue_id: 对话ID
            
        Returns:
            context: 对话上下文
        """
        if dialogue_id in self.dialogues:
            return self.dialogues[dialogue_id]['context']
        else:
            logger.warning(f"对话不存在: {dialogue_id}")
            return {}
    
    def list_dialogues(self, user_id=None):
        """列出对话
        
        Args:
            user_id: 用户ID
            
        Returns:
            dialogues: 对话列表
        """
        if user_id:
            return [d for d in self.dialogues.values() if d['user_id'] == user_id]
        else:
            return list(self.dialogues.values())
    
    def delete_dialogue(self, dialogue_id):
        """删除对话
        
        Args:
            dialogue_id: 对话ID
        """
        if dialogue_id in self.dialogues:
            del self.dialogues[dialogue_id]
            logger.info(f"删除对话: {dialogue_id}")
        else:
            logger.warning(f"对话不存在: {dialogue_id}")
    
    def set_max_dialogue_history(self, max_history):
        """设置最大对话历史长度
        
        Args:
            max_history: 最大历史长度
        """
        self.max_dialogue_history = max_history
        self._save_config()
        logger.info(f"设置最大对话历史长度: {max_history}")

if __name__ == "__main__":
    # 测试对话管理器
    manager = DialogueManager()
    
    # 开始对话
    dialogue_id = manager.start_dialogue('test_user')
    print(f"开始对话，对话ID: {dialogue_id}")
    print()
    
    # 处理消息
    test_messages = [
        '帮我生成一个电商平台的PRD',
        '推荐一个金融系统的技术栈',
        '帮我写一个Python的阶乘函数'
    ]
    
    for message in test_messages:
        print(f"用户输入: {message}")
        response = manager.process_message(dialogue_id, message)
        print(f"识别的意图: {response['intent']['intent']}")
        print(f"提取的实体: {response['entities']}")
        print()
    
    # 获取对话历史
    history = manager.get_dialogue_history(dialogue_id)
    print("对话历史:")
    for msg in history:
        print(f"{msg['type']}: {msg['content']} ({msg['timestamp']})")
    print()
    
    # 更新上下文
    manager.update_context(dialogue_id, {'project_name': '测试项目'})
    context = manager.get_context(dialogue_id)
    print(f"更新后的上下文: {context}")
    print()
    
    # 结束对话
    manager.end_dialogue(dialogue_id)
    print("对话已结束")
