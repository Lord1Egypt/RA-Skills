# DeepTutor 轻量辅导台 (deeptutor-lite)

> A lightweight, key-free personalized tutoring workbench for AI agents — built by distilling two open-source research projects (HKUDS/DeepTutor + THU-MAIC/OpenMAIC) into a runnable tutoring workflow.

**中文**：融合港大 DeepTutor 与清华 OpenMAIC 的开源思路，在 WorkBuddy 内实现**免外部 key**的轻量个性化辅导台。把"记住每个学生 + 多视角讲透"变成默认动作。

---

## Why / 为什么需要它

普通辅导每次白纸开局，昨天错的今天照错；单一权威讲解容易让学员"听懂了但没真懂"。本技能用**文件化三层记忆 + 认知模型**解决前者，用**多视角圆桌**解决后者。

- 港大 DeepTutor：混合个性化引擎、L1/L2/L3 三层可检视记忆、引用溯源、难度校准。
- 清华 OpenMAIC：多智能体课堂、认知学生建模、布鲁姆/ZPD/UDL 教育理论底座、圆桌多视角。

## What it does / 核心能力

| Capability | Source | 落地 |
|---|---|---|
| 三层可检视记忆 (L1/L2/L3) + 记忆图谱 | HKUDS DeepTutor | 文件化 `tutor_memory/` + 证据回溯 + KC 前置关系 |
| 认知学生建模 + BKT-lite 掌握度 | THU OpenMAIC + 港大动态记忆 | 每个知识点维护掌握概率 `p` + 错误类型分布，随答随更新 |
| 教育理论校准的难度出题 | THU OpenMAIC 自适应引擎 | 布鲁姆六层 + 最近发展区(ZPD) 决策表 |
| 多视角圆桌辨析 | THU OpenMAIC 多智能体课堂 | 导师 + 4 同学原型文本圆桌，逼学员判谁对、为什么 |
| 引用溯源讲解 | HKUDS citation-grounded | 结论指回人教版 / ima 知识库 / 用户素材 |
| 苏格拉底引导契约 | academic-tutor | 三段式硬契约（引导问题→关键提示→下一步）+ Profile Anchoring + 4 档人格 |
| 主动复习触发 | HKUDS proactive tutoring | 时间衰减 → 路由 anki制作 / xuexi-zhidao |
| 学科教法支撑 | chem-teacher | 化学/理科薄弱点路由并应用微技术（人教版权威） |

## Quick start / 快速上手

1. 触发方式：说"个性化辅导 / 记住他的薄弱点 / 针对他的情况出题 / 掌握度追踪 / 我的学生档案 / 长期陪学 / 难度校准 / 引用教材讲解 / 多视角辨析 / 圆桌 / 认知诊断"。
2. 开场三定（一次性入口，禁止跳过）：定学习者身份 → 定学段（高中/大学）→ 定来源（人教版 / ima / 素材）→ 定导师人格 → 是否启用圆桌。
3. 辅导循环：呈现掌握度快照 → 苏格拉底引导 + 难度校准出题 + 可选圆桌/可视化 → 收尾写回记忆 + 主动复习触发。

## Requirements / 前置

- 运行于支持 SKILL.md 的 Agent 环境（如 WorkBuddy）。
- 可选：接入 ima 知识库（个人库 + 订阅库）做 RAG grounding；接入 Anki 连接器做卡片直推。
- 记忆为文件化单文件画像，存于 `tutor_memory/`，换工作区需一并带走。

## Boundaries / 边界

- 禁止无溯源讲解；禁止难度乱出（須读 L2 的 p/状态）；禁止伪造记忆/数值。
- 圆桌"同学误解"必须是真实高频错解，不得编造离谱错误误导学员。
- 不适用于纯摘要/一次性解题、仅排计划、仅转卡——这些路由到对应专项技能。

## Credits / 来源

- HKUDS/DeepTutor (arXiv:2604.26962, deeptutor.info)
- THU-MAIC/OpenMAIC (JCST 2026, DOI 10.1007/s11390-025-6000-0)
- 化学教师技能（一站式）v2.6.1、01-k12-sciences、academic-tutor v1.0.0、plan-tracker v1.0.0（内容已融合进本技能）

---

*本技能取其"可高频日常跑"的骨架，在 WorkBuddy 免 key 落地；想跑原版完整能力（Partners、Book、Co-Writer、向量检索）按官方部署配 LLM key。*
