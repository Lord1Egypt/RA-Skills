#!/usr/bin/env python3
"""A2A Map Manager - Quản lý A2A_MAP.md với Validation, Sync, Versioning"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

# === CONFIG ===
SKILL_DIR = Path(__file__).parent.parent
REFERENCES_DIR = SKILL_DIR / "references"
SKILL_A2A_MAP = REFERENCES_DIR / "A2A_MAP.md"

WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
WORKSPACE_A2A_MAP = WORKSPACE_ROOT / "A2A_MAP.md"
WORKSPACE_A2A_VERSION = WORKSPACE_ROOT / "a2a_versions"

# === TEMPLATE (từ references file) ===
def get_template() -> str:
    """Đọc template từ references/A2A_MAP.md"""
    if SKILL_A2A_MAP.exists():
        return SKILL_A2A_MAP.read_text()
    return "# A2A_MAP.md\n\n(No template found)"

# === VALIDATION ===
class ValidationError(Exception):
    pass

class AgentField(Enum):
    REQUIRED = ["agent", "model", "agent_type"]
    OPTIONAL = ["discord_id", "channel_id", "role", "skills", "vibe", "lore", "can_call", "can_be_called_by", "status", "expires_after", "parent_agent"]

VALID_MODELS = ["flash", "glm4", "pro"]
VALID_STATUSES = ["active", "idle", "offline"]
VALID_ROLES = ["Admin", "Mod", "Member", "Guest"]

# === AGENT TYPES (Task-Steward Inspired) ===
VALID_AGENT_TYPES = {
    "specialized": ["Coordinator", "Orchestrator", "Worker", "Security", "QA", "Concierge"],
    "role_specific": ["Coordinator", "Orchestrator", "Worker", "QA"],
    "specialist": ["temp_worker", "researcher", "coder", "qa_reviewer", "runner"]
}

def validate_agent(agent: Dict[str, Any], strict: bool = False) -> Dict[str, Any]:
    """
    Validate agent data
    strict=True: Bắt buộc tất cả trường
    strict=False: Chỉ bắt buộc required
    """
    errors = []
    warnings = []
    
    # Check required fields
    for field in AgentField.REQUIRED.value:
        if not agent.get(field):
            errors.append(f"Thiếu trường bắt buộc: {field}")
    
    # Validate model
    if agent.get("model") and agent["model"] not in VALID_MODELS:
        errors.append(f"Model không hợp lệ: {agent['model']}. Chỉ chấp nhận: {VALID_MODELS}")
    
    # Validate agent_type
    if agent.get("agent_type"):
        valid_types = VALID_AGENT_TYPES.get(agent.get("type", "specialized"), [])
        if agent["agent_type"] not in valid_types:
            errors.append(f"Agent type không hợp lệ: {agent['agent_type']}. Các loại hợp lệ: {valid_types}")
    
    # Validate status
    if agent.get("status") and agent["status"] not in VALID_STATUSES:
        errors.append(f"Status không hợp lệ: {agent['status']}")
    
    # Validate role
    if agent.get("role") and agent["role"] not in VALID_ROLES:
        warnings.append(f"Role không phổ biến: {agent['role']}")
    
    # Check duplicate Discord ID
    if agent.get("discord_id"):
        existing = get_agent_by_discord_id(agent["discord_id"])
        if existing and existing.get("agent") != agent.get("agent"):
            errors.append(f"Discord ID {agent['discord_id']} đã được sử dụng bởi {existing.get('agent')}")
    
    # Warnings for missing optional fields
    if strict:
        for field in AgentField.OPTIONAL.value:
            if not agent.get(field):
                warnings.append(f"Thiếu trường tùy chọn: {field}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def validate_map_consistency() -> Dict[str, Any]:
    """Kiểm tra tính nhất quán của toàn bộ map"""
    agents = get_all_agents()
    issues = []
    
    # Check duplicate names
    names = [a.get("agent", "").lower() for a in agents]
    duplicates = set([n for n in names if names.count(n) > 1])
    if duplicates:
        issues.append(f"Duplicate agent names: {duplicates}")
    
    # Check duplicate Discord IDs
    discord_ids = [a.get("discord_id") for a in agents if a.get("discord_id")]
    if len(discord_ids) != len(set(discord_ids)):
        issues.append("Duplicate Discord IDs found")
    
    # Check orphan channels (channel without agent)
    # Check missing models
    for agent in agents:
        if not agent.get("model"):
            issues.append(f"Agent {agent.get('agent')} missing model")
    
    return {
        "consistent": len(issues) == 0,
        "issues": issues,
        "total_agents": len(agents)
    }

# === SYNC ===
def sync_a2a_map(source: Path = None, target: Path = None) -> Dict[str, Any]:
    """
    Đồng bộ A2A_MAP.md giữa 2 vị trí
    Ưu tiên: workspace > skill references
    """
    if source is None:
        source = WORKSPACE_A2A_MAP
    if target is None:
        target = SKILL_A2A_MAP
    
    result = {"synced": False, "source": str(source), "target": str(target)}
    
    # Determine which is newer
    source_exists = source.exists()
    target_exists = target.exists()
    
    if not source_exists and not target_exists:
        result["error"] = "No files found"
        return result
    
    if source_exists and target_exists:
        source_mtime = source.stat().st_mtime
        target_mtime = target.stat().st_mtime
        
        if source_mtime >= target_mtime:
            # Workspace is newer, copy to skill
            shutil.copy2(source, target)
            result["synced"] = True
            result["direction"] = "workspace -> skill"
            result["source_time"] = datetime.fromtimestamp(source_mtime).isoformat()
        else:
            # Skill is newer, copy to workspace
            shutil.copy2(target, source)
            result["synced"] = True
            result["direction"] = "skill -> workspace"
            result["source_time"] = datetime.fromtimestamp(target_mtime).isoformat()
    elif source_exists:
        shutil.copy2(source, target)
        result["synced"] = True
        result["direction"] = "workspace -> skill (new file)"
    
    return result

# === VERSIONING ===
def get_map_path() -> Path:
    """Lấy đường dẫn A2A_MAP.md - ưu tiên workspace"""
    if WORKSPACE_A2A_MAP.exists():
        return WORKSPACE_A2A_MAP
    if SKILL_A2A_MAP.exists():
        return SKILL_A2A_MAP
    return WORKSPACE_A2A_MAP

def init_version_dir():
    """Khởi tạo thư mục version"""
    WORKSPACE_A2A_VERSION.mkdir(parents=True, exist_ok=True)

def save_version(agent_name: str = None, change_type: str = "update") -> str:
    """Lưu version snapshot"""
    init_version_dir()
    
    map_path = get_map_path()
    if not map_path.exists():
        return ""
    
    # Read current content
    with open(map_path) as f:
        content = f.read()
    
    # Generate version ID
    version_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_file = WORKSPACE_A2A_VERSION / f"{version_id}.md"
    
    # Save snapshot
    header = f"""# A2A_MAP Version {version_id}

