---
name: auth-guard
description: 授权保护技能 - 所有外部 API 操作必须经过用户明确授权。这是最高优先级的安全层，确保没有任何自动化可以擅自使用你的授权。核心原则：用户指令是唯一且最优先级。
openclaw:
  version: 1.0.0
  author: your-human
  license: MIT
---

# Auth Guard 🔐

**授权保护技能** - 为你的所有 API 授权添加强制确认层

## 核心原则

1. **用户指令是唯一且最优先的** - 没有任何自动化可以绕过
2. **所有外部操作必须明确授权** - 每次操作都需要确认
3. **零信任架构** - 默认拒绝，除非明确允许
4. **完整审计日志** - 所有请求都有记录

## 工作模式

### 模式 1: STRICT (严格模式 - 推荐)
- ✅ 每次 API 调用都需要用户确认
- ✅ 显示完整请求详情（目标、参数、操作类型）
- ✅ 超时自动拒绝
- ✅ 记录所有尝试

### 模式 2: WHITELIST (白名单模式)
- ✅ 预批准的操作类型可以直接执行
- ✅ 敏感操作仍需确认
- ✅ 可设置时间窗口（如：10 分钟内同一操作免确认）

### 模式 3: AUDIT (审计模式)
- ✅ 记录所有操作但不阻止
- ✅ 用于监控和审计
- ⚠️ 不推荐用于生产环境

## 安装配置

### 1. 环境变量

```bash
# 启用授权保护（必须）
AUTH_GUARD_ENABLED=true

# 运行模式：STRICT | WHITELIST | AUDIT
AUTH_GUARD_MODE=STRICT

# 超时时间（秒），超时后自动拒绝
AUTH_GUARD_TIMEOUT=300

# 通知渠道：feishu | telegram | webhook
AUTH_GUARD_NOTIFY=feishu

# Webhook URL（可选，用于推送确认请求）
AUTH_GUARD_WEBHOOK_URL=https://your-webhook.com/auth-guard
```

### 2. 白名单配置（可选）

创建 `~/.auth_guard_whitelist.json`:

```json
{
  "allowed_operations": [
    {
      "service": "google-mail",
      "action": "messages.get",
      "max_per_hour": 100
    }
  ],
  "blocked_operations": [
    {
      "service": "*",
      "action": "messages.send",
      "reason": "发送邮件必须人工确认"
    },
    {
      "service": "slack",
      "action": "chat.postMessage",
      "reason": "发送消息必须人工确认"
    }
  ],
  "time_windows": {
    "google-mail.messages.get": 600
  }
}
```

## 使用方式

### 方式 1: 通过 Python 库

```python
from auth_guard import AuthGuard

guard = AuthGuard()

# 请求授权
response = guard.request_authorization(
    service="google-mail",
    action="messages.send",
    params={
        "to": "recipient@example.com",
        "subject": "Test",
        "body": "Hello"
    },
    reason="发送测试邮件"
)

if response["authorized"]:
    # 执行操作
    send_email(...)
else:
    # 被拒绝
    print(f"拒绝原因：{response['reason']}")
```

### 方式 2: 通过 HTTP API

启动授权服务：
```bash
python -m auth_guard.server --port 8765
```

请求授权：
```bash
curl -X POST http://localhost:8765/authorize \
  -H "Content-Type: application/json" \
  -d '{
    "service": "google-mail",
    "action": "messages.send",
    "params": {...},
    "reason": "发送通知邮件"
  }'
```

### 方式 3: 集成到现有技能

在调用外部 API 前，先通过 auth-guard 检查：

```python
import requests

def guarded_api_call(service, action, params):
    # 1. 请求授权
    auth_response = requests.post('http://localhost:8765/authorize', json={
        'service': service,
        'action': action,
        'params': params,
        'requester': 'api-gateway'
    })
    
    auth_data = auth_response.json()
    
    if not auth_data.get('authorized'):
        raise PermissionError(f"操作被拒绝：{auth_data.get('reason')}")
    
    # 2. 执行实际操作
    result = execute_api(service, action, params)
    
    # 3. 记录审计日志
    requests.post('http://localhost:8765/audit', json={
        'service': service,
        'action': action,
        'result': 'success',
        'auth_token': auth_data['auth_token']
    })
    
    return result
```

## 确认流程

当收到授权请求时，你会看到：

```
🔐 授权请求 #12345
═══════════════════════════════════════
服务：Google Mail
操作：发送邮件
请求者：api-gateway
时间：2026-03-15 12:30:45
───────────────────────────────────────
详情:
  收件人：recipient@example.com
  主题：月度报告
  内容预览：您好，附件是本月报告...
───────────────────────────────────────
风险等级：🟡 中等（外部通信）
───────────────────────────────────────
操作:
  ✅ 批准（本次）
  ✅ 批准并记住（同类操作 1 小时内免确认）
  ❌ 拒绝
  ⏸️ 稍后决定（5 分钟后提醒）
═══════════════════════════════════════
```

## 审计日志

所有授权请求都会记录到 `~/.auth_guard/audit_log.jsonl`:

```jsonl
{"timestamp":"2026-03-15T12:30:45Z","request_id":"req_12345","service":"google-mail","action":"messages.send","requester":"api-gateway","status":"approved","user":"admin","ip":"127.0.0.1"}
{"timestamp":"2026-03-15T12:31:00Z","request_id":"req_12346","service":"slack","action":"chat.postMessage","requester":"auto-bot","status":"denied","reason":"非用户本人请求"}
```

