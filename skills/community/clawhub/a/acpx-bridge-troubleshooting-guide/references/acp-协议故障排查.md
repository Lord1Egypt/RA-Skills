# ACP 协议故障排查参考

## 常见错误代码

### WebSocket 错误

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 1005 | 连接断开（无状态码） | 检查 Gateway 日志，重启 Gateway |
| 1006 | 异常关闭 | 检查网络配置和防火墙 |

### JSON-RPC 错误

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| -32601 | 方法未找到 | 检查 ACP 命令是否正确 |
| -32602 | 无效参数 | 检查参数格式 |

## 排查步骤

### 1. 检查 Gateway 状态
```bash
openclaw gateway status
openclaw gateway logs
```

### 2. 测试 ACP 连接
```bash
# 直接测试（绕过 acpx）
openclaw acp client

# 通过 acpx 测试
acpx openclaw exec 'status'
```

### 3. 检查日志输出

**问题**: Gateway 的 ACP 后端将日志行和 JSON-RPC 消息混在同一个 WebSocket 流中发送

**影响**: acpx 期望纯 JSON，导致解析失败超时

**解决方案**:
- 方案 A: 暂时放弃 acpx 桥接，继续用 echo agent
- 方案 B: 修改 Gateway 源码，日志输出到 stderr
- 方案 C: acpx 配置中添加日志过滤

### 4. 验证配置
```bash
openclaw doctor
openclaw config validate
```

## 已知问题

### acpx 0.3.0 问题
- ACP 协议错误处理不完善
- 日志解析可能失败

### acpx 0.4.0 修复
- 修复 -32601/-32602 错误处理
- 修复中断会话处理

## 推荐方案

### 方案优先级

1. **首选**: 直接使用 `openclaw acp client`（官方推荐）
2. **次选**: 修复 acpx 配置后使用
3. **备选**: 通过 `sessions_spawn(runtime="acp")` 内部调用

### 架构选择

| 需求 | 推荐方案 |
|------|----------|
| 飞书 → OpenClaw 主 agent | openclaw acp |
| 飞书 → Claude Code | ACP 后端绑定 |
| 多 agent 路由 | acpx（谨慎使用） |

## 环境检查清单

- [ ] ~/.openclaw/gateway.token 文件存在
- [ ] ~/.acpx/config.json 配置正确
- [ ] acpx 版本为最新 (0.4.0+)
- [ ] Gateway 服务正在运行
- [ ] 端口 18789 可访问
- [ ] 配置修改后已重启 Gateway
