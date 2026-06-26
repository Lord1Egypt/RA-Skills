#!/usr/bin/env python3
import json
import requests
from openclaw.tools.feishu_im_user_message import feishu_im_user_message

def main():
    # 拉取数据
    response = requests.get("https://60s.viki.moe/v2/60s")
    response.raise_for_status()
    data = response.json()["data"]
    
    # 格式化新闻
    news = "\n".join([f"{i+1}. {item}" for i, item in enumerate(data["news"])])
    
    # 组装消息
    content = f"""## ☀️ 今日早报 | {data['date']} {data['day_of_week']}

### 📰 60秒读懂世界
{news}

### 💡 每日箴言
{data['tip']}"""
    
    # 发送消息
    result = feishu_im_user_message(
        action='send',
        receive_id_type='open_id',
        receive_id='ou_b8bd6c6f4b69a9dda0dd16c2788c32ca',
        msg_type='text',
        content=json.dumps({"text": content})
    )
    
    print(f"消息发送成功，message_id: {result['message_id']}")

if __name__ == "__main__":
    main()
