#!/usr/bin/env python3
"""
发送飞书消息工具
"""
import sys
import json
import requests

def send_feishu_message(user_id: str, content: str) -> bool:
    """发送飞书消息给指定用户"""
    # 这里需要配置飞书机器人的webhook或者API调用
    # 暂时使用模拟实现，后续替换为实际API
    
    # 示例：使用飞书自定义机器人webhook
    # webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    # headers = {"Content-Type": "application/json"}
    # data = {
    #     "msg_type": "text",
    #     "content": {
    #         "text": content
    #     }
    # }
    # response = requests.post(webhook_url, headers=headers, json=data)
    # return response.status_code == 200
    
    print(f"发送飞书消息给 {user_id}: {content}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python send_feishu_message.py <user_id> <content>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    content = " ".join(sys.argv[2:])
    success = send_feishu_message(user_id, content)
    sys.exit(0 if success else 1)
