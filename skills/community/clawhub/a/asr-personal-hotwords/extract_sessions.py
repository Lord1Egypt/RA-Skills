#!/usr/bin/env python3
"""
extract_sessions.py — 从 OpenClaw session JSONL 文件中提取对话数据

输出格式: 每行 "发送者：内容"，兼容 asr-corrector 的 chat_data 输入。
"""

import json
import glob
import os
import re
import sys
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

CST = timezone(timedelta(hours=8))

# 需要跳过的消息前缀
SKIP_PREFIXES = [
    "[cron:",
    "[Subagent Context]",
    "<<<BEGIN_OPENCLAW_INTERNAL_CONTEXT>>>",
    "[Untrusted daily memory",
    "BEGIN_QUOTED_NOTES",
    "END_QUOTED_NOTES",
    "[Startup context loaded",
    "[Bootstrap truncation",
    "Conversation info (untrusted",
    "Sender (untrusted metadata)",
    "[Queued user message",
    "Replied message (untrusted",
    "System (untrusted):",
    "[Mon ", "[Tue ", "[Wed ", "[Thu ", "[Fri ", "[Sat ", "[Sun ",
]

# 需要跳过的消息内容关键词
SKIP_CONTAINS = [
    "sessions_spawn",
    "HEARTBEAT_OK",
    "NO_REPLY",
    "openclaw-memory-promotion",
    "OPENCLAW_CACHE_BOUNDARY",
    "Runtime: agent=main",
    "[Subagent Task]",
    "[Internal task completion event]",
    "Subagent Context",
]


def should_skip(content: str) -> bool:
    """判断是否应跳过该消息"""
    if len(content) < 3:
        return True
    for prefix in SKIP_PREFIXES:
        if content.startswith(prefix):
            return True
    check_region = content[:300]
    for pattern in SKIP_CONTAINS:
        if pattern in check_region:
            return True
    # 跳过纯 JSON / 纯代码块
    if content.startswith("{") and content.endswith("}"):
        return True
    if content.startswith("```"):
        return True
    # 跳过纯英文/代码日志（不含任何中文字符）
    if not re.search(r'[\u4e00-\u9fff]', content):
        return True
    # 跳过以 URL 开头的消息
    if re.match(r'^https?://', content):
        return True
    return False


