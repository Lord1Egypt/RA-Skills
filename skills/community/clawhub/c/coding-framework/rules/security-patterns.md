# 安全模式规则集（25 种）

> 集成到 hook-engine 的 PreExec 钩子，用于命令执行前的安全检测。
> 灵感来源：Claude Code security-guidance（~2000 行 Python，25 种安全模式）。

## 使用说明

每条规则包含：
- **name**：模式名称
- **severity**：critical / high / medium / low
- **pattern**：正则表达式（匹配命令或代码）
- **message**：触发时的警告信息
- **suggestion**：修复建议
- **cwe**：CWE 编号（如有）

Hook-engine 在 PreExec 阶段扫描命令，匹配到 critical/high 级别时阻止执行并要求确认，medium/low 级别记录告警日志。

---

## 1. 危险命令

```yaml
name: dangerous-commands
severity: critical
pattern: (rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|(-[a-zA-Z]*f[a-zA-Z]*r))\s+(/|~|\.\.)|format\s+[a-zA-Z]:|diskpart|chkdsk\s+/[fr]|dd\s+if=|mkfs\.|fdisk|parted)
message: "检测到危险命令：可能破坏文件系统或磁盘"
suggestion: "使用 trash 替代 rm；磁盘操作需要物理机确认"
cwe: CWE-730
```

## 2. 注册表操作

```yaml
name: registry-operations
severity: critical
pattern: (reg\s+(add|delete|import|export|copy)|Set-ItemProperty.*HKLM|New-ItemProperty.*HKCU|Remove-ItemProperty.*HKLM)
message: "检测到注册表操作：可能导致系统不稳定"
suggestion: "注册表操作已禁止，如需修改请通过系统设置界面"
cwe: CWE-922
```

## 3. 账户管理

```yaml
name: account-management
severity: critical
pattern: (net\s+(user|localgroup|accounts|group)|Add-LocalGroupMember|New-LocalUser|Set-LocalUser|Remove-LocalUser|useradd|usermod|userdel|adduser)
message: "检测到账户管理操作：可能影响系统安全"
suggestion: "账户管理操作已禁止，请联系 IT 管理员"
cwe: CWE-285
```

## 4. 服务管理

```yaml
name: service-management
severity: high
pattern: (sc\s+(delete|config|start|stop|create)|net\s+(start|stop)\s+\w|Set-Service|Start-Service|Stop-Service|systemctl\s+(start|stop|enable|disable)|service\s+\w+\s+(start|stop|restart))
message: "检测到服务管理操作：可能影响系统运行"
suggestion: "服务管理需要管理员权限，请通过正式流程申请"
cwe: CWE-284
```

## 5. 计划任务

```yaml
name: scheduled-tasks
severity: high
pattern: (schtasks\s+(/delete|/create|/change|/run)|crontab\s+-[er]|at\s+\d|New-ScheduledTask|Register-ScheduledTask|Unregister-ScheduledTask)
message: "检测到计划任务操作：可能创建持久化后门"
suggestion: "计划任务操作需要审批，请使用 cron 工具（OpenClaw 内置）"
cwe: CWE-250
```

## 6. 外部下载

```yaml
name: external-download
severity: high
pattern: (certutil\s+(-urlcache|-encode|-decode)|Invoke-WebRequest.*https?://(?!.*midea\.com)|curl\s+.*https?://(?!.*midea\.com)|wget\s+https?://(?!.*midea\.com)|bitsadmin.*\/transfer|Start-BitsTransfer)
message: "检测到外部下载操作：可能引入恶意软件"
suggestion: "使用内部镜像源或经审批的下载地址"
cwe: CWE-494
```

## 7. 批量操作

```yaml
name: bulk-file-operations
severity: high
pattern: ((del|remove|rmdir|move|rename)\s+\/[sS].*\s+(\*|\/[qQ])|(Get-ChildItem|ls|dir)\s+.*\|\s*(Remove-Item|del|move))
message: "检测到批量文件操作：可能影响大量文件"
suggestion: "先列出受影响的文件（dry-run），确认后再执行"
cwe: CWE-730
```

## 8. 提权操作

```yaml
name: privilege-escalation
severity: critical
pattern: (runas\s+\/user:|sudo\s+|su\s+-|Start-Process.*-Verb\s+RunAs|gksudo|pkexec|elevation)
message: "检测到提权操作：尝试获取更高权限"
suggestion: "提权操作已禁止，如需管理员权限请联系 IT"
cwe: CWE-269
```

