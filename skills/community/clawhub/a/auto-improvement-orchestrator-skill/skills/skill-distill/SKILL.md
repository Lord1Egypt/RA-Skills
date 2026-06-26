---
name: skill-distill
category: tool
description: |
  当需要把多个功能重叠的 skill 合并为一个蒸馏版 skill 时使用。
  不适用于从 skills 提取 rules（rules extraction is a separate capability from ECC's rules-distill skill, not part of this repo）或从 session 历史提取 skills（用 distill CLI）。
license: MIT
triggers:
  - 蒸馏.*skill
  - 合并.*skill
  - merge.*skill
  - distill.*skill
  - 多个.*skill.*合成
  - skill.*太多.*重复
  - consolidate.*skill
---

# Skill Distill — 多 Skill 蒸馏合并

把 N 个功能重叠的 skill 合并为 1 个蒸馏版 skill。

与 rules extraction（a separate capability from ECC's `rules-distill` skill, not part of this repo）和 `nclandrei/distill`（sessions → skills）不同，本 skill 的输入和输出都是 skill：skills → skill。

## When to Use

- 同一领域有 2+ 个 skill 功能重叠（如多个写作相关 skill）
- 用户分不清该用哪个 skill（路由冲突）
- 想减少 skill 总数降低元数据 token 开销

## When NOT to Use

- 从 skills 提取跨领域原则到 rules（rules extraction is a separate capability from ECC's `rules-distill` skill, not part of this repo）
- 从 session 历史提取重复模式为 skill（用 distill CLI / `skill-create`）
- 优化单个 skill 的质量（用 `improvement-orchestrator`）

<example>
正确用法：把 human-writing + slopbuster + humanizer 三个写作 skill 蒸馏为 deslop
输入：3 个 SKILL.md + 各自的 references/
分析：交集（两次 pass 流程、AI 模式列表）→ body；差集（中文特有模式、voice calibration）→ 独特贡献；长尾细节 → references/
输出：1 个 SKILL.md (~200 行) + 3 个 references/ 文件
reasoning: 三个 skill 有 70%+ 内容重叠，但各有 ~20% 独特贡献。蒸馏版保留所有独特贡献，去掉重复。
</example>

<anti-example>
错误用法：把 cpp-expert 和 ios-expert 蒸馏为一个
这两个 skill 领域不同（C++ 核心层 vs iOS 平台层），只是在同一个项目中配合使用。
MUST 蒸馏的是功能重叠的 skill，NEVER 蒸馏职责不同的 skill。
即使两个 skill 经常一起触发，如果它们解决的是不同问题，就不该合并。
</anti-example>

## Workflow

MUST 按 4 个 Phase 顺序执行。NEVER 跳过 Phase 2 直接写输出。

### Phase 1: 收集（确定性）

读取所有源 skill 的完整内容：

```
对每个源 skill:
  1. Read SKILL.md → 提取 frontmatter、body sections、example/anti-example
  2. Read references/*.md → 提取详细规则和示例
  3. 统计行数和 token 估算
```

输出 Inventory 表：

```
Skill Distillation — Phase 1: Inventory
────────────────────────────────────────
Sources: {N} skills
Total content: ~{X} lines / ~{Y}k tokens

| Source | Lines | Sections | References | Unique contribution |
|--------|-------|----------|------------|-------------------|
| skill-A | 200 | 12 | 2 files | ... |
| skill-B | 280 | 15 | 5 files | ... |
```

### Phase 2: 分析（LLM 判断）

对所有源 skill 内容做交叉分析，每条知识点分类为 4 种：

| 分类 | 定义 | 去向 |
|------|------|------|
| **交集** | 2+ 个源 skill 都有，表述相似 | 去重后进 body |
| **独特贡献** | 只在 1 个源 skill 中有，但有价值 | 保留，进 body 或 references |
| **冲突** | 2+ 个源 skill 说法矛盾 | 展示给用户决定 |
| **冗余** | 可从 LLM 通用知识推导出 | 丢弃（token 效率） |

MUST 逐条标注来源 skill。NEVER 无标注地混合内容。

**Token 预算控制**：
- SKILL.md body: ≤500 行（skill-creator 规范）
- 交集内容的精简版进 body，完整版进 references/
- 每个独特贡献评估"值不值 token"——如果只在特定场景有用，放 references/

