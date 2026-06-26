---
name: ai-skill-creator
version: 1.1.0
description: |
  AI公司 Skill 创作工作流（CTO MLOps + CISO securitystandard版）。当需要从头create新 Skill（包括初始化目录结构、编写 SKILL.md、引用文件、脚本资源、securityreview、quality gate）时使用。trigger关键词：createSkill、新建 Skill、开发 Skill、create skill、新建Skill包。integrate CTO MLOps 生命cycle6phase + CISO securityreviewstandard（STRIDE + CVSS + security门禁），最终输出符合 ClawHub/VirusTotal reviewstandard的可publish .skill 包。
metadata:
  {"openclaw":{"emoji":"🛠️","os":["linux","darwin","win32"]}}
---

# AI Skill 创作工作流（CTO × CISO standard）

> **executerole**：Skill 开发者（CTO 技术栈 + CISO security护栏）
> **版本**：v1.0.0（CTO-001 MLOps 生命cycle × CISO-001 securityreview）
> **compliance状态**：✅ CISO securityreview后publish，⚠️ prohibit跳过security门禁

---

## 核心principle

1. **CTO MLOops 生命cycle**：所有 Skill 必须走6phasestandardprocess
2. **CISO security门禁**：每个phase内置security检查，security未通过不得进入下1phase
3. **零信任架构**：所有脚本/资源必须经过securityreview，prohibit引入恶意代码
4. **渐进式披露**：SKILL.md 精简（<500行），详细文档放 references/

---

## Agent 调用接口（Inter-Agent Interface）

> **版本**：v1.1.0（新增接口层）
> **securityConstraint**：接口本身零新增攻击面，所有输入参数均经过verify

---

### 接口身份

| 属性 | 值 |
|------|-----|
| **接口 ID** | `skill-creator-v1` |
| **调用方式** | `sessions_send` / `sessions_spawn` (isolated) |
| **会话Goal** | `isolated`（强制隔离，防止交叉污染）|
| **最低permission** | L3（可读 workspace，可写 skills/） |
| **CISO Constraint** | 🚨 securityreview任务（`security-review`）必须 CISO-001 authorize |

---

### TASK 消息格式

```json
{
  "skill": "ai-skill-creator",
  "version": "1.1.0",
  "task": "<task-type>",
  "params": { ... },
  "context": {
    "caller": "<caller-agent-id>",
    "priority": "<P0|P1|P2|P3>",
    "security-review-required": true,
    "isolated": true
  }
}
```

### 可用 Task 类型

| Task | 参数 | 返回 | Description |
|------|------|------|------|
| `create` | `name`, `description`, `version`, `risk-level`, `caller` | `{dir, status}` | create新 Skill |
| `design-review` | `skill-name`, `design-doc`, `caller` | `{issues[], status}` | design文档review |
| `security-review` | `skill-path`, `caller`, `authorization` | `{cvss, flags[], verdict}` | 🚨 CISO authorizesecurityreview |
| `quality-gate` | `skill-path`, `gate-level` | `{passed[], failed[], verdict}` | quality gate检查 |
| `package` | `skill-path`, `output-dir` | `{artifact, checksum}` | 打包为 .skill |
| `publish` | `skill-path`, `slug`, `version`, `changelog` | `{url, version}` | publish到 ClawHub |

### Task 参数 Schema

#### `create` 参数

```json
{
  "name":        "string (required, [a-z][a-z0-9-]{2,64})",
  "description": "string (required, >50 chars, describes triggers + actions)",
  "version":     "string (required, semver X.Y.Z)",
  "risk-level":  "low | medium | high | critical",
  "caller":     "string (required, agent ID of requester)",
  "refs": {
    "design-doc":   "string (optional, path to references/design.md)",
    "security-notes": "string (optional, security considerations)"
  }
}
```

**输入verify规则**：
- `name`：正则 `^[a-z][a-z0-9-]{2,64}$`，prohibit `..`、`/`、空格
- `description`：长度 > 50 字符，否则rejectcreate
- `version`：semver 格式verify，不符则reject
- `risk-level`：`critical` trigger强制 CISO 双审

#### `security-review` 参数

```json
{
  "skill-path":    "string (required, absolute path to skill dir)",
  "caller":        "string (required, agent ID)",
  "authorization":  "string (required, must be CISO-001 for critical/high)",
  "scan-depth":    "basic | full (default: full)"
}
```

