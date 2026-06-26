# API Security Scan Rules

## 6 大维度，100+ 检查项

---

## 维度 1: Authentication & Session — 认证与会话管理

### 1.1 密码安全
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| A001 | 密码明文传输 | 🔴 Critical | 密码必须通过 HTTPS 传输，禁止 HTTP |
| A002 | 密码明文存储 | 🔴 Critical | 密码必须使用 bcrypt/scrypt/Argon2 哈希存储 |
| A003 | 弱密码策略 | 🟠 High | 要求最少8位，包含大小写+数字+特殊字符 |
| A004 | 密码重置流程 | 🟡 Medium | 重置令牌应有时效性（≤1小时），一次性使用 |
| A005 | 暴力破解防护 | 🟠 High | 登录失败锁定机制（如5次失败锁定15分钟）|
| A006 | 凭证硬编码 | 🔴 Critical | 检查代码/配置中是否有硬编码的 API Key/密码/Token |

### 1.2 Token 安全
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| A007 | JWT 签名算法 | 🔴 Critical | 禁止 "alg": "none"，使用 RS256/ES256 |
| A008 | JWT 过期时间 | 🟠 High | Access Token ≤ 15min，Refresh Token ≤ 7天 |
| A009 | Token 传输方式 | 🟡 Medium | 优先使用 HttpOnly Cookie，避免 localStorage |
| A010 | Refresh Token 轮换 | 🟠 High | Refresh Token 应该一次性使用，使用后立即轮换 |
| A011 | Token 黑名单 | 🟡 Medium | 支持 Token 撤销/黑名单机制 |

### 1.3 OAuth/SSO
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| A012 | CSRF State 参数 | 🟠 High | OAuth 流程必须使用 state 参数防 CSRF |
| A013 | Redirect URI 白名单 | 🔴 Critical | 严格校验 redirect_uri，禁止开放重定向 |
| A014 | Authorization Code 一次性 | 🟠 High | Authorization Code 使用后立即失效 |

---

## 维度 2: Authorization & Access Control — 授权与访问控制

### 2.1 权限模型
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| B001 | IDOR 检测 | 🔴 Critical | 检查 /users/{id} 类接口是否有越权访问 |
| B002 | 水平越权 | 🔴 Critical | 用户 A 不能访问用户 B 的资源 |
| B003 | 垂直越权 | 🔴 Critical | 普通用户不能访问管理员接口 |
| B004 | 权限粒度 | 🟡 Medium | API 应实现功能级+数据级双重权限控制 |
| B005 | 默认拒绝 | 🟠 High | 默认拒绝所有访问，显式授权（白名单模式）|

### 2.2 API 端点安全
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| B006 | 管理接口暴露 | 🔴 Critical | /admin、/debug、/swagger 不应暴露在公网 |
| B007 | 批量操作限制 | 🟠 High | 批量删除/更新需额外权限验证 |
| B008 | 资源所有权 | 🟠 High | 每个资源操作需验证当前用户是否为资源所有者 |
| B009 | CORS 配置 | 🟠 High | 禁止 Access-Control-Allow-Origin: *（生产环境）|

---

## 维度 3: Input Validation & Injection — 输入验证与注入防护

### 3.1 注入攻击
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| C001 | SQL 注入 | 🔴 Critical | 使用参数化查询，禁止字符串拼接 SQL |
| C002 | NoSQL 注入 | 🔴 Critical | 过滤 $where、$regex 等 MongoDB 操作符 |
| C003 | 命令注入 | 🔴 Critical | 禁止直接将用户输入传入系统命令 |
| C004 | LDAP 注入 | 🟠 High | 对 LDAP 查询输入进行转义 |
| C005 | SSRF | 🔴 Critical | 验证/限制外部请求目标，禁止请求内网地址 |
| C006 | 模板注入 | 🟠 High | 禁止在模板引擎中直接执行用户输入 |

### 3.2 输入验证
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| C007 | 类型校验 | 🟠 High | 严格校验参数类型（string/number/array）|
| C008 | 长度限制 | 🟡 Medium | 所有字符串输入应有最大长度限制 |
| C009 | 枚举值校验 | 🟡 Medium | sort/order/method 等参数应使用白名单 |
| C010 | 文件上传 | 🔴 Critical | 校验文件类型、大小、内容（Magic bytes）|
| C011 | JSON/XML 炸弹 | 🟠 High | 限制请求体大小和嵌套深度 |
| C012 | 正则 DoS | 🟠 High | 避免使用回溯复杂度高的正则表达式 |

---

## 维度 4: Data Protection & Privacy — 数据保护与隐私

### 4.1 敏感数据
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| D001 | PII 暴露 | 🔴 Critical | 响应中不应包含身份证号、银行卡号等 PII |
| D002 | 密码返回 | 🔴 Critical | API 响应中不应返回密码字段（即使哈希后）|
| D003 | 错误信息泄露 | 🟠 High | 错误响应不应泄露堆栈/SQL/内部路径 |
| D004 | 日志敏感数据 | 🟠 High | 日志中不应记录密码/Token/PII |
| D005 | 分页数据泄露 | 🟡 Medium | 分页接口应限制每页最大数量 |

