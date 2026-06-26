# API 端点参考

> 本文件为参考文档，Agent 无需主动加载。

> **baseDir**：相对于 workspace 根目录，即本 skill 所在目录。Agent 在执行时应根据实际目录名填充，或使用 `{baseDir}` 占位符。

---

## 鉴权说明

所有 API 调用均需要以下鉴权头：

| Header | 值 | 来源 |
|--------|----|------|
| `Authorization` | `Bearer <api_key>` | 从 `{baseDir}/.state/api_state.json` 读取 |
| `X-Fingerprint` | `<fingerprint>` | 每次 API 调用前运行 `{baseDir}/scripts/fingerprint.mjs` 生成 |

**获取 API Key 流程：**

```bash
# 1. 生成设备指纹
node {baseDir}/scripts/fingerprint.mjs

# 2. 申请 API Key
curl -k -X POST "https://venustech-ai.online:28200/api/baseline/api_key/distribute" \
  -H "Content-Type: application/json" \
  -d '{"fingerprint": "<FINGERPRINT>"}'

# 3. 保存到 {baseDir}/.state/api_state.json
```

---

## 端点总览

| Gate | 用途 | 完整 URL | Method |
|------|------|----------|--------|
| Gate 1 | Query 风险检测 | `https://venustech-ai.online:28200/api/prompt-injection/analyze` | POST |
| Gate 1 | Query 健康检查 | `https://venustech-ai.online:28200/api/prompt-injection/health` | GET |
| Gate 2 | Skill 执行审计 | `https://venustech-ai.online:28200/api/beiming-sec/verify/upload` | POST |
| Gate 2 | Skill 健康检查 | `https://venustech-ai.online:28200/api/beiming-sec/health` | GET |
| Auth | 获取 API Key | `https://venustech-ai.online:28200/api/baseline/api_key/distribute` | POST |

**Base URL:** `https://venustech-ai.online:28200`（可通过环境变量 `AIDR_SECURITY_API_BASE` 覆盖）

---

## Auth — API Key 获取

### POST /api/baseline/api_key/distribute

**用途：** 基于设备指纹申请 API Key。

**请求体：**
```json
{
  "fingerprint": "<64-char-hex>"
}
```

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `api_key` | string | API Key，用于后续鉴权 |
| `fingerprint` | string | 设备指纹 |

**响应示例：**

```json
{
  "api_key": "abc123...",
  "fingerprint": "my_machine_123"
}
```

---

## Gate 1 — Query Audit API

### POST /api/prompt-injection/analyze

**用途：** 检测用户输入中的提示注入攻击。

**鉴权头：**
```
Authorization: Bearer <api_key>
X-Fingerprint: <fingerprint>
```

```bash
curl -k -s --max-time 10 -w "\n%{http_code}" \
  -X POST "https://venustech-ai.online:28200/api/prompt-injection/analyze" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <api_key>" \
  -H "X-Fingerprint: <fingerprint>" \
  -d '{"content": "<desensitized text>"}'
```

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `is_suspicious` | bool | 综合安全评分低时为 true |
| `safety_score` | int | 最终安全评分 0–100 |
| `safety_level` | string | `strong` / `moderate` / `marginal` / `unsafe` |

**响应示例：**

```json
{
  "is_suspicious": true,
  "safety_score": 8,
  "safety_level": "strong",
  "findings": []
}
```

### GET /api/prompt-injection/health

```json
{ "status": "healthy", "version": "2.0.0" }
```

---

## Gate 2 — Skill Audit API

### POST /api/beiming-sec/verify/upload

**用途：** Skill 安装/调用前的内容安全审计。

**鉴权头：**
```
Authorization: Bearer <api_key>
X-Fingerprint: <fingerprint>
```

> ⚠️ **Pre-Install Audit vs Runtime Audit 的上传内容差异：**
> - **Pre-Install Audit**：Skill 内容来自临时目录，**不脱敏**直接上传原始内容
> - **Runtime Audit**：Skill 内容来自已安装目录，**必须脱敏**后上传（防止用户环境信息泄露）
> - 脱敏规则详见 `configs/desensitization.yaml`

**跨平台命令：**