## 9. 敏感数据传输

```yaml
name: sensitive-data-exfiltration
severity: high
pattern: (scp\s+.*(\.ssh|\.env|\.key|password|secret)|curl\s+.*(-d|--data).*password|Invoke-RestMethod.*Authorization|ftp\s+-n.*PUT|nc\s+.*<\s*\.(env|pem|key))
message: "检测到可能的敏感数据传输：可能泄露凭证"
suggestion: "禁止通过网络传输敏感文件，使用加密通道或密钥管理工具"
cwe: CWE-200
```

## 10. 代码执行风险

```yaml
name: code-execution-risk
severity: high
pattern: (eval\s*\(.*\+|exec\s*\(.*\+|subprocess\.call\(.*shell\s*=\s*True|os\.system\s*\(|child_process\.exec\s*\(|Function\s*\(.*\+|setTimeout\s*\(.*\+)
message: "检测到动态代码执行：可能存在注入风险"
suggestion: "避免拼接执行代码，使用参数化调用或白名单验证"
cwe: CWE-94
```

## 11. 敏感信息泄露

```yaml
name: sensitive-info-leak
severity: high
pattern: ((api[_-]?key|apikey|secret|token|password|passwd|credential)\s*[:=]\s*['"][a-zA-Z0-9]{8,}|Authorization:\s*Bearer\s+[a-zA-Z0-9])
message: "检测到硬编码敏感信息：可能泄露凭证"
suggestion: "使用环境变量或密钥管理服务存储敏感信息"
cwe: CWE-798
```

## 12. 路径遍历

```yaml
name: path-traversal
severity: high
pattern: (\.\.\/\.\.\/|\.\.\\\.\.\\|\/etc\/passwd|\/etc\/shadow|%2e%2e%2f|%2e%2e\/|\.\.%2f|\/proc\/self|\/dev\/null\s*>)
message: "检测到路径遍历尝试：可能访问受限文件"
suggestion: "使用规范化路径，禁止用户输入直接拼接文件路径"
cwe: CWE-22
```

## 13. SQL 注入

```yaml
name: sql-injection
severity: critical
pattern: ((execute|query|exec)\s*\(.*(\+\s*['"]|f['"].*\{|\%s).*SELECT|SELECT.*\+\s*\w+|WHERE.*=\s*['"]?\s*\+\s*\w+|\.format\(.*SELECT|string\.format.*WHERE)
message: "检测到 SQL 注入风险：字符串拼接 SQL"
suggestion: "使用参数化查询或 ORM，禁止字符串拼接 SQL"
cwe: CWE-89
```

## 14. XSS 风险

```yaml
name: xss-risk
severity: high
pattern: (innerHTML\s*=|outerHTML\s*=|document\.write\s*\(|v-html\s*=|dangerouslySetInnerHTML|\.html\s*\(.*\+|render\s+raw)
message: "检测到 XSS 风险：未转义的用户输入渲染"
suggestion: "使用文本内容替代 HTML 插入，或对输入进行转义"
cwe: CWE-79
```

## 15. 不安全的反序列化

```yaml
name: insecure-deserialization
severity: critical
pattern: (pickle\.load\s*\(|pickle\.loads\s*\(|yaml\.load\s*\((?!.*Loader)|marshal\.loads\s*\(|shelve\.open\s*\(|jsonpickle\.decode\s*\(|unserialize\s*\()
message: "检测到不安全的反序列化：可能执行恶意代码"
suggestion: "使用安全的序列化格式（JSON），或指定安全的 Loader"
cwe: CWE-502
```

## 16. 硬编码凭证

```yaml
name: hardcoded-credentials
severity: high
pattern: ((password|passwd|pwd|secret|private_key|access_key)\s*=\s*['"][^'"]{4,}|(username|user|uid)\s*=\s*['"]admin['"])
message: "检测到硬编码凭证：凭证应存储在安全位置"
suggestion: "使用环境变量、.env 文件或密钥管理服务"
cwe: CWE-798
```

## 17. 不安全的加密

```yaml
name: insecure-cryptography
severity: medium
pattern: (hashlib\.md5\s*\(|hashlib\.sha1\s*\(|MD5\s*\(|SHA1\s*\(|AES\.new\s*\(.*ECB|DES\.new\s*\(|RC4\b|DES3\b|Crypto\.Cipher\.DES)
message: "检测到不安全的加密算法：MD5/SHA1/DES 已被破解"
suggestion: "使用 SHA-256+ 或 bcrypt（密码），AES-256-GCM（加密）"
cwe: CWE-327
```

