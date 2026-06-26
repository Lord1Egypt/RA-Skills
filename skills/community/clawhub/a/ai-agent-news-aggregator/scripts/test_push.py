#!/usr/bin/env python3
"""
test_push.py - 测试推送功能

发送一条测试消息到飞书，验证配置是否正确。

用法:
    python test_push.py [--config sources.json]
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def load_config(config_path):
    """加载配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_test_message():
    """格式化测试消息"""
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    message = f"""🤖 AI Agent 资讯聚合 - 测试消息

✅ 技能配置成功！

📋 测试内容
• 搜索关键词：8 个 AI Agent 相关关键词
• RSS 源：5 个技术博客
• 推送目标：飞书群聊

🛠️ 功能列表
• 🔍 DuckDuckGo 搜索
• 🧹 智能去重
• 📊 自动分类
• 📝 摘要生成
• 🚀 飞书推送

📅 下次运行
设置定时任务后，将按指定时间自动推送

---
测试时间：{date}
技能版本：1.0.0
"""
    return message

def main():
    config_path = Path(__file__).parent / "sources.json"
    
    # 加载配置
    config = load_config(config_path)
    channel_id = config.get("feishu", {}).get("channel_id", "")
    
    if not channel_id:
        print("❌ 错误：未配置 channel_id")
        return 1
    
    # 格式化消息
    message = format_test_message()
    
    # 输出（由 OpenClaw 捕获并发送）
    result = {
        "success": True,
        "channel_id": channel_id,
        "message": message,
        "test": True
    }
    
    # 使用 UTF-8 编码输出（避免 Windows 控制台编码问题）
    print(json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8').decode('utf-8'))
    return 0

if __name__ == "__main__":
    sys.exit(main())
