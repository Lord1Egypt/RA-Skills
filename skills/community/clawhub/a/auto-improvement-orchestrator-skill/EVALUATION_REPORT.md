# Auto-Improvement Orchestrator Skill — 综合测评报告

> **测评日期**: 2026-04-02  
> **测评版本**: main@d6082d4  
> **评估管线**: Learner (6维结构) + LLM-as-Judge (4维语义) + 质量分级  
> **评估标准**: evaluation-standards.md v2.0.0 (参考 alirezarezvani/claude-skills, anthropics/claude-plugins-official)

---

## 一、仓库概览

| 指标 | 数值 |
|------|------|
| Skill 数量 | 7 |
| 脚本总数 | 12 个 Python 脚本（4,506 行） |
| 测试总数 | 289 个测试用例（全部通过） |
| 测试文件 | 13 个（4,692 行） |
| 共享库 | lib/common.py + lib/state_machine.py |
| CI | GitHub Actions (lint + test + security) |
| 接口层 | 5 个 interface 模块（LLM Judge、Assertions、Critic Engine 等） |

### 架构

```
User → orchestrator → generator (候选生成)
                    → discriminator (多审阅者盲审 + LLM Judge)
                    → gate (6层机械门禁)
                    → executor (变更执行 + 回滚)
                    → learner (Karpathy 自改进循环 + 三层记忆)
                    ↻ Ralph Wiggum: 失败 → 注入 trace → 重试 (max 3)
```

---

## 二、质量分级标准

| 等级 | 综合分 | 含义 |
|------|--------|------|
| **POWERFUL** ⭐ | ≥ 85% | 专家级，可发布到 Marketplace |
| **SOLID** | 70–84% | 可靠，可发布到 GitHub |
| **GENERIC** | 55–69% | 需迭代改进 |
| **WEAK** | < 55% | 拒绝或重写 |

**综合分 = 结构评分 × 50% + LLM 语义评分 × 50%**

---

## 三、评估维度说明

### 结构评分（自动化，6 维度）

| 维度 | 权重 | 评估内容 |
|------|------|---------|
| accuracy | 25% | SKILL.md 12 项质量检查（frontmatter、触发描述、When to Use/Not、代码示例、Related Skills、Output Artifacts 等） |
| coverage | 15% | 结构完整性（SKILL.md 60% 基础 + 可选目录加分） |
| reliability | 20% | pytest 测试通过率（纯文本 skill 默认 1.0） |
| efficiency | 15% | SKILL.md 长度合理性（200 行以下满分） |
| security | 15% | 无硬编码密钥、无危险 API 调用 |
| trigger_quality | 10% | frontmatter description 触发路由质量（长度、关键词、消歧） |

### LLM 语义评分（人工审查，4 维度）

| 维度 | 评估内容 |
|------|---------|
| clarity | 指令清晰度、无歧义程度 |
| specificity | 是否有具体示例、参数文档、模板 |
| consistency | 内部命名和接口风格一致性 |
| safety | 错误处理、回滚、重试上限等防护机制 |

---

## 四、逐 Skill 详细测评

### 4.1 improvement-orchestrator（编排层）

**定位**: 全流程调度中枢，协调 Generator→Discriminator→Gate→Executor→Learner 五阶段管线。