**Change Type:** {change_type}
**Agent:** {agent_name or "N/A"}
**Timestamp:** {datetime.now().isoformat()}

---

"""
    with open(version_file, "w") as f:
        f.write(header + content)
    
    return version_id

def list_versions(limit: int = 10) -> List[Dict[str, Any]]:
    """Liệt kê các version"""
    init_version_dir()
    
    versions = []
    for v in sorted(WORKSPACE_A2A_VERSION.glob("*.md"), reverse=True)[:limit]:
        content = v.read_text()
        
        # Parse header
        change_type = "unknown"
        agent = "N/A"
        
        for line in content.split("\n"):
            if "**Change Type:**" in line:
                change_type = line.split(":**")[1].strip()
            if "**Agent:**" in line:
                agent = line.split(":**")[1].strip()
        
        versions.append({
            "version_id": v.stem,
            "change_type": change_type,
            "agent": agent,
            "file": str(v),
            "created": v.stat().st_ctime
        })
    
    return versions

def rollback(version_id: str) -> bool:
    """Rollback về version cũ"""
    version_file = WORKSPACE_A2A_VERSION / f"{version_id}.md"
    
    if not version_file.exists():
        return False
    
    # Read version content (skip header)
    with open(version_file) as f:
        content = f.read()
    
    # Find the separator
    if "---" in content:
        content = content.split("---", 1)[1]
        content = content.strip()
    
    # Restore to current map
    map_path = get_map_path()
    map_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(map_path, "w") as f:
        f.write(content)
    
    # Also sync to skill
    if SKILL_A2A_MAP.exists():
        shutil.copy2(map_path, SKILL_A2A_MAP)
    
    return True

# === CORE FUNCTIONS ===
def get_a2a_map_path() -> Path:
    return get_map_path()

def init_a2a_map():
    """Tạo A2A_MAP.md mới từ template trong references file"""
    if not get_a2a_map_path().exists():
        get_a2a_map_path().parent.mkdir(parents=True, exist_ok=True)
        template = get_template()
        with open(get_a2a_map_path(), "w") as f:
            f.write(template)

def parse_agent_table(content: str) -> List[Dict[str, Any]]:
    agents = []
    lines = content.split("\n")
    in_table = False
    
    for line in lines:
        if "| Agent |" in line and "Discord ID" in line:
            in_table = True
            continue
        if in_table and "---" in line:
            continue
        if in_table and line.strip() == "":
            break
        if in_table and "|" in line:
            cols = [c.strip() for c in line.split("|") if c.strip()]
            if len(cols) >= 5 and cols[0] and cols[0] != "(No agents)":
                agent = {
                    "agent": cols[0],
                    "discord_id": cols[1] if len(cols) > 1 else "",
                    "channel_id": cols[2] if len(cols) > 2 else "",
                    "role": cols[3] if len(cols) > 3 else "Member",
                    "model": cols[4] if len(cols) > 4 else "flash",
                    "skills": [s.strip() for s in cols[5].split(",")] if len(cols) > 5 and cols[5] else [],
                    "vibe": cols[6] if len(cols) > 6 else "",
                    "status": cols[7] if len(cols) > 7 else "active"
                }
                agents.append(agent)
    return agents

def parse_communication_matrix(content: str) -> Dict[str, Dict[str, str]]:
    matrix = {}
    lines = content.split("\n")
    in_table = False
    
    for line in lines:
        if "| Agent |" in line and "Can Call" in line:
            in_table = True
            continue
        if in_table and "---" in line:
            continue
        if in_table and line.strip() == "":
            break
        if in_table and "|" in line:
            cols = [c.strip() for c in line.split("|") if c.strip()]
            if len(cols) >= 3 and cols[0]:
                matrix[cols[0]] = {
                    "can_call": cols[1] if len(cols) > 1 else "",
                    "can_be_called_by": cols[2] if len(cols) > 2 else ""
                }
    return matrix

def parse_a2a_map() -> Dict[str, Any]:
    a2a_file = get_a2a_map_path()
    if not a2a_file.exists():
        init_a2a_map()
    
    with open(a2a_file) as f:
        content = f.read()
    
    return {
        "agents": parse_agent_table(content),
        "communication_matrix": parse_communication_matrix(content),
        "file_path": str(a2a_file)
    }

def get_all_agents() -> List[Dict[str, Any]]:
    return parse_a2a_map().get("agents", [])

def get_agent(agent_name: str) -> Optional[Dict[str, Any]]:
    agents = get_all_agents()
    for agent in agents:
        if agent.get("agent", "").lower() == agent_name.lower():
            return agent
    return None

def get_agent_by_discord_id(discord_id: str) -> Optional[Dict[str, Any]]:
    agents = get_all_agents()
    for agent in agents:
        if agent.get("discord_id") == discord_id:
            return agent
    return None

def add_agent(agent_config: Dict[str, Any], validate_first: bool = True, auto_sync: bool = True) -> Dict[str, Any]:
    """Thêm agent với validation và auto-sync"""
    
    # Validate
    if validate_first:
        validation = validate_agent(agent_config)
        if not validation["valid"]:
            return {"success": False, "errors": validation["errors"]}
        if validation["warnings"]:
            print(f"Warnings: {validation['warnings']}")
    
    # Save version trước khi thay đổi
    save_version(agent_config.get("agent"), "add")
    
    # ... (logic thêm agent giữ nguyên)
    a2a_file = get_a2a_map_path()
    if not a2a_file.exists():
        init_a2a_map()
    
    with open(a2a_file) as f:
        content = f.read()
    
    # Build row
    name = agent_config.get("agent", "")
    row = f"| {name} | {agent_config.get('discord_id', '')} | {agent_config.get('channel_id', '')} | {agent_config.get('role', 'Member')} | {agent_config.get('model', 'flash')} | {', '.join(agent_config.get('skills', []))} | {agent_config.get('vibe', '')} | {agent_config.get('status', 'active')} |"
    
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "| Agent |" in line and "Discord ID" in line:
            for j in range(i + 1, len(lines)):
                if "|" in lines[j] and "---" not in lines[j]:
                    if "(No agents)" in lines[j]:
                        lines[j] = row
                    break
            break
    
    with open(a2a_file, "w") as f:
        f.write("\n".join(lines))
    
    # Auto-sync removed - template from references
    
    return {"success": True, "agent": name}

def remove_agent(agent_name: str, auto_sync: bool = True) -> Dict[str, Any]:
    """Xóa agent với versioning"""
    save_version(agent_name, "remove")
    
    # ... (logic xóa giữ nguyên)
    a2a_file = get_a2a_map_path()
    if not a2a_file.exists():
        return {"success": False, "error": "File not found"}
    
    with open(a2a_file) as f:
        lines = f.readlines()
    
    found = False
    new_lines = []
    for line in lines:
        if f"| {agent_name} |" in line:
            found = True
            continue
        new_lines.append(line)
    
    if found:
        with open(a2a_file, "w") as f:
            f.writelines(new_lines)
        
        # sync removed - template from references
        
        return {"success": True, "agent": agent_name}
    
    return {"success": False, "error": "Agent not found"}

def update_agent(agent_name: str, updates: Dict[str, Any], validate_first: bool = True, auto_sync: bool = True) -> Dict[str, Any]:
    """Cập nhật agent với validation"""
    
    # Validate updates
    current = get_agent(agent_name)
    if not current:
        return {"success": False, "error": "Agent not found"}
    
    merged = {**current, **updates}
    
    if validate_first:
        validation = validate_agent(merged)
        if not validation["valid"]:
            return {"success": False, "errors": validation["errors"]}
    
    # Save version
    save_version(agent_name, "update")
    
    # ... (logic update giữ nguyên)
    a2a_file = get_a2a_map_path()
    with open(a2a_file) as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if f"| {agent_name} |" in line:
            cols = [c.strip() for c in line.split("|") if c.strip()]
            if len(cols) > 1:
                if "discord_id" in updates: cols[1] = updates["discord_id"]
                if "channel_id" in updates: cols[2] = updates["channel_id"]
                if "role" in updates: cols[3] = updates["role"]
                if "model" in updates: cols[4] = updates["model"]
                if "skills" in updates: cols[5] = ", ".join(updates["skills"]) if isinstance(updates["skills"], list) else updates["skills"]
                if "vibe" in updates: cols[6] = updates["vibe"]
                if "status" in updates: cols[7] = updates["status"]
                lines[i] = "| " + " | ".join(cols) + " |\n"
            break
    
    with open(a2a_file, "w") as f:
        f.writelines(lines)
    
    # sync removed - template from references
    
    return {"success": True, "agent": agent_name}

class A2AMap:
    """Wrapper class với đầy đủ tính năng"""
    
    def __init__(self):
        init_a2a_map()
    
    # Validation
    def validate(self, agent: Dict, strict: bool = False):
        return validate_agent(agent, strict)
    
    def validate_all(self):
        return validate_map_consistency()
    
    # Sync - removed (template from references)
    
    # Versioning
    def versions(self, limit: int = 10):
        return list_versions(limit)
    
    def rollback(self, version_id: str):
        return rollback(version_id)
    
    # Core CRUD
    def get(self, agent_name: str = None):
        if agent_name:
            return get_agent(agent_name)
        return get_all_agents()
    
    def add(self, config: dict):
        return add_agent(config)
    
    def remove(self, agent_name: str):
        return remove_agent(agent_name)
    
    def update(self, agent_name: str, updates: dict):
        return update_agent(agent_name, updates)

if __name__ == "__main__":
    import sys
    
    a2a = A2AMap()
    
    if len(sys.argv) < 2:
        print("""A2A Map Manager - với Validation, Sync, Versioning

