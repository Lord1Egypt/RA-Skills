#!/usr/bin/env python3
"""
Dify Chat CLI - Dify 工作流对话机器人

调用本地知识库查询工作流，支持多轮对话和流式响应输出。

Usage:
    dify-chat -q "问题内容"
    dify-chat -q "问题" -c conv_xxx
    dify-chat --show-config

Requirements:
    requests library (pip install requests)
"""

import argparse
import os
import sys
import json
import requests


def load_env():
    """加载环境变量配置文件"""
    env_file = os.path.expanduser("~/.openclaw/config/dify.env")
    
    if not os.path.exists(env_file):
        print(f"\033[0;31m❌ Error: Environment file not found: {env_file}\033[0m", file=sys.stderr)
        sys.exit(1)
    
    # 读取环境变量
    env_vars = {}
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars


def check_required_vars(env_vars):
    """检查必需的环境变量"""
    required = ['DIFY_API_KEY']
    missing = [var for var in required if not env_vars.get(var)]
    
    if missing:
        print(f"\033[0;31m❌ Error: Missing required environment variables: {', '.join(missing)}\033[0m", file=sys.stderr)
        sys.exit(1)


def show_config(env_vars):
    """显示当前配置"""
    print("\033[0;34m📋 Current Configuration:\033[0m")
    print(f"   API Base: \033[0;32m{env_vars.get('DIFY_API_BASE', 'not set')}\033[0m")
    print(f"   User: \033[0;32m{env_vars.get('DIFY_USER', 'openclaw-user')}\033[0m")
    
    if env_vars.get('DIFY_API_BASE'):
        print("\033[0;32m✅ Status: Connected\033[0m")
    else:
        print("\033[0;31m❌ Status: Incomplete config\033[0m")


def call_dify_api(query, conv_id, env_vars):
    """调用 Dify API，支持流式响应"""
    url = f"{env_vars['DIFY_API_BASE']}/chat-messages"
    headers = {
        "Authorization": f"Bearer {env_vars['DIFY_API_KEY']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {},
        "query": query,  # ✅ 添加 query 字段
        "response_mode": "blocking",  # ✅ 改为 streaming
        "conversation_id": "",
        "user": env_vars.get("DIFY_USER", "openclaw-user")  # ✅ 添加 user 字段
    }
    
    print("\033[0;34m🔄 Calling Dify API...\033[0m")
    
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()
        
        conversation_id = None
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                
                # Parse SSE data format: "data: {...}"
                if decoded_line.startswith("data: "):
                    try:
                        json_data = json.loads(decoded_line[6:])
                        
                        # Extract conversation_id
                        if conversation_id is None and json_data.get("conversation_id"):
                            conversation_id = json_data["conversation_id"]
                            print(f"\033[1;33m💬 Conversation ID: {conversation_id}\033[0m", file=sys.stderr)
                        
                        # Extract answer text
                        if "answer" in json_data and json_data["answer"]:
                            print(json_data["answer"], end="", flush=True)
                        
                        # Check if completed (status 2 = completed)
                        if json_data.get("status") == 2:
                            break
                    except json.JSONDecodeError:
                        pass
        
        print()  # Newline after output
        
        return conversation_id
        
    except requests.exceptions.ConnectionError:
        print(f"\033[0;31m❌ Error: Cannot connect to {env_vars.get('DIFY_API_BASE', 'unknown')}\033[0m", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"\033[0;31m❌ API Error: {e}\033[0m", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Dify Chat - 工作流对话机器人",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dify-chat -q "什么是公司报销政策？"
  dify-chat -q "年假怎么算？" -c conv_xxx
  dify-chat --show-config
"""
    )
    
    parser.add_argument(
        "-q", "--query",
        type=str,
        help="要查询的问题（必填）"
    )
    
    parser.add_argument(
        "-c", "--conv-id",
        type=str,
        help="会话 ID，用于多轮对话"
    )
    
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="显示当前配置"
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    env_vars = load_env()
    check_required_vars(env_vars)
    
    # Handle --show-config
    if args.show_config:
        show_config(env_vars)
        return
    
    # Validate required query parameter
    if not args.query:
        print("\033[0;31m❌ Error: Query parameter (-q) is required\033[0m", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Call Dify API
    print("\n\033[0;34m🤖 Dify Chat Bot:\033[0m")
    print(f"\033[1;33m📝 Your query:\033[0m {args.query}")
    print("-" * 50)
    
    conv_id = call_dify_api(args.query, args.conv_id, env_vars)
    
    if conv_id and not args.conv_id:
        print(f"\n\033[1;33m💬 Conversation ID: {conv_id}\033[0m")


if __name__ == "__main__":
    main()
