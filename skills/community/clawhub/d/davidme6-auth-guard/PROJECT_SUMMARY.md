# Auth Guard 项目总结

## 项目信息

- **项目名称**: Auth Guard (授权保护技能)
- **版本**: 1.0.0
- **创建日期**: 2026-03-15
- **作者**: your-human
- **许可证**: MIT

## 核心功能

### 1. 强制授权确认
- 所有外部 API 操作必须经过用户明确授权
- 显示完整请求详情（服务、操作、参数）
- 超时自动拒绝（默认 300 秒）

### 2. 三种运行模式
- **STRICT** - 严格模式，每次操作都需要确认（推荐）
- **WHITELIST** - 白名单模式，预批准的操作可直接执行
- **AUDIT** - 审计模式，只记录不阻止

### 3. 完整审计日志
- 所有请求记录到 `~/.auth_guard/audit_log.jsonl`
- 支持查询、过滤、导出
- 90 天保留期

### 4. 飞书通知集成
- 实时推送授权请求
- 交互式按钮（批准/拒绝）
- 优先级标记（普通/高/紧急）

### 5. 白名单/黑名单
- 可配置允许的操作
- 可配置禁止的操作
- 支持时间窗口和速率限制

## 文件结构

```
auth-guard/
├── SKILL.md                  # 技能文档（10.6 KB）
├── README.md                 # 使用说明（5.8 KB）
├── README_GITHUB.md          # GitHub README（1.2 KB）
├── auth_guard.py             # 核心模块（16.5 KB）
├── cli.py                    # 命令行工具（5.9 KB）
├── test.py                   # 测试脚本（1.9 KB）
├── config.example.json       # 配置示例（374 B）
├── whitelist.example.json    # 白名单示例（952 B）
├── clawhub.yaml              # ClawHub 配置（1.5 KB）
├── PUBLISH.md                # 发布指南（1.9 KB）
├── install.sh                # Linux/Mac 安装脚本（1.6 KB）
├── install.ps1               # Windows 安装脚本（1.9 KB）
├── .gitignore                # Git 忽略文件（318 B）
└── _meta.json                # 元数据（387 B）

总计：13 个文件，约 50 KB
```

## 已完成的开发任务

- [x] 核心授权模块 (`auth_guard.py`)
- [x] 命令行工具 (`cli.py`)
- [x] 配置管理
- [x] 审计日志系统
- [x] 飞书通知集成
- [x] 白名单/黑名单系统
- [x] 测试脚本
- [x] 完整文档（SKILL.md, README.md）
- [x] 安装脚本（Windows/Linux/Mac）
- [x] ClawHub 配置文件
- [x] GitHub 仓库初始化
- [x] 发布指南

## 待完成的部署任务

### GitHub 部署

```bash
# 1. 在 GitHub 创建仓库
# 访问 https://github.com/new
# 仓库名：auth-guard-skill
# 描述：Authorization protection skill for OpenClaw
# 可见性：Public

# 2. 添加远程仓库并推送
cd auth-guard
git remote add origin https://github.com/YOUR_USERNAME/auth-guard-skill.git
git branch -M main
git push -u origin main

# 3. 创建 Release
# 访问 https://github.com/YOUR_USERNAME/auth-guard-skill/releases/new
# Tag: v1.0.0
# Title: Auth Guard v1.0.0 - Initial Release
```

### ClawHub 部署

**方式 1: 使用 CLI**
```bash
clawhub login
cd auth-guard
clawhub publish
```

**方式 2: 手动上传**
1. 访问 https://clawhub.com
2. 登录账号
3. 点击 "Publish Skill"
4. 填写信息并上传 clawhub.yaml
5. 提交审核

## 使用方法

### 基础使用

```python
from auth_guard import AuthGuard

guard = AuthGuard()

result = guard.request_authorization(
    service="google-mail",
    action="messages.send",
    params={"to": "test@example.com"},
    reason="发送测试邮件"
)

if result["authorized"]:
    print("已授权")
else:
    print(f"被拒绝：{result['reason']}")
```

### 命令行

```bash
# 查看状态
python cli.py status

# 批准请求
python cli.py approve req_abc123

# 拒绝请求
python cli.py deny req_abc123

# 查看审计日志
python cli.py audit --today --limit 10

# 紧急停止
python cli.py emergency-stop
```

### 安装

**Windows:**
```powershell
.\install.ps1
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

## 配置示例

### `~/.auth_guard/config.json`

```json
{
  "enabled": true,
  "mode": "STRICT",
  "timeout_seconds": 300,
  "notification": {
    "channel": "feishu",
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK"
  },
  "security": {
    "api_key": "CHANGE_ME",
    "allowed_ips": ["127.0.0.1"]
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
  ]
}
```

## 与 api-gateway 集成

在 `api-gateway` skill 中调用 auth-guard：

```python
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
    
    # 2. 执行请求
    return execute_request(service, path, method, data)
```

## 安全特性

1. **零信任架构** - 默认拒绝所有请求
2. **强制确认** - 用户指令是唯一且最优先
3. **完整审计** - 所有操作都有记录
4. **速率限制** - 防止授权请求洪水攻击
5. **紧急停止** - 一键禁用所有授权
6. **令牌管理** - 授权令牌有时效性，可撤销

## 测试状态

- [x] 配置加载测试
- [x] 白名单检查测试
- [x] 黑名单检查测试
- [x] 命令行工具测试
- [x] 审计日志测试
- [ ] 飞书通知测试（需要配置 webhook）
- [ ] 集成测试（需要 api-gateway 配合）

## 下一步行动

### 立即执行

1. **创建 GitHub 仓库** - 上传代码
2. **发布到 ClawHub** - 让其他人可以安装
3. **配置飞书 webhook** - 测试通知功能

### 后续优化

1. **添加 Web UI** - 提供网页界面管理授权
2. **支持更多通知渠道** - Telegram, WhatsApp, Email
3. **批量操作** - 支持批量批准/拒绝
4. **定时授权** - 支持时间段授权（如：工作时间免确认）
5. **多用户支持** - 支持多个用户分别授权

## 重要提醒

⚠️ **安全警告：**
- 不要将 `AUTH_GUARD_ENABLED` 设置为 `false`
- 不要将 `AUTH_GUARD_MODE` 设置为 `AUDIT`（除非仅用于测试）
- 定期审查审计日志
- 保护好配置文件中的 API 密钥
- 定期轮换 API 密钥

## 联系与支持

- **GitHub Issues**: https://github.com/YOUR_USERNAME/auth-guard-skill/issues
- **Email**: your-email@example.com
- **文档**: 参见 SKILL.md 和 README.md

---

*你的授权，你做主。没有任何自动化可以绕过。* 🔐🦀

**创建时间**: 2026-03-15 13:02
**最后更新**: 2026-03-15 13:02
