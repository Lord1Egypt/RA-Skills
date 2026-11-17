# 能力词典（capability-dictionary）

**只做解释层**：为 `GET /api/features` 返回的 id 提供中文名、归组、用途深解与组合说明。词典不是功能清单，禁止单独当清单用——清单只来自运行时接口（capabilities 章）。

**技能已知最新版本：3.1.0**（2026-09-17 时点注记，勘误维护：FMR 新版实测后回写此行；capabilities 章 404 分支的版本比对以此为准）。

**特性与组合的分工**：特性行答"系统有什么、怎么开启"；组合行答"拿这些特性解决什么问题的成套走法"。组合不得是特性的复述——判据：删掉这条组合后，用户若不丢失任何"怎么做"的信息，就不该设这条组合。

## 事实优先级与回写

1. 运行时 `GET /api/features`（`name`/`summary`/`requires`/`lifecycle`）＞ 2. 本词典 ＞ 3. `research/` 时点快照。
冲突以接口为准，按接口呈现后提议勘误回写（须用户确认，由仓库维护层落账）。接口出现未收录 id：按接口文案呈现；**回写本词典须用户确认**，回写格式 = 表内加行 + 行尾注记（`<!-- 2026-XX-XX 回写，依据 /api/features 实测 -->`）。

## 定位叙述（L1，照此口径输出）

Free Model Router（FMR）是装在本机的**可自动扩展的免费 token 池工具**：渠道生态持续扩展，免费额度持续进池，单渠道失效不碍事——这是它与一般模型网关的区分点。它同时是一个本机模型网关：一个 OpenAI/Anthropic 兼容端点统一接入，主备自动故障转移，渠道与 key 集中管理。典型收益：给 agent harness 供模型；一机多个 harness 共用一个池子；免费额度最大化。

## 五组（L2 归组用）

基础接入 / 渠道与 key / 模型路由 / 进阶玩法 / 运维保障。

## A. 特性 id 表

| id | 中文名 | 归组 | 深解（用途与要点） | 操作入口 |
|---|---|---|---|---|
| unified-endpoint | 统一兼容端点 | 基础接入 | OpenAI 与 Anthropic 兼容端点，harness 改 baseURL 即接入 | access 章 |
| failover | 主备故障转移 | 基础接入 | 主模型/渠道失效自动切备用，任务不中断；主备顺序即热池顺序 | usage 章 |
| virtual-models | 虚拟模型名 | 基础接入 | 固定虚拟名自动映射到当前可用渠道；真名透传会 400 | access 章 |
| provider-management | 渠道与 key 管理 | 渠道与 key | 渠道启停、key 录入、坏模型禁用，全部本机集中管理 | usage 章 |
| multi-apikey | 多 key 轮询 | 渠道与 key | 单渠道录多把 key 轮换，额度成倍扩展；未启用时面板/REST 可开启 | usage 章 |
| health-check | 渠道健康检查 | 渠道与 key | 定期探活渠道与模型，坏渠道自动降权出热池 | usage 章 |
| groups | 自定义分组 | 模型路由 | 按能力评分把模型编组（如"高能力组"），虚拟名按组路由 | usage 章重操作 |
| router-mapping | 路由映射 | 模型路由 | 把使用场景映射到分组，各场景各走各的路 | usage 章重操作 |
| custom-providers | 自定义渠道 | 进阶玩法 | 把任意 OpenAI 兼容站点接进池子，与内置渠道同权参与路由 | usage 章重操作 |
| moa | MoA 聚合回答 | 进阶玩法 | 多模型分头作答再合议（MoA），带档位与长文自动升级阈值 | usage 章重操作 |
| timeout-profile | 超时档位 | 进阶玩法 | 按渠道健康度自适应调超时，慢渠道不拖死任务 | usage 章重操作 |
| credits | 兑换与积分 | 运维保障 | 扩额机制层：兑换码、积分、推荐奖励三类来源（只答"有什么"）；成套用法归组合 credit-max，不在此重复 | usage 章 |
| announcements | 官方公告 | 运维保障 | 渠道公告经 Router 下发，在面板与事件中提示 | usage 章事件 |

## B. 虚拟端点 id 表

| id | 中文名 | 说明 |
|---|---|---|
| model-router | 默认入口 | 纯文本对话，自动选主渠道；带图输入自动升 omni |
| model-router-omni | 全模态入口 | 文本+图像输入 |
| model-router-image | 图像生成入口 | 文本输入 → 图像输出 |
| model-router-moa | MoA 入口 | 多模型合议回答 |
| model-router-max | 高能力入口 | 走评分门槛最高的"高能力组"（3.1.0 实测门槛 ≥95） |
| model-router-pro | Pro 入口 | 与 max 同为分组型入口，具体分组以 `/api/groups` 实测为准 |

## C. 组合 id 表

| id | 名称 | requires | 解决什么问题 | 步骤入口 |
|---|---|---|---|---|
| free-first-paid-fallback | 免费为主、自有渠道兜底 | custom-providers, groups | 免费渠道集体失效时任务不中断，自有 key 只在兜底时消耗 | usage 章重操作 |
| moa-quality | MoA 提质 | moa | 质量敏感任务走 MoA 合议、速度敏感走单模型；档位按延迟/深度取舍，长文自动升档防截断 | usage 章重操作 |
| scenario-routing | 分场景路由 | groups, router-mapping | 代码/写作/图像各走各组，互不挤占 | usage 章重操作 |
| multi-key-scale | 多 key 扩量 | multi-apikey | 单 key 限速/额度瓶颈；在支持多 key 的渠道把 key 槽配满，轮询平滑单 key 限速 | usage 章 |
| slow-network-resilience | 弱网容错 | timeout-profile, health-check | 慢渠道卡死任务；坏渠道自动让位 | usage 章重操作 |
| multimodal-dispatch | 多模态分流 | virtual-models | 图像/视觉任务走对入口，不浪费文本额度 | access 章 |
| multi-harness-pool | 一机多 harness 共用池 | unified-endpoint | 多个 agent 工具共享同一 token 池 | access 章 |
| credit-max | 额度最大化 | credits | 成套走法（答"怎么做"）：推荐链接常驻分享、兑换码即到即兑、积分定期兑换，并经官方公告蹲新渠道与活动；与 multi-key-scale 分工——这条扩生态总量，那条扩单渠道容量 | usage 章 |

<!-- 条目来源：3.1.0 运行时观测（/api/moa-config、/api/groups、/api/timeout-profile、/v1/models 实测可达）+ spec.md 上游建议 combos 初稿。FMR 新版 /api/features 上线后以接口实测为准对齐，并按头部规则回写。 -->
