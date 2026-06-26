#!/usr/bin/env python3
"""
Dashboard Configuration Manager - Simplified Version
管理Dashboard的配置信息
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器 - 简化版"""
    
    DEFAULT_CONFIG = {
        "dashboard_name": "Agent Dashboard",
        "dashboard_subtitle": "实时监控 Agent 状态与 Token 使用情况",
        "theme": "dark",
        "refresh_interval": 30,
        "host": "0.0.0.0",
        "port": 5177,
        "debug": False,
        "show_cost_estimates": True,
        "cost_decimal_places": 4,
        "token_cost": {
            "input_price_per_1m": 2.0,
            "output_price_per_1m": 8.0,
            "cache_price_per_1m": 1.0,
            "currency": "CNY"
        },
        "agent_configs": {
            "main": {
                "name": "小七",
                "role": "主助手",
                "emoji": "🎯",
                "color": "main",
                "description": "主要对话助手，处理日常任务"
            },
            "coder": {
                "name": "Coder",
                "role": "代码专家",
                "emoji": "💻",
                "color": "coder",
                "description": "专注代码编写与技术支持"
            },
            "brainstorm": {
                "name": "Brainstorm",
                "role": "创意顾问",
                "emoji": "💡",
                "color": "brainstorm",
                "description": "头脑风暴与创意生成"
            },
            "writer": {
                "name": "Writer",
                "role": "写作助手",
                "emoji": "✍️",
                "color": "writer",
                "description": "文档撰写与内容创作"
            },
            "investor": {
                "name": "Investor",
                "role": "投资分析",
                "emoji": "📈",
                "color": "investor",
                "description": "投资分析与市场研究"
            }
        },
        "view_mode": "grid",  # grid, grid-horizontal, list
        "agent_order": [],  # 自定义排序，空数组表示按默认顺序
        "openclaw_base_url": "http://127.0.0.1:18789"  # OpenClaw 服务基础 URL
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self._config: Dict[str, Any] = {}
        
        # 确定配置文件路径
        if config_path:
            self.config_path = Path(config_path)
        else:
            project_dir = Path(__file__).parent
            self.config_path = project_dir / "data" / "config.json"
        
        # 确保目录存在
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载配置
        self.load()
    
    def load(self) -> Dict[str, Any]:
        """从文件加载配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                # 合并默认配置
                self._config = self._merge_config(self.DEFAULT_CONFIG.copy(), loaded)
                print(f"[Config] 配置已加载: {self.config_path}")
            except Exception as e:
                print(f"[Config] 加载配置失败: {e}, 使用默认配置")
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            print(f"[Config] 配置文件不存在，创建默认配置")
            self._config = self.DEFAULT_CONFIG.copy()
            self.save()
        
        return self._config
    
    def _merge_config(self, default: Dict, override: Dict) -> Dict:
        """递归合并配置"""
        result = default.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def save(self) -> bool:
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[Config] 保存配置失败: {e}")
            return False
    
    def get(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self._config
    
    def update(self, updates: Dict[str, Any]) -> bool:
        """更新配置"""
        try:
            self._config = self._merge_config(self._config, updates)
            return self.save()
        except Exception as e:
            print(f"[Config] 更新配置失败: {e}")
            return False
    
    def update_agent_avatar(self, agent_name: str, avatar_path: str) -> bool:
        """更新agent头像路径"""
        if "agent_configs" not in self._config:
            self._config["agent_configs"] = {}
        
        if agent_name not in self._config["agent_configs"]:
            self._config["agent_configs"][agent_name] = {
                "name": agent_name.capitalize(),
                "role": "Agent",
                "emoji": "🤖",
                "color": "cyan",
                "description": f"{agent_name} agent"
            }
        
        self._config["agent_configs"][agent_name]["avatar_path"] = avatar_path
        return self.save()
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """获取agent配置"""
        configs = self._config.get("agent_configs", {})
        if agent_name in configs:
            return configs[agent_name]
        
        # 返回默认配置
        if agent_name in self.DEFAULT_CONFIG["agent_configs"]:
            return self.DEFAULT_CONFIG["agent_configs"][agent_name]
        
        return {
            "name": agent_name.capitalize(),
            "role": "Agent",
            "emoji": "🤖",
            "color": "cyan",
            "description": f"{agent_name} agent"
        }
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, 
                       cache_read: int = 0, cache_write: int = 0) -> Dict[str, float]:
        """计算token成本"""
        cost_config = self._config.get("token_cost", {})
        input_price = cost_config.get("input_price_per_1m", 2.0)
        output_price = cost_config.get("output_price_per_1m", 8.0)
        cache_price = cost_config.get("cache_price_per_1m", 1.0)
        currency = cost_config.get("currency", "CNY")
        
        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price
        cache_cost = ((cache_read + cache_write) / 1_000_000) * cache_price
        total = input_cost + output_cost + cache_cost
        
        return {
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "cache_cost": round(cache_cost, 6),
            "total_cost": round(total, 6),
            "currency": currency
        }


# 全局配置管理器实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """获取全局配置管理器"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    return _config_manager


def get_config() -> Dict[str, Any]:
    """快捷函数：获取当前配置"""
    return get_config_manager().get()


if __name__ == "__main__":
    manager = ConfigManager()
    config = manager.get()
    
    print("=" * 50)
    print("Dashboard Configuration")
    print("=" * 50)
    print(f"Dashboard名称: {config['dashboard_name']}")
    print(f"刷新间隔: {config['refresh_interval']}秒")
    print(f"Token成本: 输入{config['token_cost']['input_price_per_1m']}/1M, 输出{config['token_cost']['output_price_per_1m']}/1M")
    
    cost = manager.calculate_cost(1000000, 500000, 200000)
    print(f"\n测试成本计算:")
    print(f"  总成本: {cost['total_cost']} {cost['currency']}")
