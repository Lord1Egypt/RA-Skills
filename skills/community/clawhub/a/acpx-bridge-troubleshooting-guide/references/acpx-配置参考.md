# acpx 配置参考文档

## 官方文档
- **acpx 文档**: https://docs.openclaw.ai/cli/acp
- **GitHub**: https://github.com/openclaw/openclaw

## 配置文件位置
```
~/.acpx/config.json
```

## 正确配置示例
```json
{
  "defaultAgent": "openclaw",
  "timeout": 900,
  "agents": {
    "openclaw": {
      "command": "openclaw",
      "args": ["acp", "client"]
    },
    "claude": {
      "command": "claude"
    }
  }
}
```

## 常见配置错误

### ❌ 错误：添加 --url 和 --token-file 参数
```json
// 不要这样配置
{
  "args": ["acp", "client", "--url", "ws://127.0.0.1:18789", "--token-file", "..."]
}
```
**原因**: `openclaw acp client` 会自动从 OpenClaw 配置读取 URL 和 token，额外参数会导致冲突。

### ✅ 正确：只配置 command 和 args
```json
{
  "args": ["acp", "client"]
}
```

## 版本信息

| 版本 | 发布日期 | 关键修复 |
|------|----------|----------|
| 0.3.0 | 2026-03-12 | 基础版本 |
| 0.4.0 | 2026-03-29 | 修复 -32601/-32602 ACP 协议错误处理 |

## 更新命令
```bash
npm install -g acpx@latest
acpx --version
```

## ACP 与 acpx 的区别

| 特性 | openclaw acp | acpx |
|------|--------------|------|
| 类型 | OpenClaw 内置命令 | 独立 npm 包 |
| 推荐度 | ⭐⭐⭐⭐⭐ (官方推荐) | ⭐⭐ (第三方工具) |
| 配置复杂度 | 低 | 中 |
| 适用场景 | 直接 ACP 桥接 | 多 agent 路由 |

## 测试命令
```bash
# 测试 ACP 连接
openclaw acp client

# 测试 acpx 连接
acpx openclaw exec 'status'

# 检查 Gateway 状态
openclaw gateway status
```
