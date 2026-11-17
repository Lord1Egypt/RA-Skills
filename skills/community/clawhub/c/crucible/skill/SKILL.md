---
name: crucible
description: Use when the user wants a full product delivery pipeline (PM→UX→Dev→Test), or when building something from scratch with quality gates, or when requesting "团队化开发", "全流程", "带审查的开发", "自审开发", "迭代交付", "crucible". Supports configurable stages with built-in implement→review→fix self-review loops.
license: MIT
user-invocable: true
disable-model-invocation: false
---

# 🔬 Crucible — 严峻考验式交付

> 每个 Stage 内部自带 **implement → self-review → fix** 循环，产出质量在阶段内收敛。
> 阶段间设 Gate 门禁做跨角色校验，PASS 放行 / REJECT 返工。
> 阶段和 Gate 均可按需开关，适配不同场景。
> **融合**: Ponytail (极简编码) + Superpowers (纪律协议) + ECC (验证+安全) + OpenSpec (规格驱动)

---

## 融合方法论参考

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| [references/methodology.md](references/methodology.md) | Ponytail Ladder + 理性化防御 + 验证纪律 | 每个 Stage 开始时 |
| [references/verification.md](references/verification.md) | Pre-Gate 6 阶段自动化验证 + Build 恢复 | 提交 Gate 前 |
| [references/security-checklist.md](references/security-checklist.md) | 10 节安全清单 | Gate 3 安全敏感代码时 |
| [references/tooling.md](references/tooling.md) | Codegraph + OpenSpec 指南 | 管线启动时 |
| [companion/pm-disciplines.md](companion/pm-disciplines.md) | PM 深度方法论 | Stage 1 |
| [companion/dev-disciplines.md](companion/dev-disciplines.md) | Dev 深度方法论 | Stage 3 |
| [companion/test-disciplines.md](companion/test-disciplines.md) | Test 深度方法论 | Stage 4 |
| [companion/gate-disciplines.md](companion/gate-disciplines.md) | Gate 增强方法论 | 每个 Gate |

---

## Pipeline 全景

### 两层循环架构

```
外层: [Stage 1] → [Gate 1] → [Stage 2] → [Gate 2] → ... → ✅

内层（每个 Stage 内部）:
  implement → self-review → fix → self-review → ... → PASS → 提交 Gate
```

**Stage 内部循环**确保产出质量在阶段内收敛；**Gate 间校验**确保跨阶段/跨角色的一致性。

### 完整 Pipeline（8 阶段）

```
[PM/PRD ⟳] → [Gate 1] → [UX 设计 ⟳] → [Gate 2]
    → [Dev∥Dev∥Dev ⟳] → [Gate 3]
    → [测试 ⟳] → [Gate 4] → ✅
```

⟳ = Stage 内部的 implement→review→fix 自审循环

### 可配置

