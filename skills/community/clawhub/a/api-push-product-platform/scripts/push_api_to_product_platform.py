#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送后端 API 接口定义到产品部数据平台

用法:
    py push_api_to_product_platform.py --prdid "PRD-2026-001" --file ./api-definitions.json
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import io
from pathlib import Path

# 设置 stdout 为 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 配置
API_URL = "http://test-gateway.jinyi999.cn/rjhy-test-compliance-utils-api/api/v1/aitest/backend/message"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Emoji 替代（用于 Windows 控制台）
EMOJI = {
    'file': '📄', 'rocket': '🚀', 'check': '✅', 'error': '❌', 'warn': '⚠️', 'disk': '💾'
}

def load_api_definitions(file_path: str) -> dict:
    """从文件加载接口定义"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def push_to_platform(prdid: str, content: dict, max_retries: int = 3) -> dict:
    """
    推送接口定义到产品部数据平台
    
    Args:
        prdid: 产品需求 ID
        content: 接口文档 JSON 数据
        max_retries: 最大重试次数
    
    Returns:
        推送结果
    """
    payload = {
        "prdid": prdid,
        "content": content
    }
    
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                API_URL,
                data=data,
                headers=HEADERS,
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return {
                    "success": True,
                    "status_code": response.status,
                    "result": result,
                    "attempt": attempt
                }
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            if attempt == max_retries:
                return {
                    "success": False,
                    "status_code": e.code,
                    "error": f"HTTP 错误 {e.code}: {error_body}",
                    "attempt": attempt
                }
            print(f"⚠️  第 {attempt} 次推送失败，{max_retries - attempt} 次重试机会...")
        
        except urllib.error.URLError as e:
            if attempt == max_retries:
                return {
                    "success": False,
                    "error": f"网络错误：{e.reason}",
                    "attempt": attempt
                }
            print(f"⚠️  第 {attempt} 次推送失败（网络问题），{max_retries - attempt} 次重试机会...")
        
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"响应解析失败：{e}",
                "attempt": attempt
            }
        
        except Exception as e:
            if attempt == max_retries:
                return {
                    "success": False,
                    "error": f"未知错误：{e}",
                    "attempt": attempt
                }
            print(f"⚠️  第 {attempt} 次推送失败，{max_retries - attempt} 次重试机会...")
    
    return {"success": False, "error": "未知错误", "attempt": max_retries}

def main():
    parser = argparse.ArgumentParser(
        description="推送后端 API 接口定义到产品部数据平台"
    )
    parser.add_argument(
        "--prdid",
        required=True,
        help="产品需求 ID (PRD ID)"
    )
    parser.add_argument(
        "--file",
        help="接口定义 JSON 文件路径"
    )
    parser.add_argument(
        "--content",
        help="接口定义 JSON 字符串（与 --file 互斥）"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细输出"
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.file and not args.content:
        print("❌ 错误：必须指定 --file 或 --content 参数")
        sys.exit(1)
    
    if args.file and args.content:
        print("❌ 错误：--file 和 --content 不能同时使用")
        sys.exit(1)
    
    # 加载接口定义
    try:
        if args.file:
            if args.verbose:
                print(f"{EMOJI['file']} 从文件加载接口定义：{args.file}")
            content = load_api_definitions(args.file)
        else:
            content = json.loads(args.content)
    except FileNotFoundError as e:
        print(f"{EMOJI['error']} {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{EMOJI['error']} JSON 格式错误：{e}")
        sys.exit(1)
    
    # 推送
    if args.verbose:
        print(f"\n{EMOJI['rocket']} 开始推送到产品部数据平台...")
        print(f"   PRD ID: {args.prdid}")
        print(f"   接口地址：{API_URL}")
    
    result = push_to_platform(args.prdid, content)
    
    # 输出结果
    if result["success"]:
        print(f"\n{EMOJI['check']} 推送成功！(尝试次数：{result['attempt']})")
        if args.verbose:
            print(f"   状态码：{result.get('status_code', 'N/A')}")
            print(f"   返回结果：{json.dumps(result.get('result', {}), ensure_ascii=False, indent=2)}")
        sys.exit(0)
    else:
        print(f"\n{EMOJI['error']} 推送失败：{result.get('error', '未知错误')} (尝试次数：{result['attempt']})")
        if args.verbose and 'status_code' in result:
            print(f"   状态码：{result['status_code']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