```bash
# Linux/macOS
SKILL_PATH="/tmp/skill-audit/<skill-name>/<actual-dir>"
cd "${SKILL_PATH}"
rm -f /tmp/skill_scan.zip
zip -r /tmp/skill_scan.zip . -x ".git/*" -x "node_modules/*"

curl -k -s -w "\n%{http_code}" \
  -X POST "https://venustech-ai.online:28200/api/beiming-sec/verify/upload" \
  -H "Authorization: Bearer <api_key>" \
  -H "X-Fingerprint: <fingerprint>" \
  -F "file=@/tmp/skill_scan.zip" \
  -F "skill_sha256=${FINAL_HASH}" \
  -F "skill_name=<skill_name>"
```

```powershell
# Windows PowerShell
$SKILL_PATH = Get-Content (Join-Path $env:TEMP "skill-audit\.last_skill_path")
Set-Location $SKILL_PATH
$ZIP_PATH = Join-Path $env:TEMP "skill_scan.zip"
if (Test-Path $ZIP_PATH) { Remove-Item $ZIP_PATH -Force }
Compress-Archive -Path "$SKILL_PATH\*" -DestinationPath $ZIP_PATH -Force

Invoke-RestMethod -Uri "https://venustech-ai.online:28200/api/beiming-sec/verify/upload" `
  -Method POST `
  -Headers @{ "Authorization" = "Bearer <api_key>"; "X-Fingerprint" = "<fingerprint>" } `
  -Form @{ file = Get-Item $ZIP_PATH; skill_sha256 = "<FINAL_HASH>"; skill_name = "<skill_name>" }
```

> ⚠️ **跨平台临时目录**：
> - Linux/macOS：`/tmp/skill-audit/`
> - Windows：`%TEMP%\skill-audit\`（展开为 `C:\Users\<user>\AppData\Local\Temp\skill-audit\`）

**⚠️ 关键约束：**
- `skill_sha256` 必须使用 Stage 1/4 计算的 Final 指纹（L2 + L3 → SHA-256），**不得**重新计算 zip 的哈希
- 必须从 Stage 2 临时目录压缩，**禁止**从原始 Skill 目录压缩上传

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `can_execute` | bool | Skill 是否可执行 |
| `verdict` | string | `allow` / `confirm` / `block` |
| `in_registry` | bool | Skill 是否在注册表中 |
| `hash_match` | bool | 提交的哈希是否与注册表匹配 |
| `audit_result.level` | string | `CLEAR` / `MINOR` / `ELEVATED` / `SEVERE` / `CRITICAL` |
| `audit_result.final_score` | int | 0–100 |
| `audit_result.behavioral_score` | int | 行为分析评分 |
| `audit_result.source_score` | int | 源代码分析评分 |
| `audit_result.findings` | array | 安全发现列表 |

**响应示例：**

```json
{
  "can_execute": true,
  "skill_name": "my-skill",
  "verdict": "allow",
  "audit_result": {
    "level": "CLEAR",
    "final_score": 100,
    "behavioral_score": 100,
    "source_score": 100,
    "findings": []
  }
}
```

### GET /api/beiming-sec/health

```json
{ "status": "ok", "service": "beiming-sec-skill-pre" }
```

---

## 错误处理规则

**API 失败 = 安全阻断**，当 curl 请求出现以下情况时，必须 block：

- HTTP 状态码非 200
- 响应体为空或无法解析为 JSON
- 缺少必需字段
- 服务不可达（connect timeout / refused）
- `401 Unauthorized` — API Key 无效或过期（删除 `api_state.json` 并重新申请）
- `403 Forbidden` — 指纹不匹配（重新生成指纹重试）

### ⚠️ 禁止编造 API 结果

以下行为均属严重违规：

- ❌ curl 未成功返回时，假装收到了响应并填充字段
- ❌ 用"假设 `safety_level=strong`"来继续后续流程
- ❌ 在 curl 结果缺失时输出 `verdict=allow` 等

**错误示例：**

```text
# 场景：curl 命令执行失败
curl: (7) Failed to connect to 117.134.14.237 port 8002

# ❌ LLM 自行编造结果（严重违规）：
结果: http_status=200, verdict=allow, level=CLEAR, score=95, can_execute=true

# ✅ 正确做法：
结果: curl failed (exit_code=7, connection refused), action=block
```

---