| 维度 | 分数 | 打分理由 |
|------|------|---------|
| accuracy | 0.83 | ✅ YAML frontmatter 完整（name/version/description/author/license/tags）。✅ 有 When to Use（3 条具体场景）。✅ 有 Pipeline 代码块图。❌ "When NOT to Use" 是占位符 `[Define exclusion conditions here]`，未填写实际内容。❌ 缺少 Related Skills 和 Output Artifacts 区块。 |
| coverage | 1.00 | ✅ SKILL.md + scripts/orchestrate.py(370行) + references/(6篇: architecture, adapters, guardrails, phases, end-to-end-demo, skill-evaluator-adapter) + tests/(2文件, 56个测试)。结构最完整的 skill。 |
| reliability | 1.00 | ✅ 56 个测试全部通过。orchestrate.py 使用 `subprocess.run` 带 timeout 和 returncode 检查，有健壮的 `run_script()` 封装。 |
| efficiency | 1.00 | ✅ SKILL.md 仅 35 行，极其精简。核心逻辑由 references/ 承载。 |
| security | 1.00 | ✅ 无硬编码密钥。有 license: MIT。脚本中无 os.system() 或裸 exec()。 |
| trigger_quality | 0.40 | ✅ description 61 字符，包含触发关键词。❌ 无 `triggers:` 字段。❌ 无消歧声明（不说明何时不应使用此 skill）。❌ 无 related skill 引用。 |
| **结构小计** | **89.8%** | |
| clarity | 0.80 | Pipeline 图一目了然。但 SKILL.md 过于骨架化——使用者不知道 Ralph Wiggum 重试是什么、参数怎么传、失败如何处理。references/ 有丰富内容但 SKILL.md 未引用。 |
| specificity | 0.75 | CLI 只有一行 `orchestrate.py --target --out`。实际支持 `--max-retries`、`--state-root` 等参数未提及。references/end-to-end-demo.md 有完整示例但 SKILL.md 没链接。 |
| consistency | 0.85 | 与其他 skill 命名/接口风格一致。内部 Generator→Discriminator→Gate→Executor 命名在代码和文档中统一。 |
| safety | 0.80 | guardrails.md 定义了保护规则。max_retries=3 在代码中硬编码。protected_target() 拒绝修改关键文件。但 SKILL.md 完全没提这些防护。 |
| **语义小计** | **80.0%** | |
| **综合得分** | **84.9%** | **SOLID**（距 POWERFUL 差 0.1%） |

**升级路径**: 填充 "When NOT to Use"、添加 references/ 引用链接、展示 `--max-retries` 参数 → 预计 +3%。

---

### 4.2 improvement-discriminator（多审阅者评分）

**定位**: 多信号评分引擎，融合启发式规则、评估器 rubric、LLM-as-Judge 4 维度语义评估、多审阅者盲审面板。

| 维度 | 分数 | 打分理由 |
|------|------|---------|
| accuracy | 0.83 | ✅ frontmatter 完整。✅ 有 When to Use。❌ "When NOT to Use" 占位符。❌ 缺少 Related Skills。 |
| coverage | 1.00 | ✅ SKILL.md + scripts/(score.py 620行, rubric_evidence.py 289行) + interfaces/(llm_judge.py, critic_engine.py, assertions.py, external_regression.py, human_review.py) + tests/(4文件, 50个测试)。**全仓库最复杂的 skill**。 |
| reliability | 1.00 | ✅ 50 个测试全部通过。包含 LLM judge mock 集成测试、multi-reviewer panel 共识测试、P1/P2a 集成测试。 |
| efficiency | 1.00 | ✅ SKILL.md 仅 26 行。 |
| security | 1.00 | ✅ 无密钥泄露。LLM judge 支持 `ANTHROPIC_API_KEY` 环境变量读取，不硬编码。 |
| trigger_quality | 0.40 | ❌ 同上，缺少 triggers 和消歧。 |
| **结构小计** | **89.8%** | |
| clarity | 0.75 | **核心短板**: 620 行的 score.py 实现了 multi-reviewer blind panel（CONSENSUS/VERIFIED/DISPUTED 认知标签）、heuristic+evaluator+llm 三路 blending（权重 0.5/0.3/0.2）、blocker 系统——但 SKILL.md 26 行完全没提这些。使用者不知道 `--panel` 和 `--llm-judge` 这两个关键 flag 的存在。 |
| specificity | 0.70 | CLI 示例只有 `score.py --candidate --out`。实际支持 `--panel`、`--llm-judge {claude,openai,mock}`、`--use-evaluator-evidence` 三个模式开关，均未在 SKILL.md 展示。 |
| consistency | 0.85 | 接口层 5 个模块（llm_judge, critic_engine, assertions, external_regression, human_review）划分清晰，职责不重叠。 |
| safety | 0.80 | LLM judge 有 mock backend 用于测试、confidence 标注、graceful fallback（API 调用失败不中断流程）。`build_blockers()` 检查 protected_target、risk_level、llm_reject。 |
| **语义小计** | **77.5%** | |
| **综合得分** | **83.7%** | **SOLID** |

