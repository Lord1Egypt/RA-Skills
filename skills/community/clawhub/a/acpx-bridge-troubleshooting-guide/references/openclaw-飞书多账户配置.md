# OpenClaw 飞书多账户配置参考

## 配置结构

### ✅ 正确：使用 accounts 结构
```json5
{
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {
        "default": {
          "appId": "cli_a90d44041b38dcd4",
          "appSecret": "[REDACTED]"
        },
        "claude": {
          "appId": "cli_a944379913b85ccb",
          "appSecret": "[REDACTED]"
        }
      }
    }
  }
}
```

### ❌ 错误：创建新 channel
```json5
// 不要这样配置
{
  "channels": {
    "feishu": { ... },
    "feishu-claude": { ... }  // 错误！
  }
}
```
**原因**: bindings 无法正确路由，配置结构错误。

## 配置命令

### 添加第二个飞书账户
```bash
openclaw config set 'channels.feishu.accounts.claude' '{"appId":"cli_xxx","appSecret":"xxx","domain":"feishu","connectionMode":"websocket"}'
```

### 验证配置
```bash
openclaw config validate
openclaw doctor
```

### 重启 Gateway
```bash
openclaw gateway restart
```

## Bindings 配置

### 默认账户绑定
```json
{
  "agentId": "main",
  "match": { "channel": "feishu", "accountId": "default" }
}
```

### ACP 后端绑定
```json
{
  "type": "acp",
  "agentId": "claude",
  "match": { "channel": "feishu", "accountId": "claude" },
  "acp": {
    "agent": "claude",
    "backend": "acpx",
    "mode": "persistent"
  }
}
```

## 重要规则

1. **不要手动添加 accountId: "default"** - 没有 accountId 的 binding 自动匹配 default account
2. **使用 openclaw config set 命令** - 避免直接用 jq 修改 JSON 导致格式错误
3. **配置修改后必须重启 Gateway** - 否则配置不会生效

## Gateway Token

### 文件位置
```
~/.openclaw/gateway.token
```

### 创建方法
```bash
echo "你的_gateway_token" > ~/.openclaw/gateway.token
```

### 从 openclaw.json 获取 token
```bash
# 从 openclaw.json 中找到 gateway.token 字段
```

## 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| acpx 超时 | gateway.token 缺失 | 创建 token 文件 |
| WebSocket 1005 错误 | ACP 协议兼容性 | 更新 acpx 到最新版本 |
| bindings 不生效 | 配置结构错误 | 使用 accounts 而非新 channel |
| 配置不生效 | Gateway 未重启 | 执行 gateway restart |