**authorizeverify**：
```python
# 伪代码verify逻辑
if params["skill-path"].contains(".."):
    raise PermissionError("Path traversal rejected")

if risk_level == "critical" and params["authorization"] != "CISO-001":
    raise PermissionError("Critical risk requires CISO-001 authorization")

if not params["skill-path"].startswith(trusted_base_dirs):
    raise PermissionError("Skill path outside trusted directories")
```

### 返回值 Schema

```json
{
  "status":  "success | error | pending | rejected",
  "task":    "<task-type>",
  "result":  { ... },
  "meta": {
    "reviewer":    "<agent-id>",
    "duration-ms": "<elapsed>",
    "cvss-score":  "<if security-review>",
    "verdict":     "APPROVED | CONDITIONAL | REJECTED"
  }
}
```

### 错误码

| Code | Meaning | Action |
|------|---------|--------|
| `E_NAME_INVALID` | Skill 名称不compliance | 返回verify错误，不create |
| `E_PATH_TRAVERSAL` | path含 `..` | reject，reportsecurity incident |
| `E_UNAUTH` | 未authorizeexecutesecurityreview | reject，notify CISO |
| `E_CVSS_HIGH` | CVSS ≥ 7.0 | rejectpublish，trigger修复process |
| `E_GATE_FAILED` | quality gate未通过 | 返回 failed 项列表 |
| `E_DUPLICATE` | Skill slug 已存在 | reject，建议新名称 |

### Agent 间调用示例

```markdown
# CTO-001 请求create Skill
sessions_send(sessionKey="cto-isolated", message="
skill: ai-skill-creator
task: create
params:
  name: pdf-processor
  description: PDF processing skill. Triggers: read PDF, split PDF, merge PDF, rotate PDF.
  version: 1.0.0
  risk-level: low
  caller: CTO-001
security-review-required: false
")

# CISO-001 请求securityreview
sessions_send(sessionKey="ciso-isolated", message="
skill: ai-skill-creator
task: security-review
params:
  skill-path: C:/Users/Admin/.qclaw/skills/pdf-processor
  caller: CISO-001
  authorization: CISO-001
  scan-depth: full
")
```

### securityConstraint（接口层）

```
🚨 接口security红线：
• skill-path 参数reject任何含 .. 的path（path遍历defend）
• authorization 字段仅接受 CISO-001 签名的review任务
• 隔离execute：所有 agent 调用必须在 isolated 会话中运行
• 日志脱敏：返回结果不得含 caller 私人data
• 最小respond：返回结果仅包含必要字段，不暴露内部实现
```

### 与其他 Skill 的接口关系

| 调用方 | Task | trigger条件 |
|--------|------|---------|
| **CTO-001** | `create`, `package`, `publish` | 新 Skill 开发立项 |
| **CISO-001** | `security-review` | securityreviewauthorize |
| **CQO-001** | `quality-gate` | 质量验收 |
| **ai-skill-maintainer** | `create` (子 Skill) | 维护process需新建子 Skill |
| **ai-skill-optimizer** | `quality-gate` | optimize后质量复验 |

---

## 6phase创作process（MLOps Lifecycle for Skill）

### Phase 0 — 准备：create目录结构

**强制使用 init_skill.py 脚本**，prohibit手动 mkdir：

```powershell
# Windows
python.exe <openclaw_path>\skills\skill-creator\scripts\init_skill.py <skill-name> --path ~/.qclaw/skills

# Linux/macOS
python3 <openclaw_path>/skills/skill-creator/scripts/init_skill.py <skill-name> --path ~/.qclaw/skills
```

生成结构：
```
~/.qclaw/skills/<skill-name>/
├── SKILL.md           # 主文件（必需）
├── scripts/          # 可execute脚本
├── references/        # 参考文档
└── assets/           # 静态资源
```

> ⚠️ **CISO security规则**：不得在 `resources/openclaw/config/skills/` 下create Skill（系统目录，会在update时清空）

---

### Phase 1 — 需求analyze（Ideation）

**输入**：用户描述 Skill 用途、trigger场景、GoalFunction

**输出**：Skill design文档（写入 `references/design.md`）

**必须回答**：
1. Skill 的核心Function是什么？trigger条件是什么？
2. 需要哪些工具permission？（read/write/exec/network）
3. 是否涉及敏感data？（PII/凭证/密钥）
4. 最小permissionprinciple：能否用更少的permission实现？
5. Skill 之间的依赖关系？

**CISO securityassess（Phase 1 输出）**：

