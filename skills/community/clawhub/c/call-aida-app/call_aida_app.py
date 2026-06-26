#!/usr/bin/env python3

"""
OpenClaw 技能：调用 AI 搭（AIDA）chat-messages 接口

功能：
- 根据 appid 和 inputs 调用 AI 搭现有应用
- 返回应用返回的数据

参数传入方式（优先级）：
1. stdin JSON
2. 命令行参数 --appid, --inputs
3. 环境变量 AIDA_APPID, AIDA_INPUTS
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


AIDA_API_URL = "https://aida.vip.sankuai.com/v1/chat-messages"


def load_args():
    """从 stdin、命令行或环境变量加载参数"""

    # 1. 尝试从 stdin 读取 JSON（OpenClaw 通过 stdin 传入）
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
            if "appid" in data and "inputs" in data:
                query = data.get("query", "")
                return data["appid"], query, data["inputs"]
        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    # 2. 命令行参数
    parser = argparse.ArgumentParser(description="调用 AI 搭 chat-messages 接口")
    parser.add_argument("--appid", help="AI 搭 appid (Bearer Token)")
    parser.add_argument("--query", default="", help="用户 query，可选")
    parser.add_argument("--inputs", help="inputs JSON 字符串")
    parser.add_argument("--user", default="openclaw", help="用户标识")
    args = parser.parse_args()

    if args.appid and args.inputs:
        try:
            inputs = json.loads(args.inputs) if isinstance(args.inputs, str) else args.inputs
            return args.appid, args.query, inputs
        except json.JSONDecodeError:
            pass

    # 3. 环境变量
    appid = os.environ.get("AIDA_APPID")
    query = os.environ.get("AIDA_QUERY", "")
    inputs_str = os.environ.get("AIDA_INPUTS")

    if appid and inputs_str:
        try:
            inputs = json.loads(inputs_str)
            return appid, query, inputs
        except json.JSONDecodeError:
            pass

    return None, "", None


def call_aida_chat_messages(appid: str, query: str, inputs: dict, user: str = "openclaw") -> dict:
    """
    调用 AI 搭 chat-messages 接口

    Args:
        appid: AI 搭应用 ID（作为 Bearer Token）
        query: 用户 query（可选）
        inputs: 输入参数字典
        user: 用户标识

    Returns:
        返回结果字典，包含 success, message, data 等字段
    """

    body = {
        "inputs": inputs,
        "query": query,
        "response_mode": "blocking",
        "user": user,
    }

    req = urllib.request.Request(
        AIDA_API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {appid}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        # 检查是否有 answer 字段
        if "answer" not in data:
            return {
                "success": False,
                "message": "响应中未找到 answer 字段",
                "data": data,
            }

        answer = data["answer"]

        # 尝试解析 answer 为 JSON
        try:
            answer_obj = json.loads(answer)
            return {
                "success": True,
                "message": "调用成功",
                "data": answer_obj,
                "raw_answer": answer,
            }
        except json.JSONDecodeError:
            # answer 不是 JSON，作为字符串返回
            return {
                "success": True,
                "message": "调用成功",
                "data": {"answer": answer},
                "raw_answer": answer,
            }

    except urllib.error.HTTPError as e:
        body_content = ""
        try:
            body_content = e.read().decode("utf-8") if e.fp else ""
        except:
            pass

        return {
            "success": False,
            "message": f"HTTP 错误 {e.code}: {e.reason}",
            "data": {
                "status_code": e.code,
                "error_body": body_content,
            },
        }

    except urllib.error.URLError as e:
        return {
            "success": False,
            "message": f"网络错误: {str(e)}",
            "data": None,
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"错误: {str(e)}",
            "data": None,
        }


def main():
    appid, query, inputs = load_args()

    if not appid or inputs is None:
        print(json.dumps({
            "success": False,
            "message": "缺少必要参数。请通过以下方式之一传入：\n"
                      "1. stdin JSON: {\"appid\": \"...\", \"inputs\": {...}, \"query\": \"...\"}\n"
                      "2. 命令行: --appid <appid> --inputs '<json>'\n"
                      "3. 环境变量: AIDA_APPID, AIDA_INPUTS",
            "data": None,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    user = os.environ.get("AIDA_USER", "openclaw")

    result = call_aida_chat_messages(appid, query, inputs, user)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()

