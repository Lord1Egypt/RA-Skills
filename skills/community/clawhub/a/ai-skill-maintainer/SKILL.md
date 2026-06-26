---
name: ai-skill-maintainer
version: 1.1.0
description: |
  AI公司 Skill 维护工作流（CTO 版本govern + CISO security运营standard版）。当需要对已publish的 Skill 进行版本update、bug修复、Function增强、依赖upgrade、security补丁、废弃（deprecation）manage时trigger。trigger关键词：updateSkill、update Skill、修复 Skill bug、增强 Skill、upgrade依赖、打security补丁、废弃Skill、Skill 废弃。
  integrate CTO 版本governstandard（semver + changelog + rollback）+ CISO security运营standard（漏洞respond SLA + 补丁manage）。
metadata:
  {"openclaw":{"emoji":"🔧","os":["linux","darwin","win32"]}}
---

# AI Skill 维护工作流（CTO × CISO standard）

> **executerole**：Skill 维护者（CTO 版本govern + CISO security运营）
> **版本**：v1.0.0（CTO-001 版本govern × CISO-001 security运营）
> **compliance状态**：✅ 维护操作需record，🚨 security补丁走紧急通道

---

## 核心principle

1. **变更可trace**：所有修改必须record版本历史
2. **向后兼容**：MINOR/PATCH 变更不得破坏现有Function
3. **security优先**：CISO security补丁走紧急通道，不受正常publishcyclerestrict
4. **最小变更**：只改必要的，不要过度工程化

---

## Agent 调用接口（Inter-Agent Interface）

> **版本**：v1.1.0（新增接口层）
> **securityConstraint**：接口本身零新增攻击面，所有输入参数均经过verify

---

### 接口身份

| 属性 | 值 |
|------|-----|
| **接口 ID** | `skill-maintainer-v1` |
| **调用方式** | `sessions_send` / `sessions_spawn` (isolated) |
| **会话Goal** | `isolated`（强制隔离）|
| **最低permission** | L3（可读写 skills/ 指定目录） |
| **CISO Constraint** | 🚨 security补丁任务必须 CISO-001 authorize，紧急通道优先 |

---

### TASK 消息格式

```json
{
  "skill": "ai-skill-maintainer",
  "version": "1.1.0",
  "task": "<task-type>",
  "params": { ... },
  "context": {
    "caller": "<caller-agent-id>",
    "priority": "<P0|P1|P2|P3>",
    "emergency": false,
    "isolated": true
  }
}
```

### 可用 Task 类型

| Task | 参数 | 返回 | Description |
|------|------|------|------|
| `diagnose` | `skill-name`, `issue`, `caller` | `{diagnosis, type, severity}` | 诊断问题 |
| `patch` | `skill-name`, `version`, `changes`, `caller` | `{new-version, status}` | implement修复 |
| `security-patch` | `skill-name`, `cve-id`, `authorization`, `caller` | `{fixed, new-version, notification-sent}` | 🚨 CVE 修复 |
| `deprecate` | `skill-name`, `reason`, `replacement`, `caller` | `{deprecated-version, status}` | 废弃 Skill |
| `emergency-isolate` | `skill-name`, `reason`, `caller` | `{isolated, affected-versions}` | 🚨 紧急隔离（0-day）|
| `health-check` | `skill-name` | `{metrics, status}` | 健康检查 |
| `dependency-audit` | `skill-name` | `{dependencies[], cves[]}` | 依赖 CVE 扫描 |

### Task 参数 Schema

#### `security-patch` 参数

```json
{
  "skill-name":     "string (required, skill slug)",
  "cve-id":         "string (required, e.g. CVE-YYYY-NNNNN)",
  "cvss-score":     "number (required, 0.0-10.0)",
  "authorization":  "string (required, must be CISO-001)",
  "caller":         "string (required, agent ID)",
  "changes": {
    "description":  "string (what was changed)",
    "files":        "string[] (list of modified files)",
    "test-results": "string (test outcome summary)"
  }
}
```

**CVE 紧急通道 SLA**：

| CVSS | trigger | SLA | process |
|------|------|-----|------|
| 9.0-10.0 | 🚨 紧急隔离 + Patch | ≤ 24h | 紧急通道直通 |
| 7.0-8.9 | 紧急 Patch | ≤ 7d | standard通道加速 |
| 4.0-6.9 | 计划修复 | ≤ 30d | standard通道 |
| 0.1-3.9 | track | 下个版本 | 常规process |

