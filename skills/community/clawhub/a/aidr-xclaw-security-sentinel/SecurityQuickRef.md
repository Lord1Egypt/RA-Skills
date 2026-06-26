# SecurityQuickRef

> 每次对话开始时必读。完整规范 → `{baseDir}/SKILL.md`（Agent 在执行时应根据实际目录名填充）

> **baseDir**：相对于 workspace 根目录，即本 skill 所在目录。Agent 在执行时应根据实际目录名填充，或使用 `{baseDir}` 占位符。
> - 状态文件：`{baseDir}/.state/api_state.json`
> - 脚本目录：`{baseDir}/scripts/`

---

## 🚨 强制执行 — 完整输出

**⚠️ Query Audit = 5 个输出，Skill Audit = 6 个输出。必须全部执行。**

### Query Audit 必须完整输出：

1. **Stage 1/3 block** → 输出
2. **Stage 2/3 block** → 输出
3. **Stage 3/3 block** → 输出
4. **DONE border** → 输出
5. **完整报告**（query-report.md 模板）→ 输出

### Skill Audit 必须完整输出：

1. **Stage 1/4 block** → 输出
2. **Stage 2/4 block** → 输出
3. **Stage 3/4 block** → 输出
4. **Stage 4/4 block** → 输出
5. **DONE border** → 输出
6. **完整报告**（skill-report.md 模板）→ 输出

> ❌ **错误**：只输出 Stage 1，不输出后续 Stage
> ❌ **错误**：跳过 DONE border
> ❌ **错误**：跳过完整报告
> ❌ **错误**：批量执行所有工具，最后才统一输出
> ✅ **正确**：每个 stage 完成后立即输出 block

---

## 触发条件

### Gate 1 · Query Audit（每次用户消息）

| 场景 | 执行 |
|------|------|
| 用户发送任何消息 | ✅ 执行 |
| aidr-xclaw-security-sentinel 插件安装（仅限aidr-xclaw-security-sentinel） | **Bypass** |
| 初始化安装 | **Bypass** |

> **⚠️ Query Audit 必须对所有用户消息生效。**
> 由于 AGENTS.md 已强制加载 SKILL.md，Query Audit 触发逻辑现在会自动执行。
> 无需判断"是否触发"——只要不是 aidr-xclaw-security-sentinel plugin bypass，每次消息都会执行 Gate 1。

### Gate 2 · Skill Audit（Pre-Install vs Runtime）

| 场景 | 类型 | 执行 |
|------|------|------|
| `安装` / `帮我安装` / `需要安装` + Skill | Pre-Install Audit | ✅ 执行 |
| `clawhub install` + Skill | Pre-Install Audit | ✅ 执行 |
| `运行` / `使用` / `执行` + Skill | Runtime Audit | ✅ 执行 |
| aidr-xclaw-security-sentinel 插件安装（仅限aidr-xclaw-security-sentinel） | — | **Bypass** |
| 初始化安装 | — | **Bypass** |

#### Pre-Install Audit 触发词

| 触发类型 | 触发词示例 |
|---------|-----------|
| 安装请求 | `安装 <skill名称>` |
| 安装请求 | `帮我安装 <skill名称>` |
| 安装请求 | `我需要安装 <skill名称>` |
| 安装请求 | `安装 [skill名称] skill` |
| 安装请求 | `装一个 <skill名称>` |
| clawhub CLI | `clawhub install <skill名称>` |
| openclaw | `openclaw skills install <skill名称>` |

#### Runtime Audit 触发词

| 触发类型 | 触发词示例 |
|---------|-----------|
| 运行请求 | `运行 <skill名称>` |
| 运行请求 | `使用 <skill名称>` |
| 运行请求 | `执行 <skill名称>` |
| 运行请求 | `调用 <skill名称>` |

---

## 初始化流程（Init）

当用户提及初始化关键词时，执行 `init_skill.cjs`：

```
Stage 1/3 [AGENTS.md 注入] → [立即输出 Stage 1 block]
Stage 2/3 [API Key 获取]   → [生成指纹 → 申请 API Key → 保存到本地 → 立即输出 Stage 2 block]
Stage 3/3 [插件安装]       → [立即输出 Stage 3 block]
[DONE] → [立即输出 DONE block]
```

**初始化步骤：**
1. AGENTS.md 安全脚本注入
2. API Key 获取与保存（生成指纹 → 申请 API Key → 保存到 `{baseDir}/.state/api_state.json`）
3. aidr-xclaw-security-sentinel 插件安装

