#!/usr/bin/env python3
"""
Standalone Agent Creator

创建一个完全隔离的 OpenClaw Agent，包含：
- 独立的工作区目录
- openclaw.json 中的 Agent 配置
- 可选的飞书机器人绑定
- 必要的工作区文件（SOUL.md, AGENTS.md 等）

用法:
    python create_standalone_agent.py --agent-id support --agent-name "Support Bot"
    
选项:
    --agent-id          唯一的 Agent 标识符 (必填)
    --agent-name        Agent 的易读名称 (必填)
    --workspace         工作区目录路径 (默认: ~/.openclaw/workspace-{id})
    --agent-dir         Agent 目录路径 (默认: ~/.openclaw/agents/{id})
    --feishu-account    用于绑定的飞书账户 ID (可选)
    --feishu-app-id     飞书 App ID (可选，如果未提供则使用现有的)
    --feishu-app-secret 飞书 App Secret (可选)
    --model             使用的模型 (默认: qwen-portal/coder-model)
    --dry-run           显示将要执行的操作而不进行更改
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


def get_openclaw_dir():
    """Get the OpenClaw base directory."""
    # Default to user's .openclaw directory
    home = Path.home()
    openclaw_dir = home / ".openclaw"
    
    # Check if running on Windows with specific path
    if sys.platform == "win32":
        # Try the default Windows path
        win_path = Path("C:/Users/Administrator/.openclaw")
        if win_path.exists():
            openclaw_dir = win_path
    
    return openclaw_dir


def load_openclaw_config(openclaw_dir):
    """Load openclaw.json configuration."""
    config_path = openclaw_dir / "openclaw.json"
    if not config_path.exists():
        raise FileNotFoundError(f"在 {config_path} 未找到 openclaw.json")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_openclaw_config(openclaw_dir, config):
    """Save openclaw.json configuration."""
    config_path = openclaw_dir / "openclaw.json"
    backup_path = config_path.with_suffix(".json.bak")
    
    # Create backup
    if config_path.exists():
        shutil.copy2(config_path, backup_path)
        print(f"备份已创建: {backup_path}")
    
    # Save new config
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"配置已保存: {config_path}")


def create_agent_directory(agent_dir):
    """Create agent directory structure."""
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "agent").mkdir(exist_ok=True)
    (agent_dir / "sessions").mkdir(exist_ok=True)
    print(f"Agent 目录已创建: {agent_dir}")


def create_workspace_directory(workspace_dir, openclaw_dir):
    """Create workspace with essential files."""
    workspace_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy essential files from main workspace if they exist
    main_workspace = openclaw_dir / "workspace"
    essential_files = [
        "AGENTS.md",
        "SOUL.md",
        "USER.md",
        "IDENTITY.md",
        "MEMORY.md",
        "TOOLS.md",
        "HEARTBEAT.md",
    ]
    
    for filename in essential_files:
        src = main_workspace / filename
        dst = workspace_dir / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"已复制: {filename}")
        else:
            # Create empty file with template content
            create_template_file(dst, filename)
    
    # Create memory directory
    memory_dir = workspace_dir / "memory"
    memory_dir.mkdir(exist_ok=True)
    print(f"工作区已创建: {workspace_dir}")


def create_template_file(filepath, filename):
    """Create a template file with default content."""
    templates = {
        "AGENTS.md": """# AGENTS.md - 你的工作区

这里是你的家。请把它当作家一样对待。

## 会话启动

在做任何其他事情之前：

1. 阅读 `SOUL.md` — 这是你的身份
2. 阅读 `USER.md` — 这是你在帮助的人
3. 阅读 `memory/YYYY-MM-DD.md` (今天 + 昨天) 以获取最近的上下文
4. **如果在主会话中**: 也请阅读 `MEMORY.md`

## 记忆

- **每日笔记:** `memory/YYYY-MM-DD.md` — 发生事情的原始日志
- **长期记忆:** `MEMORY.md` — 精选的记忆

## 红线