def extract_text(content) -> str:
    """从 message content 中提取纯文本"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "\n".join(parts)
    return ""


def resolve_self_agent(session_base_dir: str) -> tuple:
    """
    自动识别当前 agent 名称和工作空间。
    通过 skill 所在路径推断 agent 的 workspace，再从 openclaw.json 中反查 agent 名称。
    
    Returns:
        (agent_name, workspace_path)
    """
    import json as _json
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 从 skill 路径推断 workspace: .../workspace[-xxx]/skills/asr-personal-hotwords/
    parts = skill_dir.replace("\\", "/").split("/")
    workspace_path = None
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] == "skills" and i > 0:
            workspace_path = "/".join(parts[:i])
            break
    
    # 读取 openclaw.json 查找匹配的 agent
    oc_config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(oc_config_path, "r", encoding="utf-8") as f:
            oc_config = _json.load(f)
        
        agents_cfg = oc_config.get("agents", {})
        defaults_workspace = agents_cfg.get("defaults", {}).get("workspace", "")
        agent_list = agents_cfg.get("list", [])
        
        if workspace_path:
            # 先检查是否匹配某个 agent 的独立 workspace
            for agent in agent_list:
                agent_ws = agent.get("workspace", "")
                if agent_ws and os.path.normpath(agent_ws) == os.path.normpath(workspace_path):
                    return (agent["id"], workspace_path)
            # 检查是否匹配 defaults workspace（未配置独立 workspace 的 agent）
            if defaults_workspace and os.path.normpath(defaults_workspace) == os.path.normpath(workspace_path):
                # 找第一个没有独立 workspace 的 agent
                for agent in agent_list:
                    if not agent.get("workspace"):
                        return (agent["id"], workspace_path)
    except Exception as e:
        logger.warning(f"读取 openclaw.json 失败: {e}")
    
    # 回退：环境变量
    env_agent = os.environ.get("OPENCLAW_AGENT_NAME", "main")
    return (env_agent, workspace_path or defaults_workspace or "")


def extract_sessions(
    target_date: str,
    session_base_dir: str = "~/.openclaw/agents",
    agents: list = None,
    max_content_len: int = 300,
    end_date: str = None,
) -> list[dict]:
    """
    从 OpenClaw session 文件中提取指定日期的对话。

    Args:
        target_date: 起始日期 "YYYY-MM-DD"
        session_base_dir: agent sessions 根目录
        agents: 要提取的 agent 列表, None 或 ["*"] 表示全部
        max_content_len: 单条消息最大字符数
        end_date: 结束日期 "YYYY-MM-DD"（含），默认等于 target_date

    Returns:
        按时间排序的消息列表 [{"sender": str, "content": str, "timestamp": str}]
    """
    session_base_dir = os.path.expanduser(session_base_dir)
    if end_date is None:
        end_date = target_date

    # 生成需要匹配的日期前缀列表
    date_prefixes = []
    current = datetime.strptime(target_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    while current <= end:
        date_prefixes.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    # 扫描 agent 目录
    if agents is None or agents == ["*"]:
        agent_dirs = glob.glob(os.path.join(session_base_dir, "*/sessions"))
    elif agents == ["self"]:
        agent_name, _ = resolve_self_agent(session_base_dir)
        logger.info(f"自动识别当前 agent: {agent_name}")
        d = os.path.join(session_base_dir, agent_name, "sessions")
        agent_dirs = [d] if os.path.isdir(d) else []
    else:
        agent_dirs = []
        for agent in agents:
            d = os.path.join(session_base_dir, agent, "sessions")
            if os.path.isdir(d):
                agent_dirs.append(d)

    messages = []
    files_scanned = 0
    files_matched = 0

    for agent_dir in agent_dirs:
        agent_name = agent_dir.split("/agents/")[1].split("/sessions")[0]
        for fpath in glob.glob(os.path.join(agent_dir, "*.jsonl")):
            # 跳过 reset/deleted 文件
            basename = os.path.basename(fpath)
            if ".reset." in basename or ".deleted." in basename:
                continue

            # 快速跳过：文件修改时间早于目标日期则跳过
            try:
                mtime = os.path.getmtime(fpath)
                mtime_date = datetime.fromtimestamp(mtime, tz=CST).strftime("%Y-%m-%d")
                if mtime_date < target_date:
                    continue
            except OSError:
                pass

            files_scanned += 1

            try:
                file_has_match = False
                with open(fpath, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        obj = json.loads(line)
                        if obj.get("type") != "message":
                            continue

                        ts_str = obj.get("timestamp", "")
                        # 转换为 CST 日期再过滤（JSONL 中时间戳是 UTC）
                        try:
                            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                            ts_date_cst = dt.astimezone(CST).strftime("%Y-%m-%d")
                        except (ValueError, TypeError):
                            continue
                        if ts_date_cst not in date_prefixes:
                            continue

                        msg = obj.get("message", {})
                        role = msg.get("role", "")
                        if role not in ("user", "assistant"):
                            continue

                        content = extract_text(msg.get("content", ""))
                        if not content or not content.strip():
                            continue

                        stripped = content.strip()
                        if should_skip(stripped):
                            continue

                        file_has_match = True

                        # 截断 + 清理换行
                        if len(stripped) > max_content_len:
                            stripped = stripped[:max_content_len] + "..."
                        stripped = stripped.replace("\n", " ").strip()

                        sender = "用户" if role == "user" else "助手"
                        messages.append({
                            "sender": sender,
                            "content": stripped,
                            "timestamp": ts_str,
                            "agent": agent_name,
                        })

                if file_has_match:
                    files_matched += 1
            except Exception as e:
                logger.warning(f"读取文件失败 {fpath}: {e}")

    # 按时间排序
    messages.sort(key=lambda x: x["timestamp"])

    logger.info(
        f"扫描 {files_scanned} 个文件, {files_matched} 个匹配, "
        f"提取 {len(messages)} 条消息 "
        f"(日期: {target_date}" + (f" ~ {end_date}" if end_date != target_date else "") + ")"
    )
    return messages


def format_chat_data(messages: list[dict]) -> str:
    """将消息列表格式化为 asr-corrector 的 chat_data 格式"""
    lines = []
    for msg in messages:
        lines.append(f"{msg['sender']}：{msg['content']}")
    return "\n".join(lines)


def chunk_chat_data(messages: list[dict], max_lines: int = 400, max_chars: int = 9500) -> list[str]:
    """
    将消息分块，确保每块不超过 API 限制。

    Returns:
        chat_data 文本块列表
    """
    chunks = []
    current_lines = []
    current_chars = 0

    for msg in messages:
        line = f"{msg['sender']}：{msg['content']}"
        line_len = len(line) + 1  # +1 for newline

        if current_lines and (len(current_lines) >= max_lines or current_chars + line_len > max_chars):
            chunks.append("\n".join(current_lines))
            current_lines = []
            current_chars = 0

        current_lines.append(line)
        current_chars += line_len

    if current_lines:
        chunks.append("\n".join(current_lines))

    return chunks


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="从 OpenClaw session 提取对话数据")
    parser.add_argument("--date", default=None, help="目标日期 YYYY-MM-DD（默认前一天）")
    parser.add_argument("--start", default=None, help="起始日期")
    parser.add_argument("--end", default=None, help="结束日期")
    parser.add_argument("--agents", nargs="+", default=["*"], help="Agent 列表")
    parser.add_argument("--max-len", type=int, default=300, help="单条消息最大字符")
    parser.add_argument("--output", default=None, help="输出文件路径")
    args = parser.parse_args()

    if args.start and args.end:
        target_date = args.start
        end_date = args.end
    elif args.date:
        target_date = args.date
        end_date = args.date
    else:
        yesterday = datetime.now(CST) - timedelta(days=1)
        target_date = yesterday.strftime("%Y-%m-%d")
        end_date = target_date

    messages = extract_sessions(
        target_date=target_date,
        agents=args.agents,
        max_content_len=args.max_len,
        end_date=end_date,
    )

    chat_data = format_chat_data(messages)
    print(f"提取 {len(messages)} 条消息, {len(chat_data)} 字符", file=sys.stderr)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(chat_data)
        print(f"已保存到 {args.output}", file=sys.stderr)
    else:
        print(chat_data)
