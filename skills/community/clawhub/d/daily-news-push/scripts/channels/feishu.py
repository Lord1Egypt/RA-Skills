"""
飞书渠道推送实现
使用 feishu_im_user_message 发送消息
"""

import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import BaseChannel


class FeishuChannel(BaseChannel):
    """飞书推送渠道"""
    
    def __init__(self, receiver_id: str, receive_id_type: str = "open_id"):
        """
        初始化
        
        Args:
            receiver_id: 接收人ID
            receive_id_type: open_id (单聊) 或 chat_id (群聊)
        """
        self.receiver_id = receiver_id
        self.receive_id_type = receive_id_type
        
    def get_name(self) -> str:
        return "飞书"
    
    def send(self, content: str, title: str = None) -> bool:
        """
        使用 feishu_im_user_message 发送消息
        
        飞书要求 content 是JSON字符串
        """
        try:
            # 飞书消息格式：text 类型内容是 JSON 字符串
            content_json = json.dumps({"text": content}, ensure_ascii=False)
            
            result = {
                "action": "send",
                "receive_id_type": self.receive_id_type,
                "receive_id": self.receiver_id,
                "msg_type": "text",
                "content": content_json
            }
            
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 在实际OpenClaw环境中，这里会被框架调用
            return True
            
        except Exception as e:
            print(f"[ERROR] 飞书发送失败: {e}")
            return False