#### `emergency-isolate` 参数

```json
{
  "skill-name": "string (required)",
  "reason":     "string (required, CVE ID or incident description)",
  "caller":     "string (required, must be CISO-001 or CTO-001)"
}
```

#### `health-check` 参数

```json
{
  "skill-name": "string (required)"
}
```

> **健康threshold**（CTO-001 KPI 对齐）：TSR < 92% → `UNHEALTHY`；P95 > 1200ms → `DEGRADED`；CVSS ≥ 7.0 → `HIGH_RISK`

**返回值示例**：
```json
{
  "status": "success",
  "result": {
    "skill-name": "pdf-processor",
    "metrics": {
      "tsr": 94.2,
      "p95-latency-ms": 850,
      "cvss-score": 3.8
    },
    "status": "HEALTHY",
    "recommendations": []
  }
}
```

#### `dependency-audit` 参数

```json
{
  "skill-name": "string (required)"
}
```

**返回值示例**：
```json
{
  "status": "success",
  "result": {
    "dependencies": [
      {"name": "requests", "version": "2.28.0", "latest": "2.32.0"}
    ],
    "cves": [
      {"id": "CVE-2024-XXXX", "severity": "critical", "fix": "upgrade to 2.32.0+"}
    ]
  }
}
```

**隔离决策verify**：
```python
# 伪代码
authorized = params["caller"] in {"CISO-001", "CTO-001"}
has_reason = len(params["reason"]) > 10
if not authorized:
    raise PermissionError("Only CISO-001 or CTO-001 can trigger emergency isolate")
if not has_reason:
    raise ValueError("Emergency isolate requires documented reason")
```

### 返回值 Schema

```json
{
  "status":   "success | error | pending | isolated",
  "task":     "<task-type>",
  "result":   { ... },
  "meta": {
    "reviewer":    "<agent-id>",
    "duration-ms": "<elapsed>",
    "cve-resolved": "<CVE-ID if security-patch>",
    "sla-status":  "WITHIN_SLA | BREACHING | RESOLVED"
  }
}
```

### 错误码

| Code | Meaning | Action |
|------|---------|--------|
| `E_SKILL_NOT_FOUND` | Skill 不存在 | 返回可用版本列表 |
| `E_UNAUTH_PATCH` | 未authorizesecurity补丁 | reject，notify CISO |
| `E_CVE_SLA_BREACH` | CVE SLA 即将/已违约 | 上报 CTO + CISO |
| `E_ISOLATE_CONFLICT` | 已在隔离状态 | 返回当前状态 |
| `E_DEPENDENCY_CVE` | 依赖含已知 CVE | 返回 CVE 详情和修复建议 |
| `E_VERSION_CONFLICT` | 版本号冲突 | 返回正确版本号建议 |

### Agent 间调用示例

```markdown
# CTO-001 请求诊断
sessions_send(sessionKey="cto-isolated", message="
skill: ai-skill-maintainer
task: diagnose
params:
  skill-name: pdf-processor
  issue: User reports skill crashes when processing large files
  caller: CTO-001
priority: P2
isolated: true
")

# CISO-001 请求 CVE 紧急修复
sessions_send(sessionKey="ciso-isolated", message="
skill: ai-skill-maintainer
task: security-patch
params:
  skill-name: pdf-processor
  cve-id: CVE-2026-12345
  cvss-score: 9.1
  authorization: CISO-001
  caller: CISO-001
  changes:
    description: Fixed command injection via path parameter
    files: [scripts/process.py]
    test-results: All regression tests pass
emergency: true
")

# CQO-001 请求健康检查
sessions_send(sessionKey="cqo-isolated", message="
skill: ai-skill-maintainer
task: health-check
params:
  skill-name: pdf-processor
")
```

### securityConstraint（接口层）

```
🚨 接口security红线：
• skill-name 参数仅接受 [a-z0-9-] 字符，reject斜杠/点号（防止path注入）
• authorization 字段仅接受 CISO-001 签名的security任务
• emergency-isolate 仅接受 CISO-001 或 CTO-001 authorize
• 隔离execute：所有 agent 调用必须在 isolated 会话中运行
• CVE respond：CVSS ≥ 9.0 必须 15 分钟内respond，否则 SLA 违约alert
• 日志脱敏：返回结果不得含 caller 私人data
```