阶段和 Gate 均可按需跳过或关闭，见 [使用模式](#使用模式)。

---

## 与 orch-pipeline 的区别

| 维度 | `orch-pipeline` (ECC) | `crucible` (本 Skill) |
|------|----------------------|---------------------------|
| 起点 | 已有 spec/doc | 原始用户需求 |
| 覆盖阶段 | Plan → Implement → Review → Commit | PM → UX → Dev → Test → Acceptance |
| Gate 数量 | 2（Plan 审批 + Commit 审批） | 4（UX 评审 + Dev 评审 + Code Review + 产品验收） |
| Gate 类型 | 人工审批 | Agent 自动审查 + 人工兜底 |
| 角色模拟 | 单一开发者视角 | PM + UX + Dev + Test + Product |
| 循环机制 | 无 | REJECT → Fix → Re-review（最多 3 轮） |
| 并行开发 | 无 | Stage 3 支持并行 fan-out |
| 组合关系 | 被 `orch-*` 调用 | Stage 3 可委托 `orch-build-mvp` |

---

## 核心原则

### 1. 门禁是真正的关卡

Gate 审查者被明确要求 **默认怀疑**，寻找问题而非确认通过。

- **PASS**: 无阻断性问题，制品合格
- **PASS with leftovers**: 通过但有遗留项 → 自动成为下一阶段的 must-solve
- **REJECT**: 存在阻断性问题 → 必须修复后 Re-review

### 2. 遗留项自动传递

Gate N 的 leftover items 自动注入 Stage N+1 的 prompt 中，标记为 **must-solve**。
这是 Pipeline 的核心价值之一 — 跨阶段信息不丢失。

### 3. 并行 Fan-out + 串行 Gate

开发阶段可以并行（如 backend + frontend + admin），但 Gate 审查是串行的。
并行开发后，**API 契约一致性** 是 Gate 3 的首要检查点。

### 4. Stage 内部自审循环（核心特性）

每个 Stage 在产出制品后，**自动触发 self-review**，不通过则内部 fix→re-review，直到自审 PASS 才提交 Gate。

```
Stage 内部:
  implement → self-review
    → PASS → 提交 Gate
    → FAIL → fix → self-review（最多 3 轮）→ 提交 Gate
```

**自审 vs Gate 的区别**：
- **自审（Stage 内部）**：同角色或同类型 Agent 审查自身产出，快速迭代，确保基本质量
- **Gate（Stage 之间）**：跨角色审查（如 UX 审 PRD、Dev 审 UX、Reviewer 审 Code），确保一致性

自审使得 **即使跳过 Gate，单阶段也能保证质量**。

### 5. REJECT→Fix→Re-review 循环（Gate 级）

```
Gate REJECT → 记录问题清单 → Fix Agent 修复 → Re-review
  → PASS → 继续
  → REJECT → 再修复（最多 3 轮）→ 人工介入
```

### 6. 编排者不做具体工作

编排者（Claude Code）负责：派发 Agent、收集结果、判断 Gate 通过与否、传递上下文。
编排者 **不写代码、不做设计、不做评审** — 只调度。

---

## 阶段定义

### Stage 1: PM / PRD

| 项 | 说明 |
|---|---|
| **输入** | 用户需求描述 |
| **产出** | `docs/PRD.md` |
| **Agent** | `product-manager` 或 `planner` |
| **内容** | 功能列表、页面清单、数据模型、API 端点、MVP 边界 |

**融合方法论** (详见 [companion/pm-disciplines.md](companion/pm-disciplines.md)):
- **Pattern Grounding**: 先搜索代码库已有惯例，写入 PRD "Patterns to Mirror" 段
- **约束集思维**: PRD 增加 Hard/Soft Constraints 段
- **YAGNI 裁剪**: 对每个 feature 跑 Ponytail Ladder 第 1 级

PRD 最小结构：
```markdown
# PRD: {产品名}
## 产品概述
## 功能列表（编号 F1-Fn）
## 页面清单（表格：页面名/路径/字段）
## 数据模型（表格：字段/类型/说明）
## API 端点（表格：方法/路径/说明）
## MVP 边界（包含/不包含）
## Patterns to Mirror（已有代码惯例）
## Constraints（Hard/Soft）
## MVP Feature 裁剪表
```

### Gate 1: UX 评审 PRD

| 项 | 说明 |
|---|---|
| **输入** | PRD.md |
| **产出** | `docs/gate1-ux-review.md` |
| **Agent** | UX 设计师角色（prompt 见 [roles.md](roles.md)） |
| **检查维度** | 用户流程合理性、信息架构、交互遗漏、页面间跳转逻辑 |
| **通过标准** | 无阻断性 UX 缺陷 |
| **输出** | PASS/REJECT + leftover items |

### Stage 2: UX 设计

| 项 | 说明 |
|---|---|
| **输入** | PRD.md + Gate 1 leftovers |
| **产出** | `docs/UX-Design.md` |
| **Agent** | UX 设计师角色 |
| **内容** | 页面布局、组件拆分、交互流程、配色方案、字体规范、间距系统 |

**融合方法论**:
- **AI Slop Detection**: 审查 UX 设计是否使用了通用 AI 模式（紫蓝渐变、无目的毛玻璃、过度圆角、无意义的 hero section）→ 替换为有意图的设计决策
- **Ponytail native-first**: CSS over JS, platform widget over custom lib（详见 [references/methodology.md](references/methodology.md) Ladder 第 4 级）

### Gate 2: Dev 评审 UX 可行性

| 项 | 说明 |
|---|---|
| **输入** | PRD.md + UX-Design.md |
| **产出** | `docs/gate2-dev-review.md` |
| **Agent** | 高级工程师角色 |
| **检查维度** | 技术可行性、平台限制（如小程序 WebView 不支持 backdrop-filter）、性能风险、组件复杂度 |
| **通过标准** | 所有设计方案技术上可实现 |
| **输出** | PASS/REJECT + 必须调整项（如降级方案） |

### Stage 3: 开发实现

| 项 | 说明 |
|---|---|
| **输入** | PRD.md + UX-Design.md + Gate 2 调整项 |
| **产出** | 完整代码（如 backend/ + miniprogram/ + admin/） |
| **Agent** | 多个开发 Agent **并行** fan-out |
| **并行策略** | 按模块拆分：backend / frontend / admin |

**融合方法论** (详见 [companion/dev-disciplines.md](companion/dev-disciplines.md)):
- **Ponytail Ladder** 嵌入每个 Dev Agent prompt（7 级极简决策）
- **双阶段审查**（spec 合规 + 代码质量）替代单阶段自审
- **Minimal Verifiable Phase**: 3-5 任务一批，增量验证
- **Build-fix 恢复**: build 失败 → 最小 diff 修复循环
- **Codegraph**: 每次修改前 impact analysis

**并行开发的关键**：在 prompt 中明确 **API 契约**（从 PRD 提取），所有 Agent 必须遵循相同的接口定义。

API 契约注入模板：
```markdown
## API 契约（所有端必须遵循）
| 方法 | 路径 | Request | Response |
|------|------|---------|----------|
| GET | /api/v1/categories | — | [{id, name, cover_url, image_count}] |
| POST | /api/v1/images | JSON: {name, image_url, thumb_url?, category_id} | {id, ...} |
```

### Gate 3: Code Review

| 项 | 说明 |
|---|---|
| **输入** | 全部代码 + PRD API 定义 + UX 设计规范 |
| **产出** | `docs/gate3-code-review.md` |
| **Agent** | 代码审查员角色（建议 opus/sonnet） |
| **首要检查** | **API 契约一致性**（前后端接口字段名、格式、数据类型是否匹配） |
| **次要检查** | 安全性、代码质量、UX 还原度、Gate 2 调整项落地 |
| **循环** | REJECT → Fix Agent → Re-review（最多 3 轮） |

**融合方法论** (详见 [companion/gate-disciplines.md](companion/gate-disciplines.md)):
- **误报过滤门**: 报告 finding 前问 4 个问题，12 种显式误报直接跳过
- **安全清单**: 安全敏感代码触发 10 节安全审查 ([security-checklist.md](references/security-checklist.md))
- **审查反馈处理**: 禁止表演性认同，先验证再接受

API 契约验证清单：
```markdown
| 端点 | 后端 Response 字段 | 前端使用字段 | 匹配 |
|------|-------------------|-------------|------|
| GET /categories | image_count | item.image_count? | ✅/❌ |
| POST /images | JSON body? | 发送格式? | ✅/❌ |
```

**Gate 3 是最容易 REJECT 的门禁** — 并行开发必然导致前后端契约差异。

### Stage 4: 测试

| 项 | 说明 |
|---|---|
| **输入** | 完整代码（Gate 3 PASS 后） |
| **产出** | `tests/` + `docs/gate4-test-report.md` |
| **Agent** | 测试工程师角色 |
| **内容** | API 集成测试，覆盖正常路径 + 主要异常路径（401/404/409） |

**融合方法论** (详见 [companion/test-disciplines.md](companion/test-disciplines.md)):
- **TDD Iron Law** (可选 `--tdd`): 没有失败测试就不能写生产代码
- **BDD 场景**: Given/When/Then 格式覆盖 happy path + 边界
- **系统调试法**: 4 阶段 (根因→模式→假设→最小修复)
- **E2E** (可选): Playwright POM 模式
- **YAGNI**: trivial one-liners 不需测试

### Gate 4: 产品验收

| 项 | 说明 |
|---|---|
| **输入** | 全部交付物（代码 + 文档 + 测试报告） |
| **产出** | `docs/gate4-product-acceptance.md` |
| **Agent** | 产品经理角色 |
| **检查维度** | PRD 功能覆盖率、API 端点覆盖率、UX 还原度、测试通过率、可运行性 |
| **通过标准** | 核心功能全部可用，无阻断性问题 |

---

## Pre-Gate 自动化验证

**所有 Gate 审查前必须先通过 6 阶段自动化验证** (详见 [references/verification.md](references/verification.md)):

```
Build → Type Check → Lint → Test (≥80%) → Security Scan → Diff Review
```

只有全部 PASS (Verdict: READY) 才进入 Gate 审查。FAIL → 回到 Stage 内部 fix 循环。
Gate 不浪费审查轮次在 trivially broken 的代码上。

---

## 编排协议

### 启动

```
/ccg:crucible <需求描述>           → 完整 8 阶段
/ccg:crucible --minimal <需求>     → 最小 4 阶段（跳过 UX 设计）
/ccg:crucible --from-stage 3      → 从指定阶段继续
```

### Stage 执行协议（含自审循环）

```python
for stage in pipeline:
    if stage.skipped:
        continue

    # 1. 构造 Agent prompt
    prompt = build_prompt(
        task=stage.task,
        upstream_docs=collect_docs(stage.inputs),
        gate_leftovers=previous_gate.leftovers,
        api_contract=prd.api_endpoints
    )
    
    # 2. Stage 内部循环：implement → self-review → fix
    for round in range(MAX_SELF_REVIEW_ROUNDS):  # 默认 3
        result = dispatch_agent(prompt, model=stage.model)
        
        if not stage.self_review:
            break  # 自审关闭，直接提交 Gate
        
        review = dispatch_review_agent(result.artifacts, stage.review_criteria)
        if review.verdict == "PASS":
            break
        
        # 自审未通过 → fix → 下一轮
        prompt = build_fix_prompt(result.artifacts, review.issues)
    
    # 3. 提交 Gate（如果启用）
    if stage.gate.enabled:
        gate_result = run_gate(stage.gate, result.artifacts)
        
        gate_round = 0
        while gate_result.verdict == "REJECT":
            fix_result = dispatch_fix_agent(gate_result.issues)
            gate_result = run_rereview(fix_result, gate_result.issues)
            gate_round += 1
            if gate_round >= 3:
                escalate_to_human()
        
        previous_gate.leftovers = gate_result.leftovers
```

### 自审 Agent 与执行 Agent 的关系

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **同 Agent 自审** | 执行 Agent 在 prompt 中被要求"写完后自查" | 轻量级，PM/UX/测试 |
| **独立审查 Agent** | 派发独立的 review Agent 审查执行 Agent 的产出 | 重量级，代码开发 |
| **跳过自审** | 不审查，直接提交 Gate | Gate 审查足够强，或时间紧迫 |

**代码开发推荐独立审查 Agent**：执行 Agent 写代码 → 独立 code-reviewer Agent 审查 → Fix Agent 修复 → 再审查。

### Gate 报告标准格式

所有 Gate 报告写入 `docs/gate{N}-{name}.md`：

```markdown
# Gate N: {名称}

## 结论: PASS / REJECT

## 审查详情
[逐项审查，每项标注 ✅/❌/⚠️]

## 遗留项（不影响通过但应修复）
- [P2/P3 级别问题]

## 必须修复（仅 REJECT 时）
| # | 级别 | 问题 | 位置 | 修复建议 |
|---|------|------|------|----------|
| C1 | CRITICAL | ... | file:line | ... |
```

### Re-review 报告格式

```markdown
# Gate N Round M: 修复验证

## 结论: PASS / REJECT

## 逐项验证
### C1: {问题描述} ✅/❌
[证据：代码位置 + 修复内容]
```

---

## 并行开发编排

### 拆分策略

```
Stage 3: 开发（并行）
├── Agent-Backend:   backend/     （API + 数据模型 + 业务逻辑）
├── Agent-Frontend:  frontend/    （用户端 UI）
└── Agent-Admin:     admin/       （管理后台 UI）
```

每个 Agent 的 prompt 必须包含：
1. 完整的 API 契约表
2. Gate 2 的所有调整项
3. 自己负责的目录范围（文件隔离）

### Gate 3 对并行产出的审查重点

1. **API 契约一致性**（最重要）— 前后端字段名、数据类型、请求格式
2. **数据流完整性** — 如缩略图链路：upload → 返回 URL → 表单保存 → 入库 → 前端展示
3. **Gate 2 调整项落地** — 所有降级方案是否实现

---

## 模型选择策略

| 阶段 | 推荐模型 | 原因 |
|------|----------|------|
| PM/PRD | sonnet | 结构化思维，不需要最强推理 |
| Gate 1 (UX 评审) | sonnet | 设计判断力 |
| UX 设计 | sonnet | 设计模式识别 + 创意 |
| Gate 2 (Dev 评审) | sonnet | 技术可行性判断 |
| 开发 (并行) | sonnet | 标准编码能力，并行需要速度 |
| Gate 3 (Code Review) | opus 或 sonnet | 跨文件分析，API 契约比对 |
| 测试 | sonnet | 标准测试编写 |
| Gate 4 (产品验收) | sonnet | 对照文档审查 |

**原则：Gate 审查 ≥ Stage 执行的模型级别。** 审查需要判断力，执行需要速度。

---

## 防失败机制

### Gate 连续 REJECT 升级

| 轮次 | 策略 |
|------|------|
| REJECT R1 | Fix Agent 修复 → Re-review |
| REJECT R2 | 换更强模型 Fix → Re-review |
| REJECT R3 | STOP，报告给人工决策 |

### 上下文管理

- 每阶段完成后写入 `docs/`，后续阶段只读文件路径，不传全文
- Gate 报告是摘要，不是全文复制
- 编排者保持上下文精简，只做调度

### Agent 失败恢复

```
Agent 超时/无响应 → 重新派发同类型 Agent → 仍失败 → 人工介入
```

---

## 实战经验（来自 sparks-lab 项目验证）

### Gate 3 的 API 契约验证价值

在 sparks-lab 项目中，Gate 3 首轮 REJECT 发现 4 项 CRITICAL：
- C1: POST /images 后端期望 multipart，前端发送 JSON → **Admin 创建图片完全不可用**
- C2: 图片 URL 缺少前导 `/`，小程序无法解析 → **所有图片 404**
- C3: 分类计数字段名 `count` vs `image_count` → **计数始终为 0**
- C4: 文件删除路径基于 CWD → **删除操作静默失败**

**这 4 项都是并行开发导致的契约不一致**，如果不在 Gate 3 拦截，将直接进入测试阶段才发现问题。

### Re-review 的价值

Gate 3 Round 2 不仅验证了 4 项修复，还发现了 1 项新引入的 HIGH 问题（upload 端点丢弃 thumb_url），在 PASS 前修复了缩略图链路。

### 遗留项传递的价值

Gate 2 要求"FlowerImage 增加 thumb_url 字段"，这个 leftover 成功传递到 Stage 3 开发 prompt 中，确保数据模型正确。

---

## 使用模式

Pipeline 的每个 Stage 和 Gate 均可独立开关。以下是典型组合：

### 模式 A: 完整交付（8 阶段）

从用户需求到可交付产品的全流程。

```
[PM ⟳] → [G1] → [UX ⟳] → [G2] → [Dev∥Dev∥Dev ⟳] → [G3] → [Test ⟳] → [G4] → ✅
```

**适用**: 新产品、需要 PM + UX + Dev + Test 全角色参与

### 模式 B: 开发+自审（最常用）

已有设计文档，只需要高质量开发。Stage 内自审保证代码质量。

```
[Dev ⟳] → ✅
```

⟳ = implement → code-review → fix → code-review → PASS

**适用**: 已有 PRD/设计稿，只需编码实现。自审循环确保代码质量。

### 模式 C: 开发+Gate 审查

开发带自审，外加跨角色 Code Review Gate 做最终校验。

```
[Dev ⟳] → [Gate: Code Review] → ✅
```

**适用**: 需要额外的独立审查视角（如安全审查、架构审查）

### 模式 D: 并行开发+契约校验

多模块并行开发，Gate 3 专注 API 契约一致性。

```
[Dev∥Dev∥Dev ⟳] → [Gate: API 契约校验] → [Test ⟳] → ✅
```

**适用**: 前后端分离开发，需要确保接口一致

### 模式 E: 仅审查

已有代码，只需要审查和改进。

```
[Gate: Code Review] → [Fix ⟳] → ✅
```

**适用**: 代码质量改进、安全审计、重构评估

### 模式 F: 自定义组合

编排者根据用户需求自由组合：

```python
pipeline = Pipeline(
    stages=[
        Stage("dev", self_review=True, review_criteria="code-quality"),
        Stage("test", self_review=True),
    ],
    gates=[
        Gate("code-review", after="dev"),
    ]
)
```

### 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `self_review` | `true` | Stage 内部是否启用自审循环 |
| `self_review_rounds` | `3` | 自审最大轮次 |
| `gate.enabled` | `true` | Stage 后的 Gate 是否启用 |
| `gate.rounds` | `3` | Gate REJECT→Fix 最大轮次 |
| `parallel` | `false` | Stage 内是否并行 fan-out 多个 Agent |
| `model` | `sonnet` | 执行 Agent 的模型 |
| `review_model` | 继承 `model` | 审查 Agent 的模型（建议 ≥ 执行模型） |

### 入口命令

```
/ccg:crucible <需求>                    → 模式 A（完整交付）
/ccg:crucible --dev <需求>              → 模式 B（开发+自审）
/ccg:crucible --dev --review <需求>     → 模式 C（开发+Gate）
/ccg:crucible --parallel <需求>         → 模式 D（并行+契约）
/ccg:crucible --review-only <path>      → 模式 E（仅审查）
/ccg:crucible --stages dev,test <需求>  → 模式 F（自定义）
```

---

## 参考文件

### 核心
- [roles.md](roles.md) — 各阶段 Agent 角色 prompt 模板
- [gates.md](gates.md) — Gate 审查 prompt 模板和评分标准

### 方法论参考 (references/)
- [references/methodology.md](references/methodology.md) — Ponytail Ladder + 理性化防御 + 验证纪律
- [references/verification.md](references/verification.md) — Pre-Gate 6 阶段自动化验证 + Build 恢复协议
- [references/security-checklist.md](references/security-checklist.md) — 10 节安全审查清单
- [references/tooling.md](references/tooling.md) — Codegraph + OpenSpec 工具链指南
- [references/lessons.md](references/lessons.md) — sparks-lab 项目实战经验总结

### 阶段深度方法论 (companion/)
- [companion/pm-disciplines.md](companion/pm-disciplines.md) — PM: brainstorming + pattern grounding + YAGNI
- [companion/dev-disciplines.md](companion/dev-disciplines.md) — Dev: Ladder + 双阶段审查 + build-fix
- [companion/test-disciplines.md](companion/test-disciplines.md) — Test: TDD + BDD + 系统调试法
- [companion/gate-disciplines.md](companion/gate-disciplines.md) — Gate: 误报过滤 + 审查反馈 + 分支收尾

### 融合来源
Crucible 蒸馏了以下 Claude Code skill 的核心方法论:
- **Ponytail** — 极简编码哲学 (The Ladder, YAGNI, 反过度工程)
- **Superpowers** — 纪律协议 (TDD, 子 Agent 编排, 理性化防御, 验证完成)
- **ECC** — 工程实践 (验证循环, 误报过滤, 构建修复, 安全清单)
- **OpenSpec** — 规格驱动 (约束集, 零决策计划, PBT 属性)
- **Codegraph** — 结构化代码智能 (推荐 MCP 工具)
