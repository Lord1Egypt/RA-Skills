# Agent 卸载 — 技术实现

## 前置：列出可卸载的 Agent

```bash
SKILL_DIR="/Applications/QClaw.app/Contents/Resources/openclaw/config/skills/qclaw-openclaw"
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents list
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents bindings
```

**禁止卸载 `main` agent**（受保护）。

## 三种卸载模式

| 模式 | 操作 | 适用场景 |
|------|------|----------|
| **仅取消飞书绑定** | 移除 bindings，保留 agent + 工作区 + 账号 | 暂停飞书入口，保留数据 |
| **完全卸载** | 删除 agent + 工作区 + 飞书账号 | 彻底清除 |
| **取消** | 不操作 | 用户反悔 |

## 模式 1：仅取消飞书绑定

通过 `gateway config.patch` 移除 bindings 中该 agent 的条目，保留其余配置不变。

验证：`agents bindings` 确认该 agent 不再出现。

## 模式 2：完全卸载

**步骤 1：删除 agent**

```bash
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents delete {agentId} --force
```

此命令自动：移除 agent 配置、移除 bindings、删除工作区目录。

**步骤 2：删除通道账号配置（必须！）**

⚠️ 若账号配置残留但无 binding，消息会 fallback 到 `defaultAccount` → main agent 响应。

`gateway config.patch` **无法删除 key**（只能合并写入），必须用 Python 直接操作：

```python
import json

path = '/Users/honor/.qclaw/openclaw.json'
with open(path, 'r') as f:
    config = json.load(f)

# 删除指定飞书账号
accounts = config.get('channels', {}).get('feishu', {}).get('accounts', {})
for account_id in ['{feishuAccount}']:  # 列出所有要删除的账号
    if account_id in accounts:
        del accounts[account_id]

with open(path, 'w') as f:
    json.dump(config, f, indent=2)
```

仅当该账号被其他 agent 复用时，才保留账号配置。

**步骤 3：验证**

```bash
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents list
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents bindings
```

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| 尝试删除 main agent | 拒绝，提示保护机制 |
| Agent 不存在 | 列出可用 agent 供用户重新选择 |
| 工作区删除失败 | 检查目录权限，给出手动删除路径 |
| 配置更新失败 | 检查 gateway 状态，回滚到操作前状态 |