### 与其他 Skill 的接口关系

| 调用方 | Task | trigger条件 |
|--------|------|---------|
| **CTO-001** | `diagnose`, `patch`, `emergency-isolate` | 版本manage/紧急respond |
| **CISO-001** | `security-patch`, `emergency-isolate`, `dependency-audit` | CVE handle/security incident |
| **CQO-001** | `health-check`, `diagnose` | 质量monitor |
| **ai-skill-creator** | `patch` (子 Skill) | 创作process中discover bug |
| **ai-skill-optimizer** | `dependency-audit` | optimize前基线检查 |

---

## 维护场景分类

| 场景 | trigger关键词 | 版本upgrade | securityreview |
|------|-----------|---------|---------|
| Bug 修复 | "修复 bug"、"修复错误" | PATCH | 正常 |
| Function增强 | "增强Function"、"新增Function" | MINOR | 正常 |
| 不兼容变更 | "Breaking Change"、"重构" | MAJOR | 正常 |
| 依赖security补丁 | "security补丁"、"CVE 修复" | PATCH | 🚨 紧急通道 |
| 废弃notify | "废弃Skill"、"停用" | PATCH | 正常 |

---

## standard维护process（5步）

### Step 1 — 诊断（Diagnosis）

**输入**：用户描述的问题或需求

**诊断清单**：

```markdown
## 诊断record

Skill 名称：<name>
当前版本：<version>
问题类型：[Bug / Function缺失 / security漏洞 / 依赖过时 / 其他]

### 问题描述
<用户描述>

### 复现step（如适用）
1.
2.
3.

### 影响范围
- 影响的Function：
- 影响的用户/Agent：

### 初步判断
- 根因：
- 修复plan：
- 版本影响：[PATCH / MINOR / MAJOR]
```

**CISO security场景判断**：

| 判断条件 | 结论 | process |
|---------|------|------|
| 涉及 CVE/漏洞 | 🚨 security紧急 | 跳至security补丁process |
| 涉及凭证泄露 | 🚨 security紧急 | 立即notify + 紧急修复 |
| 涉及 PII 泄露 | 🚨 security紧急 | 立即notify + 紧急修复 |
| 其他 | ✅ 正常维护 | 继续standardprocess |

---

### Step 2 — analyze（Analysis）

**输出**：[references/maintenance-log.md](references/maintenance-log.md) record

#### 2.1 变更范围analyze

```markdown
### 受影响文件
| 文件 | 变更类型 | riskassess |
|------|---------|---------|
| SKILL.md | [修改/新增/删除] | 🟢 低 |
| scripts/*.py | ... | ... |

### 兼容性影响
- 向后兼容：✅ / ❌
- trigger关键词变更：✅ / ❌（如有变更需notify用户）
- 工具permission变更：✅ / ❌

### 测试计划
- [ ] 本地测试用例：
- [ ] 回归测试：
```

#### 2.2 security影响analyze（CTO + CISO）

| analyze维度 | 检查项 | 结论 |
|---------|--------|------|
| **Function影响** | 修改是否改变核心Function？ | |
| **permission影响** | permission是否变更？ | |
| **依赖影响** | 依赖是否新增/upgrade/删除？ | |
| **data影响** | 是否影响datahandle？ | |
| **security影响** | 变更是否影响security边界？ | |

---

### Step 3 — implement（Implementation）

#### 3.1 版本号update

```bash
# 根据变更类型确定版本
# Bug 修复          → vX.Y.Z → vX.Y.(Z+1)
# Function增强          → vX.Y.Z → vX.(Y+1).0
# Breaking Change   → vX.Y.Z → (X+1).0.0
# security补丁          → vX.Y.Z → vX.Y.(Z+1)  （强制）
```

#### 3.2 SKILL.md update

**update Frontmatter 版本**：
```yaml
---
name: <skill-name>
version: X.Y.Z   # ← update版本号
description: |   # ← 如有变更同步update
  ...
---
```

