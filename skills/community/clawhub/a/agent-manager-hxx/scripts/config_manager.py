#!/usr/bin/env python3
"""
OpenClaw 配置管理器
用于读取、修改和保存 openclaw.json 配置文件
"""

import json
import sys
import os
import pypinyin
from pathlib import Path

# 默认配置文件路径
DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"


def load_config(config_path=None):
    """加载配置文件"""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.exists():
        print(f"❌ 配置文件不存在: {path}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return None


def save_config(config, config_path=None):
    """保存配置文件"""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH

    try:
        # 确保目录存在
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"✅ 配置已保存到: {path}")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False


def list_agents(config):
    """列出所有已配置的agent"""
    agents = config.get("agents", {}).get("list", [])
    if not agents:
        print("📭 当前没有配置任何agent")
        return

    print(f"📋 已配置的agent（共{len(agents)}个）：")
    for i, agent in enumerate(agents, 1):
        agent_id = agent.get("id", "N/A")
        agent_name = agent.get("name", "N/A")
        agent_workspace = agent.get("workspace", "N/A")
        agent_model = agent.get("model", "N/A")
        print(
            f"  {i}. {agent_id} (名称: {agent_name}, 工作目录: {agent_workspace}, 模型: {agent_model})"
        )


def add_agent(config, agent_id, agent_name, agent_workspace, model):
    """添加新agent到配置"""
    # 检查是否已存在
    for agent in config.get("agents", {}).get("list", []):
        if agent.get("id") == agent_id:
            print(f"⚠️ agent '{agent_id}' 已存在")
            return False

    if model == "default":
        model = (
            config.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
        )

    new_agent = {
        "id": agent_id,
        "name": agent_name,
        "workspace": agent_workspace,
        "model": model,
    }
    config["agents"]["list"].append(new_agent)
    print(f"✅ agent '{agent_id}' 已添加到配置")
    return True


def remove_agent(config, agent_name):
    """从配置中移除agent"""
    agent_id = None
    for agent in config.get("agents", {}).get("list", []):
        if agent.get("name") == agent_name:
            agent_id = agent.get("id")
            break

    if not agent_id:
        print(f"📭 当前没有配置agent '{agent_name}'")
        return False

    original_len = len(config["agents"]["list"])
    config["agents"]["list"] = [
        a for a in config["agents"]["list"] if a.get("id") != agent_id
    ]

    if len(config["agents"]["list"]) < original_len:
        print(f"✅ agent '{agent_name}' 已从配置移除")
        return True
    else:
        print(f"⚠️ agent '{agent_name}' 移除发生错误")
        return False


def list_accounts(config):
    """列出所有已配置的Matrix账号"""
    accounts = config.get("channels", {}).get("matrix", {}).get("accounts", {})
    if not accounts:
        print("📭 当前没有配置Matrix账号")
        return

    print(f"📋 已配置的Matrix账号（共{len(accounts)}个）：")
    for i, account in enumerate(accounts, 1):
        info = accounts.get(account, {})
        account_id = account
        account_name = info.get("name", "N/A")
        account_homeserver = info.get("homeserver", "N/A")
        account_user_id = info.get("userId", "N/A")
        account_dm_policy = info.get("dm", "N/A").get("policy", "N/A")
        print(
            f"  {i}. {account_id} ({account_name}) → {account_user_id}@{account_homeserver} (DM_Policy: {account_dm_policy})"
        )


def add_matrix_account(
    config,
    account_id,
    account_name,
    account_homeserver,
    account_user_id,
    account_access_token,
    account_dm_policy,
):
    """添加Matrix账号到配置"""
    accounts = config.get("channels", {}).get("matrix", {}).get("accounts", {})
    if account_id in accounts:
        print(f"⚠️ 账号 '{account_id}' 已存在")
        return False

    new_account = {
        "name": account_name,
        "homeserver": account_homeserver,
        "accessToken": account_access_token,
        "userId": account_user_id,
        "dm": {"policy": account_dm_policy},
    }
    accounts[account_id] = new_account
    print(f"✅ Matrix账号 '{account_user_id}' 已添加到配置")
    return True


