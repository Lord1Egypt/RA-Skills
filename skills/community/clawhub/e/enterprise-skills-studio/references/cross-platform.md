# 跨平台适配（可移植性）

来源：Agentman《2026 Agent Skills 生态报告》、Anthropic 跨 surface 说明、用户目标平台清单。本技能产出的技能需能在多桌面 Agent 间移植。

## 一、开放标准底座

Agent Skills 规范于 2025-12-18 发布为开放标准 **agentskills.io**。采纳者含 OpenAI Codex、Cursor、Gemini CLI、VS Code、Goose、Databricks、Spring AI、Mistral，以及本技能面向的 **WorkBuddy、Claude Code、龙虾、Hermes** 等桌面 Agent。

→ 本技能产出的 `SKILL.md` 遵循标准格式，天然可移植，无需重写。

## 二、通用核心（跨平台一致）

- 目录结构：`SKILL.md` + `scripts/` + `references/` + `assets/`
- 字段规则：name / description 规范一致
- 三级加载：元数据→指令→资源，各平台均支持

## 三、平台差异与适配要点

| 平台 | 注意点 |
|------|--------|
| Claude Code | 支持项目级 `.claude/skills/`、动态命令；部分特性（动态上下文命令）在 chat/API 不一 |
| API 部署 | 容器无网络、不可运行时装包，依赖须预置；单包 ≤30MB |
| WorkBuddy / 龙虾 / Hermes | 遵循各自技能目录约定；触发方式/路径按平台文档微调 |
| 通用 | 跨 surface 不自动同步，以 Git 为单一真源，各 surface 分别 release |

## 四、适配做法

1. 先按 open standard 写一次（本技能默认产出即标准）
2. 针对目标平台做**轻量适配**：目录位置、触发方式、依赖预置
3. 不要为单一平台过度特化，保持核心可移植
4. 移植/升级后跑兼容验证：旧场景回归 + 新场景验证 + 边界压力

## 五、可移植性即复利

按标准写一次 → 跨 WorkBuddy/Codex/Claude Code/Cursor/龙虾/Hermes 等多平台免改运行，降低重复成本，形成跨平台复利效应。
