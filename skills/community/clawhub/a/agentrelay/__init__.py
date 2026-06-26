#!/usr/bin/env python3
"""AgentRelay Skill - 工具函数实现"""

import json
import random
import string
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# 配置 - 使用环境变量或默认路径
import os
BASE_DIR = Path(os.getenv("OPENCLAW_DATA_DIR", Path.home() / ".openclaw" / "data"))
STORAGE_PATH = BASE_DIR / "agentrelay" / "storage"
LOG_PATH = BASE_DIR / "agentrelay" / "logs"
REGISTRY_PATH = BASE_DIR / "agentrelay" / "registry.json"
STORAGE_ALIAS = "s"
DEFAULT_TTL_HOURS = 24
DEFAULT_REGISTRY_TTL_HOURS = 24 * 7

def ensure_dirs():
    """确保目录存在"""
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_registry() -> Dict[str, Any]:
    """读取持久化 registry。"""
    ensure_dirs()
    if not REGISTRY_PATH.exists():
        return {"events": {}}

    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        raw = f.read().strip()

    if not raw:
        return {"events": {}}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        data, _ = decoder.raw_decode(raw)
        # Auto-heal the registry if trailing garbage was left behind.
        save_registry(data)

    if "events" not in data or not isinstance(data["events"], dict):
        data = {"events": {}}
    return data

def save_registry(registry: Dict[str, Any]) -> None:
    """写回持久化 registry。"""
    ensure_dirs()
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