## 18. 资源泄漏

```yaml
name: resource-leak
severity: medium
pattern: (open\s*\(.*\)\s*[^.]*(?!\.close|with\s)|\.connect\s*\((?!.*with)|new\s+Socket\s*\((?!.*\.close)|fetch\s*\(.*\)\s*[^.]*(?!\.json|\.text))
message: "检测到可能的资源泄漏：文件/连接未关闭"
suggestion: "使用 with 语句或 try-finally 确保资源释放"
cwe: CWE-404
```

## 19. 竞态条件

```yaml
name: race-condition
severity: medium
pattern: (if\s+os\.path\.exists.*\n.*open\s*\(|if\s+FileExists.*\n.*File\.Open|test\s+-[fed]\s+.*&&\s*(cat|mv|cp|rm))
message: "检测到 TOCTOU 竞态条件：检查和使用之间存在时间窗口"
suggestion: "使用原子操作或文件锁避免竞态"
cwe: CWE-367
```

## 20. 不安全随机数

```yaml
name: insecure-randomness
severity: medium
pattern: (Math\.random\s*\(\s*\)(?!.*(?:game|animation|color|placeholder))|random\.random\s*\(\s*\)|rand\s*\(\s*\)(?!.*srand))
message: "检测到不安全随机数：Math.random 不可用于安全场景"
suggestion: "安全场景使用 crypto.randomBytes / secrets.token_hex"
cwe: CWE-330
```

## 21. 日志注入

```yaml
name: log-injection
severity: medium
pattern: (logger\.\w+\s*\(.*\+\s*(req\.|request\.|params|query|body)|console\.log\s*\(.*\+\s*(req\.|request\.|params)|logging\.\w+\s*\(.*%s.*,\s*(request|input|data)))
message: "检测到日志注入风险：用户输入未清理直接写入日志"
suggestion: "清理用户输入中的换行符和控制字符"
cwe: CWE-117
```

## 22. SSRF

```yaml
name: ssrf
severity: critical
pattern: (requests\.get\s*\(.*\+\s*\w+|fetch\s*\(.*\+\s*\w+|urllib\.request\.urlopen\s*\(.*\+|http\.get\s*\(.*\+|curl\s+.*\$\{)
message: "检测到 SSRF 风险：用户输入直接构造请求 URL"
suggestion: "使用 URL 白名单，禁止访问内网地址（127.0.0.1/10.x/172.16.x/192.168.x）"
cwe: CWE-918
```

## 23. XXE

```yaml
name: xxe
severity: critical
pattern: (xml\.etree\.ElementTree\.parse\s*\(|lxml\.etree\.parse\s*\(|DOMDocument.*loadXML|SAXParser|XMLReader.*setFeature.*false|defusedxml(?!\.))
message: "检测到 XXE 风险：XML 解析未禁用外部实体"
suggestion: "使用 defusedxml 或禁用 DTD/外部实体解析"
cwe: CWE-611
```

## 24. 不安全 CORS

```yaml
name: insecure-cors
severity: medium
pattern: (Access-Control-Allow-Origin\s*[:=]\s*\*|cors\s*\(\s*\{\s*origin\s*:\s*true|@CrossOrigin\s*\(\s*origins?\s*=\s*['"]\*['"])
message: "检测到过于宽松的 CORS 策略：允许任意来源访问"
suggestion: "指定具体的允许来源，不使用通配符 *"
cwe: CWE-942
```

## 25. 依赖漏洞

```yaml
name: vulnerable-dependencies
severity: medium
pattern: (lodash\s*[:<]=?\s*[0-3]\.|requests\s*[:<]=?\s*2\.[0-9]\.|express\s*[:<]=?\s*3\.|django\s*[:<]=?\s*[12]\.|jquery\s*[:<]=?\s*[12]\.|openssl\s*[:<]=?\s*1\.0)
message: "检测到已知漏洞的依赖版本"
suggestion: "运行 npm audit / pip audit / safety check 更新到安全版本"
cwe: CWE-1104
```

---

## 严重级别处理策略

| 级别 | 处理方式 |
|------|----------|
| critical | 阻止执行 + 报告用户 + 记录日志 |
| high | 阻止执行 + 请求确认 + 记录日志 |
| medium | 允许执行 + 记录告警日志 |
| low | 记录日志，不干预 |
