# Agent 创建 — 技术实现

## 前置：读取当前配置

```bash
SKILL_DIR="/Applications/QClaw.app/Contents/Resources/openclaw/config/skills/qclaw-openclaw"
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents list
bash "$SKILL_DIR/scripts/openclaw-mac.sh" models list
bash "$SKILL_DIR/scripts/openclaw-mac.sh" config get channels  # 了解已有通道和账号
```

## 步骤 1：添加通道账号（仅新账号需要，可选）

通道绑定是**可选的**。若不绑定，agent 仅有独立工作区，可通过 sessions_spawn 等方式调用。

### 飞书（新账号）

使用 `gateway config.patch` 写入，**禁止直接编辑 openclaw.json**：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "{feishuAccount}": {
          "appId": "{appId}",
          "appSecret": "{appSecret}"
        }
      }
    }
  }
}
```

### 其他通道

参考已有通道配置结构，用同样方式 patch。

## 步骤 2：创建 Agent

### 带通道绑定

```bash
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents add {agentId} \
  --workspace ~/.openclaw/workspace-{agentId} \
  --model {model} \
  --bind {channel}:{accountId} \
  --non-interactive
```

### 不绑定通道（纯工作区）

```bash
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents add {agentId} \
  --workspace ~/.openclaw/workspace-{agentId} \
  --model {model} \
  --non-interactive
```

- workspace 会自动创建，无需预先 mkdir
- `--bind` 格式：`channel:accountId`，如 `feishu:bot_test`、`wechat-access:user123`
- 通道账号必须在此步骤前已存在于配置中

## 步骤 2.5：首次启用飞书通道（仅第一次配置飞书时需要）

飞书账号写入后，通道不会自动激活，需要运行 doctor --fix：

```bash
bash "$SKILL_DIR/scripts/openclaw-mac.sh" doctor --fix
```

doctor 会输出 `feishu configured, enabled automatically.` 并写入配置。
等待 2 秒让 gateway 热加载后再执行 agents add。

> 判断是否需要此步骤：若 `agents add --bind feishu:xxx` 报 `Unknown channel "feishu"`，则需要执行。

## 步骤 3：验证

```bash
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents list
bash "$SKILL_DIR/scripts/openclaw-mac.sh" agents bindings
```

## 工作区命名规范

- 路径：`~/.openclaw/workspace-{agentId}`
- 与主 agent 的 `~/.qclaw/workspace` 同级
- agentId 只用小写字母、数字、连字符

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| Agent ID 已存在 | 提示用户换名称 |
| 工作区目录已存在 | 询问是否覆盖或换名称 |
| 通道账号无效 | 检查账号配置是否正确写入 |
| 模型不存在 | 从 `models list` 结果中重新选择 |
| 配置写入失败 | 检查 gateway 状态，用 `health` 命令诊断 |
