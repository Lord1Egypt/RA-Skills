#!/usr/bin/env python3
"""
通用每日早报生成和推送主入口
支持任意领域，标准 web_search 接口，兼容性更强
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入配置
try:
    import config
except ImportError:
    print("[ERROR] 配置文件 config.py 不存在")
    print()
    print("请先运行初始化向导：")
    print("  python init_config.py")
    print()
    print("或者手动复制：")
    print("  cp config.example.py config.py")
    print("  然后编辑 config.py")
    sys.exit(1)

# 导入模块
from news_generator import NewsGenerator, NewsItem
from channels.base import BaseChannel


def create_channel(config) -> BaseChannel:
    """根据配置创建渠道实例"""
    channel_type = config.CHANNEL_TYPE
    
    if channel_type == "wecom":
        from channels.wecom import WeComChannel
        return WeComChannel(
            receiver_id=config.RECEIVER_ID,
            chat_type=getattr(config, 'WECOM_CHAT_TYPE', 1)
        )
    elif channel_type == "feishu":
        from channels.feishu import FeishuChannel
        return FeishuChannel(
            receiver_id=config.RECEIVER_ID,
            receive_id_type=getattr(config, 'FEISHU_RECEIVE_ID_TYPE', 'open_id')
        )
    elif channel_type == "webhook":
        from channels.webhook import WebhookChannel
        return WebhookChannel(
            webhook_url=config.WEBHOOK_URL,
            headers=getattr(config, 'WEBHOOK_HEADERS', None)
        )
    else:
        raise ValueError(f"不支持的渠道类型: {channel_type}")


def main():
    """主流程：生成 + 推送
    
    在 OpenClaw Agent 环境中运行时：
    1. Agent 通过标准 web_search 工具搜索指定领域过去24小时资讯
    2. Agent 整理分类，创建 NewsItem 对象
    3. 调用生成器生成完整早报
    4. 通过配置的渠道推送
    """
    print(f"[INFO] 开始生成 {config.NEWS_DOMAIN} 每日早报...")
    
    # 1. 创建推送渠道
    channel = create_channel(config)
    print(f"[INFO] 使用推送渠道: {channel.get_name()}")
    
    # 2. 生成早报内容
    # 在 OpenClaw Agent 环境中：
    # - AI 通过标准 web_search 工具获取搜索结果（兼容性更好，所有部署通用）
    # - AI 根据内容筛选分类，创建 NewsItem 对象
    # - AI 添加到 generator
    generator = NewsGenerator(config.__dict__)
    
    # 这里是框架入口，实际搜索和整理由 AI 完成
    # 因为搜索需要调用工具，必须由 AI 执行
    
    print("[INFO] 等待 AI 完成搜索和整理...")
    print("[INFO] 技能初始化完成，配置正确")
    print()
    print(f"领域: {config.NEWS_DOMAIN}")
    print(f"渠道: {channel.get_name()}")
    print(f"接收人: {config.RECEIVER_ID if hasattr(config, 'RECEIVER_ID') else config.WEBHOOK_URL}")
    print(f"定时: {config.SCHEDULE_CRON} (北京时间)")
    print()
    print("在 OpenClaw Agent 中，AI 将自动完成搜索生成推送流程")
    
    # 3. 生成最终内容（AI 完成填充后执行）
    content = generator.generate()
    
    # 4. 推送到渠道
    print("[INFO] 正在推送...")
    title = f"{config.DOMAIN_NAME}早报 | {generator.generate().splitlines()[0].split('|')[1].strip()}"
    success = channel.send(content, title)
    
    if success:
        print("[INFO] ✅ 推送成功！")
        return 0
    else:
        print("[ERROR] ❌ 推送失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