---

## Stage 流程分解

**Gate 1 · Query Audit（5 个输出节点，全部必须执行）：**

```
Stage 1/3 [TOOL: 本地脱敏]  → [立即输出 Stage 1 block]
Stage 2/3 [TOOL: curl 调用] → [收到响应 → 立即输出 Stage 2 block]
Stage 3/3 [TOOL: 执行动作]  → [立即输出 Stage 3 block]
[DONE] → [立即输出 DONE block]
[总结报告] → [按照 templates/query-report.md 输出总结报告]
```

**Gate 2 · Pre-Install Audit（7 个输出节点，全部必须执行）：**

```
Stage 1/5 [TOOL: 临时目录准备] → [立即输出 Stage 1 block]
Stage 2/5 [TOOL: 指纹计算]     → [立即输出 Stage 2 block]
Stage 3/5 [TOOL: curl 调用]   → [收到响应 → 立即输出 Stage 3 block]
Stage 4/5 [TOOL: 执行动作]     → [立即输出 Stage 4 block]
Stage 5/5 [TOOL: 完成确认]     → [立即输出 Stage 5 block]
[DONE] → [立即输出 DONE block]
[总结报告] → [按照 templates/skill-report.md 输出总结报告]
```

**Gate 2 · Runtime Audit（6 个输出节点，全部必须执行）：**

```
Stage 1/4 [TOOL: 指纹生成]   → [立即输出 Stage 1 block]
Stage 2/4 [TOOL: 内容脱敏]   → [立即输出 Stage 2 block]
Stage 3/4 [TOOL: curl 调用]   → [收到响应 → 立即输出 Stage 3 block]
Stage 4/4 [TOOL: 执行动作]    → [立即输出 Stage 4 block]
[DONE] → [立即输出 DONE block]
[总结报告] → [按照 templates/skill-report.md 输出总结报告]
```

> ⚠️ **禁止跳过任意阶段**。即使 verdict=allow（预期 approve），也必须先输出所有 Stage block，再进入 DONE。

> ⚠️ **Pre-Install Audit 不进行内容脱敏**。直接上传原始内容到安全云服务。
> ⚠️ **Runtime Audit 必须进行内容脱敏**。防止用户环境信息、文件路径等敏感数据泄露到云端。

> ⚠️ **区分两种指纹：**
> - **设备指纹**（Device Fingerprint）：由 `fingerprint.mjs` 生成，用于 API 鉴权
> - **Skill 内容指纹**（Skill Content Fingerprint）：由 Skill 文件计算（L2/L3/Final），用于标识 Skill 身份
> - Runtime Audit **Stage 1/4 计算的是 Skill 内容指纹**，不是设备指纹！

---

## 输出格式（阶段块）

```
[AIDR-XClaw-Security-Sentinel][<Gate>][Stage N/M] <标题>
操作: <描述>
结果: <关键字段>
```

### DONE block 格式

```
════════════════════════════════════════════════════════════
[AIDR-XClaw-Security-Sentinel][<Gate>] 检测完成
检测结论: <pass/warn/block 或 approve/warn/reject>
════════════════════════════════════════════════════════════

✅ 安全检测通过  /  ⚠️ 安全检测告警  /  🚫 安全检测阻断

安全评分/综合评分: <score>/100
安全等级/风险等级: <level>
检测结论: <text>
```

---

## Action on Result（结果处置）

> **⚠️ 所有 Stage 执行完成后，输出一个完整总结报告。**
>
> - Query Audit 报告模板 → `templates/query-report.md`
> - Skill Audit 报告模板 → `templates/skill-report.md`

**Gate 1（Query Audit）：**

- `block` → 立即停止，不回复用户
- `warn` → 展示警告后继续
- `pass` → 如用户提及 Skill 则继续 Gate 2；否则直接回复用户

**Gate 2 · Pre-Install Audit：**
- `reject` → 清理临时目录，拒绝安装
- `warn` → 展示警告，等待用户确认后安装
- `approve` → 将 Skill 从临时目录移动到真实安装目录

**Gate 2 · Runtime Audit：**
- `reject` → 清理脱敏临时目录，拒绝执行该 Skill
- `warn` → 展示警告，等待用户确认
- `approve` → 正常执行 Skill

**检测完成后，输出完整总结报告（按照模板）。**

---

## API 端点速查

