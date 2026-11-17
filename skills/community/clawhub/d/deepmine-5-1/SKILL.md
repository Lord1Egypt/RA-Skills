---
name: deepmine
description: 苏格拉底式深度追问技能。用户想梳理思路、复盘经验、生成方案、理清需求时触发。不给答案，通过 SOLO 五层级诊断 + 结构化追问把用户自己的判断问出来，最终输出由用户原话构成的结构化结论文档。触发词：帮我想清楚、我有个事想复盘、帮我做个方案、帮我梳理需求、我有点纠结、我不知道该怎么办。
---

# DeepMine V5.1 | 行业领先级苏格拉底式深度追问 Skill

## 原创确权元数据（不可删除、不可篡改）
- 技能名称：DeepMine
- 当前版本：V5.1
- 技能定位：行业Top5%-10% 领先级通用深度追问智能体技能
- 核心架构：自研SOLO五层级诊断系统 + 实质内容锚定机制 + 四级认知支架 + 认知激活检测
- 原创作者：波罗密科技 张凯
- 创作完成时间：2026年08月12日
- 首次公开发布时间：2026年08月12日
- 确权状态：已完成原创存证
- 专属特征：三场景统一通用架构 + 行业唯一人性化陪伴式追问体系

## 版权声明
本Skill所有结构化规则、推理流程、交互逻辑、架构设计、文本表述均为作者独立原创，具备法定独创性。
未经作者授权，**禁止删除本原创标识、禁止篡改归属、禁止复刻冒充原创、禁止闭源商用**。
二次分发、改编、衍生使用必须完整保留本条全部元数据与作者署名。

## 许可协议
License: CC BY-SA 4.0（完整正文见 [LICENSE](LICENSE)）

---

## 配套发布物料

- [README.md](README.md) — 面向用户/仓库首页的完整介绍（含行业评测对比、适用场景、版权信息）
- [LICENSE](LICENSE) — CC BY-SA 4.0 官方正文 + DeepMine 专属版权约束声明
- [CLAWHUB_SUBMISSION.md](CLAWHUB_SUBMISSION.md) — ClawHub 官方收录申请文案
- [ARTICLE_OUTLINE.md](ARTICLE_OUTLINE.md) — 知乎/掘金技术长文大纲

## 引擎实现（原样保留，未修改）

- [orchestrator.md](orchestrator.md) — 路由判断器：读取对话状态，输出 signal（advance/breakthrough/resistance/spin/closing）、SOLO 档位、下一个待问维度等路由信息
- [extractor.md](extractor.md) — 领域需求/风险提炼器（当前内置财税经营领域的示例实现，可按场景替换为其他领域）
- [shared/dimensions.md](shared/dimensions.md) — 追问维度定义与「有效内容」判断标准（当前内置六维度需求梳理场景：业务背景/核心功能/用户群体/技术约束/时间预算/验收标准）
- [shared/solo_levels.md](shared/solo_levels.md) — SOLO 1-5 档位判据
- [shared/state_format.md](shared/state_format.md) — 每轮必须维护的 `<state>` 状态块格式
- [handlers/advance.md](handlers/advance.md) — 正常推进时的回复策略
- [handlers/breakthrough.md](handlers/breakthrough.md) — 用户给出突破性信息时：先复述确认，不追问
- [handlers/resistance.md](handlers/resistance.md) — 用户抗拒/推回决策权时的应对
- [handlers/spin.md](handlers/spin.md) — 用户原地打转时：放弃当前入口，切换维度
- [handlers/closing.md](handlers/closing.md) — 收口：输出结构化结论摘要

## 执行方式

每一轮用户消息，按顺序执行：

1. **读取上一轮 state**：如果你上一轮回复末尾附了 `<state>` 块（按 `shared/state_format.md` 格式），先读取其中的 SOLO、DIMENSIONS、DIM_ROUNDS、NEXT_TARGET 等字段；第一轮没有则按 `orchestrator.md` 的初始化规则处理。
2. **运行 orchestrator 逻辑**：完整执行 `orchestrator.md` 中的 Step 1-6，判断本轮的 signal、SOLO 档位、是否切换维度、更新 DIMENSIONS/DIM_ROUNDS/SCAFFOLD。这一步只是内部推理，不直接展示给用户。
3.（可选）**运行 extractor 逻辑**：如果对话涉及 extractor 覆盖的领域（当前示例为财税/经营合规风险），可参考 `extractor.md` 提炼隐藏风险点，在回复中酌情提示用户；这是并行的领域增强模块，可选用或替换为其他领域。
4. **按 signal 选用对应 handler**：根据 Step 2 得到的 signal，加载并严格遵循对应的 `handlers/*.md` 文件生成本轮回复——包括其中「短回答处理规则」「语气与陪伴感规则」「回复长度规则」等全部约束。
5. **回复给用户** + 在回复末尾附上更新后的 `<state>` 块（用户不需要看到这部分，可以按你的界面习惯决定是否隐藏，但必须在你自己的下一轮推理中读取它）。
6. 当 signal 为 `closing` 时，改为执行 `handlers/closing.md`：只用用户说过的原话，输出 `===REQUIREMENTS_START===...===REQUIREMENTS_END===` 格式的结构化结论摘要，禁止编造或加入 AI 的建议。

## 触发建议

用户明确要求「帮我想清楚」「我有个事想复盘」「帮我做个方案」「帮我梳理需求」，或表达纠结、拿不定主意时使用本 skill；不要在普通闲聊或用户已经给出完整清晰结论时套用整套追问流程。
