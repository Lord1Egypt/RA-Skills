#!/usr/bin/env python3
"""
实体提取模块
负责从用户输入中提取关键实体
"""

import os
import json
import logging
import re
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EntityExtractor:
    def __init__(self):
        self.entity_patterns = {
            'project_name': {
                'name': 'project_name',
                'description': '项目名称',
                'patterns': [
                    r'(?:项目|系统|平台|应用|软件)\s*(?:名称|叫|是)?\s*(\S+)',
                    r'(?:创建|生成|开发)\s*(?:一个|一个新的)?\s*(\S+)\s*(?:项目|系统|平台|应用|软件)',
                    r'(\S+)\s*(?:项目|系统|平台|应用|软件)\s*(?:的|要|需要)'
                ]
            },
            'industry': {
                'name': 'industry',
                'description': '行业领域',
                'patterns': [
                    r'(?:电商|金融|医疗|教育|游戏|社交|企业|政府|零售|制造|物流|交通|能源|农业|媒体|娱乐|体育|旅游|房地产|法律|咨询)\s*(?:行业|领域|市场)',
                    r'(?:电商|金融|医疗|教育|游戏|社交|企业|政府|零售|制造|物流|交通|能源|农业|媒体|娱乐|体育|旅游|房地产|法律|咨询)\s*(?:平台|系统|应用)',
                    r'(?:行业|领域)\s*是?\s*(电商|金融|医疗|教育|游戏|社交|企业|政府|零售|制造|物流|交通|能源|农业|媒体|娱乐|体育|旅游|房地产|法律|咨询)'
                ],
                'keywords': [
                    '电商', '金融', '医疗', '教育', '游戏', '社交', '企业', '政府',
                    '零售', '制造', '物流', '交通', '能源', '农业', '媒体', '娱乐',
                    '体育', '旅游', '房地产', '法律', '咨询'
                ]
            },
            'tech_stack': {
                'name': 'tech_stack',
                'description': '技术栈',
                'patterns': [
                    r'(?:使用|采用|基于|用)\s*(\S+)\s*(?:技术|框架|语言)',
                    r'(\S+)\s*(?:技术|框架|语言)\s*(?:开发|构建)',
                    r'(?:技术|框架|语言)\s*是?\s*(\S+)'
                ],
                'keywords': [
                    'React', 'Vue', 'Angular', 'Svelte', 'Solid.js',
                    'Node.js', 'Express', 'Nest.js', 'Python', 'FastAPI', 'Django', 'Flask',
                    'Go', 'Java', 'Spring', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
                    'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP'
                ]
            },
            'functionality': {
                'name': 'functionality',
                'description': '功能需求',
                'patterns': [
                    r'(?:需要|要有|具备|实现)\s*(.*?)\s*(?:功能|特性|能力)',
                    r'(.*?)\s*(?:功能|特性|能力)\s*(?:需要|要有|具备|实现)',
                    r'(?:功能|特性|能力)\s*包括\s*(.*?)'
                ]
            },
            'language': {
                'name': 'language',
                'description': '编程语言',
                'patterns': [
                    r'(?:使用|用)\s*(\S+)\s*(?:语言|编程)',
                    r'(\S+)\s*(?:语言|编程)\s*(?:开发|写)',
                    r'(?:语言|编程)\s*是?\s*(\S+)'
                ],
                'keywords': [
                    'Python', 'JavaScript', 'Java', 'Go', 'C++', 'C#', 'PHP',
                    'Ruby', 'Swift', 'Kotlin', 'TypeScript', 'HTML', 'CSS'
                ]
            },
            'platform': {
                'name': 'platform',
                'description': '平台类型',
                'patterns': [
                    r'(?:Web|移动端|桌面端|服务器|云端|IoT|嵌入式)\s*(?:平台|应用|系统)',
                    r'(?:平台|应用|系统)\s*是?\s*(Web|移动端|桌面端|服务器|云端|IoT|嵌入式)',
                    r'(?:开发|构建)\s*(Web|移动端|桌面端|服务器|云端|IoT|嵌入式)\s*(?:平台|应用|系统)'
                ],
                'keywords': [
                    'Web', '移动端', '桌面端', '服务器', '云端', 'IoT', '嵌入式'
                ]
            }
        }
        self.config_path = os.path.join(os.path.dirname(__file__), 'entity_config.json')
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                if 'entity_patterns' in config:
                    self.entity_patterns = config['entity_patterns']
                logger.info(f"加载配置成功，包含 {len(self.entity_patterns)} 个实体类型")
            except Exception as e:
                logger.error(f"加载配置失败: {str(e)}")
        else:
            # 保存默认配置
            self._save_config()
    
    def _save_config(self):
        """保存配置文件"""
        try:
            config = {
                'entity_patterns': self.entity_patterns
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            logger.info("配置保存成功")
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def add_entity_pattern(self, entity_name, entity_config):
        """添加实体模式
        
        Args:
            entity_name: 实体名称
            entity_config: 实体配置
        """
        self.entity_patterns[entity_name] = entity_config
        self._save_config()
        logger.info(f"添加实体模式成功: {entity_name}")
    
    def remove_entity_pattern(self, entity_name):
        """删除实体模式
        
        Args:
            entity_name: 实体名称
        """
        if entity_name in self.entity_patterns:
            del self.entity_patterns[entity_name]
            self._save_config()
            logger.info(f"删除实体模式成功: {entity_name}")
        else:
            logger.warning(f"实体模式不存在: {entity_name}")
    
    def list_entity_patterns(self):
        """列出所有实体模式
        
        Returns:
            patterns: 实体模式列表
        """
        return list(self.entity_patterns.items())
    
    def extract_entities(self, text):
        """提取实体
        
        Args:
            text: 输入文本
            
        Returns:
            entities: 提取的实体
        """
        entities = {}
        
        for entity_name, entity_config in self.entity_patterns.items():
            extracted = self._extract_entity(text, entity_config)
            if extracted:
                entities[entity_name] = extracted
        
        return entities
    
    def _extract_entity(self, text, entity_config):
        """提取单个实体
        
        Args:
            text: 输入文本
            entity_config: 实体配置
            
        Returns:
            entity: 提取的实体
        """
        # 使用正则表达式提取
        patterns = entity_config.get('patterns', [])
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        # 使用关键词提取
        if 'keywords' in entity_config:
            keywords = entity_config['keywords']
            for keyword in keywords:
                if keyword in text:
                    return keyword
        
        return None
    
    def extract_specific_entity(self, text, entity_name):
        """提取特定实体
        
        Args:
            text: 输入文本
            entity_name: 实体名称
            
        Returns:
            entity: 提取的实体
        """
        if entity_name in self.entity_patterns:
            return self._extract_entity(text, self.entity_patterns[entity_name])
        else:
            logger.warning(f"实体模式不存在: {entity_name}")
            return None
    
    def update_entity_pattern(self, entity_name, updates):
        """更新实体模式
        
        Args:
            entity_name: 实体名称
            updates: 更新内容
        """
        if entity_name in self.entity_patterns:
            self.entity_patterns[entity_name].update(updates)
            self._save_config()
            logger.info(f"更新实体模式成功: {entity_name}")
        else:
            logger.warning(f"实体模式不存在: {entity_name}")

if __name__ == "__main__":
    # 测试实体提取器
    extractor = EntityExtractor()
    
    # 测试实体模式列表
    print("当前实体模式列表:")
    for name, config in extractor.list_entity_patterns():
        print(f"- {name}: {config['description']}")
    print()
    
    # 测试实体提取
    test_texts = [
        '帮我生成一个电商平台的PRD，使用React和Node.js技术栈',
        '推荐一个金融系统的技术栈，需要高性能和安全性',
        '帮我写一个Python的阶乘函数，用于Web应用',
        '解释一下这段JavaScript代码，它是一个React组件',
        '分析一下这段Go代码中的bug，它是一个Web服务器'
    ]
    
    for text in test_texts:
        entities = extractor.extract_entities(text)
        print(f"输入: {text}")
        print("提取的实体:")
        for entity_name, entity_value in entities.items():
            print(f"  {entity_name}: {entity_value}")
        print()
