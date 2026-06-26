# 来源地图与注意事项

这个 Skill 是面向 agent 使用的独立整理与来源标注。仓库在 `docs/` 下附带中英文 source PDFs，方便阅读和引用；Skill 指令避免长篇原文摘录，并使用原创 operational synthesis。

## 主要 startup 来源

- Anthropic / Claude blog: "The founder's playbook: Building an AI-native startup"，发布于 2026-05-14。
- English PDF: `docs/The-Founders-Playbook-05062026_v3.pdf`
- Chinese PDF: `docs/创业者手册-构建AI原生创业公司-中文.pdf`

被转化为 Skill 的核心思想：

- startup lifecycle 被重构为 `Idea`、`MVP`、`Launch`、`Scale`。
- founder 的角色从 individual contributor 转向 orchestrator of agents and systems。
- AI 的最大价值是压缩 research、coding 和 operational workflow loops，但不能绕过 evidence。
- 每个阶段都需要 exit criteria、failure modes 和 AI-assisted exercises。
- AI-native 的主要风险包括：未验证就 build、agentic technical debt、false PMF、founder bottleneck、推迟 security/compliance、缺少 operational maturity。
- Scale 阶段的 defensibility 来自 domain depth、user data loops、integrations、workflow lock-in 和 auditable operating systems。

## Agent Skills 来源

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills overview: https://agentskills.io/home
- Agent Skills creator best practices: https://agentskills.io/skill-creation/best-practices
- Anthropic Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Bilingual README layout reference: https://github.com/marswaveai/skills/tree/main

设计选择：

- `SKILL.md` 保持简洁，符合 progressive disclosure。
- frontmatter 保持 `name` 和 `description`。
- 把触发场景写进 description。
- 详细框架放入 `references/`。
- 中文用户优先加载 `.zh.md` reference 文件。
- 脚本只承担 deterministic helper output。

## 注意事项

- 依赖具体产品、beta features、APIs、security tools、compliance requirements 前，必须确认当前可用性。
- AI 生成的 security、legal、compliance、fundraising、financial 建议不能替代专业意见。
- 除非用户拥有相应权利，不要把 source documents 的长篇原文复制进下游 artifact。
- 基于本框架发布重要内容时，应标注公开来源。
