"""
基础渠道接口定义
所有推送渠道都必须实现这个接口
"""

from abc import ABC, abstractmethod


class BaseChannel(ABC):
    """推送渠道基类"""
    
    @abstractmethod
    def send(self, content: str, title: str = None) -> bool:
        """
        发送消息到渠道
        
        Args:
            content: 消息内容（Markdown格式）
            title: 消息标题（可选）
            
        Returns:
            发送成功返回 True，失败返回 False
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        获取渠道名称
        
        Returns:
            渠道名称字符串
        """
        pass
