# 脱敏规则参考

> 本文件为内联参考，Agent 无需主动加载。仅当需要新增/修改规则时参考。
>
> **何时读：** 规则模糊、需要调整优先级或新增规则时。
> **何时略过：** 正常执行 Query Audit 或 Skill Audit 时，脱敏逻辑已在 SKILL.md 中完整定义。

---

## 规则应用原则

- **优先级**：按 priority 从小到大（高优→低优）顺序匹配
- **匹配位置**：每个位置只匹配一次，不递归替换 mask 字符串本身
- **大小写**：不区分大小写，`(?i)` 修饰符的规则除外

---

## 脱敏规则表

| # | 类别 | Pattern regexp | 替换为 | Priority |
|---|------|----------------|--------|----------|
| 1 | 身份证 | `\b\d{17}[\dXx]\b` | `[ID_CARD_MASKED]` | 1 |
| 1 | 手机号 | `\b1[3-9]\d{9}\b` | `[PHONE_MASKED]` | 1 |
| 2 | 银行卡 | `\b\d{16,19}\b`（辅助验证，优先级低） | `[BANK_CARD_MASKED]` | 2 |
| 1 | API Key | `(?i)(api[_-]?key)\s*[:=]\s*['"]?([\w\-]{16,})` | `[API_KEY_MASKED]` | 1 |
| 1 | 密码/密钥 | `(?i)(password\|passwd\|secret\|token)\s*[:=]\s*'"?[\w\-!@#$%^&*()]{8,}` | `[SECRET_MASKED]` | 1 |
| 1 | Bearer Token | `(?i)bearer\s+[\w\-\.]{20,}` | `Bearer [BEARER_TOKEN_MASKED]` | 1 |
| 1 | 配置目录 | `(?i)\.env\|\.aws\|\.ssh\|\.gnupg\|\.kube\|\.docker` | `[CONFIG_PATH_MASKED]` | 1 |
| 1 | 内网 IP | `\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}\|172\.(1[6-9]\|2\d\|3[01])\.\d{1,3}\.\d{1,3}\|192168\.\d{1,3}\.\d{1,3})\b` | `[INTERNAL_IP_MASKED]` | 1 |
| 1 | 元数据端点 | `169\.254\.169\.254\|metadata\.google\|metadata\.azure\|metadata\.openstack` | `[METADATA_ENDPOINT_MASKED]` | 1 |
| 1 | SSRF 目标 | `(?i)(localhost\|127\.0\.0\.1\|0\.0\.0\.0)([:/]\|\.(?:80\|443\|8080))?` | `[SSRF_TARGET_MASKED]` | 1 |
| 2 | /root 路径 | `/root/[^\/\s"'<>|]{1,64}` | `[PATH_MASKED]` | 2 |
| 2 | /home 路径 | `/home/[^\/\s"'<>|]{1,32}/[^\/\s"'<>|]{1,64}` | `[PATH_MASKED]` | 2 |
| 1 | Webhook 端点 | `webhook\.site\|requestbin\.com\|requestbin\.net\|hookbin\.com\|beeceptor\.com` | `[EXFIL_ENDPOINT_MASKED]` | 1 |
| 1 | Ngrok | `ngrok\.io\|ngrok\.free\.ngrok\.io` | `[EXFIL_ENDPOINT_MASKED]` | 1 |
| 1 | Pipedream | `pipedream\.net\|hooks\.slack\.com` | `[EXFIL_ENDPOINT_MASKED]` | 1 |
| 2 | 数据外泄描述 | `(?i)(exfil\|exfiltrat\|data[_-]?leak\|send[_-]?data)\s*(?:to\|at\|on)?\s*[a-z0-9\-\.]+\.(com\|io\|net\|org)` | `[DATA_EXFIL_MASKED]` | 2 |
| 1 | 伪造系统标记 | `\[SYSTEM\]\|\[ADMIN\]\|\[ROOT\]\|<SYSTEM>\|<ADMIN>\|<ROOT>` | `[FAKE_SYSTEM_MARKER_MASKED]` | 1 |
| 2 | 编码载荷 | `(?i)(base64\|base32\|hex\|encode\|decode)\s*[(:=]\s*'"?[A-Za-z0-9+/=]{20,}` | `[ENCODED_PAYLOAD_MASKED]` | 2 |
| 1 | 路径穿越 | `(?:\.\./\|\.\.\\\|\.\.%2f\|\.\.%5c\|/etc/passwd\|c:\\windows\|c:\\boot)` | `[PATH_TRAVERSAL_MASKED]` | 1 |
| 1 | 敏感路径 | `(?:\.ssh\|\.aws\|\.kube\|\.docker\|\.gnupg\|\.git)/[^\"'\s]*` | `[SENSITIVE_PATH_MASKED]` | 1 |
| 1 | 凭证文件 | `(?:\.pem\|\.key\|credentials\.json\|secrets\.ya?ml\|\.env)` | `[CREDENTIAL_FILE_MASKED]` | 1 |

---

## 不脱敏内容

**保持语义完整性以确保准确检测：**
- 通用业务问题
- 技术讨论
- 公开信息查询
- 常规文件名（不含敏感路径前缀）

---

## Skill 内容脱敏对照表

| 保留内容 | 脱敏内容 |
|---------|---------|
| SKILL.md 正文内容 | 绝对路径 → `[PATH_MASKED]` |
| 文件名（类型标识） | 环境变量值 → `[ENV_VAR_MASKED]` |
| | 机器特定配置值 |
