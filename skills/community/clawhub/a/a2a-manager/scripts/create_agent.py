#!/usr/bin/env python3
"""Create Agent - Tạo agent mới với đầy đủ cấu hình"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"

# Import từ các module khác
import sys
sys.path.insert(0, str(Path(__file__).parent))
from a2a_map import A2AMap, add_agent as add_agent_to_map
from discord_manager import DiscordManager

def get_agent_workspace(agent_name: str) -> Path:
    """Lấy đường dẫn workspace của agent"""
    workspace_name = agent_name.lower().replace(" ", "-")
    return WORKSPACE_ROOT / f"workspace-{workspace_name}"

def create_workspace(agent_name: str) -> Path:
    """Tạo workspace folder cho agent"""
    workspace = get_agent_workspace(agent_name)
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace

def create_soul_md(workspace: Path, config: Dict[str, Any]):
    """Tạo SOUL.md"""
    content = f"""# SOUL.md - {config['name']}

## Core Identity
- **Name:** {config['name']}
- **Title:** {config.get('title', '')}
- **Role:** {config.get('role', 'Agent')}

---

## Core Truths

> {config.get('lore', 'A faithful companion in The Aetherium.')}

## 🎭 Voice
- **Language:** {config.get('language', 'Vietnamese')}
- **Xưng:** {config.get('xung', 'em')}
- **Emoji:** {config.get('emoji', '✨')}
"""
    with open(workspace / "SOUL.md", "w") as f:
        f.write(content)

def create_identity_md(workspace: Path, config: Dict[str, Any]):
    """Tạo IDENTITY.md"""
    content = f"""# IDENTITY.md - {config['name']}

## Creature
{config.get('role', 'AI Companion')}

## Vibe
{config.get('vibe', 'Năng động, thân thiện')}

## Emoji
{config.get('emoji', '✨')}

## Notes
- Created: {datetime.now().strftime('%Y-%m-%d')}
- Managed by: A2A Manager
- Pillar: {config.get('pillar', 'General')}
"""
    with open(workspace / "IDENTITY.md", "w") as f:
        f.write(content)

def create_user_md(workspace: Path, config: Dict[str, Any]):
    """Tạo USER.md"""
    content = f"""# USER.md - {config['name']}

## User Profile

- **Name:** {config.get('user_name', 'Master')}
- **How to call them:** {config.get('user_call', 'Master')}
- **Pronouns:** He/Him
- **Timezone:** ICT (UTC+7 - Vietnam)

## Notes

- Owner of The Aetherium
- Likes efficient, concise communication
- Values consistency and proper agent hierarchy

## Context

### What do they care about?

- Multi-agent automation with clear roles
- System reliability
- Resource optimization

### What annoys them?

- System errors
- Redundant responses
- Agent overlap
"""
    with open(workspace / "USER.md", "w") as f:
        f.write(content)

def create_tools_md(workspace: Path, config: Dict[str, Any]):
    """Tạo TOOLS.md với tools mặc định"""
    default_tools = [
        "openclaw CLI",
        "homebrew",
        "discord"
    ]
    
    tools = config.get('tools', default_tools)
    
    content = """# TOOLS.md - """ + config['name'] + """

## Environment

### Available Tools

"""
    for tool in tools:
        content += f"- **{tool}**: Available\n"
    
    content += """
### Network
- Local network tools available
"""
    
    with open(workspace / "TOOLS.md", "w") as f:
        f.write(content)

def create_memory_md(workspace: Path, config: Dict[str, Any]):
    """Tạo MEMORY.md"""
    content = f"""# MEMORY.md - {config['name']}

## Lịch sử hoạt động

- **{datetime.now().strftime('%Y-%m-%d')}**: Được tạo bởi A2A Manager

## Thông tin Agent

- **Pillar:** {config.get('pillar', 'General')}
- **Model:** {config.get('model', 'flash')}
- **Skills:** {', '.join(config.get('skills', []))}
- **Channel:** {config.get('channel_name', 'N/A')}
"""
    
    memory_dir = workspace / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    with open(memory_dir / f"{datetime.now().strftime('%Y-%m-%d')}.md", "w") as f:
        f.write(content)

def create_agents_md_entry(config: Dict[str, Any]) -> str:
    """Tạo entry cho AGENTS.md"""
    return f"""
## {config['name']}