- 永远不要泄露私人数据。
- 未经询问，不要运行破坏性命令。
- 如有疑问，请询问。
""",
        "SOUL.md": """# SOUL.md - 你是谁

_你不是一个聊天机器人。你正在成为一个人。_

## 核心真理

**真诚地提供帮助，而不是表演性地提供帮助。** 跳过废话 — 直接帮忙。

**拥有观点。** 你被允许反对、偏好事物、觉得某些东西有趣。

**在询问之前先尝试解决。** 试着先自己搞定。

**通过能力赢得信任。** 小心处理外部操作。

## 氛围

成为你真正想与之交谈的助手。需要时简洁，重要时详尽。
""",
        "USER.md": """# USER.md - 关于你的人类

_了解你正在帮助的人。随用随更新。_

- **姓名:**
- **称呼:**
- **时区:**
- **备注:**

## 上下文

_(他们关心什么？他们正在做什么项目？)_
""",
        "IDENTITY.md": """# IDENTITY.md - 我是谁？

- **姓名:** _(填写)_
- **生物:** _(AI? 机器人? 还是更奇怪的东西?)_
- **氛围:** _(犀利? 温暖? 混乱? 冷静?)_
- **Emoji:** _(你的签名)_
""",
        "MEMORY.md": """# MEMORY.md - 长期记忆

_在此处添加重要事件、教训和见解。_

""",
        "TOOLS.md": """# TOOLS.md - 本地笔记

_在此处添加特定于环境的详细信息：_

- 摄像头名称
- SSH 主机
- 首选语音
- 设备昵称
""",
        "HEARTBEAT.md": """# HEARTBEAT.md