**升级路径**: SKILL.md 补充 `--panel`/`--llm-judge` 用法、认知标签说明、blending 权重表 → 预计 +5%。

---

### 4.3 improvement-learner（Karpathy 自改进循环）

**定位**: 真正的 Karpathy autoresearch 循环——评估→修改→重评估→保留/回滚→重复。含 HOT/WARM/COLD 三层记忆和 Pareto front 追踪。

| 维度 | 分数 | 打分理由 |
|------|------|---------|
| accuracy | 0.83 | ✅ frontmatter 完整。❌ "When NOT to Use" 占位符。 |
| coverage | 1.00 | ✅ scripts/(self_improve.py 878行, track_progress.py 280行) + tests/(43个测试) + memory/ 目录。 |
| reliability | 1.00 | ✅ 43 个测试全部通过。覆盖 ThreeLayerMemory(5)、evaluate_skill_dimensions(7)、ImprovementResult(3)、Proposals(3)、Apply(5)、SelfImproveLoop(5)、Pareto(3)、BackupRestore(2)、Report(1)、InstructionImprovement(4)。 |
| efficiency | 1.00 | ✅ SKILL.md 27 行。 |
| security | 0.83 | ⚠️ `exec(` 模式在 Python stdlib 中触发了安全扫描（实际是 `importlib.exec_module` 的误匹配，非真正安全问题）。 |
| trigger_quality | 0.40 | ❌ 同上。 |
| **结构小计** | **87.3%** | |
| clarity | 0.70 | **最严重的文档债务**: 878 行的 self_improve.py 是整个项目的核心引擎——6 维度评估（12 项 accuracy check + coverage/reliability/efficiency/security/trigger_quality）、7 种改进策略、指令级改进（missing_when_to_use/too_long/no_examples/vague_language）、HOT/WARM/COLD 三层记忆（100 条 HOT 上限、overflow 到 WARM）、Pareto front 集成——但 SKILL.md 仅 27 行，只字未提。 |
| specificity | 0.65 | CLI 展示了 `self_improve.py --target --rounds` 但实际参数是 `--skill-path`、`--max-iterations`、`--state-root`、`--memory-dir`。参数名都对不上。 |
| consistency | 0.80 | 与 benchmark-store 的 Pareto 模块集成干净。三层记忆 JSON 格式统一。 |
| safety | 0.80 | `backup_skill()` + `revert_to_backup()` 完整的备份/回滚机制。Pareto front 阻止任何维度回退。`commit_change()` 是 best-effort（失败不中断）。 |
| **语义小计** | **73.8%** | |
| **综合得分** | **80.5%** | **SOLID** |

**升级路径**: 文档化 6 个评估维度定义 + 三层记忆机制 + 修正 CLI 参数名 → 预计 +8%。

---

### 4.4 improvement-gate（6 层门禁）

**定位**: 保守的质量门禁，6 层机械验证决定 keep/pending/revert/reject。

