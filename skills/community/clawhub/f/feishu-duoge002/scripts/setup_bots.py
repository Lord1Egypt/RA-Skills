#!/usr/bin/env python3
"""
Feishu Multi-Bot Setup - 批量创建多个独立飞书机器人
每个机器人拥有独立记忆、独立存储空间、独立大模型配置
"""
import json
import os
import sys
import subprocess
from typing import List, Dict, Any

def run_command(cmd: str, check: bool = True) -> str:
    """运行命令并返回输出"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        print(f"Exit code: {result.returncode}")
        # 不直接退出，让用户可以继续处理其他机器人
        return ""
    return result.stdout

def main():
    if len(sys.argv) != 2:
        print("Usage: python setup_bots.py <config.json>")
        print("Example: python setup_bots.py bots_config.json")
        sys.exit(1)
    
    config_path = sys.argv[1]
    if not os.path.exists(config_path):
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    bots = config.get('bots', [])
    if not bots:
        print("Error: No bots found in config")
        sys.exit(1)
    
    print(f"Found {len(bots)} bots to setup")
    
    # 读取现有的 openclaw 配置
    openclaw_config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(openclaw_config_path, 'r', encoding='utf-8') as f:
        openclaw_config = json.load(f)
    
    # 确保 channels 和 feishu 存在
    if 'channels' not in openclaw_config:
        openclaw_config['channels'] = {}
    if 'feishu' not in openclaw_config['channels']:
        openclaw_config['channels']['feishu'] = {
            'enabled': True,
            'accounts': {}
        }
    
    # 转换为多账号格式
    feishu_config = openclaw_config['channels']['feishu']
    if 'accounts' not in feishu_config:
        # 转换从单账号到多账号格式
        print("Converting single-account feishu config to multi-accounts format...")
        if feishu_config.get('appId'):
            existing_account = feishu_config.copy()
            # 移除顶层 key
            for k in ['enabled']:
                existing_account.pop(k, None)
            feishu_config = {
                'enabled': True,
                'accounts': {
                    'default': existing_account
                }
            }
        else:
            feishu_config = {
                'enabled': True,
                'accounts': {}
            }
        openclaw_config['channels']['feishu'] = feishu_config
    
    # 确保 agents 列表存在
    if 'agents' not in openclaw_config:
        openclaw_config['agents'] = {
            'defaults': {
                'workspace': '/root/.openclaw/workspace',
                'model': {
                    'primary': 'volcengine-plan/ark-code-latest'
                }
            },
            'list': [
                {
                    'id': 'main'
                }
            ]
        }
    
    if 'list' not in openclaw_config['agents']:
        openclaw_config['agents']['list'] = [
            {
                'id': 'main'
            }
        ]
    
    # 确保 bindings 存在
    if 'bindings' not in openclaw_config:
        openclaw_config['bindings'] = []
    
    # 为每个机器人创建配置
    for bot in bots:
        name = bot['name']
        agent_id = bot['agentId']
        app_id = bot['appId']
        app_secret = bot['appSecret']
        encrypt_key = bot.get('encryptKey', '')
        verification_token = bot.get('verificationToken', '')
        connection_mode = bot.get('connectionMode', 'websocket')
        model = bot.get('model', '')  # 如果指定了就用指定的模型，否则用默认
        personality = bot.get('personality', {})
        
        workspace_path = os.path.expanduser(f"~/.openclaw/agents/{agent_id}/workspace")
        agent_dir = os.path.expanduser(f"~/.openclaw/agents/{agent_id}/agent")
        os.makedirs(workspace_path, exist_ok=True)
        os.makedirs(agent_dir, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"⚙️  Setting up bot: {personality.get('role', name)} ({agent_id})")
        print(f"{'='*60}")
        
        # 检查 agent 是否已存在
        agents_list = openclaw_config['agents']['list']
        exists = any(agent.get('id') == agent_id for agent in agents_list)
        
        if not exists:
            # 创建 agent
            run_command(f"openclaw agents add {agent_id} --workspace {workspace_path} --non-interactive")
            # 添加到 agents 列表
            agents_list.append({
                'id': agent_id,
                'name': agent_id,
                'workspace': workspace_path,
                'agentDir': agent_dir
            })
            print(f"✅ Created agent: {agent_id}")
        else:
            print(f"⚠️ Agent {agent_id} already exists, skipping creation")
        
        # 设置模型如果指定了
        if model:
            # 直接修改 agent 配置文件
            agent_config_path = os.path.expanduser(f"~/.openclaw/agents/{agent_id}/agent/openclaw.json")
            if os.path.exists(agent_config_path):
                with open(agent_config_path, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)
                # 设置模型
                if 'model' not in agent_config:
                    agent_config['model'] = {}
                agent_config['model']['primary'] = model
                with open(agent_config_path, 'w', encoding='utf-8') as f:
                    json.dump(agent_config, f, indent=2)
                print(f"✅ Set model to: {model}")
            else:
                print(f"⚠️ Agent config not found at {agent_config_path}, skipping model set")
        
        # 添加到飞书账号配置
        feishu_account = {
            "appId": app_id,
            "appSecret": app_secret,
            "encryptKey": encrypt_key,
            "verificationToken": verification_token,
            "connectionMode": connection_mode,
            "domain": "feishu",
            "webhookPath": f"/webhook/feishu/{name}",
            "dmPolicy": "open",
            "groupPolicy": "open",
            "requireMention": False,
            "reactionNotifications": "off",
            "typingIndicator": True,
            "resolveSenderNames": True,
            "allowFrom": []  # 空数组表示允许所有人，dmPolicy=open 配合这个
        }
        feishu_config['accounts'][name] = feishu_account
        print(f"✅ Added feishu account configuration")
        
        # 检查是否已经有 binding
        bindings = openclaw_config.get('bindings', [])
        binding_exists = any(
            b.get('type') == 'route' and 
            b.get('match', {}).get('channel') == 'feishu' and 
            b.get('match', {}).get('accountId') == name and
            b.get('agentId') == agent_id
            for b in bindings
        )
        
        if not binding_exists:
            # 添加路由绑定
            bindings.append({
                "type": "route",
                "agentId": agent_id,
                "match": {
                    "channel": "feishu",
                    "accountId": name
                }
            })
            print(f"✅ Added route binding for {agent_id} -> feishu:{name}")
        else:
            print(f"⚠️ Route binding already exists, skipping")
        
        # 生成配置文件
        role = personality.get('role', name)
        tagline = personality.get('tagline', '')
        style = personality.get('style', '')
        style_description = personality.get('styleDescription', style)
        responsibilities: List[str] = personality.get('responsibilities', [])
        description = personality.get('description', '')
        motto = personality.get('motto', '')
        emoji = personality.get('emoji', '🤖')
        
        # SOUL.md
        soul_content = f"""# SOUL.md - {role}

