# Academic Results Writer (v1.2.1)

根据统计输出、图表、caption 和草稿撰写、修改和审计学术 Results 部分。是 `paper-results-reverse-engineer` v3.0 的正向写作搭档。

## 适用场景

- 根据统计结果写 Results（ANOVA、t 检验、回归、SEM、元分析等）
- 修改润色已有的 Results 草稿
- 将表格或图表转换为 Results 段落
- 审计 Results 是否存在 Discussion 泄露、因果膨胀或统计缺失
- 将 Results 适配目标期刊风格（心理学报、APA 等）
- 参考目标论文的 Results 结构来组织自己的结果（不复制内容）
- 使用 reverse-engineer v3.0 的 Module H Writer Transfer Packet 进行风格迁移

## 任务路由

| 用户说 | 任务类型 |
|--------|---------|
| "根据统计结果写 Results" | `write-from-statistics` |
| "润色/修改这段结果" | `revise-draft` |
| "根据这张表写结果段" | `table-to-results` |
| "根据这张图/caption 写结果" | `figure-to-results` |
| "检查结果部分有没有问题" | `audit-only` |
| "改成心理学报/APA 风格" | `journal-style` |
| "参考这篇论文的 Results 写法" | `target-paper-style-adaptation` |

## 默认输出格式

1. 【结果组织建议】
2. 【可直接使用的结果段】
3. 【统计报告检查】
4. 【结果与讨论边界提醒】
5. 【可选替代表达】

默认为标准深度（精简版）。用户明确要求时切换至完整审计深度。长输出自动切换至文件输出模式 → `~/Desktop/OpenClaw_Paper_Analysis/outputs_md/results_writer/`。

## 目标论文风格适配流程

1. **提取** → 目标论文的 Results 结构、段落模式、统计报告惯例和图表叙事方式
2. **设计匹配检查** → 哪些可迁移，哪些不能迁移
3. **风格迁移方案** → 适配后用于用户数据的组织结构
4. **撰写** → 仅使用用户自己的数据和统计结果

**Source Ledger（来源账本）为强制项：** 必须区分"目标来源 / 用户数据来源 / 用户草稿来源"。目标缺失时 fail-closed。

**核心护栏：** 不复制目标论文句子。不使用目标论文统计值。不将目标论文结论写成用户结果。8-section 输出仅在目标可访问且 ≥3 个可用证据点时启用。

## 双 Skill 联用流程

1. 使用 `paper-results-reverse-engineer` 拆解目标论文的 Results
2. 请求 Module H Writer Transfer Packet
3. 将 Module H 连同你自己的统计结果、图表、草稿一起输入 `academic-results-writer`
4. writer 仅迁移结构和叙事逻辑，绝不复制目标论文的句子、统计值、结论或图表解读

## Module H 桥接流程

当输入包含来自 `paper-results-reverse-engineer` v3.0 的 Module H Writer Transfer Packet 时：
- H1 → 来源账本
- H2 → 设计匹配判定
- H3–H5 → 结果组织与叙事
- H6 → Results–Discussion 边界
- H7 → 风险标记（不可迁移项）
- H8 → Writer 模式 / 输出深度

## 反抄袭规则

- 只迁移结果组织逻辑，不复制原句
- 只参考统计报告顺序，不复制目标论文统计值
- 只借鉴图表叙事方式，不复制图表解读
- 不将目标论文的理论解释或结论写入用户 Results
- 不模仿特定作者的个人写作风格
- 不生成可替代目标论文的近义段落

## 推荐上手 Prompts

### 根据统计结果写 Results

请使用 academic-results-writer，根据以下统计结果写 Results。默认中文，心理学论文风格。请输出：结果组织建议、可直接使用的结果段、统计报告检查、结果与讨论边界提醒、可选替代表达。不要补入我没有提供的统计值。

### 修改草稿

请使用 academic-results-writer，帮我修改下面这段 Results。要求：保留原有统计信息，不新增未提供的数据；检查 Discussion leakage、因果语言、统计报告格式和心理学报/APA 风格问题；给出修订版和修改说明。

### 图表转 Results

请使用 academic-results-writer，根据下面这张图/表及其 caption 写 Results 段落。要求：先说明图/表回答的问题，再描述图/表结构，然后报告主要趋势和统计证据。不要根据图像臆造没有提供的统计值。

### 目标论文风格适配

请使用 academic-results-writer，参考这篇目标文献的 Results 结构，帮助我写自己的 Results。只能迁移组织顺序、统计报告逻辑和图表叙事方式，不能复制目标文献句子、统计值、结论或理论解释。若目标文献与我的研究设计不兼容，请使用 design-incompatible fallback。

### Module H 桥接

请使用 academic-results-writer，并根据下面的 Module H Writer Transfer Packet 写作迁移包，帮助我把自己的统计结果写成 Results。只能迁移结构和叙事逻辑，不能复制目标文献句子、统计值、结论或理论解释。

## 示例

- `examples/write-from-anova.md` — 中文 ANOVA 结果段示例
- `examples/revise-draft.md` — 修改草稿示例
- `examples/figure-to-results.md` — 图表 caption → Results 段落
- `examples/target-paper-adaptation.md` — 设计不兼容目标适配
- `examples/module-h-bridge.md` — Module H 桥接示例

## 目录结构

```
academic-results-writer/
├── SKILL.md                      # skill 主定义
├── README.md                     # 本文件
├── CHANGELOG.md                  # 版本记录
├── docs/                         # 详细规范
│   ├── statistical-templates.md
│   ├── writing-templates.md
│   ├── figure-table-templates.md
│   ├── journal-style.md
│   ├── revision-mode.md
│   ├── target-paper-adaptation.md
│   ├── module-h-bridge.md
│   ├── quality-checklist.md
│   ├── sleep-eeg-guardrails.md
│   └── meta-analysis-guardrails.md
└── examples/                     # 使用示例
    ├── write-from-anova.md
    ├── revise-draft.md
    ├── figure-to-results.md
    ├── target-paper-adaptation.md
    └── module-h-bridge.md
```

## 版本

- **公开版本：** 1.2.1
- **内部版本：** academic-results-writer-v1.2.1-stable
- **适用范围：** 心理学及行为科学的学术 Results 写作
