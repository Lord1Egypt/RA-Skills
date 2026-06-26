# API Security Scanner 🔒

> OpenClaw Skill — REST API 安全扫描工具

## 功能

对 REST API 端点进行自动化安全审计，覆盖 **OWASP API Security Top 10**：

- 🔐 **认证与会话** — 密码安全、Token安全、OAuth/SSO
- 🛡️ **授权与访问控制** — IDOR检测、越权防护、CORS配置
- 💉 **输入验证与注入** — SQL/NoSQL/命令注入、SSRF、文件上传
- 🔒 **数据保护与隐私** — PII保护、传输加密、静态加密
- ⏱️ **速率限制与防DoS** — 限流策略、慢查询防护
- ⚙️ **配置与基础设施** — 调试模式、日志审计、依赖安全

## 4种使用模式

| 模式 | 用途 | 耗时 |
|------|------|------|
| Full Scan | 完整扫描多个端点 | ~5min |
| Quick Check | 快速检查单个端点 | ~1min |
| Config Audit | 审查API网关/框架配置 | ~3min |
| Report Generation | 生成结构化安全报告 | ~2min |

## 安装

```bash
clawhub install CainGao/api-security-scanner
```

## 使用

```
# 完整扫描
请扫描以下 API 端点的安全问题：
POST /api/v1/users/register
GET /api/v1/users/{id}
POST /api/v1/auth/login

# 快速检查
快速检查 POST /api/v1/payments/charge 的安全问题

# 配置审计
审查以下 Nginx 配置的 API 安全性：
（粘贴配置）

# 报告生成
根据以下发现生成安全报告：
（粘贴漏洞列表）
```

## 覆盖范围

- **6大安全维度**
- **100+ 检查项**
- **5级风险分级** (Critical/High/Medium/Low/Passed)
- **4大框架安全要点** (Spring Boot / Express / FastAPI / Go)

## 关联产品

- [ai-smart-commit](https://clawhub.ai/CainGao/ai-smart-commit) — 智能Git提交信息生成
- [ai-content-polish](https://clawhub.ai/CainGao/ai-content-polish) — 中文AI内容去痕
- [video-script-cn](https://clawhub.ai/CainGao/video-script-cn) — 短视频脚本写作
- [ai-code-audit](https://clawhub.ai/CainGao/ai-code-audit) — AI代码审查

## License

MIT
