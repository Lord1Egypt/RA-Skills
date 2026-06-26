# 与 seo-geo-claude-skills 的集成方案

本项目的定位不是替代 `seo-geo-claude-skills`，而是补齐其中 **面向开发者工具与开源项目的 GEO 监控闭环**。前者提供通用 SEO/GEO 能力，后者提供垂直化监控、铺设、修复与案例化方法。两者结合时，可以形成“通用能力层 + 垂直工作流层”的协作结构。[1]

## 集成思路

建议把 `seo-geo-claude-skills` 视为底层能力库，把本仓库视为执行编排层。这样可以避免重复建设通用研究、内容优化与实体治理逻辑，同时把精力放在 Query Pool、模型分渠道策略和负向修复 SOP 上。

## 技能调用对照表

| 工作流阶段 | 本仓库技能 | 可配合的外部技能 | 使用时机 |
|---|---|---|---|
| 关键词研究 | `geo-keyword-matrix` | `keyword-research` `serp-analysis` `competitor-analysis` | 季度刷新 Query Pool 或新产品启动时 |
| GEO 监控 | `geo-monitor` | `rank-tracker` `memory-management` | 周度监控与复盘 |
| 发布前质检 | `geo-content-check` | `geo-content-optimizer` `content-quality-auditor` `entity-optimizer` `schema-markup-generator` | 每次内容发布前 |
| 负向修复 | `geo-fix-negative` | `geo-content-optimizer` `entity-optimizer` `content-refresher` | 每次出现负向或错误回答时 |

## 推荐安装方式

如果用户已经在使用现成的通用技能库，建议把本仓库作为垂直扩展层单独安装。这样不会破坏原有工作流，同时便于后续升级。

```bash
npx skills add veeicwgy/geo-monitor-toolkit
```

如果只需要其中一个能力，也可以按单技能安装：

```bash
npx skills add veeicwgy/geo-monitor-toolkit -s geo-monitor
```

## OpenClaw / ClawHub 路径

如果要走最快上线路径，建议先把根 `SKILL.md` 与四个子技能目录作为可安装包发布，再逐步补充更复杂的自动化脚本。这样能够先满足 **1-2 天内可安装、可试用** 的目标，然后再把周报自动化、Evidence Log 处理等更重的能力继续产品化。

## 最小可行集成范围

| 范围 | 是否建议首版纳入 | 说明 |
|---|---|---|
| 关键词矩阵 Skill | 是 | 直接提高新项目上手效率 |
| 周报框架 Skill | 是 | 能把监控体系标准化 |
| 发布前质检 Skill | 是 | 能减少无效铺设 |
| 负向修复 Skill | 是 | 能把异常处理从临时应对变成 SOP |
| 全自动抓取脚本 | 否 | 首版先交付方法与 Skill，后续再自动化 |

## 实施建议

首版发布时，优先确保以下三件事：文档足够清晰、技能结构可安装、案例足够完整。只要这三项成立，就已经具备仓库开源传播和社区试用的基础。

## References

[1]: https://github.com/aaron-he-zhu/seo-geo-claude-skills "aaron-he-zhu/seo-geo-claude-skills"
