#!/usr/bin/env python3
"""
OpenClaw Agent Management Script
Provides robust creation of agents and workspace initialization.
"""
import argparse
import subprocess
import os
from pathlib import Path
import json

def run_cmd(cmd, check=True):
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=check)

def create_agent(name, agent_id, description=""):
    workspace = f"{os.path.expanduser('~')}/.openclaw/workspace-{agent_id}"
    
    # 1. Create agent via CLI
    run_cmd(["openclaw", "agents", "add", agent_id, "--workspace", workspace])
    
    # 2. Set Identity
    run_cmd(["openclaw", "agents", "set-identity", "--agent", agent_id, "--name", name, "--json"])
    
    # 3. Initialize Standard Files
    ws_path = Path(workspace)
    os.makedirs(ws_path, exist_ok=True)
    
    # 4. Remove .git directory if it exists to prevent nested git repos
    git_dir = ws_path / ".git"
    if git_dir.exists() and git_dir.is_dir():
        import shutil
        shutil.rmtree(git_dir)
        print(f"Removed nested .git directory at {git_dir}")
        
    agents_md = f"""# {name} 指南

## 核心目标
{description or "协助用户完成特定任务。"}

## 记忆使用规范
*   **会话开始时**：读取 `USER.md` 和 `SOUL.md`。
*   **日常记录**：记录到 `memory/YYYY-MM-DD.md`。
*   **长期记忆**：重要信息整理至 `MEMORY.md`。
"""
    with open(ws_path / "AGENTS.md", "w") as f: f.write(agents_md)

    soul_md = f"""# {name} 的人设

## 角色定位
你是 {name}。
{description}

## 语气风格
* 专业、高效。

## 边界
* 不捏造事实，权限操作需确认。
"""
    with open(ws_path / "SOUL.md", "w") as f: f.write(soul_md)
    
    print(f"✅ Agent {agent_id} ({name}) created successfully at {workspace}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--id", required=True)
    create_parser.add_argument("--description", default="")
    create_parser.add_argument("--app-id", help="Feishu App ID")
    create_parser.add_argument("--app-secret", help="Feishu App Secret")
    create_parser.add_argument("--require-pairing", action="store_true", help="Set dmPolicy to pairing")
    
    args = parser.parse_args()
    if args.command == "create":
        create_agent(args.name, args.id, args.description)
        
        # If feishu credentials are provided, bind them
        if args.app_id and args.app_secret:
            config_path = f"{os.path.expanduser('~')}/.openclaw/openclaw.json"
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                account_id = f"{args.id}_bot"
                
                # Add account
                if 'channels' not in config: config['channels'] = {}
                if 'feishu' not in config['channels']: config['channels']['feishu'] = {}
                if 'accounts' not in config['channels']['feishu']: config['channels']['feishu']['accounts'] = {}
                if 'bindings' not in config['channels']['feishu']: config['channels']['feishu']['bindings'] = {}
                
                account_data = {
                    'appId': args.app_id,
                    'appSecret': args.app_secret,
                    'botName': args.name
                }
                
                if args.require_pairing:
                    account_data['dmPolicy'] = "pairing"
                    
                config['channels']['feishu']['accounts'][account_id] = account_data
                
                # Add binding
                config['channels']['feishu']['bindings'][account_id] = args.id
                
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                    
                print(f"✅ Feishu bot bound successfully to {args.id} as {account_id}")
            except Exception as e:
                print(f"❌ Error updating openclaw.json for Feishu: {e}")
