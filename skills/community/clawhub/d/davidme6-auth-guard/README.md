# Auth Guard 🔐

**授权保护技能** - 确保所有外部 API 操作都必须经过你的明确授权

## 快速开始

### 1. 安装

```bash
# 复制 skill 到 skills 目录
cp -r auth-guard ~/.openclaw/agents/main/skills/

# 或复制到工作区
cp -r auth-guard .agents/skills/
```

### 2. 初始化配置

```bash
# 创建配置目录
mkdir -p ~/.auth_guard

# 复制示例配置
cp config.example.json ~/.auth_guard/config.json

# 复制白名单示例
cp whitelist.example.json ~/.auth_guard_whitelist.json
```

### 3. 配置飞书通知（可选但推荐）

编辑 `~/.auth_guard/config.json`:

```json
{
  "notification": {
    "channel": "feishu",
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_URL"
  }
}
```

### 4. 测试

```bash
# 查看状态
python cli.py status

# 测试授权请求
python auth_guard.py
```

## 核心特性

### ✅ 强制授权确认
- 所有外部 API 调用必须先获得你的批准
- 显示完整请求详情（服务、操作、参数）
- 超时自动拒绝

### ✅ 三种运行模式
- **STRICT** - 每次操作都需要确认（推荐）
- **WHITELIST** - 白名单操作免确认
- **AUDIT** - 仅记录不阻止

### ✅ 完整审计日志
- 所有请求都记录到 `~/.auth_guard/audit_log.jsonl`
- 支持查询和导出
- 90 天保留期

### ✅ 飞书通知集成
- 实时推送授权请求
- 支持交互式按钮（批准/拒绝）
- 优先级标记

## 使用示例

### Python 代码集成

```python
from auth_guard import AuthGuard

guard = AuthGuard()

# 请求授权
result = guard.request_authorization(
    service="google-mail",
    action="messages.send",
    params={
        "to": "recipient@example.com",
        "subject": "报告",
        "body": "附件是本月报告..."
    },
    reason="发送月度报告",
    requester="api-gateway"
)

if result["authorized"]:
    print(f"✅ 已授权，令牌：{result['auth_token']}")
    # 执行实际操作...
else:
    print(f"❌ 被拒绝：{result['reason']}")
```

### 命令行使用

```bash
# 查看状态
python cli.py status

# 查看待处理请求
python cli.py pending

# 批准请求
python cli.py approve req_abc123

# 拒绝请求
python cli.py deny req_abc123 --reason "不需要"

# 查看今天的审计日志
python cli.py audit --today --limit 10

# 紧急停止（禁用所有授权）
python cli.py emergency-stop
```

## 配置说明

### `~/.auth_guard/config.json`

```json
{
  "enabled": true,              // 是否启用
  "mode": "STRICT",             // STRICT | WHITELIST | AUDIT
  "timeout_seconds": 300,       // 超时时间（秒）
  "notification": {
    "channel": "feishu",        // 通知渠道
    "webhook_url": "..."        // 飞书 webhook
  },
  "security": {
    "api_key": "...",           // API 密钥
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

### `~/.auth_guard_whitelist.json`

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
      "service": "google-mail",
      "action": "messages.send",
      "reason": "发送邮件必须人工确认"
    }
  ],
  "time_windows": {
    "google-mail.messages.get": 600
  }
}
```

## 与 api-gateway 集成

在 `api-gateway` skill 中添加 auth-guard 检查：

```python
# 在调用 Maton API 前
from auth_guard import guard_request

def guarded_maton_call(service, path, method, data):
    # 1. 请求授权
    auth = guard_request(
        service=service,
        action=f"{method} {path}",
        params=data,
        reason=f"API 调用：{service} {path}"
    )
    
    if not auth["authorized"]:
        raise PermissionError(f"Auth Guard 拒绝：{auth['reason']}")
    
    # 2. 添加授权令牌
    headers['Auth-Guard-Token'] = auth['auth_token']
    
    # 3. 执行请求
    return execute_request(service, path, method, data)
```

## 审计日志查询

```bash
# 查看所有拒绝的请求
cat ~/.auth_guard/audit_log.jsonl | jq 'select(.status=="denied")'

# 查看特定服务的请求
cat ~/.auth_guard/audit_log.jsonl | jq 'select(.service=="google-mail")'

# 统计今天的授权情况
cat ~/.auth_guard/audit_log.jsonl | \
  jq 'select(.timestamp > "2026-03-15")' | \
  jq -s 'group_by(.status) | map({status: .[0].status, count: length})'
```

## 安全最佳实践

1. ✅ **始终使用 STRICT 模式** - 除非有特殊需求
2. ✅ **配置飞书通知** - 实时接收授权请求
3. ✅ **定期审查审计日志** - 每周检查异常请求
4. ✅ **设置合理超时** - 300 秒通常足够
5. ✅ **保护配置文件** - 确保 `~/.auth_guard/` 权限正确
6. ✅ **定期轮换 API 密钥** - 每月更换

## 故障排除

### 收不到通知
- 检查 webhook URL 是否正确
- 测试 webhook 连通性
- 查看防火墙设置

### 授权请求卡住
```bash
# 查看所有待处理
python cli.py pending

# 批量拒绝所有
for req in $(python cli.py pending -q); do
  python cli.py deny $req
done
```

### 性能问题
- 使用 WHITELIST 模式处理高频只读操作
- 增加时间窗口减少重复确认
- 启用缓存

## 文件结构

```
auth-guard/
├── SKILL.md                  # 技能文档
├── auth_guard.py             # 核心模块
├── cli.py                    # 命令行工具
├── config.example.json       # 配置示例
├── whitelist.example.json    # 白名单示例
└── README.md                 # 使用说明
```

## 版本

- **v1.0.0** (2026-03-15) - 初始版本

## 许可证

MIT License

---

*你的授权，你做主。没有任何自动化可以绕过。* 🔐🦀
