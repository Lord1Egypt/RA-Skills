"""
监听器模块 - Specialist Agent 监听并处理任务
"""

import os
import sys
import time
import json
import threading
from typing import Optional, Dict, Any

# 添加 src 目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.routing import TeamRouter


class BaseListener:
    """监听器基类"""
    
    def __init__(self, agent_name: str, config_path: Optional[str] = None):
        self.agent_name = agent_name
        self.router = TeamRouter(config_path)
        self.running = False
        
    def get_mq_messages(self, agent: str, timeout: int = 5) -> list:
        """
        从 MQ 获取消息
        
        Args:
            agent: 目标 agent 名称
            timeout: 超时时间（秒）
            
        Returns:
            消息列表
        """
        # TODO: 实现真实的 MQ 读取
        # 目前是占位符，需要接入实际的 MQ 系统
        return []
    
    def process_message(self, message: Dict[str, Any]) -> str:
        """
        处理单条消息
        
        Args:
            message: 消息内容
            
        Returns:
            处理结果
        """
        task = message.get('task', '')
        return f"[{self.agent_name}] 处理任务: {task}"
    
    def send_to_group(self, message: str, chat_id: str) -> bool:
        """
        发送消息到群里
        
        Args:
            message: 消息内容
            chat_id: 群 ID
            
        Returns:
            是否发送成功
        """
        # TODO: 实现真实的 Feishu API 调用
        print(f"[{self.agent_name}] 发送到群 {chat_id}: {message[:50]}...")
        return True
    
    def start(self):
        """启动监听"""
        self.running = True
        print(f"[{self.agent_name}] 监听器已启动")
        
        while self.running:
            messages = self.get_mq_messages(self.agent_name)
            for msg in messages:
                result = self.process_message(msg)
                # 发送到群里
                chat_id = msg.get('chat_id')
                if chat_id:
                    self.send_to_group(result, chat_id)
            
            time.sleep(1)
    
    def stop(self):
        """停止监听"""
        self.running = False
        print(f"[{self.agent_name}] 监听器已停止")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Agent 监听器')
    parser.add_argument('--agent', required=True, help='Agent 名称')
    parser.add_argument('--config', help='配置文件路径')
    
    args = parser.parse_args()
    
    listener = BaseListener(args.agent, args.config)
    
    try:
        listener.start()
    except KeyboardInterrupt:
        listener.stop()


if __name__ == "__main__":
    main()