def upsert_registry_event(event_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """更新单个事件的持久化索引。"""
    registry = load_registry()
    events = registry.setdefault("events", {})
    existing = events.get(event_id, {})
    merged = {**existing, **event_data, "updated_at": datetime.now().isoformat()}
    events[event_id] = merged
    save_registry(registry)
    return merged

def get_registry_event(event_id: str) -> Dict[str, Any]:
    """从持久化索引读取事件。"""
    registry = load_registry()
    return registry.get("events", {}).get(event_id, {})

def get_event_file(event_id: str) -> Path:
    """获取事件文件路径"""
    return STORAGE_PATH / f"{event_id}.json"

def read_event_file(event_id: str) -> Dict[str, Any]:
    """读取事件文件"""
    file_path = get_event_file(event_id)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_secret(length: int = 6) -> str:
    """生成随机 Secret Code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def parse_iso_datetime(value: str) -> Optional[datetime]:
    """解析 ISO 时间戳。"""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None

def get_event_ttl_hours(content: Dict[str, Any]) -> int:
    """从内容中提取保留时长，默认 24 小时。"""
    ttl = (
        content.get("ttl_hours")
        or content.get("payload", {}).get("content", {}).get("ttl_hours")
    )
    try:
        ttl_value = int(ttl)
    except (TypeError, ValueError):
        ttl_value = DEFAULT_TTL_HOURS
    return max(1, ttl_value)

def get_file_alias_path(file_path: Path, storage_root: Path, alias: str = "s") -> str:
    """获取文件别名路径（如 s/file.json）"""
    try:
        relative = file_path.relative_to(storage_root)
        return f"{alias}/{relative}"
    except ValueError:
        return str(file_path)

def resolve_alias(ptr: str, storage_root: Path, alias: str = "s") -> Path:
    """解析别名路径到完整路径"""
    if ptr.startswith(f"{alias}/"):
        return storage_root / ptr[len(alias)+1:]
    return Path(ptr)

def log_transaction(event_id: str, msg_type: str, sender: str, receiver: str, 
                   status: str, hint: str, ptr: str, notes: str, 
                   next_action_plan: str = "", log_path: Path = None):
    """
    记录交易日志
    
    Args:
        event_id: 事件 ID
        msg_type: 消息类型 (REQ, CMP, RECEIVED_CONFIRMATION, CREATE_POINTER)
        sender: 发送方
        receiver: 接收方
        status: 状态 (RECEIVED, CONFIRMED, COMPLETED, PREPARING)
        hint: 简述
        ptr: 文件指针
        notes: 详细说明
        next_action_plan: 下一步行动计划
        log_path: 日志路径（默认 LOG_PATH）
    """
    if log_path is None:
        log_path = LOG_PATH
    
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "event_id": event_id,
        "type": msg_type,
        "sender": sender,
        "receiver": receiver,
        "status": status,
        "hint": hint,
        "ptr": ptr,
        "notes": notes,
        "next_action_plan": next_action_plan
    }
    
    log_file = log_path / f"transactions_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def build_csv(msg_type: str, event_id: str, ptr: str, data: str = "") -> str:
    """构建 CSV 消息（格式：TYPE,ID,PTR,,DATA）"""
    # 简化格式：TYPE,ID,PTR,, （RESERVED 字段留空）
    return f"{msg_type},{event_id},{ptr},,{data}"

def parse_csv(csv_msg: str) -> Dict[str, str]:
    """解析 CSV 消息"""
    parts = csv_msg.split(',', 4)
    if len(parts) < 4:
        raise ValueError(f"Invalid CSV format: {csv_msg}")
    
    return {
        "type": parts[0],
        "event_id": parts[1],
        "ptr": parts[2],
        "reserved": parts[3] if len(parts) > 3 else "",
        "data": parts[4] if len(parts) > 4 else ""
    }

def normalize_relay_message(raw_message: str) -> str:
    """从完整 AgentRelay 文本中提取 CSV 协议消息"""
    text = raw_message.strip()
    if not text:
        raise ValueError("Empty AgentRelay message")

    if "AgentRelay:" in text:
        text = text.split("AgentRelay:", 1)[1].strip()

    if "\n" in text:
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("- ") or ":" in line and "," not in line:
                continue
            if "," in line:
                return line

    return text

# ========== 主要工具函数 ==========

def agentrelay_send(agent_id: str, message_type: str, event_id: str, 
                   content: Dict[str, Any], secret: Optional[str] = None) -> Dict[str, Any]:
    """
    发送 AgentRelay 消息
    
    Args:
        agent_id: 目标 agent ID
        message_type: "REQ" or another explicit protocol type
        event_id: 事件 ID
        content: 内容字典
        secret: Secret Code（可选）
    
    Returns:
        dict: {file_path, ptr, csv_message, secret}
    """
    ensure_dirs()
    
    # 生成或验证 Secret
    if secret is None:
        secret = generate_secret(6)
    
    sender = content.get("sender_agent")
    receiver = content.get("receiver_agent") or agent_id
    ttl_hours = get_event_ttl_hours(content)

    if not sender:
        raise ValueError(f"Event {event_id} is missing sender_agent")
    if not receiver:
        raise ValueError(f"Event {event_id} is missing receiver_agent")

    # 准备文件内容
    file_content = {
        "meta": {
            "event_id": event_id,
            "type": message_type,
            "secret": secret,
            "created_at": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "ttl_hours": ttl_hours,
        },
        "payload": {
            "content": content
        }
    }
    
    # 写入文件
    file_name = f"{event_id}.json"
    file_path = STORAGE_PATH / file_name
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(file_content, f, ensure_ascii=False, indent=2)

    upsert_registry_event(
        event_id,
        {
            "event_id": event_id,
            "type": message_type,
            "secret": secret,
            "sender": sender,
            "receiver": receiver,
            "ttl_hours": ttl_hours,
            "ptr": get_file_alias_path(file_path, STORAGE_PATH, STORAGE_ALIAS),
            "file_path": str(file_path),
            "file_exists": True,
            "status": "sent",
            "created_at": file_content["meta"]["created_at"],
        },
    )
    
    # 生成指针
    ptr = get_file_alias_path(file_path, STORAGE_PATH, STORAGE_ALIAS)
    
    # 构建 CSV 消息
    csv_message = build_csv(message_type, event_id, ptr, '')
    
    # 记录日志
    log_transaction(
        event_id, message_type, sender, agent_id,
        "SENT", f"{message_type} to {agent_id}", ptr,
        "File created", log_path=LOG_PATH
    )
    
    return {
        "file_path": str(file_path),
        "ptr": ptr,
        "csv_message": csv_message,
        "secret": secret
    }

def agentrelay_receive(csv_message: str) -> Dict[str, Any]:
    """
    接收并解析 AgentRelay 消息
    
    Args:
        csv_message: CSV 格式消息
    
    Returns:
        dict: {type, event_id, ptr, content, secret}
    """
    csv_message = normalize_relay_message(csv_message)
    parsed = parse_csv(csv_message)
    
    msg_type = parsed["type"]
    event_id = parsed["event_id"]
    ptr = parsed["ptr"]
    
    # 解析文件指针
    file_path = resolve_alias(ptr, STORAGE_PATH, STORAGE_ALIAS)
    
    # 读取文件
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    content = data.get("payload", {}).get("content", {})
    secret = data.get("meta", {}).get("secret", "")
    
    meta = data.get("meta", {})

    sender = meta.get("sender")
    receiver = meta.get("receiver")
    
    if not sender or not receiver:
        raise ValueError(
            f"Event {event_id} is missing explicit sender/receiver metadata"
        )
    
    # 📍 日志 #1: REQ RECEIVED
    log_transaction(
        event_id, msg_type, sender, receiver,
        "RECEIVED", f"Read {ptr}", ptr,
        "File read successfully",
        "Will acknowledge and fetch file",  # next_action_plan
        log_path=LOG_PATH
    )
    
    # 📍 日志 #2: RECEIVED_CONFIRMATION (自动确认收到)
    log_transaction(
        event_id, "RECEIVED_CONFIRMATION", receiver, sender,
        "CONFIRMED", "Confirmed request receipt", "",
        "Received REQ, will process task",
        "Processing task, will send CMP when done",  # next_action_plan
        log_path=LOG_PATH
    )

    if meta.get("burn_on_read") or content.get("burn_on_read"):
        file_path.unlink(missing_ok=True)
        upsert_registry_event(
            event_id,
            {
                "event_id": event_id,
                "file_exists": False,
                "status": "burned_on_read",
                "burned_at": datetime.now().isoformat(),
            },
        )
    else:
        upsert_registry_event(
            event_id,
            {
                "event_id": event_id,
                "file_exists": True,
                "status": "received",
                "last_received_at": datetime.now().isoformat(),
            },
        )
    
    return {
        "type": msg_type,
        "event_id": event_id,
        "ptr": ptr,
        "content": content,
        "secret": secret,
        "full_data": data
    }

def agentrelay_cmp(event_id: str, secret: str, sender_override: str = None, receiver_override: str = None) -> str:
    """
    构建 CMP (Complete) 消息 - 任务完成确认
    
    Args:
        event_id: 事件 ID
        secret: Secret Code
        sender_override: 可选的发送方覆盖
        receiver_override: 可选的接收方覆盖
    
    Returns:
        str: CSV 格式的 CMP 消息
    """
    data = read_event_file(event_id)
    meta = data.get("meta", {})
    stored_secret = meta.get("secret", "")

    if secret and stored_secret and secret != stored_secret:
        raise ValueError(f"Secret mismatch for event {event_id}")

    effective_secret = secret or stored_secret
    if not effective_secret:
        raise ValueError(f"Missing secret for event {event_id}")

    current_agent = meta.get("receiver")
    next_agent = meta.get("sender")
    if not current_agent or not next_agent:
        raise ValueError(
            f"Event {event_id} is missing explicit sender/receiver metadata"
        )
    
    sender = sender_override or current_agent
    receiver = receiver_override or next_agent

    # CMP 消息不需要文件指针，直接在 DATA 字段放 Secret
    cmp_msg = build_csv("CMP", event_id, "", effective_secret)

    upsert_registry_event(
        event_id,
        {
            "event_id": event_id,
            "type": meta.get("type", "REQ"),
            "secret": effective_secret,
            "sender": receiver,
            "receiver": sender,
            "status": "completed",
            "cmp_message": cmp_msg,
            "completed_at": datetime.now().isoformat(),
        },
    )
    
    # 📍 日志 #3: CMP COMPLETED
    log_transaction(
        event_id, "CMP", sender, receiver,
        "COMPLETED", f"CMP generated for {event_id}", "",
        f"CMP message: {cmp_msg}",
        "Event completed",  # next_action_plan
        log_path=LOG_PATH
    )
    
    return cmp_msg

def agentrelay_verify(cmp_message: str) -> Dict[str, Any]:
    """
    校验收到的 CMP 消息是否与事件文件中的 secret 一致

    Args:
        cmp_message: 完整消息或裸 CSV

    Returns:
        dict: 校验结果
    """
    csv_message = normalize_relay_message(cmp_message)
    parsed = parse_csv(csv_message)

    if parsed["type"] != "CMP":
        raise ValueError(f"Expected CMP message, got {parsed['type']}")

    event_id = parsed["event_id"]
    received_secret = parsed["data"]
    event_record = get_registry_event(event_id)
    data = None

    try:
        data = read_event_file(event_id)
        expected_secret = data.get("meta", {}).get("secret", "")
    except FileNotFoundError:
        expected_secret = event_record.get("secret", "")

    if not expected_secret:
        raise FileNotFoundError(
            f"No event metadata available for {event_id}; cannot verify CMP"
        )

    verified = bool(expected_secret) and received_secret == expected_secret

    sender = (
        (data or {}).get("meta", {}).get("sender")
        or event_record.get("sender")
    )
    receiver = (
        (data or {}).get("meta", {}).get("receiver")
        or event_record.get("receiver")
    )

    upsert_registry_event(
        event_id,
        {
            "event_id": event_id,
            "verified": verified,
            "last_verification_at": datetime.now().isoformat(),
            "last_received_secret": received_secret,
            "status": "verified" if verified else "verification_failed",
        },
    )

    return {
        "status": "ok" if verified else "mismatch",
        "event_id": event_id,
        "verified": verified,
        "expected_secret": expected_secret,
        "received_secret": received_secret,
        "sender": sender,
        "receiver": receiver,
        "file_exists": get_event_file(event_id).exists(),
    }

def cleanup_stale_events(
    default_ttl_hours: int = DEFAULT_TTL_HOURS,
    registry_ttl_hours: int = DEFAULT_REGISTRY_TTL_HOURS,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    清理过期事件文件与 registry 记录。

    文件级 TTL 优先取事件自身 ttl_hours，否则使用 default_ttl_hours。
    registry 记录在文件已不存在时，超过 registry_ttl_hours 后清理。
    """
    ensure_dirs()
    current_time = now or datetime.now()
    registry = load_registry()
    events = registry.setdefault("events", {})

    deleted_files = []
    deleted_registry = []
    kept_registry = {}

    for event_id, record in list(events.items()):
        file_path = get_event_file(event_id)
        file_exists = file_path.exists()
        ttl_hours = int(record.get("ttl_hours") or default_ttl_hours)
        created_at = parse_iso_datetime(record.get("created_at")) or parse_iso_datetime(
            record.get("updated_at")
        ) or current_time

        if file_exists:
            try:
                file_data = read_event_file(event_id)
                meta = file_data.get("meta", {})
                ttl_hours = int(meta.get("ttl_hours") or record.get("ttl_hours") or default_ttl_hours)
                created_at = parse_iso_datetime(meta.get("created_at")) or created_at
            except (ValueError, FileNotFoundError, json.JSONDecodeError):
                pass

            age_seconds = (current_time - created_at).total_seconds()
            if age_seconds >= ttl_hours * 3600:
                file_path.unlink(missing_ok=True)
                deleted_files.append(event_id)
                record = {
                    **record,
                    "file_exists": False,
                    "status": "expired",
                    "expired_at": current_time.isoformat(),
                }
            else:
                record = {**record, "file_exists": True}

        file_exists = file_path.exists()
        reference_time = parse_iso_datetime(record.get("expired_at")) or parse_iso_datetime(
            record.get("updated_at")
        ) or created_at
        registry_age_seconds = (current_time - reference_time).total_seconds()

        if (not file_exists) and registry_age_seconds >= registry_ttl_hours * 3600:
            deleted_registry.append(event_id)
            continue

        kept_registry[event_id] = record

    registry["events"] = kept_registry
    save_registry(registry)

    return {
        "status": "ok",
        "deleted_files": deleted_files,
        "deleted_registry": deleted_registry,
        "kept_events": sorted(kept_registry.keys()),
        "default_ttl_hours": default_ttl_hours,
        "registry_ttl_hours": registry_ttl_hours,
    }

def agentrelay_update_file(event_id: str, updates: Dict[str, Any], next_event_id: str = None) -> str:
    """
    为下一跳创建指针文件（Prepare pointer file for next hop）
    
    Args:
        event_id: 当前事件 ID（用于日志追溯）
        updates: 要更新的字段
        next_event_id: 下一跳的事件 ID（如果不提供，则用 event_id）
    
    Returns:
        str: 更新后的文件路径
    """
    # 如果没有指定下一跳 ID，使用当前 ID
    target_event_id = next_event_id if next_event_id else event_id
    
    file_path = STORAGE_PATH / f"{target_event_id}.json"
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 强制统一格式：必须有 payload.content
    if "payload" not in data:
        data["payload"] = {}
    if "content" not in data["payload"]:
        data["payload"]["content"] = {}
    
    # 合并更新内容
    data["payload"]["content"].update(updates)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    upsert_registry_event(
        target_event_id,
        {
            "event_id": target_event_id,
            "ptr": get_file_alias_path(file_path, STORAGE_PATH, STORAGE_ALIAS),
            "file_path": str(file_path),
            "file_exists": True,
            "status": "updated",
            "last_update_at": datetime.now().isoformat(),
        },
    )
    
    meta = data.get("meta", {})
    current_agent = meta.get("receiver")
    if not current_agent:
        raise ValueError(
            f"Event {target_event_id} is missing explicit receiver metadata"
        )
    
    # 📍 日志：CREATE_POINTER (属于下一跳的准备工作)
    ptr = get_file_alias_path(file_path, STORAGE_PATH, STORAGE_ALIAS)
    log_transaction(
        target_event_id,  # ← 使用下一跳的 event_id
        "CREATE_POINTER",
        current_agent, "next_hop",
        "PREPARING", f"Created pointer file {ptr}", ptr,
        f"Prepared for next hop with: {json.dumps(updates)}",
        "Preparing pointer file for next hop",  # next_action_plan
        log_path=LOG_PATH
    )
    
    return str(file_path)

# ========== 供 agent 调用的简化接口 ==========

class AgentRelayTool:
    """AgentRelay 工具类（供 agent 在 prompt 中调用）"""
    
    @staticmethod
    def send(agent_id: str, msg_type: str, event_id: str, content: dict) -> dict:
        """发送消息"""
        return agentrelay_send(agent_id, msg_type, event_id, content)
    
    @staticmethod
    def receive(csv_msg: str) -> dict:
        """接收消息"""
        return agentrelay_receive(csv_msg)
    
    @staticmethod
    def cmp(event_id: str, secret: str) -> str:
        """生成 CMP 完成消息"""
        return agentrelay_cmp(event_id, secret)

    @staticmethod
    def verify(cmp_message: str) -> dict:
        """校验 CMP 消息"""
        return agentrelay_verify(cmp_message)
    
    @staticmethod
    def update(event_id: str, new_content: dict, next_event_id: str = None) -> str:
        """为下一跳创建指针文件"""
        return agentrelay_update_file(event_id, new_content, next_event_id)

    @staticmethod
    def cleanup(default_ttl_hours: int = DEFAULT_TTL_HOURS,
                registry_ttl_hours: int = DEFAULT_REGISTRY_TTL_HOURS) -> dict:
        """清理过期事件与 registry。"""
        return cleanup_stale_events(default_ttl_hours, registry_ttl_hours)
