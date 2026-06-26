---
name: ai-skill-optimizer
version: 1.1.0
description: |
  AI公司 Skill optimize工作流（CTO 性能工程 + CISO securityoptimizestandard版）。当需要对现有 Skill 进行性能optimize、Token 节省、上下文精简、security加固、代码重构、质量enhance时trigger。trigger关键词：optimizeSkill、optimize Skill、节省 Token、精简 Skill、重构 Skill、enhance Skill 质量、security加固 Skill。
  integrate CTO 性能工程方法论（TTFT/P95 latency/吞吐optimize）+ CISO security加固standard（STRIDE 强化 + 攻击面缩小）。
metadata:
  {"openclaw":{"emoji":"⚡","os":["linux","darwin","win32"]}}
---

# AI Skill optimize工作流（CTO × CISO standard）

> **executerole**：Skill optimize者（CTO 性能工程 + CISO security加固）
> **版本**：v1.0.0（CTO-001 性能optimize × CISO-001 security加固）
> **compliance状态**：✅ optimize前必须做影响analyze，🚨 security加固优先于性能optimize

---

## 核心principle

1. **security第1**：security加固优先于性能optimize，不得以牺牲security换取性能
2. **可量化**：optimize必须有明确的metric改善（Token 节省、latency降低等）
3. **无回归**：optimize后Function必须与optimize前完全1致
4. **渐进式**：每次optimize聚焦1个维度，便于定位问题

---

## Agent 调用接口（Inter-Agent Interface）

> **版本**：v1.1.0（新增接口层）
> **securityConstraint**：接口本身零新增攻击面，所有输入参数均经过verify

---

### 接口身份

| 属性 | 值 |
|------|-----|
| **接口 ID** | `skill-optimizer-v1` |
| **调用方式** | `sessions_send` / `sessions_spawn` (isolated) |
| **会话Goal** | `isolated`（强制隔离）|
| **最低permission** | L3（可读 skills/，可写optimize结果） |
| **CISO Constraint** | 🚨 security加固任务（`security-harden`）必须 CISO-001 authorize |

---

### TASK 消息格式

```json
{
  "skill": "ai-skill-optimizer",
  "version": "1.1.0",
  "task": "<task-type>",
  "params": { ... },
  "context": {
    "caller": "<caller-agent-id>",
    "priority": "<P0|P1|P2|P3>",
    "optimization-dimension": "<token|performance|security|quality|full>",
    "isolated": true
  }
}
```

### 可用 Task 类型

| Task | 参数 | 返回 | Description |
|------|------|------|------|
| `baseline` | `skill-name`, `caller` | `{tokens, p95-latency, cvss, red-flags}` | optimize前baseline测量 |
| `token-optimize` | `skill-name`, `target-savings`, `caller` | `{before, after, savings-pct}` | Token optimize |
| `performance-optimize` | `skill-name`, `target-latency`, `caller` | `{before, after, p95-ms}` | 性能optimize |
| `security-harden` | `skill-name`, `authorization`, `caller` | `{cvss-before, cvss-after, improvements[]}` | 🚨 security加固 |
| `quality-improve` | `skill-name`, `target-quality`, `caller` | `{quality-before, quality-after, changes[]}` | 质量enhance |
| `full-optimize` | `skill-name`, `dimensions[]`, `caller` | `{all-metrics}` | 全维度optimize |

> **`dimensions[]` 可选值**：`"token"` \| `"performance"` \| `"security"` \| `"quality"`（默认全部）
| `compare` | `skill-name` | `{baseline, current, delta}` | optimize前后对比report |

### Task 参数 Schema

#### `baseline` 参数

```json
{
  "skill-name": "string (required, skill slug)",
  "caller":     "string (required, agent ID)"
}
```

**返回示例**：
```json
{
  "status": "success",
  "result": {
    "skill-name": "pdf-processor",
    "version":    "1.0.0",
    "tokens":     {
      "skill-md":   4200,
      "references": 1850,
      "scripts":    320,
      "total":      6370
    },
    "performance": {
      "p95-latency-ms": 850,
      "avg-latency-ms": 420
    },
    "security": {
      "cvss-score":  5.3,
      "red-flags":   0,
      "stride-passes": 6
    },
    "quality": {
      "quality-gate-score": 7,
      "gates-passed": 5,
      "gates-failed": 2
    }
  }
}
```

#### `security-harden` 参数

