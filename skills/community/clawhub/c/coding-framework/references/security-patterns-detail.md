# 安全模式详细说明

> 25 种安全模式的完整说明，含检测逻辑、修复方案和真实案例。

## 概述

安全模式集成到 hook-engine 的 PreExec 钩子，用于命令执行前和代码审查时的安全检测。
灵感来源：Claude Code security-guidance（~2000 行 Python，25 种安全模式）。

## 严重级别处理策略

| 级别 | 处理方式 | 示例 |
|------|----------|------|
| critical | 阻止执行 + 报告用户 + 记录日志 | SQL 注入、SSRF、提权 |
| high | 阻止执行 + 请求确认 + 记录日志 | XSS、硬编码凭证、外部下载 |
| medium | 允许执行 + 记录告警日志 | 不安全加密、资源泄漏、CORS |
| low | 记录日志，不干预 | 代码风格安全建议 |

## 模式分类

### 系统安全（1-8）

1. **危险命令** (critical) — rm -rf /, format, diskpart, mkfs
2. **注册表操作** (critical) — reg add/delete, Set-ItemProperty HKLM
3. **账户管理** (critical) — net user, useradd, Add-LocalGroupMember
4. **服务管理** (high) — sc delete/config, systemctl, net start/stop
5. **计划任务** (high) — schtasks, crontab, New-ScheduledTask
6. **外部下载** (high) — curl/wget 到非白名单域名, certutil
7. **批量操作** (high) — del /s /q, 管道接 Remove-Item
8. **提权操作** (critical) — runas, sudo, su, pkexec

### 数据安全（9-12）

9. **敏感数据传输** (high) — scp .ssh/.env, curl -d password
10. **代码执行风险** (high) — eval(拼接), exec(拼接), subprocess shell=True
11. **敏感信息泄露** (high) — 硬编码 API key, Bearer token
12. **路径遍历** (high) — ../../, %2e%2e, /etc/passwd

### 注入攻击（13-15）

13. **SQL 注入** (critical) — 字符串拼接 SELECT/WHERE
14. **XSS 风险** (high) — innerHTML, document.write, v-html
15. **不安全反序列化** (critical) — pickle.load, yaml.load 无 Loader

### 凭证安全（16）

16. **硬编码凭证** (high) — password=, secret=, private_key=

### 加密安全（17）

17. **不安全加密** (medium) — MD5, SHA1, DES, RC4, AES-ECB

### 资源管理（18-19）

18. **资源泄漏** (medium) — open() 无 close/with, connect() 无释放
19. **竞态条件** (medium) — TOCTOU: if exists → open

### 其他（20-25）

20. **不安全随机数** (medium) — Math.random 用于安全场景
21. **日志注入** (medium) — 用户输入直接写入日志
22. **SSRF** (critical) — 用户输入构造请求 URL
23. **XXE** (critical) — XML 解析未禁用外部实体
24. **不安全 CORS** (medium) — Access-Control-Allow-Origin: *
25. **依赖漏洞** (medium) — 已知漏洞的旧版本依赖

## CWE 映射

| 模式 | CWE |
|------|-----|
| 危险命令 | CWE-730 |
| 注册表操作 | CWE-922 |
| 账户管理 | CWE-285 |
| 服务管理 | CWE-284 |
| 计划任务 | CWE-250 |
| 外部下载 | CWE-494 |
| 批量操作 | CWE-730 |
| 提权操作 | CWE-269 |
| 敏感数据传输 | CWE-200 |
| 代码执行风险 | CWE-94 |
| 敏感信息泄露 | CWE-798 |
| 路径遍历 | CWE-22 |
| SQL 注入 | CWE-89 |
| XSS 风险 | CWE-79 |
| 不安全反序列化 | CWE-502 |
| 硬编码凭证 | CWE-798 |
| 不安全加密 | CWE-327 |
| 资源泄漏 | CWE-404 |
| 竞态条件 | CWE-367 |
| 不安全随机数 | CWE-330 |
| 日志注入 | CWE-117 |
| SSRF | CWE-918 |
| XXE | CWE-611 |
| 不安全 CORS | CWE-942 |
| 依赖漏洞 | CWE-1104 |

## 修复建议速查

| 问题 | 修复方案 |
|------|----------|
| SQL 注入 | 使用参数化查询或 ORM |
| XSS | 使用文本内容替代 HTML 插入 |
| 硬编码凭证 | 使用环境变量或密钥管理 |
| 路径遍历 | 使用规范化路径 |
| 不安全反序列化 | 使用 JSON 或指定安全 Loader |
| 不安全加密 | 使用 SHA-256+/bcrypt/AES-256-GCM |
| 资源泄漏 | 使用 with 语句或 try-finally |
| SSRF | URL 白名单 + 禁止内网访问 |
| XXE | 使用 defusedxml |
| 不安全 CORS | 指定具体允许来源 |
| 依赖漏洞 | npm audit / pip audit / safety check |