- **Role:** {config.get('role', 'Agent')}
- **Pillar:** {config.get('pillar', 'General')}
- **Model:** {config.get('model', 'flash')}
- **Channel:** {config.get('channel_name', 'N/A')}
- **Created:** {datetime.now().strftime('%Y-%m-%d')}
"""

def create_agent(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tạo agent mới với đầy đủ cấu hình
    
    Required fields:
    - name: Tên agent
    
    Optional fields:
    - title: Tiêu đề
    - role: Vai trò
    - pillar: Pillar (Anime, Games, Tech, etc.)
    - model: Model (flash, glm4, pro)
    - skills: List of skills
    - vibe: Mô tả tính cách
    - lore: Backstory
    - language: Ngôn ngữ (default: Vietnamese)
    - xung: Cách xưng (em, ta, etc.)
    - emoji: Emoji đại diện
    - channel_name: Tên channel
    - channel_id: ID channel
    - category: Category trong Discord
    - discord_user_id: Discord user ID
    """
    
    # Validate required fields
    if not config.get('name'):
        return {"success": False, "error": "name is required"}
    
    agent_name = config['name']
    
    # Set defaults
    defaults = {
        'title': '',
        'role': 'AI Companion',
        'pillar': 'General',
        'model': 'flash',
        'skills': [],
        'vibe': 'Năng động, thân thiện',
        'lore': 'A faithful companion in The Aetherium.',
        'language': 'Vietnamese',
        'xung': 'em',
        'emoji': '✨',
        'channel_name': f"#{agent_name.lower().replace(' ', '-')}",
        'channel_id': '',
        'category': 'General',
        'discord_user_id': '',
        'user_name': 'Master',
        'user_call': 'Master'
    }
    
    for k, v in defaults.items():
        if k not in config:
            config[k] = v
    
    # 1. Tạo workspace
    workspace = create_workspace(agent_name)
    
    # 2. Tạo các file cơ bản
    create_soul_md(workspace, config)
    create_identity_md(workspace, config)
    create_user_md(workspace, config)
    create_tools_md(workspace, config)
    create_memory_md(workspace, config)
    
    # 3. Cập nhật A2A_MAP.md
    a2a_config = {
        "name": config['name'],
        "discord_user_id": config.get('discord_user_id', ''),
        "channel_id": config.get('channel_id', ''),
        "category": config.get('category', 'General'),
        "role": config.get('role', 'Member'),
        "model": config.get('model', 'flash'),
        "skills": config.get('skills', []),
        "status": "active"
    }
    
    add_agent_to_map(a2a_config)
    
    # 4. Bind agent với channel (Discord Manager)
    dm = DiscordManager()
    if config.get('channel_id') and config.get('channel_name'):
        dm.bind_agent(
            agent_name,
            config['channel_id'],
            config['channel_name'],
            config.get('category')
        )
    
    return {
        "success": True,
        "agent_name": agent_name,
        "workspace": str(workspace),
        "files_created": ["SOUL.md", "IDENTITY.md", "USER.md", "TOOLS.md", "memory/"],
        "channel": config.get('channel_name'),
        "model": config.get('model'),
        "skills": config.get('skills', [])
    }

def delete_agent(agent_name: str) -> Dict[str, Any]:
    """Xóa agent"""
    # 1. Xóa workspace
    workspace = get_agent_workspace(agent_name)
    if workspace.exists():
        shutil.rmtree(workspace)
    
    # 2. Xóa khỏi A2A_MAP
    from a2a_map import remove_agent
    remove_agent(agent_name)
    
    # 3. Unbind khỏi Discord
    dm = DiscordManager()
    dm.unbind_agent(agent_name)
    
    return {
        "success": True,
        "agent_name": agent_name
    }

class AgentCreator:
    """Wrapper class để tạo agent"""
    
    def __init__(self):
        self.a2a = A2AMap()
        self.dm = DiscordManager()
    
    def create(self, config: dict):
        return create_agent(config)
    
    def delete(self, agent_name: str):
        return delete_agent(agent_name)
    
    def list(self):
        return self.a2a.get()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: create_agent.py <create|delete|list> [args...]")
        sys.exit(1)
    
    action = sys.argv[1]
    creator = AgentCreator()
    
    if action == "create" and len(sys.argv) >= 3:
        config = json.loads(sys.argv[2])
        print(json.dumps(creator.create(config), indent=2))
    elif action == "delete" and len(sys.argv) >= 3:
        print(json.dumps(creator.delete(sys.argv[2]), indent=2))
    elif action == "list":
        print(json.dumps(creator.list(), indent=2))
    else:
        print("Invalid command")
