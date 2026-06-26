import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class SearchConfigLoader:
    """配置加载器"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # 默认配置文件路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, 'config.json')

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            # 返回默认配置
            return self._get_default_config()

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "web_session": {
                "value": None,
                "description": "小红书web_session cookie值(必需)"
            },
            "search": {
                "default_page": 1,
                "default_page_size": 20,
                "default_sort": "general",
                "default_note_type": 0,
                "post_time_filter": {
                    "enabled": False,
                    "hours": 24,
                    "description": "帖子发布时间过滤:只返回过去N小时内发布的帖子"
                }
            },
            "proxy": {
                "enabled": False,
                "url": None,
                "description": "代理设置"
            },
            "rate_limit": {
                "min_interval_seconds": 1,
                "max_retries": 5,
                "description": "请求频率限制"
            },
            "onboarding_complete": False,
            "description": "Onboarding是否已完成"
        }

    def get_web_session(self) -> Optional[str]:
        """获取web_session配置"""
        web_session_config = self.config.get('web_session', {})
        return web_session_config.get('value')

    def get_search_defaults(self) -> Dict[str, Any]:
        """获取搜索默认参数"""
        search_config = self.config.get('search', {})
        return {
            'page': search_config.get('default_page', 1),
            'page_size': search_config.get('default_page_size', 20),
            'sort': search_config.get('default_sort', 'general'),
            'note_type': search_config.get('default_note_type', 0)
        }

    def get_post_time_filter(self) -> Dict[str, Any]:
        """获取帖子发布时间过滤配置"""
        return self.config.get('search', {}).get('post_time_filter', {
            'enabled': False,
            'hours': 24
        })

    def get_proxy_config(self) -> Dict[str, Any]:
        """获取代理配置"""
        return self.config.get('proxy', {})

    def get_rate_limit(self) -> Dict[str, Any]:
        """获取频率限制配置"""
        return self.config.get('rate_limit', {})

    def reload_config(self):
        """重新加载配置"""
        self.config = self._load_config()

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """更新配置文件

        Args:
            updates: 配置更新字典，支持嵌套更新
                    例如: {'search': {'default_page_size': 20}}

        Returns:
            bool: 更新是否成功
        """
        try:
            # 递归更新配置
            def deep_update(original, updates_dict):
                for key, value in updates_dict.items():
                    if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                        deep_update(original[key], value)
                    else:
                        original[key] = value

            deep_update(self.config, updates)

            # 保存到文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"更新配置失败: {e}")
            return False

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """获取默认配置(静态方法)"""
        return {
            "web_session": {
                "value": None,
                "description": "小红书web_session cookie值(必需)"
            },
            "search": {
                "default_page": 1,
                "default_page_size": 20,
                "default_sort": "general",
                "default_note_type": 0,
                "post_time_filter": {
                    "enabled": False,
                    "hours": 24,
                    "description": "帖子发布时间过滤:只返回过去N小时内发布的帖子"
                }
            },
            "proxy": {
                "enabled": False,
                "url": None,
                "description": "代理设置"
            },
            "rate_limit": {
                "min_interval_seconds": 1,
                "max_retries": 5,
                "description": "请求频率限制"
            },
            "onboarding_complete": False,
            "description": "Onboarding是否已完成"
        }

# 单例模式
_config_loader = None

def get_search_config() -> SearchConfigLoader:
    """获取配置加载器单例"""
    global _config_loader
    if _config_loader is None:
        _config_loader = SearchConfigLoader()
    return _config_loader

def save_config(updates: Dict[str, Any]) -> bool:
    """保存配置更新(便捷函数)"""
    config_loader = get_search_config()
    return config_loader.update_config(updates)

def load_config() -> Dict[str, Any]:
    """加载当前配置(便捷函数)"""
    config_loader = get_search_config()
    return config_loader.config
