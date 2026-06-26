# Auto-Coding v3 — 设计说明 / Design Document

**版本**: v3  
**Last Updated**: 2026-05-22

---

## 1. 系统本质 / Essence

**中文**: 单进程串行 + 多角色 Soul + 多模型切换 + 纪律执行层。不是任务分发器，而是自我完善的智能编程系统。

**English**: Single-process serial execution + multi-role Souls + multi-model switching + discipline enforcement layer. Not a task dispatcher, but a self-improving intelligent programming system.

### 设计哲学 / Design Philosophy

| 原则 / Principle | 说明 / Description |
|---|---|
| **极简主义** | 不写多余代码，不请求未要求的功能，不写注释解释显而易见的事 |
| **Coding Minimalism** | Don't write extra code, don't request unrequired features, don't comment the obvious |
| **手术刀式修改** | 每次修改范围明确，改动文件数 ≤5，单文件行数 ≤200 |
| **Scalpel-precision changes** | Each change has explicit scope: ≤5 files, ≤200 lines per file |
| **质量优先于速度** | 选择能力最强的模型，而非最快的模型 |
| **Quality over Speed** | Always prefer the most capable model, not the fastest |
| **纪律高于便利** | 铁律不可被「效率」理由绕过，元规则提供例外条件 |
| **Discipline over Convenience** | Iron rules cannot be bypassed for "efficiency"; meta-rules define exception conditions |

---

## 2. 架构总览 / Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    用户请求 / User Request                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Phase Model Allocator（阶段模型分配器）           │
│              Phase Model Allocator (stage model selector)    │
│                                                             │
│  根据当前阶段选择对应的 Soul + Model 组合                      │
│  Selects Soul + Model pair based on current phase            │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ 设计/分解  │    │ 编码/优化  │    │ 审查/测试  │
    │ Design    │    │ Code/Opt │    │ Review    │
    │           │    │          │    │           │
    │ Architect │    │ Senior   │    │ Reviewer  │
    │ Soul      │    │ Dev Soul │    │ + Tester  │
    └─────┬────┘    └─────┬────┘    └─────┬────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               Risk Scorecard（纪律执行层）                     │
