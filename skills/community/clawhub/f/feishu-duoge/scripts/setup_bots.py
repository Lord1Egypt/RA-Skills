#!/usr/bin/env python3
"""
Feishu Bot Setup Script
Automates the creation and configuration of Feishu bots with OpenClaw.
"""

import json
import sys
import subprocess
import os
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"Error running: {cmd}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result.stdout


def create_agent(agent_id, workspace_path):
    """Create a new OpenClaw agent."""
    print(f"Creating agent: {agent_id}")
    cmd = f'openclaw agents add {agent_id} --workspace {workspace_path} --non-interactive'
    run_command(cmd)
    print(f"✓ Agent {agent_id} created")


def create_agent_files(workspace, bot_config):
    """Create agent configuration files."""
    print(f"Creating configuration files for {bot_config['agentId']}")
    
    # Get personality config (support both old and new format)
    personality = bot_config.get('personality', bot_config)
    
    role = personality.get('role', '智能助手')
    tagline = personality.get('tagline', '你的智能助手')
    style = personality.get('style', '专业、高效')
    style_desc = personality.get('styleDescription', personality.get('style_description', ''))
    responsibilities = personality.get('responsibilities', ['回答问题', '提供帮助'])
    description = personality.get('description', f'我是你的{role}，{style}。')
    motto = personality.get('motto', '让我们一起高效工作！')
    emoji = personality.get('emoji', '🤖')
    
    # SOUL.md
    soul_content = f"""# SOUL.md - {role}

_{description}_

## 核心定位

**{role}** - {tagline}

## 职责范围

"""
    for resp in responsibilities:
        soul_content += f"- {resp}\n"
    
    soul_content += f"""
## 工作风格

**{style}**

{style_desc}

---

_{motto}_
"""
    
    with open(f"{workspace}/SOUL.md", 'w') as f:
        f.write(soul_content)
    
    # IDENTITY.md
    identity_content = f"""# IDENTITY.md - {role}

- **Name:** {role}
- **Creature:** AI Assistant
- **Vibe:** {style}
- **Emoji:** {emoji}
- **Avatar:** (optional)
"""
    
    with open(f"{workspace}/IDENTITY.md", 'w') as f:
        f.write(identity_content)
    
    # AGENTS.md
    agents_content = f"""# AGENTS.md - {role}工作空间

这是{role} ({bot_config['agentId']}) 的专属工作空间。

## 定位

对接飞书机器人：{bot_config['name']}
主要职责：{', '.join(responsibilities)}

## 文件结构

- `SOUL.md` - 角色定义和性格
- `IDENTITY.md` - 身份信息
- `MEMORY.md` - 长期记忆（重要信息）
- `memory/` - 每日记忆日志
- `TOOLS.md` - 工具使用笔记
- `HEARTBEAT.md` - 定时任务配置

## 注意事项

- 定期整理和备份重要文件
- 记录常用工具和脚本
- 保存重要对话和决策
"""
    
    with open(f"{workspace}/AGENTS.md", 'w') as f:
        f.write(agents_content)
    
    print(f"✓ Configuration files created for {bot_config['agentId']}")


def update_openclaw_config(bots):
    """Update OpenClaw configuration with Feishu accounts."""
    print("Updating OpenClaw configuration...")
    
    config_path = Path.home() / '.openclaw' / 'openclaw.json'
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Ensure channels.feishu exists
    if 'channels' not in config:
        config['channels'] = {}
    if 'feishu' not in config['channels']:
        config['channels']['feishu'] = {
            'enabled': True,
            'accounts': {}
        }
    
    # Add bot accounts
    for bot in bots:
        config['channels']['feishu']['accounts'][bot['name']] = {
            'appId': bot['appId'],
            'appSecret': bot['appSecret'],
            'encryptKey': bot['encryptKey'],
            'verificationToken': bot['verificationToken'],
            'domain': 'feishu',
            'connectionMode': bot.get('connectionMode', 'websocket'),
            'webhookPath': f"/webhook/feishu/{bot['name']}",
            'dmPolicy': 'open',
            'groupPolicy': 'open',
            'requireMention': False,
            'reactionNotifications': 'off',
            'typingIndicator': True,
            'resolveSenderNames': True
        }
    
    # Backup original config
    backup_path = config_path.with_suffix('.json.bak')
    with open(backup_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Write updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ OpenClaw configuration updated (backup: {backup_path})")


def bind_agents(bots):
    """Bind agents to Feishu accounts."""
    print("Binding agents to Feishu accounts...")
    
    for bot in bots:
        cmd = f"openclaw agents bind --agent {bot['agentId']} --bind feishu:{bot['name']}"
        run_command(cmd, check=False)  # Don't fail if already bound
        print(f"✓ Bound {bot['agentId']} to {bot['name']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: setup_bots.py <config.json>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    bots = config.get('bots', [])
    
    print(f"Setting up {len(bots)} Feishu bots...\n")
    
    # Step 1: Create agents
    for bot in bots:
        workspace = f"~/.openclay/agents/{bot['agentId']}/workspace"
        create_agent(bot['agentId'], workspace)
    
    print()
    
    # Step 2: Create agent files
    for bot in bots:
        workspace = os.path.expanduser(f"~/.openclay/agents/{bot['agentId']}/workspace")
        create_agent_files(workspace, bot)
    
    print()
    
    # Step 3: Update OpenClaw config
    update_openclaw_config(bots)
    
    print()
    
    # Step 4: Bind agents
    bind_agents(bots)
    
    print("\n" + "="*50)
    print("Setup complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Restart gateway: openclaw gateway restart")
    print("2. Configure Feishu apps to use WebSocket mode")
    print("3. Test each bot in Feishu")


if __name__ == '__main__':
    main()
