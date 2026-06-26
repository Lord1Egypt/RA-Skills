# Skill 评估标准详情

> 版本：2.0.0  
> 最后更新：2026-04-02  
> 参考：alirezarezvani/claude-skills SKILL-AUTHORING-STANDARD, anthropics/claude-plugins-official

---

## 质量分级（Quality Tiers）

> 基于综合评分（accuracy×0.3 + coverage×0.2 + reliability×0.2 + efficiency×0.15 + security×0.15）

| Tier | Score | 标准 | 发布策略 |
|------|-------|------|---------|
| **POWERFUL** ⭐ | 85%+ | 专家级内容，trigger 描述清晰，有输出物和关联 Skill，通过全部门禁 | 推荐发布到 ClawHub/Marketplace |
| **SOLID** | 70–84% | 内容可靠，结构完整，YAML frontmatter 齐全 | 可发布到 GitHub |
| **GENERIC** | 55–69% | 过于通用，缺少领域深度或结构不完整 | 内部使用，需迭代 |
| **WEAK** | <55% | 缺少 SKILL.md 或核心结构缺失 | 拒绝或完全重写 |

**Only POWERFUL ships to production marketplaces.**

## 核心设计原则

### 纯文本 Skill 同等对待

Per skill-creator 规范，**只有 SKILL.md 是必需的**。scripts/, references/, tests/, assets/ 均为可选。
- 纯文本 Skill（无 scripts/）的 reliability 默认 1.0
- coverage 以 SKILL.md 存在为基础（60%），可选目录加分
- SKILL.md > 500 行且无 references/ 会被扣分（渐进式披露）

### 10 个质量模式（来自 alirezarezvani/claude-skills）

1. **Context-First** — 检查已有上下文再提问
2. **Practitioner Voice** — 专家视角，有观点，非百科全书
3. **Multi-Mode Workflows** — 至少 2 个工作流入口
4. **Related Skills Navigation** — WHEN/NOT 消歧
5. **Reference Separation** — SKILL.md 是工作流，references/ 是知识库
6. **Proactive Triggers** — 4-6 个主动发现问题的条件
7. **Output Artifacts** — 请求到交付物的映射表
8. **Quality Loop** — 自验证 + 置信度标注
9. **Communication Standard** — Bottom Line First
10. **Python Tools** — stdlib-only, CLI-first, JSON 输出

---

## 评估维度（5 dimensions, 0.0–1.0 each）

### 1. 准确性（Accuracy）— SKILL.md 质量

**12 项检查** (每项通过 = 1/12 分):
1. YAML frontmatter 存在
2. frontmatter 有 `name:`
3. frontmatter 有 `description:`
4. description 包含触发关键词（>40 字符，"pushy"）
5. 有 "When to Use" 区块
6. 有 "When NOT to Use" 区块
7. 有代码示例（```）
8. 有 Usage/CLI 区块
9. 无模糊语言（etc., you might consider...）
10. 足够长度（>= 15 行）
11. 有 Related Skills/References 区块
12. 有 Output Artifacts/Deliverables 区块

**目标值**: ≥ 0.85

---

### 2. 覆盖率（Coverage）— 结构完整性

**计分规则**:
- SKILL.md 存在 = 60% 基础分
- scripts/ 存在 = +10%
- references/ 存在 = +10%
- tests/ 存在 = +10%
- README.md 存在 = +10%
- SKILL.md > 500 行且无 references/ = -20%

**注意**: 只有 SKILL.md 是必需的，其他均为加分项

---

### 3. 可靠性（Reliability）— 测试结果

| 场景 | 得分 |
|------|------|
| 有 tests/ 且 pytest 通过 | 1.0 |
| 有 tests/ 但 pytest 失败 | 0.5 |
| 有 scripts/ 但无 tests/ | 0.3（应该有测试） |
| 纯文本 Skill（无 scripts/） | 1.0（合法，无需测试） |

---

### 4. 效率（Efficiency）— SKILL.md 长度

```
score = min(1.0, max(0.3, 1.0 - (lines - 200) / 1000))
```
200 行以下 = 1.0，1200 行以上 = 0.3

---

### 5. 安全性（Security）

**SKILL.md 检查**（不检查实现代码）:
- 无 `api_key =` / `password =`
- 无 `sk-` API key 模式
- frontmatter 有 `license:`

**实现代码检查**:
- 无 `os.system()` 调用
- 无裸 `exec()` 调用

---

## 按类别调整权重

### 默认权重

| 维度 | 权重 | 说明 |
|------|------|------|
| 准确性 | 30% | SKILL.md 质量是最重要的 |
| 覆盖率 | 20% | 结构完整性 |
| 可靠性 | 20% | 测试通过 |
| 效率 | 15% | 合理长度 |
| 安全性 | 15% | 无泄露 |

### 按 Skill 类别调整

| 类别 | accuracy | coverage | reliability | efficiency | security |
|------|----------|----------|-------------|------------|----------|
| Tool（工具型） | 25% | 15% | 30% | 15% | 15% |
| Knowledge（知识型/纯文本） | 40% | 20% | 10% | 20% | 10% |
| Orchestration（编排型） | 30% | 20% | 25% | 10% | 15% |
| Review（评审型） | 35% | 15% | 25% | 10% | 15% |
| Rule（规则型） | 35% | 20% | 15% | 15% | 15% |
| Learning（学习型） | 25% | 20% | 30% | 10% | 15% |

---

## 评估流程

### Full Pipeline（推荐）

```
Learner (5-dim structural)
  → Discriminator (multi-reviewer panel + optional LLM judge)
  → Gate (6-layer: Schema → Compile → Lint → Regression → Review → HumanReview)
  → Pareto front check (no dimension regression allowed)
```

### 1. 结构评估（Learner）

```bash
python3 skills/improvement-learner/scripts/self_improve.py \
  --skill-path /path/to/skill \
  --max-iterations 5
```

### 2. 多审阅者评分（Discriminator）

```bash
python3 skills/improvement-discriminator/scripts/score.py \
  --skill-path /path/to/skill \
  --panel \
  --llm-judge mock \
  --output reports/
```

### 3. 门禁验证（Gate）

```bash
python3 skills/improvement-gate/scripts/gate.py \
  --state-root /path/to/state
```

### 4. Karpathy 自改进循环

```bash
# 自主改进：评估 → 修改 → 重评估 → 保留/回滚 → 重复
python3 skills/improvement-learner/scripts/self_improve.py \
  --skill-path /path/to/skill \
  --max-iterations 10 \
  --memory-dir /path/to/memory
```

---

## 参考来源

| Repo | 贡献 |
|------|------|
| `alirezarezvani/claude-skills` | 10 个质量模式, SKILL_PIPELINE, 质量分级 |
| `affaan-m/everything-claude-code` | 116 skills 架构, 多 harness 支持 |
| `anthropics/claude-plugins-official` | 官方 plugin.json 标准 |
| `sbroenne/pytest-skill-engineering` | pytest 测试框架 for skills |
| `jensoppermann/agent-skill-scanner` | 安全扫描模式 |

---

*评估标准文档 v2.0.0*  
*最后更新：2026-04-02*