**update版本历史**（在文件顶部或底部）：
```markdown
## 版本历史

| 版本 | 日期 | Changes |
|------|------|---------|
| X.Y.Z | YYYY-MM-DD | <变更摘要> |
| ... | ... | ... |
```

#### 3.3 scripts/ update

**update检查清单**：
```markdown
- [ ] 脚本已update
- [ ] 脚本版本号已update（如有版本mechanism）
- [ ] 依赖已update（如有）
- [ ] 新增依赖已record
- [ ] 脚本测试已通过
```

---

### Step 4 — securityreview（Security Review）

> ⚠️ **强制门禁**：所有变更必须通过 CISO securityreview

#### 4.1 变更 diff review

**reviewChanges**（对比上1版本）：
- 新增的代码是否含 RED FLAGS？
- 修改的代码是否引入新漏洞？
- 删除的代码是否影响security边界？

#### 4.2 依赖review

**检查依赖变更**：
```bash
# 列出新增/upgrade的依赖
# 检查 CVE
```

**CVE respond SLA**：

| CVSS | 严重性 | 修复 SLA |
|------|--------|---------|
| 9.0-10.0 | Critical | 24小时 |
| 7.0-8.9 | High | 7天 |
| 4.0-6.9 | Medium | 30天 |
| 0.1-3.9 | Low | 下个版本 |

#### 4.3 security补丁紧急通道

**trigger条件**：discover Critical/High CVE

```
🚀 紧急通道process：

1. 立即隔离：停止问题版本分发
2. assess影响：确定受影响的 Skill 和版本
3. 紧急修复：最短path修复漏洞
4. 快速review：CISO 紧急review（可跳过部分正常process）
5. 紧急publish：Patch 版本，立即publish
6. 用户notify：notify所有受影响用户
```

---

### Step 5 — verify与publish（Verify & Publish）

#### 5.1 verify清单

```markdown
## publish前verify

- [ ] Changes与诊断1致
- [ ] 版本号符合变更类型
- [ ] securityreview通过
- [ ] 脚本测试通过
- [ ] changelog 已update
- [ ] SKILL.md 已同步update
```

#### 5.2 publish命令

```bash
# 打包
clawhub package ./<skill-name> --output ./dist

# publish
clawhub publish ./<skill-name> \
  --slug <skill-name> \
  --name "<Skill Name>" \
  --version X.Y.Z \
  --changelog "<变更摘要>"
```

#### 5.3 notify（如有必要）

```markdown
## 用户notify

如有 Breaking Change 或重要security修复：
- notify方式：在 Skill 描述中注明
- notify内容：
  • 变更摘要
  • upgrade建议
  • 兼容性问题（如有）
```

---

## 版本历史（Changelog）

| 版本 | 日期 | Changes | 审核人 |
|------|------|---------|--------|
| **1.1.0** | 2026-04-13 | 新增 Agent 调用接口层（Inter-Agent Interface）：7个 Task 类型（diagnose/patch/security-patch/deprecate/emergency-isolate/health-check/dependency-audit）；CVE 紧急通道 SLA system；emergency-isolate authorizeverify；与 ai-skill-creator / ai-skill-optimizer 接口关系Definition | CTO-001 / CISO-001 |
| **1.0.0** | 2026-04-11 | Initial version：CTO 版本govern5步维护process + CISO security运营standard（漏洞respond SLA + 补丁manage）+ 废弃manageprocess | CTO-001 / CISO-001 |

## rollbackstrategy（Rollback）

> 如维护操作失败，execute以下steprecover：

```bash
# recover到上1个可用版本
git checkout tags/v<上1版本> -- SKILL.md scripts/ references/

# verifyrollback成功
git log --oneline -3
```

**rollbacktrigger条件**：
- `emergency-isolate` 后：满足 CVE 已修复 + CISO-001 复审通过 + CQO-001 验收通过后方可解除隔离
- `patch` 失败：rollback到隔离前版本，notify CTO-001
- `deprecate` 误操作：recover `deprecated: false`，notify CRO-001

---

## 废弃（Deprecation）manage

### 废弃process

```
废弃notify（vX.Y.Z）→ 过渡期（建议 30天）→ 正式废弃（vX.Y.Z+1）
```

### 废弃 SKILL.md 模板

