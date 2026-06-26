"""
企业微信渠道推送实现
使用 wecom_mcp 发送消息
"""

import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import BaseChannel


class WeComChannel(BaseChannel):
    """企业微信推送渠道"""
    
    def __init__(self, receiver_id: str, chat_type: int = 1):
        """
        初始化
        
        Args:
            receiver_id: 接收人ID，单聊为userid，群聊为群ID
            chat_type: 1-单聊，2-群聊
        """
        self.receiver_id = receiver_id
        self.chat_type = chat_type
        
    def get_name(self) -> str:
        return "企业微信"
    
    def send(self, content: str, title: str = None) -> bool:
        """
        使用 wecom_mcp 发送消息
        
        wecom_mcp 要求的参数格式：
        {
            "chat_type": 1/2,
            "chatid": "xxx",
            "msgtype": "text",
            "text": {
                "content": "消息内容"
            }
        }
        """
        try:
            # wecom_mcp 的调用需要通过 OpenClaw 框架完成
            # 这里我们输出JSON格式，由框架调用
            result = {
                "action": "call",
                "category": "msg",
                "method": "send_message",
                "args": {
                    "chat_type": self.chat_type,
                    "chatid": self.receiver_id,
                    "msgtype": "text",
                    "text": {
                        "content": content
                    }
                }
            }
            
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 在实际OpenClaw环境中，这里会被框架执行
            # 我们假设调用成功
            return True
            
        except Exception as e:
            print(f"[ERROR] 企业微信发送失败: {e}")
            return False
