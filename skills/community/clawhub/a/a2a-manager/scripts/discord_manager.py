#!/usr/bin/env python3
"""Discord Manager - Quản lý Category, Channel, Role trên Discord"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# OpenClaw workspace
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
CONFIG_FILE = WORKSPACE_ROOT / "a2a-manager" / "discord_config.json"

def load_config() -> Dict[str, Any]:
    """Load cấu hình Discord"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {
        "guild_id": "",
        "categories": {},
        "channels": {},
        "roles": {}
    }

def save_config(config: Dict[str, Any]):
    """Lưu cấu hình Discord"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

# === CATEGORY MANAGEMENT ===

def create_category(name: str, position: int = None) -> Dict[str, Any]:
    """
    Tạo category mới
    Lưu ý: Thực tế cần dùng Discord API hoặc OpenClaw message tool
    """
    config = load_config()
    
    if "categories" not in config:
        config["categories"] = {}
    
    # Generate category ID (simulated - thực tế sẽ từ Discord API)
    category_id = f"cat_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    config["categories"][name] = {
        "id": category_id,
        "name": name,
        "position": position or len(config["categories"]),
        "created_at": datetime.now().isoformat()
    }
    
    save_config(config)
    
    return {
        "success": True,
        "category_id": category_id,
        "name": name,
        "note": "Sử dụng message tool để tạo thực tế trên Discord"
    }

def delete_category(category_name: str) -> bool:
    """Xóa category"""
    config = load_config()
    
    if category_name in config.get("categories", {}):
        del config["categories"][category_name]
        save_config(config)
        return True
    return False

def rename_category(old_name: str, new_name: str) -> bool:
    """Đổi tên category"""
    config = load_config()
    
    if old_name in config.get("categories", {}):
        category_data = config["categories"][old_name]
        category_data["name"] = new_name
        config["categories"][new_name] = category_data
        del config["categories"][old_name]
        save_config(config)
        return True
    return False

def list_categories() -> List[Dict[str, Any]]:
    """Liệt kê categories"""
    config = load_config()
    return list(config.get("categories", {}).values())

# === CHANNEL MANAGEMENT ===

def create_channel(
    name: str,
    category: str = None,
    channel_type: str = "text",
    topic: str = None
) -> Dict[str, Any]:
    """Tạo channel mới"""
    config = load_config()
    
    if "channels" not in config:
        config["channels"] = {}
    
    channel_id = f"ch_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    config["channels"][name] = {
        "id": channel_id,
        "name": name,
        "category": category,
        "type": channel_type,
        "topic": topic,
        "created_at": datetime.now().isoformat()
    }
    
    save_config(config)
    
    return {
        "success": True,
        "channel_id": channel_id,
        "name": name,
        "category": category,
        "note": "Sử dụng message tool để tạo thực tế trên Discord"
    }

def delete_channel(channel_name: str) -> bool:
    """Xóa channel"""
    config = load_config()
    
    if channel_name in config.get("channels", {}):
        del config["channels"][channel_name]
        save_config(config)
        return True
    return False

def rename_channel(old_name: str, new_name: str) -> bool:
    """Đổi tên channel"""
    config = load_config()
    
    if old_name in config.get("channels", {}):
        channel_data = config["channels"][old_name]
        channel_data["name"] = new_name
        config["channels"][new_name] = channel_data
        del config["channels"][old_name]
        save_config(config)
        return True
    return False

def move_channel(channel_name: str, new_category: str) -> bool:
    """Di chuyển channel sang category khác"""
    config = load_config()
    
    if channel_name in config.get("channels", {}):
        config["channels"][channel_name]["category"] = new_category
        save_config(config)
        return True
    return False

def list_channels(category: str = None) -> List[Dict[str, Any]]:
    """Liệt kê channels"""
    config = load_config()
    channels = config.get("channels", {}).values()
    
    if category:
        channels = [ch for ch in channels if ch.get("category") == category]
    
    return list(channels)

# === ROLE MANAGEMENT ===

def create_role(
    name: str,
    color: str = "#000000",
    permissions: List[str] = None,
    hoist: bool = False
) -> Dict[str, Any]:
    """Tạo role mới"""
    config = load_config()
    
    if "roles" not in config:
        config["roles"] = {}
    
    role_id = f"role_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    config["roles"][name] = {
        "id": role_id,
        "name": name,
        "color": color,
        "permissions": permissions or [],
        "hoist": hoist,
        "created_at": datetime.now().isoformat()
    }
    
    save_config(config)
    
    return {
        "success": True,
        "role_id": role_id,
        "name": name,
        "note": "Sử dụng message tool để tạo thực tế trên Discord"
    }

def assign_role(user_id: str, role_name: str) -> Dict[str, Any]:
    """Gán role cho user"""
    config = load_config()
    
    if "user_roles" not in config:
        config["user_roles"] = {}
    
    if user_id not in config["user_roles"]:
        config["user_roles"][user_id] = []
    
    if role_name not in config["user_roles"][user_id]:
        config["user_roles"][user_id].append(role_name)
    
    save_config(config)
    
    return {
        "success": True,
        "user_id": user_id,
        "role": role_name
    }

def remove_role(user_id: str, role_name: str) -> bool:
    """Xóa role của user"""
    config = load_config()
    
    if user_id in config.get("user_roles", {}):
        if role_name in config["user_roles"][user_id]:
            config["user_roles"][user_id].remove(role_name)
            save_config(config)
            return True
    return False

def get_user_roles(user_id: str) -> List[str]:
    """Lấy roles của user"""
    config = load_config()
    return config.get("user_roles", {}).get(user_id, [])

def list_roles() -> List[Dict[str, Any]]:
    """Liệt kê roles"""
    config = load_config()
    return list(config.get("roles", {}).values())

# === AGENT BINDING ===

def bind_agent_to_channel(
    agent_name: str,
    channel_id: str,
    channel_name: str,
    category: str = None
) -> Dict[str, Any]:
    """Bind agent với channel"""
    config = load_config()
    
    if "agent_bindings" not in config:
        config["agent_bindings"] = {}
    
    config["agent_bindings"][agent_name] = {
        "channel_id": channel_id,
        "channel_name": channel_name,
        "category": category,
        "bound_at": datetime.now().isoformat()
    }
    
    save_config(config)
    
    return {
        "success": True,
        "agent": agent_name,
        "channel": channel_name
    }

def unbind_agent(agent_name: str) -> bool:
    """Unbind agent khỏi channel"""
    config = load_config()
    
    if agent_name in config.get("agent_bindings", {}):
        del config["agent_bindings"][agent_name]
        save_config(config)
        return True
    return False

def get_agent_binding(agent_name: str) -> Optional[Dict[str, Any]]:
    """Lấy binding của agent"""
    config = load_config()
    return config.get("agent_bindings", {}).get(agent_name)

class DiscordManager:
    """Wrapper class cho Discord management"""
    
    def __init__(self):
        self.config = load_config()
    
    # Category methods
    def create_category(self, name: str, position: int = None):
        return create_category(name, position)
    
    def delete_category(self, name: str):
        return delete_category(name)
    
    def rename_category(self, old: str, new: str):
        return rename_category(old, new)
    
    def list_categories(self):
        return list_categories()
    
    # Channel methods
    def create_channel(self, name: str, category: str = None, channel_type: str = "text"):
        return create_channel(name, category, channel_type)
    
    def delete_channel(self, name: str):
        return delete_channel(name)
    
    def rename_channel(self, old: str, new: str):
        return rename_channel(old, new)
    
    def move_channel(self, name: str, category: str):
        return move_channel(name, category)
    
    def list_channels(self, category: str = None):
        return list_channels(category)
    
    # Role methods
    def create_role(self, name: str, color: str = "#000000", permissions: List[str] = None):
        return create_role(name, color, permissions)
    
    def assign_role(self, user_id: str, role: str):
        return assign_role(user_id, role)
    
    def remove_role(self, user_id: str, role: str):
        return remove_role(user_id, role)
    
    def get_user_roles(self, user_id: str):
        return get_user_roles(user_id)
    
    # Binding methods
    def bind_agent(self, agent: str, channel_id: str, channel_name: str, category: str = None):
        return bind_agent_to_channel(agent, channel_id, channel_name, category)
    
    def unbind_agent(self, agent: str):
        return unbind_agent(agent)
    
    def get_binding(self, agent: str):
        return get_agent_binding(agent)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: discord_manager.py <action> [args...]")
        print("Actions: create_category, delete_category, create_channel, assign_role, bind_agent, etc.")
        sys.exit(1)
    
    action = sys.argv[1]
    dm = DiscordManager()
    
    # Parse action and execute
    if action == "create_category" and len(sys.argv) >= 3:
        print(json.dumps(dm.create_category(sys.argv[2]), indent=2))
    elif action == "delete_category" and len(sys.argv) >= 3:
        print(dm.delete_category(sys.argv[2]))
    elif action == "create_channel" and len(sys.argv) >= 3:
        category = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(dm.create_channel(sys.argv[2], category), indent=2))
    elif action == "assign_role" and len(sys.argv) >= 4:
        print(json.dumps(dm.assign_role(sys.argv[2], sys.argv[3]), indent=2))
    elif action == "bind_agent" and len(sys.argv) >= 5:
        channel_id = sys.argv[3]
        channel_name = sys.argv[4]
        category = sys.argv[5] if len(sys.argv) > 5 else None
        print(json.dumps(dm.bind_agent(sys.argv[2], channel_id, channel_name, category), indent=2))
    elif action == "list_categories":
        print(json.dumps(dm.list_categories(), indent=2))
    elif action == "list_channels":
        print(json.dumps(dm.list_channels(), indent=2))
    else:
        print("Invalid command")
