# OpenClaw 配置参考

本文档列出 OpenClaw 配置文件 (~/.openclaw/openclaw.json) 的常见配置项。

## 基础配置

### gateway

Gateway 服务配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| bind | string | 127.0.0.1 | 绑定地址 |
| port | number | 3000 | 监听端口 |
| remote.url | string | - | 远程网关URL |
| remote.bind | string | - | 远程绑定配置 |

示例：
```json
{
  "gateway": {
    "bind": "127.0.0.1",
    "port": 3000
  }
}
```

### sessions

会话管理配置：

```json
{
  "sessions": {
    "heartbeat": {
      "enabled": true,
      "interval_minutes": 15
    },
    "memory": {
      "enabled": true,
      "auto_summary": true
    }
  }
}
```

### models

模型配置：

```json
{
  "models": {
    "default": "gpt-4",
    "fallback_enabled": true,
    "max_context_tokens": 128000
  }
}
```

### plugins

插件配置：

```json
{
  "plugins": {
    "entries": {
      "webchat": {
        "enabled": true
      },
      "discord": {
        "enabled": false
      }
    }
  }
}
```

### security

安全配置：

```json
{
  "security": {
    "exec_approvals": "on-miss",
    "sandbox_enabled": true
  }
}
```

exec_approvals 可选值：
- `full`: 无需审批
- `allowlist`: 白名单模式
- `on-miss`: 未匹配时审批
- `always`: 始终审批

## 配置检查清单

- [ ] Gateway 绑定到 localhost (安全性)
- [ ] Heartbeat 已启用 (定时任务)
- [ ] Memory 已启用 (上下文记忆)
- [ ] 至少一个消息通道插件
- [ ] Exec审批模式非 full (安全性)
- [ ] 配置了模型fallback