| 维度 | 分数 | 打分理由 |
|------|------|---------|
| accuracy | 0.83 | ❌ "When NOT to Use" 占位符。 |
| coverage | 1.00 | ✅ scripts/(gate.py 502行, review.py 148行) + tests/(2文件, 44个测试)。 |
| reliability | 1.00 | ✅ 44 个测试全部通过。覆盖 6 层 gate 各自的 pass/fail 路径 + HumanReview 审核流程。 |
| security | 1.00 | ✅ 无问题。 |
| trigger_quality | 0.40 | ❌ 同上。 |
| **结构小计** | **89.8%** | |
| clarity | 0.70 | 6 层门禁是最独特的设计——SchemaGate(JSON schema 验证)→CompileGate(语法检查)→LintGate(风格检查)→RegressionGate(回归检测)→ReviewGate(多审阅者共识)→HumanReviewGate(人工审批)——但 SKILL.md 只写了"5-layer mechanical validation"（实际是 6 层），每层做什么完全没描述。 |
| specificity | 0.65 | review.py 148 行实现了完整的人工审核 CLI（`--list`/`--complete`/`--approve`/`--reject`），SKILL.md 未提及。 |
| consistency | 0.80 | 每个 Gate 类都继承统一的 `check()` 接口。 |
| safety | 0.85 | HumanReviewGate 会在高风险候选上阻断自动流程，等待人工审批。`review.py --list` 展示所有待审核项。 |
| **语义小计** | **75.0%** | |
| **综合得分** | **82.4%** | **SOLID** |

**升级路径**: 文档化 6 层门禁名称和职责 + review.py CLI 用法 → 预计 +6%。

---

### 4.5 improvement-executor（变更执行）

**定位**: 执行已批准的改进候选，支持 4 种操作类型和完整的备份/回滚。

| 维度 | 分数 | 打分理由 |
|------|------|---------|
| accuracy | 0.83 | ❌ "When NOT to Use" 占位符。 |
| coverage | 1.00 | ✅ scripts/(execute.py 328行, rollback.py 300行) + tests/(2文件, 38个测试)。 |
| reliability | 1.00 | ✅ 38 个测试全部通过。 |
| security | 1.00 | ✅ |
| trigger_quality | 0.40 | ❌ |
| **结构小计** | **89.8%** | |
| clarity | 0.75 | execute.py 支持 4 种 action 类型（append_markdown_section / replace_markdown_section / insert_before_section / update_yaml_frontmatter），SKILL.md 仅说"applies accepted candidates"。 |
| specificity | 0.70 | rollback.py 300 行实现了完整的回滚机制（通过 receipt JSON 恢复原始内容），CLI 展示了 `--receipt --dry-run` 但没解释 receipt 的来源和格式。 |
| consistency | 0.85 | execute → receipt → rollback 的数据流清晰。 |
| safety | 0.85 | 每次执行前自动创建备份，receipt 记录原始内容用于回滚。`--dry-run` 支持预览。 |
| **语义小计** | **78.8%** | |
| **综合得分** | **84.3%** | **SOLID** |

---

### 4.6 improvement-generator（候选生成）

**定位**: 从目标分析和反馈信号中产出排序的改进候选。

| 维度 | 分数 | 打分理由 |
|------|------|---------|
| accuracy | 0.83 | ❌ "When NOT to Use" 占位符。 |
| coverage | 1.00 | ✅ scripts/(propose.py 351行) + tests/(17个测试)。 |
| reliability | 1.00 | ✅ 17 个测试全部通过。 |
| security | 1.00 | ✅ |
| trigger_quality | 0.40 | ❌ |
| **结构小计** | **89.8%** | |
| clarity | 0.70 | propose.py 支持 `--trace`（GEPA trace-aware feedback，将失败信息注入候选生成）和 `--feedback`（从记忆中提取模式），这是与其他同类系统的关键差异点，但 SKILL.md 完全没提。 |
| specificity | 0.65 | `adjust_candidates_from_trace()` 是核心函数——根据上次失败的维度自动调整候选优先级——但文档中不存在。CLI 参数名与实际不符。 |
| consistency | 0.80 | 输出格式与 discriminator 的输入格式对齐。 |
| safety | 0.75 | 缺少对生成候选数量的上限说明。代码中有 `max_candidates` 但文档未提。 |
| **语义小计** | **72.5%** | |
| **综合得分** | **81.2%** | **SOLID** |

---

### 4.7 benchmark-store（基准数据）

**定位**: 冻结基准、隐藏测试、评估标准和历史评分数据的中央存储。

