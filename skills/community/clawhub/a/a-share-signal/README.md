# A股信号 `a-share-signal`

[![ClawHub downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fa-share-signal&query=%24.skill.stats.downloads&label=ClawHub%20downloads&color=0A66C2)](https://clawhub.ai/byronwang2005/a-share-signal)

`a-share-signal`是一个用于分析A股结构状态的 Skill，聚焦结构化分析结论、关键证据与风险提示。本 Skill 中涉及的理论方法，主要用于研究交流与技术框架复盘。

> 相关内容仅用于研究交流与策略参考，不构成任何投资建议。

## 功能简介

- 基于筹码分布、三周期共振、优化KDJ、威科夫与缠论等框架分析A股
- 适合将近期行情数据快速整理为更清晰的结构分析参考

## 适用场景

- 判断当前结构是否具备持续观察价值
- 检查多周期结构是否共振
- 评估突破、放量、金叉等信号质量
- 识别筹码结构、主力洗盘 / 出货倾向与阶段状态
- 在结构成立前提下给出条件性目标价与风险前提

## 数据来源

默认优先使用用户明确提供或当前会话中已知可用的新版 `mx-skills`，以便获取个股行情、财务、公告、研报等数据。路由上优先以 `mx-financial-assistant` 作为单票综合分析入口，再按需补 `mx-finance-data`、`mx-finance-search`、`mx-stocks-screener` 与 `mx-macro-data`。所有 `mx-skills` 请求都要求严格串行执行，不论是不同 skills 之间的切换，还是对单个 skill 的多次补数，都必须等待上一请求完成后再继续，以降低限流、超时和口径漂移风险。`akshare`、`baoshare` 仍保留为额外回退，但仅在用户明确同意后启用；如缺少完成当前任务所需的 `mx-skills`，会先向用户说明缺口、展示将访问的来源 URL，并在获得明确同意后再引导其前往 [ClawHub](https://clawhub.ai/u/financial-ai-analyst) 或 [mx-skills 官网](https://ai.eastmoney.com/mxClaw) 安装或更新。

> [mx-skills官网](https://ai.eastmoney.com/mxClaw)

## 兼容性

本Skill兼容主流Agent生态，包括但不限于：

- OpenClaw (ClawHub: [byronwang2005/a-share-signal](https://clawhub.ai/byronwang2005/a-share-signal)，同步可能滞后)
- Claude Code
- Codex
- OpenCode