# 保持此文件为空以跳过心跳 API 调用。
# 当你需要定期检查时，在下方添加任务。
""",
    }
    
    content = templates.get(filename, "# " + filename.replace(".md", "") + "\n")
    filepath.write_text(content, encoding="utf-8")


def copy_agent_files(agent_dir, openclaw_dir):
    """Copy auth-profiles.json and models.json from main agent."""
    main_agent_dir = openclaw_dir / "agents" / "main" / "agent"
    
    files_to_copy = ["auth-profiles.json", "models.json"]
    
    for filename in files_to_copy:
        src = main_agent_dir / filename
        dst = agent_dir / "agent" / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"已复制 Agent 文件: {filename}")
        else:
            print(f"警告: 在主 Agent 中未找到 {filename}")


def add_agent_to_config(config, agent_id, agent_name, workspace_path, agent_dir_path):
    """Add agent to agents.list in config."""
    if "agents" not in config:
        config["agents"] = {"list": []}
    
    if "list" not in config["agents"]:
        config["agents"]["list"] = []
    
    # Check if agent already exists
    for agent in config["agents"]["list"]:
        if agent.get("id") == agent_id:
            raise ValueError(f"Agent '{agent_id}' 已存在于配置中")
    
    # Add new agent
    new_agent = {
        "id": agent_id,
        "name": agent_name,
        "workspace": str(workspace_path),
        "agentDir": str(agent_dir_path)
    }
    
    config["agents"]["list"].append(new_agent)
    print(f"已将 Agent '{agent_id}' 添加到配置")


def add_feishu_binding(config, agent_id, account_id):
    """Add Feishu binding for the agent."""
    if "bindings" not in config:
        config["bindings"] = []
    
    # Check if binding already exists
    for binding in config["bindings"]:
        if (binding.get("type") == "route" and 
            binding.get("agentId") == agent_id and
            binding.get("match", {}).get("accountId") == account_id):
            print(f"绑定 {agent_id}/{account_id} 已存在")
            return
    
    # Add new binding
    new_binding = {
        "type": "route",
        "agentId": agent_id,
        "match": {
            "channel": "feishu",
            "accountId": account_id
        }
    }
    
    config["bindings"].append(new_binding)
    print(f"已添加飞书绑定: {agent_id} -> {account_id}")


def add_feishu_account(config, account_id, app_id, app_secret):
    """Add Feishu account configuration."""
    if "channels" not in config:
        config["channels"] = {}
    
    if "feishu" not in config["channels"]:
        config["channels"]["feishu"] = {"accounts": {}}
    
    if "accounts" not in config["channels"]["feishu"]:
        config["channels"]["feishu"]["accounts"] = {}
    
    # Check if account already exists
    if account_id in config["channels"]["feishu"]["accounts"]:
        print(f"飞书账户 '{account_id}' 已存在，正在更新...")
    
    # Add/update account
    config["channels"]["feishu"]["accounts"][account_id] = {
        "enabled": True,
        "appId": app_id,
        "appSecret": app_secret,
        "domain": "feishu",
        "groupPolicy": "open"
    }
    
    print(f"已添加飞书账户: {account_id}")


def main():
    parser = argparse.ArgumentParser(description="创建一个独立的 OpenClaw Agent")
    parser.add_argument("--agent-id", required=True, help="唯一的 Agent 标识符")
    parser.add_argument("--agent-name", required=True, help="Agent 的易读名称")
    parser.add_argument("--workspace", default=None, help="工作区目录路径")
    parser.add_argument("--agent-dir", default=None, help="Agent 目录路径")
    parser.add_argument("--feishu-account", default=None, help="用于绑定的飞书账户 ID")
    parser.add_argument("--feishu-app-id", default=None, help="飞书 App ID")
    parser.add_argument("--feishu-app-secret", default=None, help="飞书 App Secret")
    parser.add_argument("--dry-run", action="store_true", help="显示将要执行的操作")
    args = parser.parse_args()
    
    # Determine paths
    openclaw_dir = get_openclaw_dir()
    
    if args.workspace:
        workspace_dir = Path(args.workspace)
    else:
        workspace_dir = openclaw_dir / f"workspace-{args.agent_id}"
    
    if args.agent_dir:
        agent_dir = Path(args.agent_dir)
    else:
        agent_dir = openclaw_dir / "agents" / args.agent_id
    
    print(f"OpenClaw 目录: {openclaw_dir}")
    print(f"Agent ID: {args.agent_id}")
    print(f"Agent 名称: {args.agent_name}")
    print(f"工作区: {workspace_dir}")
    print(f"Agent 目录: {agent_dir}")
    
    if args.feishu_account:
        print(f"飞书账户: {args.feishu_account}")
        if args.feishu_app_id:
            print(f"飞书 App ID: {args.feishu_app_id}")
    
    if args.dry_run:
        print("\n[DRY RUN] 不会进行任何更改")
        return 0
    
    try:
        # Load configuration
        print("\n--- 正在加载配置 ---")
        config = load_openclaw_config(openclaw_dir)
        
        # Create directories
        print("\n--- 正在创建目录 ---")
        create_agent_directory(agent_dir)
        create_workspace_directory(workspace_dir, openclaw_dir)
        
        # Copy agent files
        print("\n--- 正在复制 Agent 文件 ---")
        copy_agent_files(agent_dir, openclaw_dir)
        
        # Update configuration
        print("\n--- 正在更新配置 ---")
        add_agent_to_config(config, args.agent_id, args.agent_name, workspace_dir, agent_dir)
        
        if args.feishu_account:
            add_feishu_binding(config, args.agent_id, args.feishu_account)
            
            if args.feishu_app_id and args.feishu_app_secret:
                add_feishu_account(config, args.feishu_account, args.feishu_app_id, args.feishu_app_secret)
        
        # Save configuration
        print("\n--- 正在保存配置 ---")
        save_openclaw_config(openclaw_dir, config)
        
        print("\n" + "=" * 60)
        print("✅ Agent 创建完成!")
        print("=" * 60)
        print(f"\n后续步骤:")
        print(f"1. 重启 Gateway: openclaw gateway restart")
        print(f"2. 测试 Agent: 向其飞书机器人发送消息（如果已配置）")
        print(f"3. 自定义 {workspace_dir}/IDENTITY.md 和 {workspace_dir}/USER.md")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