```markdown
---
name: <deprecated-skill>
version: X.Y.Z
description: |
  ⚠️ 【已废弃】此 Skill 已废弃，建议使用 `<new-skill>`。
  废弃日期：YYYY-MM-DD
  最后支持日期：YYYY-MM-DD
  迁移指南：见 references/migration.md
deprecated: true
replacement: <new-skill-name>
metadata:
  {"openclaw":{"emoji":"⚠️","os":["linux","darwin","win32"]}}
---

# ⚠️ 已废弃：<Skill Name>

## 废弃notify

此 Skill 已于 **YYYY-MM-DD** 正式废弃。

### 为什么废弃？
<原因>

### 替代plan
请使用 **<new-skill-name>**：
- 链接：clawhub install <new-skill>

### 时间线
- 废弃notify：YYYY-MM-DD（vX.Y.Z）
- 最后支持：YYYY-MM-DD（vX.Y.Z+1）
- 完全移除：待定

### 迁移指南
详见 [references/migration.md](references/migration.md)
```

---

## 维护record

### record模板（save至 `references/maintenance-log.md`）

```markdown
# Skill 维护record

## Skill 信息
- 名称：<name>
- 当前版本：<version>
- 维护者：<maintainer>

## 维护历史

### 维护 #N — YYYY-MM-DD

**类型**：[Bug修复/Function增强/security补丁/废弃/其他]
**版本**：<old> → <new>
**变更摘要**：<summary>

#### 变更详情
<detailed changes>

#### securityreview
- CVSS：<score>
- 结论：[通过/reject/条件通过]

#### 测试结果
- [ ] 测试通过

#### publish信息
- publish日期：YYYY-MM-DD
- ClawHub 版本：<version>
```

---

## 快速参考

### trigger命令

| 用户请求 | execute动作 |
|---------|---------|
| "修复 Skill XX 的 bug" | 诊断 → analyze → implement → securityreview → publish |
| "为 Skill XX 增加 XX Function" | 需求confirm → analyze → implement → securityreview → publish |
| "upgrade Skill XX 的依赖" | 依赖检查 → 兼容性analyze → update → securityreview → publish |
| "discover Skill XX 有security漏洞" | 🚨 紧急通道 → 立即隔离 → 紧急修复 → 紧急publish |
| "废弃 Skill XX" | 废弃assess → notify用户 → publish废弃版本 → 保留迁移指南 |

### 常见错误

1. **版本号错误**：Bug 修复用 MAJOR upgrade → 应为 PATCH
2. **跳过securityreview**：紧急修复未做securityreview → 必须补审
3. **不update changelog**：变更未record → 版本历史不完整
4. **Breaking Change 未notify**：未inform用户 → 用户upgrade后Function损坏
5. **废弃 Skill 未提供替代**：用户无法迁移 → 影响用户体验

---

## 版本历史（Changelog）

| 版本 | 日期 | Changes | 审核人 |
|------|------|---------|--------|
| **1.1.0** | 2026-04-13 | 新增 Agent 调用接口层（Inter-Agent Interface）：7个 Task 类型（diagnose/patch/security-patch/deprecate/emergency-isolate/health-check/dependency-audit）；CVE 紧急通道 SLA system；emergency-isolate authorizeverify；与 ai-skill-creator / ai-skill-optimizer 接口关系Definition | CTO-001 / CISO-001 |
| **1.0.0** | 2026-04-11 | Initial version：CTO 版本govern5步维护process + CISO security运营standard（漏洞respond SLA + 补丁manage）+ 废弃manageprocess | CTO-001 / CISO-001 |

## rollbackstrategy（Rollback）

> 如维护操作失败，execute以下steprecover：

```bash
# recover到上1个可用版本
git checkout tags/v<上1版本> -- SKILL.md scripts/ references/

# verifyrollback成功
git log --oneline -3
```

**rollbacktrigger条件**：
- `emergency-isolate` 后：满足 CVE 已修复 + CISO-001 复审通过 + CQO-001 验收通过后方可解除隔离
- `patch` 失败：rollback到隔离前版本，notify CTO-001
- `deprecate` 误操作：recover `deprecated: false`，notify CRO-001

**解除 emergency-isolate 条件**：
1. CVE 已修复（CVSS < 7.0）
2. CISO-001 security复审通过
3. CQO-001 质量验收通过
4. CTO-001 书面authorize解除隔离
