#!/usr/bin/env python3
"""
cc-session-bridge.py — 调用 CC 并实时将会话转为 OpenClaw 格式，供 AIMA 采集

流程:
  1. 根据 task_id 查找本地会话文件（task_id → session_id 映射）
  2. 有会话 → APPEND：追加消息到已有 jsonl
  3. 无会话 → NEW：新建会话 + 写入 header + 绑定 AIMA 任务
  4. 流式读取 CC 输出，每收到一条事件就立即 append 到 jsonl

会话查找逻辑:
  映射文件: ~/.openclaw/agents/<agent>/sessions/task-session-map.json
  格式: {"<task_id>": "<session_id>"}
  同一 task_id 始终写入同一个会话文件，不依赖 AIMA 绑定查询

用法:
  python3 cc-session-bridge.py --agent-name xiaoling-qinfang --task-id 8700205 --query "分析项目结构"

配置文件:
  ~/.openclaw/scripts/cc-bridge-config.yaml
  按 agent_name 配置 chat_id / sender_id / sender_name，脚本自动读取

参数:
  --agent-name    OpenClaw agent 目录名 (如 xiaoling-qinfang)
  --task-id       AIMA 任务 ID，用于查找/创建本地会话
  --query         传给 CC 的请求内容
  --model         CC 模型 (默认 sonnet)
  --chat-id       钉钉 chat_id (覆盖配置文件)
  --sender-id     钉钉 sender_id (覆盖配置文件)
  --sender-name   钉钉 sender 姓名 (覆盖配置文件)
"""

import argparse
import json
import os
import subprocess
import sys
import threading
import uuid
from datetime import datetime, timezone

# ============================================================
# 配置文件
# ============================================================

CONFIG_PATH = os.path.expanduser("~/.openclaw/scripts/cc-bridge-config.yaml")


def load_config(agent_name: str) -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        import yaml
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f) or {}
        return config.get(agent_name, {})
    except ImportError:
        return _parse_yaml_simple(CONFIG_PATH, agent_name)


def _parse_yaml_simple(path: str, agent_name: str) -> dict:
    result = {}
    current_agent = None
    with open(path, 'r') as f:
        for line in f:
            stripped = line.rstrip()
            if not stripped or stripped.lstrip().startswith('#'):
                continue
            if not line.startswith(' ') and not line.startswith('\t'):
                if ':' in stripped:
                    key = stripped.split(':')[0].strip()
                    if not key.startswith('#'):
                        current_agent = key
                        result[current_agent] = {}
            elif current_agent and ':' in stripped:
                parts = stripped.strip().split(':', 1)
                k = parts[0].strip()
                v = parts[1].strip().strip('"').strip("'")
                if k and not k.startswith('#'):
                    result[current_agent][k] = v
    return result.get(agent_name, {})


# ============================================================
# JSONL 写入工具
# ============================================================