### 4.2 传输安全
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| D006 | HTTPS 强制 | 🔴 Critical | 生产环境强制 HTTPS，HSTS 头 |
| D007 | 证书验证 | 🟠 High | 客户端不应跳过 SSL 证书验证 |
| D008 | 敏感头部 | 🟡 Medium | 移除 X-Powered-By、Server 等版本信息头 |

### 4.3 数据加密
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| D009 | 静态加密 | 🟠 High | 数据库中的敏感字段应加密存储 |
| D010 | 密钥管理 | 🟠 High | 加密密钥不应与代码同仓，使用 KMS |
| D011 | 加密算法 | 🟡 Medium | 禁止使用 DES/MD5/SHA1，使用 AES-256/SHA-256+ |

---

## 维度 5: Rate Limiting & DoS Protection — 速率限制与防 DoS

### 5.1 速率限制
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| E001 | 全局限流 | 🟠 High | API 网关/服务层面应有全局 QPS 限制 |
| E002 | 用户级限流 | 🟠 High | 每用户/Token 应有调用频率限制 |
| E003 | 接口级限流 | 🟡 Medium | 敏感操作（登录/支付/验证码）应有独立限流 |
| E004 | 限流响应 | 🟡 Medium | 限流时应返回 429 + Retry-After 头 |
| E005 | 限流粒度 | 🟡 Medium | 考虑按 IP + 用户 + 接口多维度限流 |

### 5.2 DoS 防护
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| E006 | 请求体大小限制 | 🟠 High | 设置合理的请求体大小上限 |
| E007 | 超时设置 | 🟡 Medium | 设置合理的连接/读取/响应超时 |
| E008 | 慢查询保护 | 🟡 Medium | 数据库查询应有超时和结果集大小限制 |
| E009 | 并发控制 | 🟡 Medium | 对资源密集型操作进行并发限制 |

---

## 维度 6: Configuration & Infrastructure — 配置与基础设施

### 6.1 API 网关配置
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| F001 | 调试模式关闭 | 🔴 Critical | 生产环境必须关闭 debug/verbose 模式 |
| F002 | API 版本管理 | 🟡 Medium | API 应有版本策略（URI/Header/Query） |
| F003 | 响应压缩 | 🟢 Info | 启用 gzip/brotli 压缩减少带宽 |
| F004 | 请求验证 | 🟠 High | 网关层应验证 Content-Type 和请求格式 |

### 6.2 日志与监控
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| F005 | 审计日志 | 🟠 High | 敏感操作应有审计日志（谁/何时/做了什么）|
| F006 | 异常监控 | 🟡 Medium | 集成异常监控和告警（4xx/5xx 异常率）|
| F007 | 请求追踪 | 🟡 Medium | 使用 Request ID / Trace ID 串联请求链路 |
| F008 | 健康检查 | 🟡 Medium | 提供 /health 端点用于服务健康检查 |

### 6.3 依赖安全
| # | 检查项 | 风险 | 规则描述 |
|---|--------|------|---------|
| F009 | 依赖版本 | 🟠 High | 定期更新依赖，修复已知 CVE |
| F010 | 最小权限 | 🟡 Medium | 容器/进程以最小权限运行（非 root）|

---

## 常见 API 框架安全检查要点

### Spring Boot / Java
- 关闭 Actuator 端点或限制访问
- Spring Security 配置审查
- CSRF 保护（非 REST API 可关闭）
- Content-Type 严格校验

### Express / Node.js
- Helmet.js 安全头
- CORS 配置审查
- 请求体解析限制（body-parser limit）
- 避免eval/Function构造器

### FastAPI / Python
- Pydantic 模型验证（默认有）
- CORS middleware 配置
- 依赖安全（pip audit）
- 调试模式关闭

### Go (Gin/Echo)
- 请求大小限制
- 超时中间件
- Recover 中间件（防 panic 崩溃）
- 安全响应头

---

## 报告模板

```markdown
# API Security Scan Report

**扫描时间**: YYYY-MM-DD HH:MM
**目标**: API Base URL / 端点列表
**扫描模式**: Full Scan / Quick Check / Config Audit

## 摘要
- 🔴 Critical: X 个
- 🟠 High: X 个
- 🟡 Medium: X 个
- 🔵 Low: X 个
- ✅ Passed: X 个
- **安全评分**: XX/100

## 详细发现

### 🔴 [CRITICAL] A001 - 密码明文传输
- **端点**: POST /api/v1/auth/login
- **描述**: 登录接口通过 HTTP 传输密码
- **影响**: 密码可被中间人窃取
- **修复建议**: 强制 HTTPS，配置 HSTS 头

## 修复优先级
1. 🔴 Critical — 立即修复（24小时内）
2. 🟠 High — 尽快修复（1周内）
3. 🟡 Medium — 计划修复（1个月内）
4. 🔵 Low — 建议修复

## 合规参考
- OWASP API Security Top 10 (2023)
- OWASP Top 10 (2021)
- CWE 常见弱点枚举
```