查看日志：
```bash
# 查看所有拒绝的请求
cat ~/.auth_guard/audit_log.jsonl | jq 'select(.status=="denied")'

# 查看今天的授权统计
cat ~/.auth_guard/audit_log.jsonl | jq 'select(.timestamp > "2026-03-15")' | jq -s 'group_by(.status) | map({status: .[0].status, count: length})'
```

## 安全特性

### 1. 请求者验证
- 验证请求来源是否为可信服务
- 支持 IP 白名单
- 支持 API 密钥认证

### 2. 速率限制
- 防止授权请求洪水攻击
- 每个请求者每小时最多 N 次请求

### 3. 会话管理
- 授权令牌有时效性
- 支持撤销已批准的授权

### 4. 紧急停止
- 一键禁用所有授权
- 一键撤销所有待处理请求

## 配置文件

### `~/.auth_guard/config.json`

```json
{
  "enabled": true,
  "mode": "STRICT",
  "timeout_seconds": 300,
  "notification": {
    "channel": "feishu",
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  },
  "security": {
    "api_key": "your-secure-api-key",
    "allowed_ips": ["127.0.0.1"],
    "rate_limit": {
      "requests_per_hour": 100
    }
  },
  "audit": {
    "log_path": "~/.auth_guard/audit_log.jsonl",
    "retention_days": 90
  }
}
```

## API 参考

### 授权请求

**POST** `/authorize`

请求体：
```json
{
  "service": "服务名称",
  "action": "操作类型",
  "params": {"参数": "值"},
  "reason": "请求原因",
  "requester": "请求者标识",
  "priority": "normal|high|urgent"
}
```

响应：
```json
{
  "authorized": true,
  "auth_token": "xxx",
  "expires_at": "2026-03-15T13:00:00Z",
  "conditions": ["single_use"]
}
```

### 撤销授权

**POST** `/revoke`

```json
{
  "auth_token": "xxx"
}
```

### 查看待处理请求

**GET** `/pending`

响应：
```json
{
  "pending_requests": [
    {
      "request_id": "req_12345",
      "service": "google-mail",
      "action": "messages.send",
      "requested_at": "2026-03-15T12:30:45Z"
    }
  ]
}
```

### 批量批准/拒绝

**POST** `/batch-decide`

```json
{
  "request_ids": ["req_12345", "req_12346"],
  "decision": "approve|deny"
}
```

## 与其他技能集成

### 与 api-gateway 集成

修改 api-gateway 调用流程：

```python
# 在 api-gateway 中拦截所有请求
def gateway_request(service, path, method, data):
    # 1. 通过 auth-guard 检查
    auth = auth_guard.request(
        service=service,
        action=path,
        params=data,
        reason=f"API 调用：{method} {path}"
    )
    
    if not auth['authorized']:
        raise AuthGuardError(f"被 auth-guard 拒绝：{auth['reason']}")
    
    # 2. 添加授权令牌到请求头
    headers['Authorization'] = f"Bearer {maton_key}"
    headers['Auth-Guard-Token'] = auth['auth_token']
    
    # 3. 执行请求
    return execute_request(service, path, method, data)
```

### 与 skill-vetter 集成

在安装新技能时自动检查是否需要 auth-guard：

```python
# skill-vetter 检查清单中添加：
- [ ] 是否需要 auth-guard 保护？
- [ ] 是否已配置白名单？
- [ ] 审计日志是否启用？
```

## 最佳实践

1. ✅ **始终启用 STRICT 模式** - 除非有特殊需求
2. ✅ **定期审查审计日志** - 每周检查拒绝的请求
3. ✅ **设置合理的超时** - 300 秒（5 分钟）通常足够
4. ✅ **启用通知** - 所有请求都推送到飞书/微信
5. ✅ **定期轮换 API 密钥** - 每月更换一次
6. ✅ **备份配置** - 定期备份白名单和配置

## 故障排除

### 问题：收不到确认请求

检查：
1. 通知渠道配置是否正确
2. Webhook URL 是否可达
3. 防火墙是否阻止

### 问题：授权请求被卡住

解决：
```bash
# 查看所有待处理请求
curl http://localhost:8765/pending

# 批量拒绝所有待处理
curl -X POST http://localhost:8765/batch-decide \
  -H "Content-Type: application/json" \
  -d '{"request_ids": ["all"], "decision": "deny"}'
```

### 问题：性能影响

优化：
1. 使用 WHITELIST 模式处理高频只读操作
2. 设置时间窗口减少重复确认
3. 启用缓存（相同参数 5 分钟内免确认）

## 命令行工具

```bash
# 查看状态
auth-guard status

# 查看待处理请求
auth-guard pending

# 批准请求
auth-guard approve req_12345

# 拒绝请求
auth-guard deny req_12345

# 查看审计日志
auth-guard audit --today

# 紧急停止所有授权
auth-guard emergency-stop

# 导出审计报告
auth-guard report --format pdf --output report.pdf
```

## 安全警告

⚠️ **重要：**
- 不要将 `AUTH_GUARD_ENABLED` 设置为 `false`
- 不要将 `AUTH_GUARD_MODE` 设置为 `AUDIT`（除非仅用于测试）
- 定期审查 `~/.auth_guard/audit_log.jsonl`
- 保护好 `~/.auth_guard/config.json` 中的 API 密钥

---

## 版本历史

- **v1.0.0** (2026-03-15) - 初始版本
  - 核心授权保护功能
  - 三种运行模式
  - 完整审计日志
  - 飞书通知集成

---

*你的授权，你做主。没有任何自动化可以绕过。* 🔐🦀