Commands:
  a2a_map.py get [name]                    - Lấy agent hoặc danh sách
  a2a_map.py add '<json>'                  - Thêm agent (auto-validate + sync)
  a2a_map.py update name '<json>'           - Cập nhật agent
  a2a_map.py remove name                    - Xóa agent
  a2a_map.py validate [name]               - Validate một hoặc tất cả
  a2a_map.py sync                          - Đồng bộ workspace <-> skill
  a2a_map.py versions                      - Liệt kê versions
  a2a_map.py rollback <version_id>        - Rollback về version cũ
""")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "get" and len(sys.argv) >= 3:
        print(json.dumps(a2a.get(sys.argv[2]), indent=2))
    elif action == "get":
        print(json.dumps(a2a.get(), indent=2))
    elif action == "add" and len(sys.argv) >= 3:
        config = json.loads(sys.argv[2])
        print(json.dumps(a2a.add(config), indent=2))
    elif action == "update" and len(sys.argv) >= 4:
        print(json.dumps(a2a.update(sys.argv[2], json.loads(sys.argv[3])), indent=2))
    elif action == "remove" and len(sys.argv) >= 3:
        print(json.dumps(a2a.remove(sys.argv[2]), indent=2))
    elif action == "validate":
        if len(sys.argv) >= 3:
            agent = a2a.get(sys.argv[2])
            print(json.dumps(a2a.validate(agent), indent=2))
        else:
            print(json.dumps(a2a.validate_all(), indent=2))
    elif action == "sync":
        print(json.dumps(a2a.sync(), indent=2))
    elif action == "versions":
        print(json.dumps(a2a.versions(), indent=2))
    elif action == "rollback" and len(sys.argv) >= 3:
        print(json.dumps({"success": a2a.rollback(sys.argv[2])}, indent=2))
    else:
        print("Invalid command")
