#!/usr/bin/env python3
"""
交互式初始化配置向导
首次安装运行这个脚本，自动生成 config.py
"""

import os
import sys


def prompt(question: str, default: str = None) -> str:
    """交互式提问，支持默认值"""
    if default:
        prompt_text = f"{question} [{default}]: "
    else:
        prompt_text = f"{question}: "
    
    try:
        answer = input(prompt_text).strip()
    except KeyboardInterrupt:
        print("\n\n取消初始化")
        sys.exit(1)
    
    if not answer and default:
        return default
    return answer


def main():
    """主交互流程"""
    print("=" * 60)
    print("  📰 通用每日早报推送 - 配置初始化向导")
    print("=" * 60)
    print()
    print("请回答以下几个问题，帮你完成配置：")
    print()
    
    # 1. 询问关注领域
    print("【1/5】 设置关注领域")
    domain = prompt("你想获取哪个领域的每日早报？（例如：AI人工智能、区块链、生物医药）", "AI人工智能")
    domain_name = prompt("领域简称（用于标题显示）", domain.split("，")[0].split(" ")[0])
    
    # 2. 询问推送渠道
    print()
    print("【2/5】 选择推送渠道")
    print("可选：1) 企业微信  2) 飞书  3) Webhook")
    channel_choice = prompt("请选择", "1")
    
    channel_map = {
        "1": "wecom",
        "2": "feishu",
        "3": "webhook"
    }
    channel_type = channel_map.get(channel_choice, "wecom")
    
    # 3. 询问接收人
    print()
    print("【3/5】 设置接收人")
    if channel_type == "wecom":
        print("企业微信：单聊填 userid，群聊填群ID")
        receiver_id = prompt("接收人ID")
        wecom_chat_type = prompt("1-单聊，2-群聊", "1")
    elif channel_type == "feishu":
        print("飞书：单聊填 open_id (格式: ou_xxx)，群聊填 chat_id (格式: oc_xxx)")
        receiver_id = prompt("接收人ID")
        feishu_type = prompt("单聊还是群聊？(1-单聊 2-群聊)", "1")
        if feishu_type == "2":
            feishu_receive_type = "chat_id"
        else:
            feishu_receive_type = "open_id"
    else:  # webhook
        print("Webhook：填写推送 URL")
        webhook_url = prompt("Webhook URL")
        print("自定义请求头（可选，JSON格式）")
        webhook_headers = prompt("请求头", '{"Content-Type": "application/json"}')
    
    # 4. 询问推送时间
    print()
    print("【4/5】 设置推送时间（cron 格式，北京时间）")
    print("示例：")
    print("  每日8:30  →  30 8 * * *")
    print("  每日9:00  →  0 9 * * *")
    schedule = prompt("cron 表达式", "30 8 * * *")
    
    # 5. 信息源优先级
    print()
    print("【5/6】 信息源优先级")
    print("AI会自动根据你关注的领域，分析判断该领域有哪些优质核心信息源，无需手动配置")
    print("如果你有特别想要优先的信息源，可以在这里输入（逗号分隔），留空则让AI自动判断")
    sources_input = prompt("自定义优先信息源（留空=AI自动判断）", "")
    if sources_input:
        source_priority = [s.strip() for s in sources_input.split(",")]
    else:
        source_priority = []  # 空列表表示让AI自动判断
    
    # 6. 确认分类名称
    print()
    print("【6/6】 分类名称（保持默认即可）")
    print("默认分类：头条 / 国际动态 / 国内动态 / 深度/学术 / 今日观察")
    use_custom = prompt("需要自定义分类名称吗？(y/N)", "n")
    
    if use_custom.lower() == "y":
        cat_headline = prompt("头条分类名", "头条")
        cat_intl = prompt("国际分类名", "国际动态")
        cat_dom = prompt("国内分类名", "国内动态")
        cat_aca = prompt("深度分类名", "深度/学术")
        cat_obs = prompt("观察分类名", "今日观察")
    else:
        cat_headline = "头条"
        cat_intl = "国际动态"
        cat_dom = "国内动态"
        cat_aca = "深度/学术"
        cat_obs = "今日观察"
    
    # 生成配置内容
    print()
    print("正在生成配置...")
    
    config_content = f'''"""
自动生成的配置文件
由 init_config.py 在 {os.path.basename(__file__)} 生成
"""

# ========== 核心配置 ==========

# 关注的领域
NEWS_DOMAIN = "{domain}"

# 领域名称（用于标题显示）
DOMAIN_NAME = "{domain_name}"

# 推送渠道类型
# 可选值: wecom (企业微信), feishu (飞书), webhook (通用Webhook)
CHANNEL_TYPE = "{channel_type}"

# 接收人ID
# - wecom: 单聊时为 userid，群聊时为群ID
# - feishu: 单聊时为 open_id (ou_xxx)，群聊时为 chat_id (oc_xxx)
# - webhook: 不需要此项，看下方 WEBHOOK_* 配置
RECEIVER_ID = "{receiver_id if 'receiver_id' in locals() else ''}"

# ========== 分类名称配置 ==========
CATEGORY_NAMES = {{
    "headline": "{cat_headline}",
    "international": "{cat_intl}",
    "domestic": "{cat_dom}",
    "academic": "{cat_aca}",
    "observation": "{cat_obs}"
}}

# ========== 信息源优先级配置 ==========
# 根据不同领域，优先推荐优质信息源
# AI会优先从这些来源抓取信息
SOURCE_PRIORITY = {source_priority}

# 是否优先保留指定来源的信息
PREFER_PRIORITY_SOURCES = True

'''

    # 添加渠道特定配置
    if channel_type == "wecom":
        config_content += f'''# ========== 企业微信额外配置 ==========
# 会话类型: 1-单聊，2-群聊
WECOM_CHAT_TYPE = {wecom_chat_type}

'''
    elif channel_type == "feishu":
        config_content += f'''# ========== 飞书额外配置 ==========
# 接收人ID类型: open_id (单聊), chat_id (群聊)
FEISHU_RECEIVE_ID_TYPE = "{feishu_receive_type}"

'''
    elif channel_type == "webhook":
        config_content += f'''# ========== Webhook 额外配置 ==========
WEBHOOK_URL = "{webhook_url}"
WEBHOOK_HEADERS = {webhook_headers}

'''

    # 添加通用配置
    config_content += '''# ========== 内容配置 ==========

# 每条分类最大条数
MAX_NEWS_PER_CATEGORY = {
    "international": 3,  # 国际动态
    "domestic": 3,       # 国内动态
    "academic": 2        # 深度/学术
}

# 是否每条都必须有来源链接
REQUIRE_SOURCE_LINK = True

# ========== 定时任务配置（cron格式，北京时间）==========
# 北京时间每日8:30: 30 8 * * *
SCHEDULE_CRON = "%s"
''' % schedule

    # 写入文件
    output_path = os.path.join(os.path.dirname(__file__), "config.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print()
    print("✅ 配置生成完成！")
    print(f"📄 配置文件: {output_path}")
    print()
    print("可以直接运行测试：")
    print("  python generate_and_send.py")
    print()
    print("然后添加到 crontab 实现每日自动推送：")
    print(f"  {schedule}  cd {os.path.dirname(os.path.abspath(output_path))} && python generate_and_send.py")
    print()


if __name__ == "__main__":
    main()