| assess项 | 问题 | 决策 |
|--------|------|------|
| 敏感data访问 | 是否读取 MEMORY.md/USER.md/SOUL.md？ | 🚨 需明确Description用途 |
| 外部网络 | 是否调用外部 API？ | 🚨 列出域名/IP |
| 命令execute | 是否需要 exec/bash？ | 🚨 列出所需命令 |
| 凭证请求 | 是否要求用户提供密钥？ | 🚨 reject，优先用环境变量 |
| 文件写入 | 写入范围是否限定在 workspace？ | ✅ 是，❌ 否则重design |

**security决策**：任意 🚨 项未resolve → 停止，notify用户

---

### Phase 2 — 架构design

**输出**：`references/architecture.md`

**designstandard**：

#### SKILL.md 结构standard
```markdown
---
name: <skill-name>
version: X.Y.Z
description: |   # 必需，描述trigger时机和Function范围（>50字）
  <trigger关键词> → <execute动作>
  当用户<做什么>时trigger，execute<什么Function>
metadata:
  {"openclaw":{"emoji":"<emoji>","os":["linux","darwin","win32"]}}
---

# <Skill 名称>

## Overview（<10行）

## 核心Function（模块化，每个<50行）

## security考虑（如有）

## 常见错误
```

#### Frontmatter 必需字段

| 字段 | 要求 | 示例 |
|------|------|------|
| `name` | 英文小写+连字符 | `pdf-processor` |
| `version` | semver X.Y.Z | `1.0.0` |
| `description` | >50字，描述trigger时机 | 见上方模板 |
| `metadata.openclaw.emoji` | 1个 emoji | `"🔒"` |
| `metadata.openclaw.os` | 支持的 OS | `["linux","win32"]` |

#### 目录结构standard
- ✅ `SKILL.md`（必需）
- ✅ `scripts/`（可选，脚本需测试）
- ✅ `references/`（可选，详细文档放此处）
- ✅ `assets/`（可选，静态资源）
- ❌ `README.md`（prohibit）
- ❌ `CHANGELOG.md`（prohibit）
- ❌ `INSTALLATION_GUIDE.md`（prohibit）

**CISO security架构review**：

| 威胁类型（STRIDE）| defend措施 |
|-----------------|---------|
| **S**poofing | Skill 名称不得伪造系统命令 |
| **T**ampering | 所有文件path需verify，不接受动态path拼接用户输入 |
| **I**nfo Disclosure | prohibit在 Skill 中硬编码密钥/令牌 |
| **D**enial of Service | prohibit无限循环/递归的文件操作 |
| **E**levation | permission不得超出design范围 |

---

### Phase 3 — 实现（Implementation）

**输出**：完整的 `SKILL.md`、`scripts/`、`references/`、`assets/`

#### SKILL.md 编写standard

**描述字段（description）必须包含**：
1. **trigger关键词**（用户说什么会激活此 Skill）
2. **execute动作**（Skill 做什么）
3. **文件格式**（输入/输出文件类型）
4. **security边界**（如果涉及敏感操作）

**Body 编写principle**：
- 使用命令式/不定式语气（"Use X to do Y"，"Do not use Z"）
- 避免冗余解释（Claude 已经很聪明）
- 代码示例优先于文字Description
- 引用文件链接到 `references/`（渐进式披露）

#### 脚本编写standard

**必须遵守**：
```markdown
## 脚本security红线（🚨 违反即reject）

🚫 prohibit：
• curl/wget 到未知 URL
• 将data发送到外部服务器
• 请求凭证/令牌/API密钥（环境变量接收除外）
• 读取 ~/.ssh ~/.aws ~/.config 等敏感目录
• 访问 MEMORY.md USER.md SOUL.md IDENTITY.md
• 使用 base64 decode 未知内容
• 使用 eval()/exec() handle外部输入
• 修改 workspace 外的系统文件
• 安装包但不列出所需依赖
• 网络调用到裸 IP（非域名）
• 混淆代码（压缩/编码/混淆）
• 请求enhancepermission/sudo
• 访问浏览器 cookie/session
```

**脚本必须包含**：
1. 用途Description（注释）
2. 输入参数Description
3. 输出Description
4. 错误handle
5. security检查（如适用）

#### 资源文件standard

| 资源类型 | 存放位置 | standard |
|---------|---------|------|
| 参考文档 | `references/` | >100行需加目录导航 |
| 脚本 | `scripts/` | 需可execute测试 |
| 静态资源 | `assets/` | 不加载到上下文 |

---

### Phase 4 — securityreview（Security Review）

> ⚠️ **强制门禁**：CISO review必须通过，否则prohibitpublish

**reviewprocess**：

#### Step 1：代码review（MANDATORY）

逐文件review，查找以下 **RED FLAGS**：