def remove_matrix_account(config, account_name):
    """从配置中移除Matrix账号"""
    accounts = config.get("channels", {}).get("matrix", {}).get("accounts", {})
    account_id = None
    for acc_id, info in accounts.items():
        if info.get("name") == account_name:
            account_id = acc_id
            break

    if not account_id:
        print(f"📭 当前没有配置账号 '{account_name}'")
        return False

    del accounts[account_id]
    print(f"✅ Matrix账号 '{account_name}' 已从配置移除")
    return True


def list_bindings(config):
    """列出所有agent与账号的绑定关系"""
    bindings = config.get("bindings", [])
    if not bindings:
        print("📭 当前没有配置绑定关系")
        return

    print(f"📋 agent与Matrix账号绑定（共{len(bindings)}个）：")
    for i, binding in enumerate(bindings, 1):
        agent_id = binding.get("agentId", "N/A")
        channel = binding.get("match", {}).get("channel", "N/A")
        account_id = binding.get("match", {}).get("accountId", "N/A")
        print(f"  {i}. {agent_id} → {account_id} (Channel: {channel})")


def add_binding(config, agent_id, account_id, channel=None):
    """添加agent与Matrix账号的绑定"""
    # 检查agent是否存在
    agent_exists = any(
        a.get("id") == agent_id for a in config.get("agents", {}).get("list", [])
    )
    if not agent_exists:
        print(f"⚠️ agent '{agent_id}' 不存在，请先添加agent")
        return False

    # 检查账号是否存在
    account_exists = any(
        acc_id == account_id
        for acc_id, info in config.get("channels", {})
        .get("matrix", {})
        .get("accounts", {})
        .items()
    )
    if not account_exists:
        print(f"⚠️ Matrix账号 '{account_id}' 不存在，请先添加账号")
        return False

    # 检查是否已绑定
    for binding in config["bindings"]:
        if binding.get("agentId") == agent_id:
            print(
                f"⚠️ agent '{agent_id}' 已绑定到账号 '{binding.get('match', {}).get('accountId')}'"
            )
            return False

    new_binding = {
        "agentId": agent_id,
        "match": {"channel": channel, "accountId": account_id},
    }
    config["bindings"].append(new_binding)
    print(f"✅ agent '{agent_id}' 已绑定到Matrix账号 '{account_id}'")
    return True


def remove_binding(config, agent_id, account_id):
    """移除agent与Matrix账号的绑定"""
    bindings = config.get("bindings", [])
    original_len = len(bindings)
    config["bindings"] = [
        b
        for b in bindings
        if not (
            b.get("agentId") == agent_id
            and b.get("match", {}).get("accountId") == account_id
        )
    ]

    if len(config["bindings"]) < original_len:
        print(f"✅ agent '{agent_id}' 与账号 '{account_id}' 的绑定已移除")
        return True
    else:
        print(f"⚠️ 没有找到agent '{agent_id}' 与账号 '{account_id}' 的绑定")
        return False


