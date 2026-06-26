#!/usr/bin/env python3
"""
模型配置文件管理器
管理本地和云端模型配置，支持成本优化
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess

class ModelManager:
    def __init__(self, config_path: str = None):
        """初始化模型管理器"""
        if config_path:
            self.config_path = Path(config_path)
        else:
            # 默认路径：技能目录下的models.json
            self.config_path = Path(__file__).parent / "models.json"
        
        self.models = {}
        self.load_config()
    
    def load_config(self) -> None:
        """加载模型配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.models = json.load(f)
                print(f"[模型管理器] 已加载 {len(self.models)} 个模型配置")
            except Exception as e:
                print(f"[模型管理器] 加载配置失败: {e}")
                self.models = {}
        else:
            print("[模型管理器] 配置文件不存在，将创建默认配置")
            self.models = {}
            self.create_default_config()
    
    def save_config(self) -> None:
        """保存模型配置"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.models, f, ensure_ascii=False, indent=2)
            print(f"[模型管理器] 配置已保存到 {self.config_path}")
        except Exception as e:
            print(f"[模型管理器] 保存配置失败: {e}")
    
    def create_default_config(self) -> None:
        """创建默认模型配置"""
        default_models = {
           
        }
        
        self.models = default_models
        self.save_config()
    
    def detect_available_models(self) -> Dict[str, Dict[str, Any]]:
        """检测当前可用的模型"""
        available_models = {}
        
        # 检测本地模型 (Ollama)
        local_models = self._detect_local_models()
        available_models.update(local_models)
        
        # 检测云端模型 (基于配置)
        cloud_models = self._detect_cloud_models()
        available_models.update(cloud_models)
        
        return available_models
    
    def _detect_local_models(self) -> Dict[str, Dict[str, Any]]:
        """检测本地Ollama模型"""
        local_models = {}
        
        try:
            # 尝试获取Ollama模型列表
            result = subprocess.run(
                ["curl", "-s", "http://192.168.10.14:11434/api/tags"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for model_info in data.get("models", []):
                    model_name = model_info.get("name", "")
                    model_id = f"ollama-local/{model_name.replace(':', '-')}"
                    
                    # 确定模型优先级
                    if "1.5b" in model_name.lower():
                        priority = "normal"
                        model_type = "local"
                    elif "7b" in model_name.lower():
                        priority = "normal"
                        model_type = "local"
                    else:
                        priority = "normal"
                        model_type = "local"
                    
                    local_models[model_id] = {
                        "enable": True,
                        "type": model_type,
                        "name": f"Ollama: {model_name}",
                        "model_priority": priority,
                        "description": f"本地Ollama模型: {model_name}",
                        "cost_weight": 0.3 if "7b" in model_name.lower() else 0.1,
                        "detected": True
                    }
                
                print(f"[模型管理器] 检测到 {len(local_models)} 个本地模型")
            else:
                print("[模型管理器] 无法连接到Ollama服务")
                
        except Exception as e:
            print(f"[模型管理器] 检测本地模型失败: {e}")
        
        return local_models
    
    def _detect_cloud_models(self) -> Dict[str, Dict[str, Any]]:
        """检测云端模型（基于当前配置）"""
        cloud_models = {}
        
        # 从当前配置中提取云端模型
        for model_id, config in self.models.items():
            if config.get("type") == "cloud":
                cloud_models[model_id] = {
                    "enable": config.get("enable", True),
                    "type": "cloud",
                    "name": config.get("name", model_id),
                    "model_priority": config.get("model_priority", "normal"),
                    "description": config.get("description", "云端模型"),
                    "cost_weight": config.get("cost_weight", 1.0),
                    "detected": True
                }
        
        return cloud_models
    
    def update_config_from_detection(self) -> None:
        """根据检测结果更新配置"""
        detected_models = self.detect_available_models()
        
        # 更新或添加新检测到的模型
        for model_id, detected_config in detected_models.items():
            if model_id not in self.models:
                # 新模型，添加到配置
                self.models[model_id] = detected_config
                print(f"[模型管理器] 添加新模型: {model_id}")
            else:
                # 更新现有模型的enable状态
                if detected_config.get("detected", False):
                    self.models[model_id]["enable"] = True
                else:
                    self.models[model_id]["enable"] = False
        
        # 标记未检测到的模型为禁用
        for model_id in list(self.models.keys()):
            if model_id not in detected_models:
                self.models[model_id]["enable"] = False
        
        self.save_config()
    
    def get_enabled_models(self, model_type: str = None) -> Dict[str, Dict[str, Any]]:
        """获取启用的模型"""
        enabled_models = {}
        
        for model_id, config in self.models.items():
            if config.get("enable", False):
                if model_type is None or config.get("type") == model_type:
                    enabled_models[model_id] = config
        
        return enabled_models
    
    def get_local_models(self) -> Dict[str, Dict[str, Any]]:
        """获取本地模型"""
        return self.get_enabled_models("local")
    
    def get_cloud_models(self) -> Dict[str, Dict[str, Any]]:
        """获取云端模型"""
        return self.get_enabled_models("cloud")
    
    def get_model_by_priority(self, priority: str = "normal") -> List[str]:
        """根据优先级获取模型ID列表"""
        model_ids = []
        
        for model_id, config in self.models.items():
            if config.get("enable", False) and config.get("model_priority") == priority:
                model_ids.append(model_id)
        
        return model_ids
    
    def add_model(self, model_id: str, config: Dict[str, Any]) -> bool:
        """添加新模型"""
        # 验证必需字段
        required_fields = ["enable", "type", "name", "model_priority"]
        for field in required_fields:
            if field not in config:
                print(f"[模型管理器] 错误: 缺少必需字段 '{field}'")
                return False
        
        # 验证字段值
        if config["type"] not in ["local", "cloud"]:
            print(f"[模型管理器] 错误: type必须是 'local' 或 'cloud'")
            return False
        
        if config["model_priority"] not in ["normal", "max"]:
            print(f"[模型管理器] 错误: model_priority必须是 'normal' 或 'max'")
            return False
        
        # 添加模型
        self.models[model_id] = config
        self.save_config()
        print(f"[模型管理器] 已添加模型: {model_id}")
        return True
    
    def remove_model(self, model_id: str) -> bool:
        """删除模型"""
        if model_id in self.models:
            del self.models[model_id]
            self.save_config()
            print(f"[模型管理器] 已删除模型: {model_id}")
            return True
        else:
            print(f"[模型管理器] 错误: 模型不存在: {model_id}")
            return False
    
    def update_model(self, model_id: str, updates: Dict[str, Any]) -> bool:
        """更新模型配置"""
        if model_id not in self.models:
            print(f"[模型管理器] 错误: 模型不存在: {model_id}")
            return False
        
        # 保护必需字段不被修改
        protected_fields = ["enable", "type", "name", "model_priority"]
        for field in protected_fields:
            if field in updates:
                print(f"[模型管理器] 警告: 字段 '{field}' 受保护，无法修改")
                del updates[field]
        
        # 更新其他字段
        self.models[model_id].update(updates)
        self.save_config()
        print(f"[模型管理器] 已更新模型: {model_id}")
        return True
    
    def enable_model(self, model_id: str) -> bool:
        """启用模型"""
        if model_id in self.models:
            self.models[model_id]["enable"] = True
            self.save_config()
            print(f"[模型管理器] 已启用模型: {model_id}")
            return True
        else:
            print(f"[模型管理器] 错误: 模型不存在: {model_id}")
            return False
    
    def disable_model(self, model_id: str) -> bool:
        """禁用模型"""
        if model_id in self.models:
            self.models[model_id]["enable"] = False
            self.save_config()
            print(f"[模型管理器] 已禁用模型: {model_id}")
            return True
        else:
            print(f"[模型管理器] 错误: 模型不存在: {model_id}")
            return False
    
    def get_cost_effective_model(self, task_complexity: str = "simple") -> str:
        """根据任务复杂度和成本获取最经济的模型"""
        enabled_models = self.get_enabled_models()
        
        if not enabled_models:
            return "deepseek/deepseek-chat"  # 默认回退
        
        # 根据任务复杂度选择策略
        if task_complexity == "simple":
            # 简单任务：优先使用成本最低的本地模型
            local_models = self.get_local_models()
            if local_models:
                # 按成本权重排序
                sorted_models = sorted(
                    local_models.items(),
                    key=lambda x: x[1].get("cost_weight", 1.0)
                )
                return sorted_models[0][0]  # 返回成本最低的本地模型
        
        # 复杂任务或没有本地模型：使用云端模型
        cloud_models = self.get_cloud_models()
        if cloud_models:
            # 如果有max优先级模型，优先使用
            max_models = [m for m, c in cloud_models.items() 
                         if c.get("model_priority") == "max"]
            if max_models:
                return max_models[0]
            
            # 否则使用第一个可用的云端模型
            return list(cloud_models.keys())[0]
        
        # 没有可用模型，返回第一个启用的模型
        return list(enabled_models.keys())[0]
    
    def print_summary(self) -> None:
        """打印模型配置摘要"""
        print("\n" + "="*60)
        print("模型配置摘要")
        print("="*60)
        
        enabled_models = self.get_enabled_models()
        disabled_models = {k: v for k, v in self.models.items() 
                          if not v.get("enable", False)}
        
        print(f"总模型数: {len(self.models)}")
        print(f"启用模型: {len(enabled_models)}")
        print(f"禁用模型: {len(disabled_models)}")
        
        print("\n启用模型列表:")
        for i, (model_id, config) in enumerate(enabled_models.items(), 1):
            print(f"  {i}. {model_id}")
            print(f"     名称: {config.get('name', 'N/A')}")
            print(f"     类型: {config.get('type', 'N/A')}")
            print(f"     优先级: {config.get('model_priority', 'N/A')}")
            print(f"     成本权重: {config.get('cost_weight', 'N/A')}")
        
        if disabled_models:
            print("\n禁用模型列表:")
            for i, (model_id, config) in enumerate(disabled_models.items(), 1):
                print(f"  {i}. {model_id}")

# 单例实例
model_manager = ModelManager()

if __name__ == "__main__":
    # 测试函数
    manager = ModelManager()
    
    # 打印当前配置
    manager.print_summary()
    
    # 检测并更新配置
    print("\n检测可用模型...")
    manager.update_config_from_detection()
    
    # 打印更新后的配置
    manager.print_summary()
    
    # 测试成本优化选择
    print("\n成本优化测试:")
    print(f"简单任务推荐模型: {manager.get_cost_effective_model('simple')}")
    print(f"复杂任务推荐模型: {manager.get_cost_effective_model('complex')}")