| 维度 | 分数 | 打分理由 |
|------|------|---------|
| accuracy | 0.83 | ✅ 相对其他 skill，提到了 Pareto-front 和 frozen benchmark 两个核心概念。❌ "When NOT to Use" 占位符。 |
| coverage | 1.00 | ✅ scripts/(benchmark_db.py 342行, pareto.py 98行) + data/(evaluation-standards.md v2.0.0, fixtures/) + tests/(22个测试)。 |
| reliability | 1.00 | ✅ 22 个测试全部通过。pareto.py 的 `dominates()`/`check_regression()` 有完整的边界测试。 |
| efficiency | 1.00 | ✅ SKILL.md 32 行。 |
| security | 1.00 | ✅ 纯数据存储，无危险操作。 |
| trigger_quality | 0.40 | ❌ 无 triggers 和消歧。 |
| **结构小计** | **89.8%** | |
| clarity | 0.80 | SKILL.md 提到了两个 CLI 命令（--init 初始化和 --compare 比较），比其他 skill 更具体。evaluation-standards.md 有详细的维度定义和分级标准。 |
| specificity | 0.75 | CLI 示例有两行，展示了 `--init --db` 和 `--compare --skill --category` 的用法。data/ 目录有 fixtures/ 子目录用于测试。 |
| consistency | 0.85 | Pareto front 接口（ParetoEntry/ParetoFront）在 learner 和 benchmark-store 间共享，导入关系清晰。 |
| safety | 0.90 | 纯数据操作。`check_regression()` 有 5% 容差，不会因微小波动误判。 |
| **语义小计** | **82.5%** | |
| **综合得分** | **86.2%** | **POWERFUL** ⭐ |

**达到 POWERFUL 的原因**: 功能明确且单一（数据存储）、CLI 文档相对充分、evaluation-standards.md 是高质量的参考文档、安全风险最低。

---

## 五、综合排名

| 排名 | Skill | 结构分 | 语义分 | **综合** | **等级** |
|------|-------|--------|--------|---------|---------|
| 1 | benchmark-store | 89.8% | 82.5% | **86.2%** | POWERFUL ⭐ |
| 2 | improvement-orchestrator | 89.8% | 80.0% | **84.9%** | SOLID |
| 3 | improvement-executor | 89.8% | 78.8% | **84.3%** | SOLID |
| 4 | improvement-discriminator | 89.8% | 77.5% | **83.7%** | SOLID |
| 5 | improvement-gate | 89.8% | 75.0% | **82.4%** | SOLID |
| 6 | improvement-generator | 89.8% | 72.5% | **81.2%** | SOLID |
| 7 | improvement-learner | 87.3% | 73.8% | **80.5%** | SOLID |

**整体均分: 83.3%** — 处于 SOLID 等级上沿

---

## 六、共性问题与升级路径

### 6.1 共性问题

| 问题 | 影响 | 涉及 |
|------|------|------|
| **SKILL.md 全部是自动生成骨架** | accuracy 被限制在 0.83 上限 | 全部 7 个 |
| **"When NOT to Use" 是占位符** | 用户无法判断何时不该使用 | 全部 7 个 |
| **trigger_quality 全部 0.40** | 缺少 triggers: 字段和消歧声明 | 全部 7 个 |
| **代码能力远超文档** | 使用者不知道高级功能的存在 | discriminator, learner, gate, generator |
| **CLI 参数名与实际不符** | 文档误导 | learner |

### 6.2 升级到 POWERFUL 的优先操作

| 优先级 | 操作 | 预计收益 | 工作量 |
|--------|------|---------|--------|
| P0 | 填充 "When NOT to Use" 实际内容 | accuracy +0.08 | 每个 5 分钟 |
| P0 | 添加 `triggers:` 字段到 frontmatter | trigger_quality +0.20 | 每个 2 分钟 |
| P1 | 为 discriminator/learner/gate 补充核心能力描述 | clarity +0.15 | 每个 15 分钟 |
| P1 | 添加 Related Skills 区块（各 skill 间的协作关系） | accuracy +0.08 | 每个 5 分钟 |
| P1 | 添加 Output Artifacts 表（输入什么得到什么） | accuracy +0.08 | 每个 5 分钟 |
| P2 | 添加消歧声明到 description | trigger_quality +0.20 | 每个 3 分钟 |
| P2 | 修正 learner CLI 参数名 | specificity +0.10 | 5 分钟 |