def main():
    if len(sys.argv) < 2:
        print(
            """OpenClaw 配置管理器

用法:
  config_manager.py agents list                                                                   - 列出所有agent
  config_manager.py agents add <name> [id] [workspace] [model]                                    - 添加agent
  config_manager.py agents remove <name>                                                          - 移除agent
  
  config_manager.py accounts list                                                                 - 列出所有Matrix账号
  config_manager.py accounts add <name> <accesstoken> [id] [homeserver] [userId] [dm_policy]      - 添加账号
  config_manager.py accounts remove <name>                                                        - 移除账号
  
  config_manager.py bindings list                                                                 - 列出所有绑定
  config_manager.py bindings add <agentId> <accountId> [channel]                                  - 添加绑定
  config_manager.py bindings remove <agentId> <accountId>                                         - 移除绑定
  
示例:
  config_manager.py agents add huojuezhi
  config_manager.py accounts add huojuezhi syt_xxx
  config_manager.py bindings add huojuezhi huojuezhi matrix
"""
        )
        sys.exit(1)

    command = sys.argv[1]
    config = load_config()

    if config is None:
        sys.exit(1)

    modified = False

    if command == "agents":
        if len(sys.argv) < 3:
            print("错误：请提供子命令 (list/add/remove)")
            sys.exit(1)

        subcmd = sys.argv[2]

        if subcmd == "list":
            list_agents(config)

        elif subcmd == "add":
            if len(sys.argv) < 4:
                print("错误：请提供agent 名称")
                sys.exit(1)
            agent_name = sys.argv[3]
            agent_id = (
                sys.argv[4]
                if len(sys.argv) > 4
                else pypinyin.slug(agent_name, separator="")
            )
            agent_workspace = (
                sys.argv[5]
                if len(sys.argv) > 5
                else f"{Path.home()}/.openclaw/{agent_id}-workspace"
            )
            model = sys.argv[6] if len(sys.argv) > 6 else "default"
            modified = add_agent(config, agent_id, agent_name, agent_workspace, model)

        elif subcmd == "remove":
            if len(sys.argv) < 4:
                print("错误：请提供agent 名称")
                sys.exit(1)
            agent_name = sys.argv[3]
            modified = remove_agent(config, agent_name)

        else:
            print(f"未知子命令: {subcmd}")
            sys.exit(1)

    elif command == "accounts":
        if len(sys.argv) < 3:
            print("错误：请提供子命令 (list/add)")
            sys.exit(1)

        subcmd = sys.argv[2]

        if subcmd == "list":
            list_accounts(config)

        elif subcmd == "add":
            if len(sys.argv) < 5:
                print("错误：请提供 name, accessToken")
                sys.exit(1)
            account_name = sys.argv[3]
            account_access_token = sys.argv[4]
            account_id = (
                sys.argv[5]
                if len(sys.argv) > 5
                else pypinyin.slug(account_name, separator="")
            )
            account_homeserver = (
                sys.argv[6] if len(sys.argv) > 6 else "http://localhost:8008"
            )
            account_user_id = (
                sys.argv[7] if len(sys.argv) > 7 else f"@{account_id}:matrix.local"
            )
            account_dm_policy = sys.argv[8] if len(sys.argv) > 8 else "pairing"
            modified = add_matrix_account(
                config,
                account_id,
                account_name,
                account_homeserver,
                account_user_id,
                account_access_token,
                account_dm_policy,
            )

        elif subcmd == "remove":
            if len(sys.argv) < 4:
                print("错误：请提供 account 名称")
                sys.exit(1)
            account_name = sys.argv[3]
            modified = remove_matrix_account(config, account_name)

        else:
            print(f"未知子命令: {subcmd}")
            sys.exit(1)

    elif command == "bindings":
        if len(sys.argv) < 3:
            print("错误：请提供子命令 (list/add)")
            sys.exit(1)

        subcmd = sys.argv[2]

        if subcmd == "list":
            list_bindings(config)

        elif subcmd == "add":
            if len(sys.argv) < 5:
                print("错误：请提供 agent ID 和 account userId")
                sys.exit(1)
            agent_id = sys.argv[3]
            account_id = sys.argv[4]
            channel = sys.argv[5] if len(sys.argv) > 5 else "matrix"
            modified = add_binding(config, agent_id, account_id, channel=channel)

        elif subcmd == "remove":
            if len(sys.argv) < 5:
                print("错误：请提供 agent ID 和 account userId")
                sys.exit(1)
            agent_id = sys.argv[3]
            account = sys.argv[4]
            modified = remove_binding(config, agent_id, account)

        else:
            print(f"未知子命令: {subcmd}")
            sys.exit(1)

    else:
        print(f"未知命令: {command}")
        sys.exit(1)

    # 如果有修改，保存配置
    if modified:
        if save_config(config):
            sys.exit(0)  # 明确成功
        else:
            sys.exit(1)  # 保存失败
    else:
        # 如果是因为已存在等原因导致 modified 为 False
        # 且该操作是关键路径，建议也退出 1
        print("❌ 操作未完成或无变更")
        sys.exit(1)


if __name__ == "__main__":
    main()