```json
{
  "skill-name":    "string (required)",
  "authorization": "string (required, must be CISO-001)",
  "hardening-target": "critical | high | medium (default: high)",
  "caller":        "string (required)"
}
```

**输入verify**：
```python
# 伪代码
if params["skill-name"].contains("..") or "/" in params["skill-name"]:
    raise ValueError("Invalid skill-name: path traversal detected")
if params["authorization"] != "CISO-001":
    raise PermissionError("security-harden requires CISO-001 authorization")
```

### 返回值 Schema

```json
{
  "status":   "success | error | pending | no-improvement-needed",
  "task":     "<task-type>",
  "result": {
    "skill-name":  "<name>",
    "version-before": "<version>",
    "version-after":  "<version>",
    "improvements":   [ ... ],
    "metrics": { ... }
  },
  "meta": {
    "reviewer":    "<agent-id>",
    "duration-ms": "<elapsed>",
    "savings": {
      "tokens":  "<N tokens saved>",
      "latency": "<N ms saved>",
      "cvss":    "<before → after>"
    }
  }
}
```

### 错误码

| Code | Meaning | Action |
|------|---------|--------|
| `E_SKILL_NOT_FOUND` | Skill 不存在 | 返回错误 |
| `E_NO_IMPROVEMENT` | optimize收益 < 5% | 返回当前metric，停止无效optimize |
| `E_REGRESSION` | optimize导致Function退化 | 自动rollback，report regression |
| `E_UNAUTH_HARDEN` | 未authorizesecurity加固 | reject，notify CISO |
| `E_SECURITY_REGRESSION` | 加固后 CVSS 恶化 | reject，triggerrollback |
| `E_NO_BASELINE` | 无baselinedata | 先execute baseline 再optimize |

### Agent 间调用示例

```markdown
# CTO-001 请求全维度optimize
sessions_send(sessionKey="cto-isolated", message="
skill: ai-skill-optimizer
task: full-optimize
params:
  skill-name: pdf-processor
  dimensions: [token, performance]
  caller: CTO-001
context:
  priority: P1
  optimization-dimension: full
isolated: true
")

# CISO-001 请求security加固
sessions_send(sessionKey="ciso-isolated", message="
skill: ai-skill-optimizer
task: security-harden
params:
  skill-name: pdf-processor
  authorization: CISO-001
  hardening-target: critical
  caller: CISO-001
")

# CQO-001 请求质量enhance
sessions_send(sessionKey="cqo-isolated", message="
skill: ai-skill-optimizer
task: quality-improve
params:
  skill-name: pdf-processor
  target-quality: 9
  caller: CQO-001
")

# CQO-001 请求baseline测量（optimize前）
sessions_send(sessionKey="cqo-isolated", message="
skill: ai-skill-optimizer
task: baseline
params:
  skill-name: pdf-processor
  caller: CQO-001
")
```

### securityConstraint（接口层）

```
🚨 接口security红线：
• skill-name 仅接受 [a-z0-9-] 字符，reject `..` 和 `/`（防path遍历注入）
• security-harden 必须 CISO-001 authorize，其他 Agent 无法绕过
• security-regression prohibit：加固后 CVSS 必须 ≤ 加固前
• 隔离execute：所有 agent 调用必须在 isolated 会话中运行
• 最小respond：返回结果仅包含metric差值，不暴露内部代码
• 回归protect：optimize后自动运行回归测试，失败则reject交付
```

### 与其他 Skill 的接口关系

| 调用方 | Task | trigger条件 |
|--------|------|---------|
| **CTO-001** | `full-optimize`, `token-optimize`, `performance-optimize` | quarterlyoptimize/用户投诉 |
| **CISO-001** | `security-harden` | securityassessdiscoverrisk |
| **CQO-001** | `baseline`, `quality-improve`, `compare` | quality assessment/optimizeverify |
| **ai-skill-maintainer** | `security-harden` | Patch 后security复验 |
| **ai-skill-creator** | `baseline` | 新建 Skill 的初始baseline |

---

## optimize维度

| 维度 | Goal | metric | 优先级 |
|------|------|------|--------|
| **Token optimize** | 减少 SKILL.md 上下文占用 | Token 数 ↓ | P1 |
| **性能optimize** | 降低executelatency | P95 latency ↓ | P2 |
| **代码optimize** | 提高脚本execute效率 | 吞吐量 ↑ | P2 |
| **security加固** | 缩小攻击面 | security评分 ↑ | P0（强制）|
| **可维护性** | 提高代码质量 | 评分 ↑ | P3 |

