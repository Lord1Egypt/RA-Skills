"""
Session Sync - 插件系统

插件开发指南：
1. 继承 Plugin 基类
2. 实现 on_sync 方法
3. 在 plugins/ 目录下创建插件文件
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Plugin(ABC):
    """插件基类"""
    
    name = "base"
    enabled = True
    
    @abstractmethod
    def on_sync(self, messages: List[Dict]) -> Dict[str, Any]:
        """
        同步后触发
        
        Args:
            messages: 新同步的消息列表
            
        Returns:
            处理结果，包含提取的信息
        """
        pass
    
    def on_shutdown(self):
        """关闭时触发"""
        pass


class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins: List[Plugin] = []
    
    def register(self, plugin: Plugin):
        """注册插件"""
        if plugin.enabled:
            self.plugins.append(plugin)
            print(f"[Plugin] 已加载: {plugin.name}")
    
    def process(self, messages: List[Dict]) -> Dict[str, Any]:
        """处理消息，触发所有插件"""
        results = {}
        for plugin in self.plugins:
            try:
                result = plugin.on_sync(messages)
                results[plugin.name] = result
            except Exception as e:
                print(f"[Plugin] {plugin.name} 处理失败: {e}")
        return results