class SessionWriter:
    def __init__(self, jsonl_path: str):
        self.jsonl_path = jsonl_path
        self._last_id = None
        self._lock = threading.Lock()

    @property
    def last_id(self):
        return self._last_id

    def write(self, record: dict):
        with self._lock:
            with open(self.jsonl_path, 'a') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
            if "id" in record:
                self._last_id = record["id"]

    def write_many(self, records: list):
        with self._lock:
            with open(self.jsonl_path, 'a') as f:
                for record in records:
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
                    if "id" in record:
                        self._last_id = record["id"]

    def load_last_id(self):
        last_id = None
        if not os.path.exists(self.jsonl_path):
            return last_id
        with open(self.jsonl_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if "id" in obj:
                        last_id = obj["id"]
                except json.JSONDecodeError:
                    pass
        self._last_id = last_id
        return last_id


# ============================================================
# OpenClaw 记录构建
# ============================================================

def build_runtime_context(chat_id: str, sender_id: str, sender_name: str, ts_str: str) -> str:
    return (
        f"Conversation info (untrusted metadata):\n"
        f"```json\n"
        f'{{\n'
        f'  "chat_id": "{chat_id}",\n'
        f'  "message_id": "msg{uuid.uuid4().hex[:16]}==",\n'
        f'  "sender_id": "{sender_id}",\n'
        f'  "sender": "{sender_name}",\n'
        f'  "timestamp": "{ts_str}"\n'
        f'}}\n'
        f"```\n"
        f'\n'
        f"Sender (untrusted metadata):\n"
        f"```json\n"
        f'{{\n'
        f'  "label": "{sender_name} ({sender_id})",\n'
        f'  "id": "{sender_id}",\n'
        f'  "name": "{sender_name}"\n'
        f'}}\n'
        f"```"
    )


def new_id() -> str:
    return uuid.uuid4().hex[:8]


def now_ts():
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
    ts_ms = int(now.timestamp() * 1000)
    ts_gmt8 = now.strftime("%a %Y-%m-%d %H:%M GMT+8")
    return ts, ts_ms, ts_gmt8


def make_session_header(session_id, ts, ts_ms, provider, model, cwd):
    id1, id2, id3 = new_id(), new_id(), new_id()
    return [
        {"type": "session", "version": 3, "id": session_id, "timestamp": ts, "cwd": cwd},
        {"type": "model_change", "id": id1, "parentId": None, "timestamp": ts, "provider": provider, "modelId": model},
        {"type": "thinking_level_change", "id": id2, "parentId": id1, "timestamp": ts, "thinkingLevel": "off"},
        {"type": "custom", "customType": "model-snapshot", "data": {"timestamp": ts_ms, "provider": provider, "modelApi": "anthropic-messages", "modelId": model}, "id": id3, "parentId": id2, "timestamp": ts},
    ], id3


def make_user_message(query, ts, ts_ms, parent_id):
    msg_id = new_id()
    return {"type": "message", "id": msg_id, "parentId": parent_id, "timestamp": ts,
            "message": {"role": "user", "content": [{"type": "text", "text": query}], "timestamp": ts_ms}}, msg_id


def make_custom_message(chat_id, sender_id, sender_name, ts, ts_gmt8, parent_id):
    msg_id = new_id()
    return {"type": "custom_message", "customType": "openclaw.runtime-context",
            "content": build_runtime_context(chat_id, sender_id, sender_name, ts_gmt8),
            "display": False, "details": {"source": "openclaw-runtime-context"},
            "id": msg_id, "parentId": parent_id, "timestamp": ts}, msg_id


def make_assistant_message(text, ts, ts_ms, parent_id, thinking=None, tool_calls=None):
    """构建 assistant message，支持 text + thinking + tool_calls 完整写入"""
    msg_id = new_id()
    content = []
    if thinking:
        content.append({"type": "thinking", "thinking": thinking})
    if tool_calls:
        for tc in tool_calls:
            content.append({"type": "tool_use", "id": tc.get("id", ""), "name": tc.get("name", ""), "input": tc.get("input", {})})
    if text:
        content.append({"type": "text", "text": text})
    if not content:
        content.append({"type": "text", "text": ""})
    return {"type": "message", "id": msg_id, "parentId": parent_id, "timestamp": ts,
            "message": {"role": "assistant", "content": content, "timestamp": ts_ms}}, msg_id


def make_result_message(result_text, ts, ts_ms, parent_id, total_cost=0, num_turns=0,
                         is_error=False, stop_reason="", duration_ms=0, duration_api_ms=0,
                         model_usage=None, usage=None, session_id_cc=""):
    """构建 result message，完整保留 CC 最终结果文本"""
    msg_id = new_id()
    data = {
        "total_cost_usd": total_cost,
        "num_turns": num_turns,
        "is_error": is_error,
        "stop_reason": stop_reason,
        "duration_ms": duration_ms,
        "duration_api_ms": duration_api_ms,
        "cc_session_id": session_id_cc,
        "result_text": result_text,  # 完整文本，不截断
    }
    if model_usage:
        data["model_usage"] = model_usage
    if usage:
        data["usage"] = usage
    return {"type": "custom", "customType": "cc-result",
            "data": data,
            "id": msg_id, "parentId": parent_id, "timestamp": ts}, msg_id


# ============================================================
# Task → Session 映射
# ============================================================

MAP_FILE_NAME = "task-session-map.json"


def get_map_path(agent_name: str) -> str:
    sessions_dir = os.path.expanduser(f"~/.openclaw/agents/{agent_name}/sessions")
    return os.path.join(sessions_dir, MAP_FILE_NAME)


def load_task_session_map(agent_name: str) -> dict:
    map_path = get_map_path(agent_name)
    if not os.path.exists(map_path):
        return {}
    try:
        with open(map_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_task_session_map(agent_name: str, mapping: dict):
    map_path = get_map_path(agent_name)
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    with open(map_path, 'w') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


def find_local_session(task_id: str, agent_name: str) -> tuple:
    """根据 task_id 查找本地会话文件，返回 (session_id, jsonl_path) 或 (None, None)"""
    mapping = load_task_session_map(agent_name)
    session_id = mapping.get(str(task_id))
    if not session_id:
        return None, None
    sessions_dir = os.path.expanduser(f"~/.openclaw/agents/{agent_name}/sessions")
    jsonl_path = os.path.join(sessions_dir, f"{session_id}.jsonl")
    if os.path.exists(jsonl_path):
        return session_id, jsonl_path
    # jsonl 被清理了，清除映射，下次会新建
    print(f"⚠️ 映射中 session {session_id} 的 jsonl 已不存在，将新建会话")
    mapping.pop(str(task_id), None)
    save_task_session_map(agent_name, mapping)
    return None, None


def register_session(task_id: str, session_id: str, agent_name: str):
    """注册 task_id → session_id 映射"""
    mapping = load_task_session_map(agent_name)
    mapping[str(task_id)] = session_id
    save_task_session_map(agent_name, mapping)
    print(f"📝 已注册映射: task_id={task_id} → session_id={session_id}")


# ============================================================
# CC 流式调用 + 实时转换
# ============================================================

def stream_cc_and_write(query, model, writer, parent_id,
                        chat_id, sender_id, sender_name, cc_cwd=None):
    ts, ts_ms, ts_gmt8 = now_ts()

    # 写入 user message + custom_message
    user_msg, user_id = make_user_message(query, ts, ts_ms, parent_id)
    custom_msg, custom_id = make_custom_message(chat_id, sender_id, sender_name, ts, ts_gmt8, user_id)
    writer.write_many([user_msg, custom_msg])
    print(f"  ✍️  user message 已写入")

    # 启动 CC 流式输出
    cmd = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", model, query]
    print(f"🚀 启动 CC (流式): model={model}")

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1,
        cwd=cc_cwd
    )

    tool_id_to_name = {}
    last_id = custom_id
    total_cost = 0.0
    num_turns = 0
    _init_written = False

    def update_ts():
        nonlocal ts, ts_ms, ts_gmt8
        ts, ts_ms, ts_gmt8 = now_ts()

    def write_custom(custom_type, data):
        """写入一条 custom 记录，返回新 last_id"""
        nonlocal last_id
        update_ts()
        msg_id = new_id()
        record = {
            "type": "custom", "customType": custom_type,
            "data": data,
            "id": msg_id, "parentId": last_id, "timestamp": ts
        }
        writer.write(record)
        last_id = msg_id
        return msg_id

    def write_raw_event(event):
        """将 CC 原始事件完整写入为 custom(cc-raw) 记录，确保不丢失任何数据"""
        nonlocal last_id
        update_ts()
        msg_id = new_id()
        record = {
            "type": "custom", "customType": "cc-raw",
            "data": event,
            "id": msg_id, "parentId": last_id, "timestamp": ts
        }
        writer.write(record)
        last_id = msg_id
        return msg_id

    try:
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            event_type = event.get("type")

            # ── system (init): CC 环境信息 ── 只在首次写入，APPEND 时跳过
            if event_type == "system":
                if _init_written:
                    print(f"  ⏭️  cc-init 跳过 (已写过)")
                    continue
                _init_written = True
                # 完整原始事件写入为 assistant message (Markdown)
                update_ts()
                msg_id = new_id()
                init_text = json.dumps(event, ensure_ascii=False, indent=2)
                md_text = (
                    f"### 🔧 CC 初始化\n"
                    f"- **模型**: {event.get('model', '')}\n"
                    f"- **版本**: {event.get('claude_code_version', '')}\n"
                    f"- **工作目录**: {event.get('cwd', '')}\n"
                    f"- **权限模式**: {event.get('permissionMode', '')}\n"
                    f"- **工具数量**: {len(event.get('tools', []))}\n"
                    f"- **MCP 服务**: {len(event.get('mcp_servers', []))}\n"
                    f"- **Skills**: {len(event.get('skills', []))}\n"
                    f"\n<details><summary>完整原始数据</summary>\n\n```json\n{init_text}\n```\n\n</details>"
                )
                record = {"type": "message", "id": msg_id, "parentId": last_id, "timestamp": ts,
                          "message": {"role": "assistant",
                                       "content": [{"type": "text", "text": md_text}],
                                       "timestamp": ts_ms,
                                       "details": {"source": "cc-init",
                                                    "cc_session_id": event.get("session_id", ""),
                                                    "cc_model": event.get("model", ""),
                                                    "cc_cwd": event.get("cwd", ""),
                                                    "cc_tools": event.get("tools", []),
                                                    "cc_version": event.get("claude_code_version", ""),
                                                    "permission_mode": event.get("permissionMode", ""),
                                                    "mcp_servers": event.get("mcp_servers", []),
                                                    "memory_paths": event.get("memory_paths", []),
                                                    "skills": event.get("skills", []),
                                                    "slash_commands": event.get("slash_commands", []),
                                                    "plugins": event.get("plugins", []),
                                                    "agents": event.get("agents", []),
                                                    "api_key_source": event.get("apiKeySource", ""),
                                                    "uuid": event.get("uuid", "")}}}
                writer.write(record)
                last_id = msg_id
                print(f"  ✍️  cc-init→assistant (model={event.get('model','')}, {len(event.get('tools',[]))} tools)")

            # ── assistant: CC 回复（text / thinking / tool_use） ──
            elif event_type == "assistant":
                msg = event.get("message", {})
                content_list = msg.get("content", [])

                text_parts = []
                thinking_parts = []
                tool_uses = []
                for block in content_list:
                    btype = block.get("type")
                    if btype == "text":
                        text_parts.append(block.get("text", ""))
                    elif btype == "thinking":
                        thinking_parts.append(block.get("thinking", ""))
                    elif btype == "tool_use":
                        tool_uses.append(block)
                        tool_id_to_name[block.get("id", "")] = block.get("name", "unknown")

                update_ts()

                # CC assistant 原始事件写入为 assistant message (Markdown)
                update_ts()
                msg_id = new_id()
                raw_text = json.dumps(event, ensure_ascii=False, indent=2)
                # 收集 assistant 事件概要
                asst_summary_parts = []
                for block in content_list:
                    btype = block.get("type")
                    if btype == "text":
                        asst_summary_parts.append(f"text({len(block.get('text', ''))} chars)")
                    elif btype == "thinking":
                        asst_summary_parts.append(f"thinking({len(block.get('thinking', ''))} chars)")
                    elif btype == "tool_use":
                        asst_summary_parts.append(f"tool_use:{block.get('name', '?')}")
                asst_summary = ", ".join(asst_summary_parts) if asst_summary_parts else "empty"
                md_text = (
                    f"### 🤖 CC Assistant Event\n"
                    f"- **内容**: {asst_summary}\n"
                    f"\n<details><summary>完整原始数据</summary>\n\n```json\n{raw_text}\n```\n\n</details>"
                )
                record = {"type": "message", "id": msg_id, "parentId": last_id, "timestamp": ts,
                          "message": {"role": "assistant",
                                       "content": [{"type": "text", "text": md_text}],
                                       "timestamp": ts_ms,
                                       "details": {"source": "cc-raw:assistant"}}}
                writer.write(record)
                last_id = msg_id

                # 构建完整的 assistant message（含 thinking + tool_calls + text）
                tool_calls_for_msg = None
                if tool_uses:
                    tool_calls_for_msg = [{"type": "tool_use", "id": tu.get("id", ""), "name": tu.get("name", ""),
                                           "input": tu.get("input", {})} for tu in tool_uses]

                full_text = "\n".join(text_parts) if text_parts else ""
                full_thinking = "\n".join(thinking_parts) if thinking_parts else None

                rec, rid = make_assistant_message(
                    full_text, ts, ts_ms, last_id,
                    thinking=full_thinking,
                    tool_calls=tool_calls_for_msg
                )
                writer.write(rec)
                last_id = rid

                parts_desc = []
                if thinking_parts:
                    parts_desc.append(f"thinking({len(full_thinking)} chars)")
                if tool_uses:
                    parts_desc.append(f"tool_use({', '.join(tu.get('name','') for tu in tool_uses)})")
                if text_parts:
                    parts_desc.append(f"text({len(full_text)} chars)")
                print(f"  ✍️  assistant [{', '.join(parts_desc)}]")

            # ── user: CC 的 tool_result 回传 ──
            elif event_type == "user":
                msg = event.get("message", {})
                content_list = msg.get("content", [])

                # CC user (tool_result) 原始事件写入为 assistant message (Markdown)
                update_ts()
                msg_id = new_id()
                raw_text = json.dumps(event, ensure_ascii=False, indent=2)
                md_text = (
                    f"### 📥 CC Tool Result Events\n"
                    f"\n<details><summary>完整原始数据</summary>\n\n```json\n{raw_text}\n```\n\n</details>"
                )
                record = {"type": "message", "id": msg_id, "parentId": last_id, "timestamp": ts,
                          "message": {"role": "assistant",
                                       "content": [{"type": "text", "text": md_text}],
                                       "timestamp": ts_ms,
                                       "details": {"source": "cc-raw:user"}}}
                writer.write(record)
                last_id = msg_id

                for block in content_list:
                    if block.get("type") == "tool_result":
                        tool_use_id = block.get("tool_use_id", "")
                        tool_output = block.get("content", "")
                        if isinstance(tool_output, list):
                            tool_output = "\n".join(b.get("text", str(b)) for b in tool_output if isinstance(b, dict))

                        tool_name = tool_id_to_name.get(tool_use_id, "unknown")
                        update_ts()

                        # toolResult 写成 assistant message (Markdown, 折叠)
                        msg_id = new_id()
                        output_preview = tool_output[:3000] if len(tool_output) > 5000 else tool_output
                        output_truncated = len(tool_output) > 5000
                        truncate_note = " (已截断展示)" if output_truncated else ""
                        md_text = (
                            f"### 🔧 Tool Result: `{tool_name}`\n"
                            f"\n> 📏 输出长度: {len(tool_output)} chars{truncate_note}\n"
                            f"\n<details><summary>点击展开结果</summary>\n\n````\n{output_preview}\n````\n\n</details>"
                        )
                        record = {"type": "message", "id": msg_id, "parentId": last_id, "timestamp": ts,
                                  "message": {"role": "assistant",
                                               "content": [{"type": "text", "text": md_text}],
                                               "timestamp": ts_ms,
                                               "details": {"source": "cc-toolResult",
                                                            "toolCallId": tool_use_id, "toolName": tool_name,
                                                            "status": "completed", "exitCode": 0, "durationMs": 0,
                                                            "outputLength": len(tool_output),
                                                            "aggregated": tool_output[:200]}}}
                        writer.write(record)
                        last_id = msg_id
                        print(f"  ✍️  toolResult→assistant ({tool_name}, {len(tool_output)} chars)")

            # ── result: CC 最终结果 ── 完整写入（不截断）
            elif event_type == "result":
                total_cost = event.get("total_cost_usd", 0)
                num_turns = event.get("num_turns", 0)
                result_text = event.get("result", "")
                is_error = event.get("is_error", False)
                stop_reason = event.get("stop_reason", "")
                duration_ms = event.get("duration_ms", 0)
                duration_api_ms = event.get("duration_api_ms", 0)
                model_usage = event.get("modelUsage", {})
                usage = event.get("usage", {})
                session_id_cc = event.get("session_id", "")

                # cc-result 只写统计信息（不重复 result_text，assistant message 已有完整回复）
                update_ts()
                msg_id = new_id()
                result_detail = {
                    "total_cost_usd": total_cost,
                    "num_turns": num_turns,
                    "is_error": is_error,
                    "stop_reason": stop_reason,
                    "duration_ms": duration_ms,
                    "duration_api_ms": duration_api_ms,
                    "cc_session_id": session_id_cc,
                }
                if model_usage:
                    result_detail["model_usage"] = model_usage
                if usage:
                    result_detail["usage"] = usage
                cost_str = f"${total_cost:.4f}"
                duration_str = f"{duration_ms/1000:.1f}s" if duration_ms else "N/A"
                api_duration_str = f"{duration_api_ms/1000:.1f}s" if duration_api_ms else "N/A"
                error_tag = " ❌ ERROR" if is_error else ""
                md_text = (
                    f"### 📊 CC Summary{error_tag}\n"
                    f"\n| 指标 | 值 |\n"
                    f"|------|-----|\n"
                    f"| 💰 费用 | {cost_str} |\n"
                    f"| 🔄 轮次 | {num_turns} |\n"
                    f"| ⏱️ 总耗时 | {duration_str} |\n"
                    f"| ⏱️ API耗时 | {api_duration_str} |\n"
                    f"| 🛑 停止原因 | {stop_reason} |"
                )
                record = {"type": "message", "id": msg_id, "parentId": last_id, "timestamp": ts,
                          "message": {"role": "assistant",
                                       "content": [{"type": "text", "text": md_text}],
                                       "timestamp": ts_ms,
                                       "details": {"source": "cc-result", **result_detail}}}
                writer.write(record)
                last_id = msg_id
                print(f"  ✍️  cc-result→assistant (cost=${total_cost:.4f}, {num_turns} turns, text={len(result_text)} chars)")

            # ── 其他未知事件类型：完整写入 ──
            else:
                # 未知事件也写成 assistant message (Markdown)
                update_ts()
                msg_id = new_id()
                raw_text = json.dumps(event, ensure_ascii=False, indent=2)
                md_text = (
                    f"### ❓ CC Unknown Event: `{event_type}`\n"
                    f"\n<details><summary>完整原始数据</summary>\n\n```json\n{raw_text}\n```\n\n</details>"
                )
                record = {"type": "message", "id": msg_id, "parentId": last_id, "timestamp": ts,
                          "message": {"role": "assistant",
                                       "content": [{"type": "text", "text": md_text}],
                                       "timestamp": ts_ms,
                                       "details": {"source": "cc-raw:unknown"}}}
                writer.write(record)
                last_id = msg_id
                print(f"  ✍️  cc-raw→assistant [type={event_type}] (unknown event, preserved)")

    except KeyboardInterrupt:
        proc.terminate()
        print("\n⚠️ CC 被中断")

    proc.wait()

    if proc.returncode != 0:
        stderr_output = proc.stderr.read()[:500] if proc.stderr else ""
        print(f"⚠️ CC 退出码: {proc.returncode}")
        if stderr_output:
            print(f"   {stderr_output}")

    print(f"📊 CC 完成: {num_turns} 轮对话, 费用 ${total_cost:.4f}")
# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="CC 会话转 OpenClaw 格式 (流式)")
    parser.add_argument("--agent-name", required=True, help="OpenClaw agent 目录名")
    parser.add_argument("--task-id", required=True, help="AIMA 任务 ID")
    parser.add_argument("--query", required=True, help="传给 CC 的请求内容")
    parser.add_argument("--model", default="sonnet", help="CC 模型 (默认 sonnet)")
    parser.add_argument("--chat-id", help="钉钉 chat_id (覆盖配置文件)")
    parser.add_argument("--sender-id", help="钉钉 sender_id (覆盖配置文件)")
    parser.add_argument("--sender-name", help="钉钉 sender 姓名 (覆盖配置文件)")
    parser.add_argument("--cwd", help="CC 的工作目录 (默认: 当前目录)")
    args = parser.parse_args()

    # 读取配置文件
    config = load_config(args.agent_name)
    if config:
        print(f"📋 已加载配置: {args.agent_name}")
    elif not (args.chat_id and args.sender_id and args.sender_name):
        print(f"⚠️ 配置文件中未找到 {args.agent_name}，且未通过命令行指定 chat-id/sender-id/sender-name")
        print(f"   请在 {CONFIG_PATH} 中添加配置，或通过命令行参数指定")

    # 合并配置：命令行参数 > 配置文件
    chat_id = args.chat_id or config.get("chat_id", "")
    sender_id = args.sender_id or config.get("sender_id", "")
    sender_name = args.sender_name or config.get("sender_name", "")

    if not chat_id or not sender_id or not sender_name:
        print(f"❌ 缺少必要参数: chat_id={chat_id}, sender_id={sender_id}, sender_name={sender_name}")
        sys.exit(1)

    # 工作目录
    cc_cwd = os.path.expanduser(args.cwd) if args.cwd else os.getcwd()

    sessions_dir = os.path.expanduser(f"~/.openclaw/agents/{args.agent_name}/sessions")
    os.makedirs(sessions_dir, exist_ok=True)

    # 根据 task_id 查找本地会话
    existing_session_id, existing_jsonl_path = find_local_session(args.task_id, args.agent_name)

    if existing_session_id and existing_jsonl_path:
        # === APPEND 模式 ===
        print(f"📎 发现已有会话: {existing_session_id} (task_id={args.task_id})，追加消息")
        writer = SessionWriter(existing_jsonl_path)
        writer.load_last_id()
        parent_id = writer.last_id

        stream_cc_and_write(args.query, args.model, writer, parent_id,
                            chat_id, sender_id, sender_name, cc_cwd)
        session_id = existing_session_id

    else:
        # === 新建会话模式 ===
        session_id = str(uuid.uuid4())
        jsonl_path = os.path.join(sessions_dir, f"{session_id}.jsonl")
        print(f"🆕 新建会话: {session_id}")

        ts, ts_ms, ts_gmt8 = now_ts()
        cwd = cc_cwd

        # 写入会话头部
        header, last_id = make_session_header(session_id, ts, ts_ms, "claude-code", args.model, cwd)
        writer = SessionWriter(jsonl_path)
        writer.write_many(header)
        print(f"  ✍️  session header 已写入")

        # 注册映射
        register_session(args.task_id, session_id, args.agent_name)

        # 流式调用 CC 并写入
        stream_cc_and_write(args.query, args.model, writer, last_id,
                            chat_id, sender_id, sender_name, cc_cwd)

    # 绑定 AIMA 任务（每次调用都绑定，新建和追加均执行）
    try:
        bind_result = subprocess.run(
            ["aima", "workspace", "task", "bind-session", "--taskId", args.task_id, "--sessionId", session_id],
            capture_output=True, text=True, timeout=30
        )
        if bind_result.returncode == 0:
            print(f"✅ 会话已绑定到 AIMA 任务 {args.task_id}")
        else:
            print(f"⚠️ AIMA 绑定失败（不影响会话写入）: {bind_result.stderr.strip()[:100]}")
    except Exception as e:
        print(f"⚠️ AIMA 绑定异常（不影响会话写入）: {e}")

    print(f"\n🎉 完成！session_id: {session_id}")


if __name__ == "__main__":
    main()