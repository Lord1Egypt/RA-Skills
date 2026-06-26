"""
插件基类定义

单独文件避免循环导入问题
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Plugin(ABC):
    """插件基类 - 所有插件必须继承此类"""
    
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
