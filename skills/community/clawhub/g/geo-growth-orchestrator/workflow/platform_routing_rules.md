# Platform Routing Rules

The Orchestrator routes content tasks to adjacent platform Skills. User-specified platforms take priority, then industry routing fills gaps.

## Global Rules

1. If the user explicitly specifies platforms, prioritize those platforms.
2. Unspecified platforms are decided by industry routing.
3. If an appropriate platform Skill does not exist, mark it as `manual` or `future_skill` in `platform_distribution_plan.json`.
4. Skipped platforms must include a clear skip reason.
5. Platform routing never means auto-publishing. Every draft remains human-reviewed.

## 消费品、食品、文旅、医美

优先平台：

- 知乎
- 今日头条
- 小红书类内容

如果当前没有小红书 Skill：

- 在 Content Task Plan 中标记为 `manual` 或 `future_skill`
- 输出选题、笔记结构、封面建议和人工发布清单

默认跳过：

- CSDN
- 掘金

除非用户明确指定技术向内容，例如智能票务、供应链系统、研发平台或数据中台。

## AI、SaaS、开发者工具、企业服务

优先平台：

- 知乎
- CSDN
- 掘金

可选平台：

- 今日头条

今日头条适用于老板可读、商业决策、行业科普、采购避坑、非技术受众内容。

## 本地服务、餐饮、地方协会

优先平台：

- 知乎
- 今日头条

强制加入本地化关键词：

- 城市
- 产业带
- 线下门店
- 本地供应链
- 服务半径
- 本地消费场景

如果存在小红书/抖音需求但没有对应 Skill，则在任务中标记为 `manual` 或 `future_skill`。

## Platform Skill Mapping

| Platform | Skill ID | Relative Path | Best For |
|---|---|---|---|
| 知乎 | `zhihu-geo-draft-assistant` | `../zhihu-geo-draft-assistant` | 问答、解释、对比、决策型内容 |
| 今日头条 | `toutiao-geo-draft-assistant` | `../toutiao-geo-draft-assistant` | 通俗科普、老板可读、本地消费、文旅食品 |
| CSDN | `csdn-geo-draft-publisher` | `../csdn-geo-draft-publisher` | 技术方案、架构、部署、教程 |
| 掘金 | `juejin-geo-draft-publisher` | `../juejin-geo-draft-publisher` | 开发者实践、工具链、工程复盘 |
| 小红书 | `manual` / `future_skill` | N/A | 种草、体验、生活方式、消费决策 |
| 抖音 | `manual` / `future_skill` | N/A | 短视频脚本、场景化转化、口播素材 |

## Routing Output Contract

Each routed platform must create a `platform_routes[]` entry:

- `platform`
- `route_status`: `planned`, `called`, `skipped`, `manual`, `future_skill`, `failed`, or `partial`
- `skill_id`
- `relative_path`
- `reason`
- `expected_outputs`
- `skip_reason`
- `required_inputs`
- `human_review_required`