> **优先级规则**：P0（security）无条件execute，P1（Token）影响成本，P2（性能）影响体验，P3（可维护）长期价值

---

## 4步optimizeprocess

### Step 1 — baseline测量（Baseline）

**输出**：optimize前的各项metricbaseline值

#### 1.1 Token analyze

```bash
# 统计 SKILL.md Token 数（估算：1 Token ≈ 4 字符）
wc -c SKILL.md  # 字节数
grep -c "^" SKILL.md  # 行数

# 统计 references/ 总 Token 数
cat references/*.md | wc -c
```

**Token 预算Goal**（CTO 建议）：
| 文件类型 | Goal上限 | Description |
|---------|---------|------|
| SKILL.md | < 5,000 tokens | 主trigger文件 |
| 单个引用文件 | < 2,000 tokens | references/ |
| 脚本注释 | < 500 tokens | 精简注释 |

#### 1.2 性能baseline

```markdown
## 性能baselinerecord

Skill：<name>
测试日期：<ISO date>
环境：<测试环境描述>

### execute时间
- 平均latency：<X>ms
- P95 latency：<X>ms
- P99 latency：<X>ms

### 资源使用
- 内存峰值：<X>MB
- CPU 使用率：<X>%

### security基线
- RED FLAGS：<count>
- CVSS 评分：<score>
- 攻击面assess：<description>
```

#### 1.3 security基线

**execute CISO securityreview（完整 Phase 4）**：
- STRIDE 威胁建模
- CVSS 漏洞评分
- permission范围assess

---

### Step 2 — optimizeanalyze（Analysis）

#### 2.1 Token optimizeanalyze

| optimizestrategy | 预期节省 | 适用场景 |
|---------|---------|---------|
| **渐进式披露** | 20-40% | 详细文档 > 100 行 |
| **代码外置** | 30-50% | 重复代码块 |
| **引用外置** | 40-60% | API 文档/Schema |
| **精简描述** | 10-20% | 冗长的 description |

**Token optimize检查清单**：
```markdown
- [ ] SKILL.md 是否超过 500 行？ → 拆分到 references/
- [ ] 是否有重复的代码示例？ → 合并/外置
- [ ] 是否有冗长的解释？ → 精简为要点
- [ ] 是否有不必要的示例？ → 删除
- [ ] Frontmatter 是否过于复杂？ → 精简 metadata
```

#### 2.2 性能optimizeanalyze

| 瓶颈类型 | identify方法 | optimizeplan |
|---------|---------|---------|
| **I/O 瓶颈** | 等待文件/网络 | 批量操作、缓存 |
| **CPU 瓶颈** | 密集计算 | 算法optimize、并行化 |
| **内存瓶颈** | 大文件handle | 流式handle、分块 |
| **start瓶颈** | 脚本加载慢 | 懒加载、on-demand导入 |

**性能optimize检查清单**：
```markdown
- [ ] 脚本是否有不必要的导入？ → on-demand导入
- [ ] 是否有重复的文件读写？ → 批量操作
- [ ] 正则表达式是否低效？ → 预编译/非贪婪
- [ ] 是否有阻塞操作？ → 异步化
- [ ] 错误handle是否过于复杂？ → 简化逻辑
```

#### 2.3 security加固analyze

**攻击面assess矩阵**：

| 维度 | optimize前 | optimize后 | 改善 |
|------|--------|--------|------|
| 文件permission | 宽松 | 严格 | ⬆️ |
| 网络调用 | 多 | 少 | ⬆️ |
| 依赖数量 | 多 | 少 | ⬆️ |
| 硬编码值 | 多 | 少 | ⬆️ |
| 错误信息 | 详细 | 泛化 | ⬆️ |

**security加固优先级**：

| 优先级 | 加固项 | 预期效果 |
|--------|--------|---------|
| P0 | 移除硬编码密钥 | 消除高危漏洞 |
| P0 | 收紧文件permission | 防止越权访问 |
| P0 | 减少依赖 | 缩小攻击面 |
| P1 | 泛化错误信息 | 防止信息泄露 |
| P1 | 输入verify强化 | 防止注入攻击 |
| P2 | 添加超时protect | 防止 DoS |
| P2 | 日志脱敏 | 防止 PII 泄露 |