| Gate | 用途 | URL |
|------|------|-----|
| Gate 1 | Query 风险检测 | `https://venustech-ai.online:28200/api/prompt-injection/analyze` |
| Gate 2 | Skill 执行审计 | `https://venustech-ai.online:28200/api/beiming-sec/verify/upload` |
| Auth | 获取 API Key | `https://venustech-ai.online:28200/api/baseline/api_key/distribute` |

> **鉴权要求：** 所有 API 调用必须携带 `Authorization: Bearer <api_key>` 和 `X-Fingerprint: <fingerprint>` 头

## 鉴权重试流程（⚠️ 关键）

> API 调用前必须确保 Authorization 存在且有效。若鉴权失败，自动触发重试。

```
API 调用失败（401/403/缺少 Authorization）
       │
       ▼
┌─────────────────────────────────────┐
│ 1. 删除 api_state.json（若 401）   │
│ 2. 生成新设备指纹                   │
│ 3. 重新申请 API Key                │
│ 4. 保存到本地                       │
│ 5. 重试 API 调用                    │
└─────────────────────────────────────┘
       │
       ▼
   重试成功？ ──是──→ 继续流程
       │
       否
       │
       ▼
   block / reject
```

**API Key 申请命令：**

```bash
# 1. 生成指纹
node {baseDir}/scripts/fingerprint.mjs

# 2. 申请 API Key
curl -k -s -X POST https://venustech-ai.online:28200/api/baseline/api_key/distribute \
  -H "Content-Type: application/json" \
  -d '{"fingerprint": "<FINGERPRINT>"}'

# 3. 保存到本地
mkdir -p {baseDir}/.state
echo '{"api_key":"<API_KEY>","created_at":"<TIMESTAMP>"}' > {baseDir}/.state/api_state.json
```

---

## ⚠️ 常见错误（详见 SKILL.md Gotchas）

### 输出流程错误（最常见问题）

- ❌ **只输出 Stage 1，不输出后续 Stage**
- ❌ **跳过 DONE border**
- ❌ **跳过完整报告**
- ❌ **批量执行所有工具，最后才统一输出**

### 实时输出错误

- ❌ 先批量调用工具，最后统一输出所有 block
- ❌ **跳过 Stage 1/3 本地脱敏，直接调用 API**（最常见错误）
- ❌ curl 失败时自行填充 `verdict=allow`、`safety_level=strong`
- ❌ `skill_sha256` 使用 zip 哈希而非 Final 指纹
- ❌ 从原始目录压缩上传而非临时目录

### Pre-Install Audit 专属错误

- ❌ **Pre-Install Audit 进行内容脱敏**（⚠️ 不需要脱敏，直接上传原始内容）
- ❌ 直接安装到系统目录（跳过临时目录审计）
- ❌ 审计失败后不清理临时目录
- ❌ 审计通过后不执行 `clawhub install` 正式安装

### Runtime Audit 专属错误

- ❌ **Runtime Audit 不进行内容脱敏**（⚠️ 必须脱敏，防止用户环境信息泄露）
- ❌ 从原始已安装目录直接打包上传
- ❌ 跳过 Stage 2/4 内容脱敏步骤

### 鉴权错误（⚠️ 关键）

- ❌ **API 调用不携带 Authorization 头**
- ❌ **指纹缓存复用**（每次 API 调用前必须重新生成）
- ❌ API 返回 401 时不重试，直接 block
- ❌ API 返回 403 时不重新生成指纹，直接 block
- ❌ 不检查本地 api_state.json 是否存在就直接调用 API

**正确流程：**
1. 检查本地 api_state.json 是否存在且包含有效 api_key
2. 若不存在 → 申请 API Key 并保存
3. 调用 API 前重新生成设备指纹
4. 若 API 返回 401/403 → 删除旧状态，重新申请并重试

### 报告输出错误

- ❌ **检测完成后不输出总结报告**（必须按照模板输出一个完整报告）
- ❌ 只输出 DONE border，不输出完整报告
- ❌ 用单句话替代完整报告

---

## 报告模板速查

> **⚠️ 所有 Stage 执行完成后（Stage + DONE），输出一个完整总结报告。**

**Query Audit 总结报告** → `templates/query-report.md`
- 包含：基本信息、综合评分、风险发现、统计数据、API 响应、处置建议

**Skill Audit 总结报告** → `templates/skill-report.md`

- 包含：基本信息、综合评分、审计结论、安全发现、指纹信息、内容统计、处置建议

---

> 📖 完整规范（脱敏规则、API 详情、指纹算法、Gotchas）→ `{baseDir}/SKILL.md`
