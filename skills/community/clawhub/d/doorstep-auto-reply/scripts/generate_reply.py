#!/usr/bin/env python3
"""
AI 自动回复生成器
根据平台、用户消息、语气生成合适的回复内容。
"""
import json
import argparse

def load_config():
    """加载关键词配置"""
    config_path = Path(__file__).parent.parent / "assets" / "keywords_config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"keywords": {}, "platforms": {}}

def generate_reply(platform, user_msg, tone="专业", include_cta=False):
    """
    基于平台和用户消息生成回复建议。
    实际使用时可由AI根据上下文动态生成更精准的回复。
    """
    # 此脚本提供回复结构和格式参考
    # AI agent 应当在此结构基础上生成实际内容
    
    reply = {
        "platform": platform,
        "user_message": user_msg,
        "tone": tone,
        "include_cta": include_cta,
        "suggested_reply": "[AI根据上下文自动生成]",
        "format_tips": {
            "抖音": "30字以内，口语化，带表情",
            "小红书": "温柔种草语气，可放长回复",
            "微信公众号": "专业准确，可带链接",
            "飞书": "结构化清晰，可带按钮"
        }.get(platform, ""),
        "cta_options": {
            "引导私信": "私信我帮您安排~",
            "引导关注": "先关注不迷路~",
            "引导预约": "点这里预约体验课",
            "引导转发": "收藏+转发给需要的朋友~"
        } if include_cta else {}
    }
    
    return reply

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="自动回复生成器")
    parser.add_argument("--platform", required=True, choices=["抖音", "小红书", "微信公众号", "飞书"])
    parser.add_argument("--user-msg", required=True, help="用户消息")
    parser.add_argument("--tone", default="专业", choices=["专业", "热情", "温柔", "官方", "幽默"])
    parser.add_argument("--include-cta", action="store_true", help="是否包含引导动作")
    
    args = parser.parse_args()
    result = generate_reply(args.platform, args.user_msg, args.tone, args.include_cta)
    print(json.dumps(result, ensure_ascii=False, indent=2))
