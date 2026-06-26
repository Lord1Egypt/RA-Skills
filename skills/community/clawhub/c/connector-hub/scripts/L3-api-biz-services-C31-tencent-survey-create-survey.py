#!/usr/bin/env python3
"""创建腾讯问卷"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://wj.qq.com/api/v2"

def get_headers() -> dict:
    """获取请求头"""
    # 简化实现，实际需要 OAuth2 授权
    access_token = os.environ.get("TENCENT_SURVEY_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 TENCENT_SURVEY_ACCESS_TOKEN 环境变量")
    
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

def create_survey(title: str, questions: list, description: str = "") -> dict:
    """创建问卷
    
    Args:
        title: 问卷标题
        questions: 问题列表
        description: 问卷描述
    
    Returns:
        API 响应
    """
    headers = get_headers()
    
    payload = {
        "title": title,
        "description": description or f"问卷：{title}",
        "questions": questions
    }
    
    resp = requests.post(f"{API_BASE}/surveys", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def create_feedback_survey(title: str) -> dict:
    """创建反馈问卷"""
    questions = [
        {
            "type": "radio",
            "title": "您对我们的服务满意吗？",
            "options": ["非常满意", "满意", "一般", "不满意", "非常不满意"],
            "required": True
        },
        {
            "type": "checkbox",
            "title": "您认为我们需要改进哪些方面？",
            "options": ["产品质量", "服务态度", "响应速度", "价格", "其他"],
            "required": False
        },
        {
            "type": "text",
            "title": "您有什么建议？",
            "required": False
        }
    ]
    
    return create_survey(title, questions)

def create_satisfaction_survey(title: str) -> dict:
    """创建满意度调查"""
    questions = [
        {
            "type": "nps",
            "title": "您向朋友推荐我们的可能性有多大？",
            "min": 0,
            "max": 10,
            "required": True
        },
        {
            "type": "radio",
            "title": "您使用我们的产品多久了？",
            "options": ["不到1个月", "1-6个月", "6-12个月", "1年以上"],
            "required": True
        },
        {
            "type": "matrix",
            "title": "请评价以下方面",
            "rows": ["产品质量", "客户服务", "价格合理性", "易用性"],
            "columns": ["非常满意", "满意", "一般", "不满意", "非常不满意"],
            "required": True
        }
    ]
    
    return create_survey(title, questions)

def main():
    parser = argparse.ArgumentParser(description="创建腾讯问卷")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 反馈问卷
    feedback_parser = subparsers.add_parser("feedback", help="反馈问卷")
    feedback_parser.add_argument("title", help="问卷标题")
    
    # 满意度调查
    satisfaction_parser = subparsers.add_parser("satisfaction", help="满意度调查")
    satisfaction_parser.add_argument("title", help="问卷标题")
    
    # 自定义问卷
    custom_parser = subparsers.add_parser("custom", help="自定义问卷")
    custom_parser.add_argument("title", help="问卷标题")
    custom_parser.add_argument("--questions", required=True, help="问题列表（JSON 格式）")
    custom_parser.add_argument("--desc", help="问卷描述")
    
    args = parser.parse_args()
    
    try:
        if args.command == "feedback":
            data = create_feedback_survey(args.title)
        elif args.command == "satisfaction":
            data = create_satisfaction_survey(args.title)
        elif args.command == "custom":
            questions = json.loads(args.questions)
            data = create_survey(args.title, questions, args.desc)
        else:
            parser.print_help()
            return
        
        if data.get("ret") == 0:
            print(f"问卷创建成功：")
            print(f"  标题：{data.get('title')}")
            print(f"  链接：{data.get('url')}")
            print(f"  ID：{data.get('survey_id')}")
        else:
            print(f"创建失败：{data.get('msg')}")
            sys.exit(1)
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
