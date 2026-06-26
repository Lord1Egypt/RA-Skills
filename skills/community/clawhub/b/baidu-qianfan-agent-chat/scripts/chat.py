#!/usr/bin/env python3
"""
千帆对话API调用脚本

用于调用百度千帆平台的对话API进行AI对话交互。
支持流式和非流式响应、多轮对话、文件上传、Function Call等功能。
会话状态自动管理：首次调用不传conversation_id，后续自动从返回中获取。
"""

import argparse
import json
import os
import sys
import requests
from typing import Optional, List, Dict, Any
from pathlib import Path


# 默认配置
DEFAULT_APP_ID = "e52a2419-4327-48e8-b9dc-9bf037199fc2"
API_URL = "https://qianfan.baidubce.com/v2/app/conversation/runs"

# 会话状态文件路径
SESSION_STATE_FILE = Path(__file__).parent.parent / "state" / "session.json"


def load_session_state() -> Dict[str, Any]:
    """加载会话状态"""
    if SESSION_STATE_FILE.exists():
        try:
            with open(SESSION_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_session_state(state: Dict[str, Any]) -> None:
    """保存会话状态"""
    SESSION_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_api_key() -> str:
    """从环境变量获取API Key"""
    api_key = os.environ.get("QIANFAN_API_KEY")
    if not api_key:
        print("错误: 未设置 QIANFAN_API_KEY 环境变量", file=sys.stderr)
        print("请运行: export QIANFAN_API_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)
    return api_key


def chat(
    query: str,
    app_id: str = DEFAULT_APP_ID,
    stream: bool = True,
    conversation_id: Optional[str] = None,
    file_ids: Optional[List[str]] = None,
    tools: Optional[List[Dict]] = None,
    tool_choice: Optional[Dict] = None,
    tool_outputs: Optional[List[Dict]] = None,
    action: Optional[Dict] = None,
    end_user_id: Optional[str] = None,
    metadata_filter: Optional[Dict] = None,
    custom_metadata: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    调用千帆对话API
    
    Args:
        query: 用户提问内容（必选）
        app_id: 应用ID
        stream: 是否流式返回
        conversation_id: 会话ID（多轮对话时传入）
        file_ids: 文件ID列表
        tools: 工具定义列表
        tool_choice: 强制执行的工具选择
        tool_outputs: 工具调用结果
        action: 动作配置
        end_user_id: 终端用户ID
        metadata_filter: 元数据过滤条件
        custom_metadata: 自定义元数据
    
    Returns:
        API响应结果
    """
    api_key = get_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    body: Dict[str, Any] = {
        "app_id": app_id,
        "query": query,
        "stream": stream,
    }
    
    # 可选参数
    if conversation_id:
        body["conversation_id"] = conversation_id
    if file_ids:
        body["file_ids"] = file_ids
    if tools:
        body["tools"] = tools
    if tool_choice:
        body["tool_choice"] = tool_choice
    if tool_outputs:
        body["tool_outputs"] = tool_outputs
    if action:
        body["action"] = action
    if end_user_id:
        body["end_user_id"] = end_user_id
    if metadata_filter:
        body["metadata_filter"] = metadata_filter
    if custom_metadata:
        body["custom_metadata"] = custom_metadata
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=body,
            stream=stream,
            timeout=60,
        )
        
        if response.status_code != 200:
            print(f"API错误 [{response.status_code}]: {response.text}", file=sys.stderr)
            sys.exit(1)
        
        if stream:
            # 流式响应处理
            full_answer = ""
            result = {}
            
            for line in response.iter_lines():
                if not line:
                    continue
                
                line_text = line.decode("utf-8")
                if line_text.startswith("data: "):
                    data = line_text[6:]  # 去掉 "data: " 前缀
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        answer_part = chunk.get("answer", "")
                        full_answer += answer_part
                        result = chunk
                        # 保存conversation_id（如果存在）
                        if "conversation_id" in chunk:
                            result["conversation_id"] = chunk["conversation_id"]
                        # 实时输出
                        print(answer_part, end="", flush=True)
                    except json.JSONDecodeError:
                        continue
            
            print()  # 换行
            result["full_answer"] = full_answer
            return result
        else:
            # 非流式响应
            return response.json()
            
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def parse_json_arg(value: str) -> Dict:
    """解析JSON参数"""
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="千帆对话API调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本对话（自动使用/保存会话状态）
  python3 chat.py --query "你好"
  
  # 开始新会话
  python3 chat.py --query "你好" --new-session
  
  # 手动指定会话ID
  python3 chat.py --query "继续" --conversation-id "xxx-xxx-xxx"
  
  # 非流式响应
  python3 chat.py --query "你好" --stream false
  
  # 使用工具定义
  python3 chat.py --query "今天北京天气" --tools-file tools/weather.json
  
  # 强制执行工具
  python3 chat.py --query "查询航班" --tool-choice '{"type":"function","function":{"name":"QueryFlights","input":{"flight_number":"CZ8889"}}}'
  
  # 上报工具调用结果
  python3 chat.py --tool-outputs '[{"tool_call_id":"xxx","output":"北京今天天气晴朗，温度32度"}]' --conversation-id "xxx"
        """,
    )
    
    # 必选参数
    parser.add_argument(
        "--query",
        help="用户提问内容（必选，除非使用tool_outputs）",
    )
    
    # 基本参数
    parser.add_argument(
        "--app-id",
        default=DEFAULT_APP_ID,
        help=f"应用ID (默认: {DEFAULT_APP_ID})",
    )
    parser.add_argument(
        "--stream",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help="是否流式返回 (默认: true)",
    )
    parser.add_argument(
        "--conversation-id",
        help="会话ID，用于多轮对话（不指定则自动从状态文件读取）",
    )
    parser.add_argument(
        "--new-session",
        action="store_true",
        help="开始新会话（忽略已保存的会话状态）",
    )
    parser.add_argument(
        "--end-user-id",
        help="终端用户ID",
    )
    
    # 文件参数
    parser.add_argument(
        "--file-ids",
        help="文件ID列表，逗号分隔",
    )
    
    # 工具参数
    parser.add_argument(
        "--tools-file",
        help="工具定义JSON文件路径",
    )
    parser.add_argument(
        "--tools",
        help="工具定义JSON字符串",
    )
    parser.add_argument(
        "--tool-choice",
        help="强制执行的工具选择，JSON字符串",
    )
    parser.add_argument(
        "--tool-outputs",
        help="工具调用结果，JSON字符串数组",
    )
    
    # 动作参数
    parser.add_argument(
        "--action",
        help="动作配置，JSON字符串，用于回复信息收集节点",
    )
    
    # 元数据参数
    parser.add_argument(
        "--metadata-filter",
        help="元数据过滤条件，JSON字符串",
    )
    parser.add_argument(
        "--custom-metadata",
        help="自定义元数据，JSON字符串",
    )
    
    # 输出参数
    parser.add_argument(
        "--json",
        action="store_true",
        help="以JSON格式输出完整响应",
    )
    
    args = parser.parse_args()
    
    # 解析文件ID
    file_ids = None
    if args.file_ids:
        file_ids = [fid.strip() for fid in args.file_ids.split(",") if fid.strip()]
    
    # 解析工具定义
    tools = None
    if args.tools_file:
        try:
            with open(args.tools_file, "r", encoding="utf-8") as f:
                tools = json.load(f)
        except Exception as e:
            print(f"读取工具定义文件失败: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.tools:
        tools = parse_json_arg(args.tools)
    
    # 解析其他JSON参数
    tool_choice = parse_json_arg(args.tool_choice) if args.tool_choice else None
    tool_outputs = parse_json_arg(args.tool_outputs) if args.tool_outputs else None
    action = parse_json_arg(args.action) if args.action else None
    metadata_filter = parse_json_arg(args.metadata_filter) if args.metadata_filter else None
    custom_metadata = parse_json_arg(args.custom_metadata) if args.custom_metadata else None
    
    # 检查必选参数
    if not args.query and not tool_outputs:
        parser.error("必须提供 --query 或 --tool-outputs")
    
    # 处理会话ID
    conversation_id = args.conversation_id
    if not conversation_id and not args.new_session:
        # 从状态文件读取会话ID
        state = load_session_state()
        conversation_id = state.get("conversation_id")
        if conversation_id:
            print(f"[使用已保存的会话: {conversation_id}]", file=sys.stderr)
    
    # 调用API
    result = chat(
        query=args.query or "",
        app_id=args.app_id,
        stream=args.stream,
        conversation_id=conversation_id,
        file_ids=file_ids,
        tools=tools,
        tool_choice=tool_choice,
        tool_outputs=tool_outputs,
        action=action,
        end_user_id=args.end_user_id,
        metadata_filter=metadata_filter,
        custom_metadata=custom_metadata,
    )
    
    # 保存会话ID
    if "conversation_id" in result:
        save_session_state({"conversation_id": result["conversation_id"]})
    
    # 输出结果
    if args.json or not args.stream:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 流式模式已经在过程中输出了答案
        if "conversation_id" in result:
            print(f"\n[conversation_id: {result['conversation_id']}]")


if __name__ == "__main__":
    main()