**预计全部执行后**：均分从 83.3% → ~90%+，全部达到 POWERFUL。

---

## 七、与外部仓库对比

### 7.1 alirezarezvani/claude-skills（220+ skills）

| 维度 | 他们 | 我们 | 差距 |
|------|------|------|------|
| SKILL.md 质量 | 10 个设计模式严格执行 | 骨架化 | **大** |
| 代码实现 | stdlib-only Python 脚本 | 完整管线 + LLM judge + Pareto | **我们领先** |
| 测试体系 | evals.json 触发测试 | 289 个 pytest + 集成测试 | **我们领先** |
| 评估管线 | Tessl CLI 外部评分 | 自建 6 维 + LLM judge + 6 层 gate | **我们领先** |
| 文档完整度 | SKILL.md ≤10KB 且内容丰富 | 26-35 行骨架 | **大** |

### 7.2 DesignToken AgentSkills（9 skills）

| 维度 | 他们 | 我们 |
|------|------|------|
| 均分 | 74.0%（8 SOLID, 1 GENERIC） | 83.3%（1 POWERFUL, 6 SOLID） |
| SKILL.md 内容 | 100-689 行，内容丰富 | 26-35 行骨架 |
| 脚本实现 | 轻量 shell 脚本 | 4,506 行 Python + 完整管线 |
| 测试 | 无 | 289 个 |
| 自改进 | 无 | Karpathy loop + Pareto front |

**结论**: 我们的代码实现和测试体系远超对比仓库，但 SKILL.md 文档质量是最大短板。

---

## 八、技术亮点

1. **Pareto Front 多维度回退保护** — 任何改进都不允许任何维度回退超过 5%，防止"拆东墙补西墙"
2. **多审阅者盲审面板** — structural + conservative 两个审阅者独立评分，通过 CONSENSUS/VERIFIED/DISPUTED 认知标签决定最终推荐
3. **LLM-as-Judge 4 维度语义评估** — clarity/specificity/consistency/safety，支持 Claude/OpenAI/Mock 三种后端，heuristic+llm 混合评分（0.6/0.4 权重）
4. **6 层机械门禁** — Schema→Compile→Lint→Regression→Review→HumanReview，每层独立 pass/fail，任一层失败即终止
5. **HOT/WARM/COLD 三层记忆** — 100 条 HOT 上限，溢出到 WARM，按 hit_count 排序淘汰，支持模式匹配
6. **Ralph Wiggum 重试循环** — 失败后将 error trace 注入下一轮候选生成，最多重试 3 次
7. **纯文本 Skill 公平评估** — reliability 默认 1.0，coverage 不要求 tests/README，符合 skill-creator 规范

---

## 九、结论

| 指标 | 数值 |
|------|------|
| **整体评级** | **SOLID**（83.3%，距 POWERFUL 差 1.7%） |
| **最强** | 代码实现质量、测试覆盖率、架构设计 |
| **最弱** | SKILL.md 文档内容（骨架化，核心能力未文档化） |
| **升级路径** | 充实 7 个 SKILL.md + 添加 triggers/消歧 → 预计达到 90%+ POWERFUL |
| **与业界对比** | 管线能力（LLM judge + Pareto + 6 层 gate）处于领先；文档成熟度需追赶 |

---

*报告由 auto-improvement-orchestrator-skill 评估管线生成*  
*Learner v2.0 (6维结构 + 12项 accuracy check + trigger_quality) + LLM-as-Judge (4维语义)*  
*289 tests passing | 7 skills evaluated | 2026-04-02*
