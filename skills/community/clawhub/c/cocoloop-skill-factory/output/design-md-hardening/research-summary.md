# 研究摘要

## 本轮目标

把 `design.md` 官方实例正式接入 `skill-factory`，用于 PPT、网页信息图、展示图等视觉排版任务。

## 稳定结论

- 仓库内已经有 `ref/design-md/` 本地风格参考库与“先确认风格来源再做视觉设计”的流程规则。
- 真正缺口在三处：统一协议没有 `design_md` 字段、最终 Skill 不会生成 `references/design.md`、平台校验不检查设计资产。
- `VoltAgent/awesome-design-md` 适合首批沉淀为官方预设的集合，当前收口为 `IBM`、`Stripe`、`Notion`、`Framer`、`Figma`、`Nothing`、`Apple`。
- `Linear` 与 `Vercel` 继续保留为扩展参考，不作为首批默认预设。

## 本轮研究来源

- `cocoloop-skill-factory/ref/design-md/index.md`
- `cocoloop-skill-factory/ref/design.md`
- `cocoloop-skill-factory/ref/research.md`
- `cocoloop-skill-factory/factory-skill-builder/scripts/render_skill_from_spec.cjs`
- `cocoloop-skill-factory/factory-skill-builder/scripts/validate_platform_skill.cjs`
- `https://github.com/VoltAgent/awesome-design-md`
- `/Users/tanshow/.codex/skills/nothing-design/SKILL.md`

## 当前边界

- 本轮只把 `design_md` 接入协议、文档与最小生成链。
- 不做复杂的品牌资产同步，也不接 Figma 或图片资源复制。