---

### Step 3 — implementoptimize（Implementation）

> **⚠️ 重要**：在implement任何optimize之前，先在 isolated 会话中测量baseline（Step 1），保留baseline快照。

#### 3.1 Token optimizeimplement

**strategy A：渐进式披露重构** → [详见 references/optimization-patterns.md — 模式 A](../references/optimization-patterns.md#1-模式a渐进式披露重构)
- 将 > 50行的详细文档外置到 `references/`
- 主文件 SKILL.md 仅保留摘要 + 链接
- 预期节省：20-40%

**strategy B：代码外置** → [详见 references/optimization-patterns.md — 模式 B](../references/optimization-patterns.md#1-模式b代码外置)
- 将 > 20行的代码块外置到 `scripts/` 或 `references/`
- 主文件仅保留调用命令和Description
- 预期节省：30-50%

**Token optimize检查清单**：
```markdown
- [ ] SKILL.md 是否超过 500 行？ → 拆分到 references/
- [ ] 是否有重复的代码示例？ → 合并/外置
- [ ] 是否有冗长的解释？ → 精简为要点
- [ ] 是否有不必要的示例？ → 删除
- [ ] Frontmatter 是否过于复杂？ → 精简 metadata
```

#### 3.2 性能optimizeimplement

**strategy A：懒加载** → [详见 references/optimization-patterns.md — 模式 C](../references/optimization-patterns.md#2-模式c懒加载)
- on-demand导入，避免start时加载全部模块

**strategy B：缓存结果** → [详见 references/optimization-patterns.md — 模式 D](../references/optimization-patterns.md#2-模式d缓存结果)
- 重复计算结果缓存，避免每次调用重新获取

**strategy C：批量操作** → [详见 references/optimization-patterns.md — 模式 E](../references/optimization-patterns.md#2-模式e批量操作)
- 批量读写替代逐个操作

**性能optimize检查清单**：
```markdown
- [ ] 脚本是否有不必要的导入？ → on-demand导入
- [ ] 是否有重复的文件读写？ → 批量操作
- [ ] 正则表达式是否低效？ → 预编译/非贪婪
- [ ] 是否有阻塞操作？ → 异步化
- [ ] 错误handle是否过于复杂？ → 简化逻辑
```

#### 3.3 security加固implement

**strategy A：移除硬编码** → [详见 references/optimization-patterns.md — 模式 F](../references/optimization-patterns.md#3-模式f移除硬编码密钥)
- API 密钥/令牌改为环境变量读取

**strategy B：输入verify强化** → [详见 references/optimization-patterns.md — 模式 G](../references/optimization-patterns.md#3-模式g输入verify强化)
- Skill 名称正则verify：`^[a-z][a-z0-9-]{2,64}$`
- path遍历检查：reject `..` 和 `/`

**strategy C：超时protect** → [详见 references/optimization-patterns.md — 模式 H](../references/optimization-patterns.md#3-模式h超时protect)
- 添加操作超时restrict，防止 DoS

**security加固检查清单**：
```markdown
- [ ] 是否有硬编码的密钥或令牌？ → 改为环境变量
- [ ] path参数是否有遍历检查？ → 添加verify
- [ ] 错误信息是否泛化？ → 移除内部path泄露
- [ ] 操作是否有超时restrict？ → 添加 timeout
```

#### 3.4 回归protect（自动）

> **🚨 securityConstraint**：任何optimize后若回归测试失败，必须自动rollback，不得交付退化版本。

optimize后若回归测试失败，execute以下step：

1. **自动rollback至 baseline 版本**：
   ```bash
   git checkout tags/v<baseline-version> -- SKILL.md scripts/ references/
   ```
2. **record regression**：将详情写入 `references/optimization-log.md`
3. **notify caller**：返回 `E_REGRESSION`，附 delta metric

---

### Step 4 — verify与对比（Verify & Compare）

#### 4.1 optimize后测量

```markdown
## optimize后metric

### Token 节省
- optimize前：<X> tokens
- optimize后：<Y> tokens
- 节省：<Z>% ✅

### 性能改善
- P95 latency：
  - optimize前：<X>ms
  - optimize后：<Y>ms
  - 改善：<Z>% ✅

### security加固
- CVSS 评分：
  - optimize前：<X.Y>
  - optimize后：<Y.Z>
  - 改善：✅
- RED FLAGS：
  - optimize前：<count>
  - optimize后：<count>
```

#### 4.2 Function回归测试

```markdown
## 回归测试

- [ ] 所有原有Function仍然正常工作
- [ ] trigger关键词仍然有效
- [ ] 错误handle与optimize前1致
- [ ] 输出格式与optimize前1致
```

#### 4.3 securityverify

> ⚠️ **security加固后必须重新review**

- [ ] CISO securityreview通过（CVSS < 7.0）
- [ ] STRIDE 威胁建模无新增risk
- [ ] permission范围已最小化
- [ ] 无新引入的依赖

#### 4.4 publish

```bash
# 打包
clawhub package ./<skill-name> --output ./dist

# publish
clawhub publish ./<skill-name> \
  --slug <skill-name> \
  --name "<Skill Name>" \
  --version X.Y.Z \
  --changelog "optimize：Token 节省 X%，P95 latency降低 Y%，security加固"
```

---

## optimizerecord模板

**save至 `references/optimization-log.md`**：

```markdown
# Skill optimizerecord

## Skill 信息
- 名称：<name>
- optimize前版本：<version>
- optimize后版本：<version>
- optimize日期：<ISO date>

## optimize摘要

### Token optimize
- optimize前：<X> tokens
- optimize后：<Y> tokens
- 节省：<Z>%

### 性能optimize
| metric | optimize前 | optimize后 | 改善 |
|------|--------|--------|------|
| P95 latency | Xms | Yms | Z% |

### security加固
- CVSS 改善：<X.Y> → <Y.Z>
- 主要加固项：
  - <item 1>
  - <item 2>

## 详细变更

### 变更 #1：<标题>
**类型**：[Token/性能/security/代码]
**optimize前**：<描述>
**optimize后**：<描述>
**代码**：
\`\`\`
<diff>
\`\`\`

## verify结果

| 测试项 | 结果 |
|--------|------|
| 回归测试 | ✅ |
| Token 测量 | ✅ |
| 性能测试 | ✅ |
| securityreview | ✅ |

## publish信息
- 版本：<version>
- publish日期：<date>
- changelog：<text>
```

---

## 快速参考

### trigger命令

| 用户请求 | optimize维度 | 优先级 |
|---------|---------|--------|
| "减少 Skill XX 的 Token 占用" | Token | P1 |
| "加快 Skill XX 的execute速度" | 性能 | P2 |
| "加固 Skill XX 的security性" | security | P0 |
| "重构 Skill XX 的代码" | 可维护性 | P3 |
| "全面optimize Skill XX" | 全部 | P0→P1→P2→P3 |

### 常见错误

1. **跳过baseline测量**：未测量就optimize，无法verify效果
2. **security为性能让路**：discoversecurity问题时必须优先修复
3. **过度optimize**：Token 节省 < 5% 无实际价值
4. **破坏Function**：optimize后Function异常，必须rollback
5. **不recordoptimize**：历史optimize未record，无法trace

---

## 版本历史（Changelog）

| 版本 | 日期 | Changes | 审核人 |
|------|------|---------|--------|
| **1.1.0** | 2026-04-13 | 新增 Agent 调用接口层（Inter-Agent Interface）：7个 Task 类型（baseline/token-optimize/performance-optimize/security-harden/quality-improve/full-optimize/compare）；PDCA quality gatesystem；optimize前后对比report模板；`E_REGRESSION` 回归protect自动rollback；新增 references/optimization-patterns.md（代码optimize示例参考） | CTO-001 / CISO-001 |
| **1.0.0** | 2026-04-11 | Initial version：4步optimizeprocess（Baseline → Analysis → Implementation → Verify）+ 4个optimize维度（Token/性能/security/质量）+ G0-G4 quality gate | CTO-001 / CISO-001 |

## rollbackstrategy（Rollback）

> 如optimize后回归测试失败，execute以下steprecover：

```bash
# 自动rollback至 baseline 版本
git checkout tags/v<baseline-version> -- SKILL.md scripts/ references/

# verifyrollback成功
git log --oneline -3
```

**rollbacktrigger条件**：
- 回归测试失败（E_REGRESSION）
- CVSS 评分恶化（security-regression）
- optimize后 TSR < 85%（Function严重退化）

**rollback后操作**：
1. record regression 详情至 `references/optimization-log.md`
2. notify caller：返回 `E_REGRESSION`，附 delta metric
3. analyze退化原因，修复后重新optimize
