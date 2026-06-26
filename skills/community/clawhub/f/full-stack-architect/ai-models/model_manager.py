#!/usr/bin/env python3
"""
AI模型管理模块
负责管理AI模型的加载和调用
"""

import os
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self):
        self.models = {}
        self.model_configs = {}
        self.model_path = os.path.join(os.path.dirname(__file__), 'models')
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        # 创建模型目录
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        
        # 加载配置
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.model_configs = json.load(f)
                logger.info(f"加载配置成功，包含 {len(self.model_configs)} 个模型配置")
            except Exception as e:
                logger.error(f"加载配置失败: {str(e)}")
                self.model_configs = {}
        else:
            # 默认配置
            self.model_configs = {
                'default': {
                    'type': 'local',
                    'name': 'default',
                    'description': '默认AI模型',
                    'enabled': True
                }
            }
            self._save_config()
    
    def _save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.model_configs, f, ensure_ascii=False, indent=2)
            logger.info("配置保存成功")
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def add_model(self, model_name, model_config):
        """添加模型配置
        
        Args:
            model_name: 模型名称
            model_config: 模型配置
        """
        self.model_configs[model_name] = model_config
        self._save_config()
        logger.info(f"添加模型配置成功: {model_name}")
    
    def remove_model(self, model_name):
        """删除模型配置
        
        Args:
            model_name: 模型名称
        """
        if model_name in self.model_configs:
            del self.model_configs[model_name]
            self._save_config()
            logger.info(f"删除模型配置成功: {model_name}")
        else:
            logger.warning(f"模型配置不存在: {model_name}")
    
    def list_models(self):
        """列出所有模型配置
        
        Returns:
            model_list: 模型配置列表
        """
        return list(self.model_configs.items())
    
    def get_model(self, model_name='default'):
        """获取模型实例
        
        Args:
            model_name: 模型名称
            
        Returns:
            model: 模型实例
        """
        if model_name in self.models:
            return self.models[model_name]
        
        # 加载模型
        model = self._load_model(model_name)
        if model:
            self.models[model_name] = model
        
        return model
    
    def _load_model(self, model_name):
        """加载模型
        
        Args:
            model_name: 模型名称
            
        Returns:
            model: 模型实例
        """
        if model_name not in self.model_configs:
            logger.warning(f"模型配置不存在: {model_name}")
            return None
        
        model_config = self.model_configs[model_name]
        
        if not model_config.get('enabled', False):
            logger.warning(f"模型已禁用: {model_name}")
            return None
        
        model_type = model_config.get('type', 'local')
        
        try:
            if model_type == 'local':
                # 本地模型
                model = self._load_local_model(model_config)
            elif model_type == 'api':
                # API模型
                model = self._load_api_model(model_config)
            else:
                logger.error(f"不支持的模型类型: {model_type}")
                return None
            
            logger.info(f"加载模型成功: {model_name}")
            return model
        except Exception as e:
            logger.error(f"加载模型失败: {str(e)}")
            return None
    
    def _load_local_model(self, model_config):
        """加载本地模型
        
        Args:
            model_config: 模型配置
            
        Returns:
            model: 模型实例
        """
        # 这里是本地模型的加载逻辑
        # 由于是模拟，返回一个简单的模型实例
        class LocalModel:
            def __init__(self, config):
                self.config = config
            
            def generate(self, prompt, max_tokens=1000):
                # 模拟生成
                return f"模拟生成的内容: {prompt[:50]}..."
        
        return LocalModel(model_config)
    
    def _load_api_model(self, model_config):
        """加载API模型
        
        Args:
            model_config: 模型配置
            
        Returns:
            model: 模型实例
        """
        # 这里是API模型的加载逻辑
        # 由于是模拟，返回一个简单的模型实例
        class APIModel:
            def __init__(self, config):
                self.config = config
            
            def generate(self, prompt, max_tokens=1000):
                # 模拟生成
                return f"API生成的内容: {prompt[:50]}..."
        
        return APIModel(model_config)
    
    def generate(self, prompt, model_name='default', max_tokens=1000):
        """生成文本
        
        Args:
            prompt: 提示词
            model_name: 模型名称
            max_tokens: 最大 token 数
            
        Returns:
            result: 生成结果
        """
        model = self.get_model(model_name)
        if not model:
            return "模型加载失败"
        
        try:
            result = model.generate(prompt, max_tokens)
            logger.info(f"生成成功，模型: {model_name}")
            return result
        except Exception as e:
            logger.error(f"生成失败: {str(e)}")
            return f"生成失败: {str(e)}"
    
    def update_model_config(self, model_name, config_updates):
        """更新模型配置
        
        Args:
            model_name: 模型名称
            config_updates: 配置更新
        """
        if model_name in self.model_configs:
            self.model_configs[model_name].update(config_updates)
            self._save_config()
            logger.info(f"更新模型配置成功: {model_name}")
            
            # 如果模型已加载，重新加载
            if model_name in self.models:
                del self.models[model_name]
        else:
            logger.warning(f"模型配置不存在: {model_name}")

if __name__ == "__main__":
    # 测试模型管理器
    manager = ModelManager()
    
    # 列出模型
    print("当前模型列表:")
    for name, config in manager.list_models():
        print(f"- {name}: {config['description']}")
    
    # 测试生成
    result = manager.generate("写一个Hello World程序")
    print(f"\n生成结果:")
    print(result)
    
    # 添加新模型
    new_model_config = {
        'type': 'api',
        'name': 'test-api',
        'description': '测试API模型',
        'enabled': True,
        'api_key': 'test-key'
    }
    manager.add_model('test-api', new_model_config)
    
    # 测试新模型
    result = manager.generate("写一个Hello World程序", model_name='test-api')
    print(f"\nAPI模型生成结果:")
    print(result)