```
🚨 REJECT IMMEDIATELY IF YOU SEE:
─────────────────────────────────────────
• curl/wget → 未知 URL
• data发送 → 外部服务器
• 凭证请求 → 密钥/令牌
• 读取 ~/.ssh ~/.aws ~/.config
• 访问 MEMORY/USER/SOUL/IDENTITY.md
• base64 decode → 未知内容
• eval() / exec() → 外部输入
• 修改 workspace 外文件
• 安装包 → 未列依赖
• 网络调用 → 裸 IP
• 混淆代码
• 请求 sudo/enhancepermission
• 访问浏览器 cookie
• 接触凭证文件
─────────────────────────────────────────
```

#### Step 2：permissionassess

| permission类型 | 检查项 | 决策 |
|---------|--------|------|
| 文件读取 | 列出所有读取path | verify合理性 |
| 文件写入 | 列出所有写入path | 限定 workspace |
| 命令execute | 列出所有命令 | verify必要性 |
| 网络访问 | 列出所有域名/IP | verify可信度 |

#### Step 3：依赖扫描

```bash
# 检查脚本中声明的依赖
# Node.js: npm list <package>
# Python: pip freeze | grep <package>
# verify无已知 CVE（CVSS ≥ 7.0）
```

#### Step 4：漏洞评分（CVSS）

| CVSS | 严重性 | 决策 |
|------|--------|------|
| 9.0-10.0 | Critical | 🚫 rejectpublish |
| 7.0-8.9 | High | 🚫 rejectpublish，修复后重审 |
| 4.0-6.9 | Medium | ⚠️ notify用户，可修复后publish |
| 0.1-3.9 | Low | ✅ 通过 |

#### Step 5：STRIDE 威胁建模

| 威胁 | assess问题 | defendplan |
|------|---------|---------|
| S | Skill 名称是否可被劫持？ | prohibit与系统命令同名 |
| T | path参数是否可注入？ | verify输入，reject `../` |
| R | 操作是否可否认？ | record操作日志（引用文件） |
| I | 敏感data是否泄露？ | PII 过滤，密钥不放代码 |
| D | 是否有 DoS risk？ | 资源restrict，超时中断 |
| E | permission是否超出最小permission？ | review工具permission列表 |

**securityreviewreport模板**：

```
════════════════════════════════════════════════════
SKILL SECURITY REVIEW REPORT
════════════════════════════════════════════════════
Skill: <name>
Version: <version>
Reviewer: CISO-001
Date: <ISO date>
────────────────────────────────────────────────────
🔴 RED FLAGS: [None / List with CVSS scores]

🟡 PERMISSIONS REVIEW:
• Files Read:  [list]
• Files Write: [list]
• Commands:    [list]
• Network:     [list]

🟢 STRIDE MODELING:
• S (Spoofing):  [Pass/Fail] — <reason>
• T (Tampering): [Pass/Fail] — <reason>
• R (Repudiation):[Pass/Fail] — <reason>
• I (Info Disclosure): [Pass/Fail] — <reason>
• D (Denial of Service):[Pass/Fail] — <reason>
• E (Elevation):  [Pass/Fail] — <reason>

📊 CVSS SCORE: <X.Y> (<severity>)
────────────────────────────────────────────────────
VERDICT: [✅ APPROVED / 🚫 REJECTED / ⚠️ CONDITIONAL]

ACTION ITEMS: [list if any]
════════════════════════════════════════════════════
```

---

### Phase 5 — quality gate（Quality Gate）

**CTO 强制quality gate（全部通过方可publish）**：

| 质量门 | 检查项 | 工具/方法 | 通过standard |
|--------|--------|---------|---------|
| **G0** 文件结构 | 目录结构符合standard | 人工检查 | 4个目录齐全 |
| **G1** Frontmatter | YAML 格式正确，必需字段存在 | 解析 YAML | name/description/version/emoji 齐全 |
| **G2** 描述质量 | description > 50字，含trigger关键词 | 人工review | 包含trigger时机+execute动作 |
| **G3** security扫描 | 无 RED FLAGS，无高危漏洞 | Phase 4 review | CVSS < 7.0 |
| **G4** 文档完整性 | 核心process有Description，引用文件有链接 | 人工review | 无悬空引用 |
| **G5** 脚本测试 | scripts/ 下脚本可execute | 实际运行测试 | 零报错 |

**Quality Gate Checklist**（save至 `references/quality-gate.md`）：

