# Auth Guard Skill for OpenClaw

🔐 **授权保护技能** - 确保所有外部 API 操作都必须经过你的明确授权

## 核心特性

- ✅ **强制授权确认** - 所有外部 API 调用必须先获得你的批准
- ✅ **三种运行模式** - STRICT（严格）/ WHITELIST（白名单）/ AUDIT（审计）
- ✅ **完整审计日志** - 所有请求都记录，支持查询和导出
- ✅ **飞书通知集成** - 实时推送授权请求，支持交互式按钮
- ✅ **零信任架构** - 默认拒绝，除非明确允许

## 快速开始

### 安装

```bash
# 通过 clawhub 安装
clawhub install auth-guard

# 或手动安装
git clone https://github.com/your-username/auth-guard-skill.git
cp -r auth-guard-skill ~/.openclaw/agents/main/skills/auth-guard
```

### 配置

```bash
# 初始化配置
mkdir -p ~/.auth_guard
cp config.example.json ~/.auth_guard/config.json
cp whitelist.example.json ~/.auth_guard_whitelist.json
```

### 使用

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
    print("✅ 已授权")
else:
    print(f"❌ 被拒绝：{result['reason']}")
```

## 文档

完整文档请参阅 [SKILL.md](SKILL.md) 或 [README.md](README.md)

## 安全警告

⚠️ **重要：**
- 不要禁用 Auth Guard（除非测试）
- 定期审查审计日志
- 保护好配置文件中的 API 密钥

## 版本

- **v1.0.0** (2026-03-15) - 初始版本

## 许可证

MIT License

---

*你的授权，你做主。没有任何自动化可以绕过。* 🔐🦀
