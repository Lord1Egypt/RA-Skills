---
name: api-security-scanner
description: |
  API 安全扫描工具。对 REST API 端点进行自动化安全审计，检测 OWASP Top 10 漏洞、
  认证/授权问题、敏感数据泄露、速率限制缺失等常见安全隐患。输出结构化安全报告。
  适合开发者在部署前快速自检，也适合安全团队做轻量级审计。
---

# API Security Scanner 🔒

## Description

Automated security scanner for REST API endpoints. Performs security audit against OWASP API Security Top 10, detecting authentication issues, authorization flaws, data exposure, injection risks, and more.

对 REST API 端点进行自动化安全审计，覆盖 OWASP API 安全 Top 10，检测认证/授权问题、数据泄露、注入风险等常见隐患。

## When to Use This Skill

Use this skill when:
- You need to audit API endpoints for security vulnerabilities（审计 API 端点的安全漏洞）
- You want to review API design/config for security best practices（审查 API 设计/配置的安全最佳实践）
- You need to generate a security report before deployment（部署前生成安全报告）
- You're reviewing API documentation for security issues（审查 API 文档中的安全问题）
- You want to harden your API against common attack vectors（加固 API 抵御常见攻击向量）

## Usage Modes

### Mode 1: Full Scan — 完整扫描
```
请扫描以下 API 端点的安全问题：

POST /api/v1/users/register
GET /api/v1/users/{id}
PUT /api/v1/users/{id}
DELETE /api/v1/users/{id}
POST /api/v1/auth/login
GET /api/v1/admin/users

Headers: Authorization: Bearer {token}
```

### Mode 2: Quick Check — 快速检查
```
快速检查这个 API 端点的安全问题：POST /api/v1/payments/charge
```

### Mode 3: Config Audit — 配置审计
```
审查以下 API 网关/中间件配置的安全性：

（粘贴 nginx.conf / express middleware / Spring Security config 等）
```

### Mode 4: Report Generation — 报告生成
```
根据以下安全扫描结果，生成一份结构化的安全报告：

（粘贴扫描结果或漏洞列表）
```

## Scanning Dimensions

This skill scans across 6 security dimensions:

1. **Authentication & Session** — 认证与会话管理
2. **Authorization & Access Control** — 授权与访问控制
3. **Input Validation & Injection** — 输入验证与注入防护
4. **Data Protection & Privacy** — 数据保护与隐私
5. **Rate Limiting & DoS Protection** — 速率限制与防 DoS
6. **Configuration & Infrastructure** — 配置与基础设施

## Output Format

Each scan produces a structured report with:
- 🔴 **Critical** — 必须立即修复
- 🟠 **High** — 高风险，尽快修复
- 🟡 **Medium** — 中等风险，计划修复
- 🔵 **Low** — 低风险，建议修复
- ✅ **Passed** — 通过检查

---
## Knowledge Files

- `scan-rules.md` — 完整扫描规则库（6大维度，100+ 检查项）