│               Risk Scorecard (discipline enforcement)         │
│                                                             │
│  Pre-Mortem → In-Flight → Post-Mortem                       │
│  阶段前自检    执行中监控     阶段后审计                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│           State Manager + Approval Rules                     │
│           状态管理器 + 审批规则引擎                             │
│                                                             │
│  .auto-coding/state.json  ←→  .auto-coding/rules.yaml       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                    📦 代码输出 / Code Output
```

### 三层防线 / Three Lines of Defense

```
第一层 / Line 1: Skill Files (skills/*.skill.md)
  └── 强制流程指令 / Mandatory process instructions

第二层 / Line 2: Risk Scorecard (risk-scorecard.skill.md)
  └── 量化指标检测 + 借口反驳 / Quantified detection + rationalization counter

第三层 / Line 3: Meta-Rules (discipline-meta.skill.md)
  └── 元规则：何时可无视指标、人工覆盖流程 / Meta-rules: when to ignore metrics, human override
```

---

## 3. 八步循环

```
设计(Design) → 分解(Decomposition) → 编码(Coding) → 测试(Testing)
    ↑____________________________________________________↓
                         反思(Reflection) → 优化(Optimization)
                                                 ↓
验证(Verification) → 输出(Output)
```

- 测试→反思→优化 形成迭代循环（最多 3 次），测试通过后跳出
- A 级快速通道：单函数/小 Bug 可跳过设计和分解，直接 Implementation → Review → Verification

| 阶段 | Soul 角色 | 说明 |
|------|----------|------|
| 设计/分解 | `software-architect` | 综合最强，架构权衡、方案对比 |
| 编码 | `senior-developer` | 代码专用，类型注解规范 |
| 测试 | `api-tester` | 全面严谨 |
| 反思/审查 | `code-reviewer` | 逻辑推理独特优势 |
| 优化 | `optimizer` | 最优雅实现 |
| 验证 | `verifier` | 严谨全面 |

---

## 4. 纪律执行体系

### Risk Scorecard 五元组

每条纪律规则由五个字段定义：

| 字段 | 类型 | 说明 |
|------|------|------|
| `discipline` | string | 要遵守的纪律 |
| `rationalization` | string[] | 常见偷懒借口（反借口表） |
| `signal` | string | 可观测信号名 |
| `threshold` | string | 触发条件表达式 |
| `action` | enum | `block` / `warn` / `log` |

### 执行时机

| 时机 | 说明 |
|------|------|
| **Pre-Mortem** 阶段前 | Agent 对照 rationalizations 自问「我有没有在找借口」 |
| **In-Flight** 执行中 | 关键操作后检测 signal 是否触发 threshold |
| **Post-Mortem** 阶段后 | 聚合检测结果，输出 Scorecard Report |

### 硬上限

| 指标 | 硬上限 | 说明 |
|------|--------|------|
| 单阶段注入技能数 | ≤2 | 严格遵守 |
| 单文件行数 | ≤200 | meta 文件除外 |
| 单次修改文件数 | ≤5 | 超过触发 🔴 block |
| 无测试新增代码行数 | ≤200 | 超过触发 🔴 block |
| 新增抽象层数 | ≤1 | 超过触发 🟡 warn (Rule of Three) |

---

## 5. 模型分配

| Provider | 用途 |
|---|---|
| 主模型 | 编码、设计、分解、输出 |
| 审查模型 | 代码审查、反思、优化、验证 |

环境变量覆盖：`AUTO_CODING_MODEL_<ROLE>=provider/model`，Fallback：`AUTO_CODING_FALLBACK_MODELS=...`

---

## 6. 内嵌 Soul 系统

8 个编码专用 Soul 直接内嵌，不再依赖外部目录：

| Agent ID | 名称 | 专长 |
|---|---|---|
| `software-architect` | 软件架构师 | 架构设计、DDD、系统思维 |
| `backend-architect` | 后端架构师 | 分布式系统、数据库、API 设计 |
| `senior-developer` | 高级开发工程师 | Python 实现、类型注解、性能优化 |
| `frontend-developer` | 前端工程师 | React/Vue、组件设计、性能 |
| `code-reviewer` | 代码审查专家 | PR 审查、安全、最佳实践 |
| `api-tester` | API 测试工程师 | 接口测试、边界条件、幂等性 |
| `optimizer` | 代码优化工程师 | 优雅重构、性能最优 |
| `verifier` | 交付验证工程师 | 功能完整性、边界覆盖 |

---

## 7. 配置与状态

```
project_dir/
├── .auto-coding/
│   ├── state.json              # 状态持久化
│   ├── workflow.yaml           # 流程配置（可选）
│   ├── rules.yaml              # 审批规则
│   └── workflow.yaml.template  # 首次运行自动生成
```

审批规则示例：`src/*`、`test/*`、`*.py` 自动批准；`config/*`、`.env*` 需人工审批；删除操作全部需审批。

---

## 8. 设计决策记录

### DD-001: 为什么用单进程串行而非多 Agent 并行？

子 Agent spawn 对模型 provider 有限制（仅支持当前 provider），且并发 spawn 带来状态同步和错误恢复的复杂度。单进程串行通过切换 Soul 和 Model 实现多视角审查，避免了并发风险。

### DD-002: 为什么引入纪律执行层？

实际使用中发现 Agent 存在「合理化偷懒」行为——跳过测试、跳过审查、过度修改。Risk Scorecard 通过量化指标 + 借口反驳机制，从行为层面约束 Agent，而非仅依赖 Prompt 指令。

### DD-003: 为什么审查模型单独配置？

推理和逻辑分析模型在代码审查中有独特优势，适合「找问题」任务。与编码模型形成互补。

### DD-004: 为什么 Skill 文件是强制指令而非建议？

Agent 存在将 Skill 文件内容降级为「参考」的倾向。铁律 0 明确规定：技能文件中的流程和检查项具有强制约束力，违反等于违反系统指令。

---

*Generated: 2026-05-22*
