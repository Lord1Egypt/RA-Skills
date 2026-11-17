# 排序、信誉与搜索技巧

## 综合分公式

```
composite = 0.5 * norm(score) + 0.3 * norm(popularity) + 0.2 * recency
  norm(score)      = min(score, 1)
  norm(popularity) = log10(1 + downloads) / 7      # 10^7 ≈ 1000 万下载 → 1.0
  recency          = clamp(1 - (now - updatedAt)/365d, 0, 1)

reputation        = 1.0 知名官方源 | 0.9 普通可信源 | 0.6 未知作者且 GitHub<100 星或安装<100
composite_final   = composite * reputation

# 叠加语义匹配（Phase 2）
final = 0.6 * composite_final + 0.4 * semantic_score
```

标记规则：

| 条件 | 标记 |
|---|---|
| `(now - updatedAt) > 365d` | `⚠️长期未维护` |
| 综合分最高 | `推荐` |
| 信誉 ≤ 未知阈值且非官方源 | `⚠️低信誉·谨慎` |
| 跨源存在 | `多源(N存在)` |
| 前置连接器未连 | `需先连接 X` |

## 来源信誉门槛

吸收自上游 `vercel-labs/skills` 的 Step 4 实践：
优先官方/知名源（`vercel-labs` / `anthropics` / `microsoft` / 腾讯文档等），
未知作者且 GitHub <100 星或安装 <100 的标「⚠️ 低信誉·谨慎」并降权。

## 信任层级（Trust Hierarchy）

| 层级 | 来源 | 审查强度 |
|---|---|---|
| 1 | 宿主官方 / 原生市场 | 低（仍需过目） |
| 2 | 知名源 + 高下载 | 中 |
| 3 | 已知作者 | 中 |
| 4 | 新 / 未知来源 | 最高 |
| 5 | 任何索取凭据的技能 | **一律人工批准** |

## 语义匹配

轻量离线意图词典 `INTENT_SYNONYMS`（20 类中英文同义词），把自然语言需求映射到技能意图。
零依赖、不依赖 embedding API。例：`search 股票` 只返回金融类技能。

> 定位说明：CLI 只提供**客观数据与校验器**，不假装做 NLP。
> 真正的语义理解交给运行此技能的 LLM 自身判断；词典匹配仅作召回辅助。

## 呈现格式（中文卡片）

```
为你找到几个相关技能（已按匹配度+热度+时效综合排序，跨源合并去重）：

| 技能 | 来源 | 综合 | 热度 | 最近更新 | 安全 | 质量 | 备注 |
|---|---|---|---|---|---|---|---|
| React Performance | 原生+ClawHub | 0.62 | 2.9K | 2026-.. | 已审 | 良(72) | 推荐 |
| 腾讯文档 | 原生市场 | 0.55 | 105 万 | 2026-.. | 已审 | — | |

要我装哪一个？（或"全装" / "看详情"）
```

- 中文用户用 `description_zh`，其他用 `description`。
- 附带 `homepage` 链接与"我帮你装"的明确邀约。
- **预览即确认**：安装前必须先把卡片给用户看，等其确认具体装哪些；HIGH/EXTREME 安全项须额外显式确认。

## 搜索技巧

1. 关键词具体：`react testing` 优于 `testing`
2. 中英都试：SkillHub 支持双语语义搜索
3. 换同义词：`deploy` 不行试 `deployment` / `ci-cd`
4. 关键词搜不到就按分类浏览：
   AI Intelligence, Developer Tools, Productivity, Data Analysis,
   Content Creation, Security & Compliance, Communication & Collaboration

## SkillHub 附加接口

```bash
curl -s "https://lightmake.site/api/v1/categories"
curl -s "https://lightmake.site/api/skills?category=developer-tools&sortBy=score&order=desc&page=1&pageSize=10"
curl -s "https://lightmake.site/api/skills/top"
curl -s "https://lightmake.site/api/v1/skills/<slug>"
```

## 找不到技能时

1. 说明在原生市场 + SkillHub + ClawHub 均未找到合适匹配（含离线情况）
2. 主动提出用通用能力直接帮做
3. 若该任务高频，建议自建：`npx skills init my-xyz-skill`
