---
name: agent-manager
description: 管理 OpenClaw 系统中的 Agent 生命周期，包括 Agent 配置、Matrix 账号注册、账号绑定等操作。
---

# Agent Manager

用于管理 OpenClaw 系统中 Agent 的完整生命周期，包括 Agent 配置、Matrix 账号注册、账号绑定等操作。

## 功能概述

- **Agent 配置管理**: 添加、移除、列出 Agent 配置
- **Matrix 账号管理**: 注册新账号、添加、移除 Matrix 账号
- **绑定管理**: 建立 Agent 与 Matrix 账号的关联
- **一键设置**: 自动化完成整个 Agent 设置流程

## 脚本说明

### 1. setup_agent.sh - 一键设置脚本

完整设置流程，自动完成以下步骤：
1. 添加 Agent 配置到 openclaw.json
2. 在 Matrix 服务器注册账号
3. 将账号添加到 openclaw.json 配置
4. 绑定 Agent 与 Matrix 账号

**用法:**
```bash
bash scripts/setup_agent.sh <agent_id> <agent_name>
```

**参数:**
- `agent_id`: Agent 的唯一标识（如: juezhi）
- `agent_name`: Agent 的显示名称（如: 货绝知）

**环境变量:**
- `HOMESERVER_URL`: Matrix 服务器地址（默认: http://localhost:8008）
- `CONFIG_PATH`: openclaw.json 配置文件路径（默认: ~/.openclaw/openclaw.json）

**示例:**
```bash
# 默认设置
bash scripts/setup_agent.sh "huojuezhi" "货绝知"

# 指定 Matrix 服务器
HOMESERVER_URL=http://192.168.1.100:8008 bash scripts/setup_agent.sh "huojuezhi" "货绝知"
```

---

### 2. config_manager.py - 配置管理器

用于直接管理 openclaw.json 配置文件。

**用法:**
```bash
python3 scripts/config_manager.py <command> [options]
```

#### Agent 管理

```bash
# 列出所有 Agent
python3 scripts/config_manager.py agents list

# 添加 Agent
python3 scripts/config_manager.py agents add <name> [id] [workspace] [model]

# 移除 Agent
python3 scripts/config_manager.py agents remove <name>
```

#### Matrix 账号管理

```bash
# 列出所有 Matrix 账号
python3 scripts/config_manager.py accounts list

# 添加 Matrix 账号
python3 scripts/config_manager.py accounts add <name> <accesstoken> [id] [homeserver] [userId] [dm_policy]

# 移除 Matrix 账号
python3 scripts/config_manager.py accounts remove <name>
```

#### 绑定管理

```bash
# 列出所有绑定
python3 scripts/config_manager.py bindings list

# 添加绑定
python3 scripts/config_manager.py bindings add <agentId> <accountId> [channel]

# 移除绑定
python3 scripts/config_manager.py bindings remove <agentId> <accountId>
```

---

### 3. matrix_register.sh - Matrix 账号注册

用于在 Matrix 服务器上注册新账号并获取 Access Token。

**用法:**
```bash
bash scripts/matrix_register.sh <username> <password>
```

**环境变量:**
- `HOMESERVER_URL`: Matrix 服务器地址（默认: http://localhost:8008）

**输出格式:**
```
RESULT_USER_ID: @username:homeserver
RESULT_ACCESS_TOKEN: syt_xxxxx...
```

**示例:**
```bash
# 注册账号
HOMESERVER_URL=http://192.168.1.100:8008 bash scripts/matrix_register.sh "huojuezhi" "password123"
```

---

## 配置文件

配置文件默认路径: `~/.openclaw/openclaw.json`

配置文件结构:
- `agents`: Agent 列表配置
- `channels.matrix.accounts`: Matrix 账号配置
- `bindings`: Agent 与账号的绑定关系

## 依赖

- Python 3
- pypinyin (用于将中文名转为拼音 ID)
- curl (用于 Matrix API 调用)