{description}

## Core Position
**{role}** - {tagline}

## Responsibilities
{chr(10).join([f"- {item}" for item in responsibilities])}

## Working Style
{style_description}

---
{motto} {emoji}
"""
        with open(os.path.join(workspace_path, 'SOUL.md'), 'w', encoding='utf-8') as f:
            f.write(soul_content)
        
        # IDENTITY.md
        identity_content = f"""# IDENTITY.md - {role}

- **Name**: {role}
- **Creature**: Feishu AI Assistant
- **Vibe**: {style}
- **Emoji**: {emoji}

## Background
{description}
"""
        with open(os.path.join(workspace_path, 'IDENTITY.md'), 'w', encoding='utf-8') as f:
            f.write(identity_content)
        
        # AGENTS.md
        agents_content = f"""# AGENTS.md - {role} Workspace

This is the dedicated workspace for {role} ({name}).

## Files
- SOUL.md - Role definition and personality
- IDENTITY.md - Identity information
- MEMORY.md - Long-term memory
- memory/ - Daily memory logs
- TOOLS.md - Tool usage notes
- HEARTBEAT.md - Scheduled tasks configuration
"""
        with open(os.path.join(workspace_path, 'AGENTS.md'), 'w', encoding='utf-8') as f:
            f.write(agents_content)
        
        # MEMORY.md
        with open(os.path.join(workspace_path, 'MEMORY.md'), 'w', encoding='utf-8') as f:
            f.write("# Long-term Memory\n\n")
        
        # TOOLS.md
        with open(os.path.join(workspace_path, 'TOOLS.md'), 'w', encoding='utf-8') as f:
            f.write("# Tool Usage Notes\n\n")
        
        # HEARTBEAT.md
        with open(os.path.join(workspace_path, 'HEARTBEAT.md'), 'w', encoding='utf-8') as f:
            f.write("# Scheduled Tasks\n\n")
        
        # memory directory
        os.makedirs(os.path.join(workspace_path, 'memory'), exist_ok=True)
        
        print(f"✅ Generated all configuration files: SOUL.md, IDENTITY.md, etc.")
    
    # 保存更新后的 openclaw 配置
    with open(openclaw_config_path, 'w', encoding='utf-8') as f:
        json.dump(openclaw_config, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"🎉 All {len(bots)} bots setup completed!")
    print(f"{'='*60}")
    print()
    print("📋 Next steps:")
    print("1. Check if all bots are configured correctly:  openclaw agents list")
    print("2. Restart gateway to apply changes:            openclaw gateway restart")
    print("3. Test the bots by sending them messages in Feishu")
    print()
    print("🔧 Troubleshooting:")
    print("- If bot doesn't reply, check gateway logs:")
    print("  journalctl --user -u openclaw-gateway.service -n 50 --no-pager")
    print("- Look for 'blocked unauthorized sender' messages")
    print("- Add the user ID to that bot's allowFrom in ~/.openclaw/openclaw.json")
    print()

if __name__ == "__main__":
    main()