### Phase 3: 用户确认

展示蒸馏方案：

```
# Distillation Plan

## Target: {new-skill-name}
Sources: {source list}

## Body content (~{N} lines)
- {section 1}: 交集，来自 A+B+C
- {section 2}: 独特贡献，来自 A
- {section 3}: 独特贡献，来自 B

## References
- full-xxx.md: 完整 {topic}（~{N} lines）来自 A+C
- yyy.md: {topic}（~{N} lines）来自 B

## Conflicts (需要你决定)
1. A 说 X，B 说 Y → 你选哪个？

## Dropped (冗余，LLM 已知)
- {list}

## Source skill 处理
- 保留源 skill（蒸馏版作为补充）
- 替换源 skill（删除源，只用蒸馏版）
- 降级源 skill（源 skill 的 description 指向蒸馏版）
```

MUST 等用户确认后再生成文件。NEVER 自动生成不经确认。

### Phase 4: 生成 + Pipeline 验证

按确认的方案生成：

```
{new-skill}/
├── SKILL.md          # body ≤500 行
└── references/       # 长尾详细内容
    ├── full-xxx.md
    └── yyy.md
```

生成后 MUST 接入 improvement pipeline 验证——这是蒸馏闭环的关键，NEVER 跳过：

```
Step 1: 跑 improvement-learner 评分
  python3 ~/.claude/skills/improvement-learner/scripts/self_improve.py \
    --skill-path {new-skill-path} --max-iterations 1

Step 2: 检查结果
  accuracy ≥ 0.80 → PASS，蒸馏完成
  accuracy < 0.80 → 跑 orchestrator 优化:
    python3 ~/.claude/skills/improvement-orchestrator/scripts/orchestrate.py \
      --target {new-skill-path} --state-root /tmp/skill-distill-state --auto

Step 3: (可选) 如有 task_suite.yaml → 跑 evaluator 执行验证
  python3 ~/.claude/skills/improvement-evaluator/scripts/evaluate.py \
    --standalone --task-suite {new-skill-path}/task_suites/task_suite.yaml \
    --state-root /tmp/skill-distill-eval
```

即使 learner 分数满分，如果有 task_suite 也 MUST 跑 evaluator——结构评分高不等于执行效果好（changelog-gen 的教训）。

## 蒸馏标准

### 值得蒸馏的信号

- 2+ 个 skill 的 triggers 有 50%+ 重叠
- 用户多次被问"用 A 还是 B"
- 同一个任务需要同时加载 2+ 个 skill

### 不值得蒸馏的信号

- 两个 skill 解决的是流程中不同阶段的问题（如 generator vs evaluator）
- 重叠只在 frontmatter description 层面，body 内容完全不同
- 合并后 SKILL.md body 会超 500 行

### Harness 配置合并

如果任一源 skill 包含 execution-harness 配置（Ralph 状态、Handoff 模板、Hook 声明），distill 必须：

1. 合并 harness 配置到蒸馏版——取所有源的 pattern 并集
2. 冲突时取更严格的配置（如 max_iterations 取最小值）
3. 在 SKILL.md 的 Related Skills 中注明依赖的 harness pattern

### 蒸馏质量检查

| 检查项 | 标准 |
|--------|------|
| 无信息丢失 | 源 skill 的每条独特贡献在蒸馏版中有对应 |
| body 精简 | ≤500 行，详细内容在 references/ |
| 来源可追溯 | 每个 section 标注来自哪个源 skill |
| learner 评分 | accuracy ≥ 0.80 |
| 路由不冲突 | triggers 不和其他 skill 重叠 |
| harness 完整 | 源 skill 的 harness pattern 全部保留 |

## Output Artifacts

| 请求 | 交付物 |
|------|--------|
| 蒸馏 | 新 skill 目录 + learner 评分 |
| 分析 | 蒸馏方案（不生成文件，只输出分析） |

## Related

- `skill-creator` — 单个 skill 的创建规范
- `skill-forge` — 从 spec 自动生成 skill + task_suite
- `rules-distill` (external, from ECC) — 从 skills 提取 rules（不是合并 skills, not part of this repo）
- `improvement-orchestrator` — 优化单个 skill 的质量

## References

- 蒸馏决策模板和完整检查清单: `references/distillation-checklist.md`