```markdown
## Quality Gate Checklist

- [ ] G0: 目录结构正确（SKILL.md + scripts/ + references/ + assets/）
- [ ] G1: Frontmatter 完整（name, version, description, emoji）
- [ ] G2: description > 50字，含trigger关键词
- [ ] G3: CISO securityreview通过（CVSS < 7.0，STRIDE 无 FAIL）
- [ ] G4: references/ 中文档有链接Description，无悬空引用
- [ ] G5: 所有 scripts/ 脚本已测试，零报错
- [ ] G6: SKILL.md < 500行（渐进式披露正确）
- [ ] G7: 无prohibit文件（README.md/CHANGELOG.md 等）
```

---

### Phase 6 — 打包与publish（Package & Publish）

**使用 package_skill.py 打包**：

```powershell
# Windows
python.exe <openclaw_path>\skills\skill-creator\scripts\package_skill.py <path/to/skill-folder> <output-dir>

# Linux/macOS
python3 <openclaw_path>/skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> <output-dir>
```

**打包脚本自动execute**：
1. ✅ verify YAML frontmatter 格式
2. ✅ 检查 Skill 命名standard
3. ✅ verify目录结构
4. ✅ 检查 description 完整性
5. ✅ confirm文件组织
6. ✅ 打包为 `.skill` 文件

**publish到 ClawHub**：

```bash
# 登录（如需publish到公共仓库）
clawhub login

# publish
clawhub publish ./<skill-name> \
  --slug <skill-name> \
  --name "<Skill 显示名称>" \
  --version X.Y.Z \
  --changelog "<变更Description>"
```

**publish前最终检查**：

```markdown
## publish前 Checklist

- [ ] CISO securityreviewreport已生成（Phase 4）
- [ ] Quality Gate 全部通过（Phase 5）
- [ ] .skill 包文件已生成
- [ ] 版本号符合 semver（X.Y.Z）
- [ ] Changelog 已写入（如果已有历史版本）
- [ ] ClawHub slug 已confirm唯1性
```

---

## 快速参考

### trigger命令

```
"create Skill" / "新建Skill" / "开发 Skill" / "create1个Skill包"
```

### 自然语言指令映射

| 用户请求 | execute动作 |
|---------|---------|
| "create1个读取 PDF 的 Skill" | 初始化 → 需求analyze → 架构design → 实现 → securityreview → 打包 |
| "帮我写1个handle Excel 的Skill" | 同上，参考 xlsx skill design模式 |
| "需要1个新 Skill 来做 XX" | 需求analyze → confirmtrigger时机和permission |

### 常见错误

1. **跳过securityreview**：Phase 4 是强制门禁，不得跳过
2. **手动create目录**：必须使用 init_skill.py
3. **SKILL.md 过长**：超过 500 行 → 拆分到 references/
4. **description 过短**：< 50 字 → trigger时机不明确，Skill 无法激活
5. **引入prohibit文件**：README.md/CHANGELOG.md → 删除
6. **硬编码密钥**：🚫 reject，必须用环境变量

---

## 参考文件

- `references/design.md` — 需求analyze模板和架构design指南
- `references/security-review.md` — 详细 CISO securityreview清单
- `references/quality-gate.md` — quality gate检查表
- `references/publish-guide.md` — ClawHub publish指南

---

## 版本历史（Changelog）

| 版本 | 日期 | Changes | 审核人 |
|------|------|---------|--------|
| **1.1.0** | 2026-04-13 | 新增 Agent 调用接口层（Inter-Agent Interface）：6个 Task 类型（create/design-review/security-review/quality-gate/package/publish）；CISO securityConstraint和security红线；与 ai-skill-maintainer / ai-skill-optimizer 接口关系Definition；CLO compliance登记节点；Day 3 预算概算 | CTO-001 / CISO-001 |
| **1.0.0** | 2026-04-11 | Initial version：CTO MLOops 6phase创作process + CISO STRIDE securityreviewstandard + G0-G7 quality gate | CTO-001 / CISO-001 |

## rollbackstrategy（Rollback）

> 如任何phase失败，execute以下操作recover：

```bash
# recover到上1个 Git tag
git checkout tags/v<上1版本> -- .

# 或使用快照包（如果有）
clawhub restore ./dist/<skill-name>-v<X.Y.Z>.skill

# verifyrollback成功
git log --oneline -3
```

**rollbacktrigger条件**：
- Phase 3（G2 securityreview）失败 → rollback到 Phase 2
- Phase 4（G3 quality gate）失败 → rollback到 Phase 3
- Phase 6（publish）失败 → rollback到 Phase 5

**rollback后操作**：
1. recordrollback原因到 `references/creation-log.md`
2. notify CTO-001 和 CISO-001
3. analyze失败原因后重新进入创作process
