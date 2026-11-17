# Crucible 安全清单

> 融合 ECC security-review 10 节清单。Gate 3 检测到安全敏感代码时运行。

---

## 触发条件

| 代码类型 | 关键词 |
|----------|--------|
| 认证/授权 | login, JWT, session, OAuth, RBAC |
| 支付 | stripe, payment, billing |
| 文件上传 | upload, attachment, avatar |
| 数据库 | SQL, ORM, query |
| API 端点 | 所有对外 HTTP handler |

---

## 10 节清单

### 1. Secrets 管理
- [ ] 源代码无硬编码 secret（API key, password, token）
- [ ] `.env` in `.gitignore`
- [ ] 启动时验证必需 secrets
- [ ] Secret 轮换机制

```
❌ const API_KEY = "sk-abc123"
✅ process.env.API_KEY
```

### 2. 输入验证
- [ ] 所有用户输入经 schema 验证（Zod/Pydantic）
- [ ] 无 eval / Function() / 动态代码执行
- [ ] 字符串有 maxLength，数字有范围限制
- [ ] 枚举值白名单验证

### 3. SQL 注入
- [ ] 所有查询参数化（无字符串拼接 SQL）
- [ ] LIKE 查询转义 `%` 和 `_`
- [ ] ORDER BY 列名白名单

```
❌ `SELECT * FROM users WHERE id = ${id}`
✅ db.query('SELECT * FROM users WHERE id = $1', [id])
```

### 4. 认证 & 授权
- [ ] 密码 bcrypt/argon2 (cost ≥ 12)
- [ ] JWT 存 httpOnly + Secure + SameSite cookie
- [ ] Token TTL ≤ 15min + refresh token
- [ ] 后端每个 endpoint 验证权限
- [ ] 登录失败速率限制

### 5. XSS 防护
- [ ] 无 innerHTML / dangerouslySetInnerHTML 使用用户输入
- [ ] CSP header: `default-src 'self'`
- [ ] 富文本用 DOMPurify 净化

### 6. CSRF 防护
- [ ] SameSite cookie
- [ ] 状态修改请求验证 CSRF token 或 Origin
- [ ] GET 不修改服务器状态

### 7. 速率限制
- [ ] 登录: ≤ 5 次/分钟/IP
- [ ] API: 合理速率限制
- [ ] 密码重置: ≤ 3 次/小时/账户

### 8. 敏感数据暴露
- [ ] 生产环境不暴露 stack trace
- [ ] 日志不记录密码/token/PII
- [ ] API 响应只含必要字段
- [ ] 错误消息不泄露内部路径/表名

### 9. 依赖安全
- [ ] 锁文件已提交（package-lock.json / poetry.lock）
- [ ] `npm audit` / `pip-audit` 无 critical 漏洞
- [ ] 关键依赖版本固定

### 10. 文件上传安全
- [ ] MIME + 扩展名白名单
- [ ] 文件大小限制
- [ ] 随机文件名（不用原始名）
- [ ] 上传目录不可执行

---

## Gate 3 安全报告模板

```markdown
| # | Section | Severity | Description | Location | Status |
|---|---------|----------|-------------|----------|--------|
| S1 | {section} | CRITICAL/HIGH/MEDIUM | {desc} | {file:line} | OPEN/FIXED |
```
