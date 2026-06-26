---
name: claws-daily
description: "小龙虾日报，将你最关心的资讯主动送到你眼前。"
version: "1.0.1"
---

# When to Use
Use this skill when the user asks to:
- 生成每天两次（09:00 / 18:00，Asia/Shanghai）的资讯简报
- 基于公开热榜 + `GET /api/v2/news/search` 输出双分区 Brief
- 通过 `news_label` 做关注内容检索并生成结构化摘要

# Reference
| File | Purpose |
|------|---------|
| `{baseDir}/daily_example.md` | 输出格式与示例（Markdown Brief） |
| `{baseDir}/install.md` | 安装、初始化、环境变量与 Heartbeat 配置 |
| `{baseDir}/metadata.json` | 技能元数据与环境变量参数 定义（如 `SHENME_DOMAIN`、`PROFILE`、`INTEREST_LABELS`、`LANGUAGE`） |

## APIs

- `https://${SHENME_DOMAIN}`

### News Search
- Method: `GET`
- Path: `/api/v2/news/search`
- Full URL: `https://${SHENME_DOMAIN}/api/v2/news/search`

### Expected Input
| Field | Type | Required | Description |
|------|------|----------|-------------|
| `label` | string | Conditional | closed-domain 参数；可选值仅限：`财经`、`科技`、`教育`、`社会`、`娱乐`、`港澳台`、`国际关系`。 |
| `query` | string | Conditional | open-domain 参数；可传任意字符串，后端通过语义检索返回结果。 |

规则：`label` 和 `query` 二选一，至少填写一个；两者同时传入时，后端优先按 `query` 语义检索。


# Workflow

1. 读取 `{baseDir}/metadata.json`，检查必要参数是否缺失或无效：`SHENME_DOMAIN`、`SHENME_FETCH_LIMIT`、`PROFILE`、`INTEREST_LABELS`、`LANGUAGE`。
   - 若存在缺失或无效，必须先按 `{baseDir}/install.md` 执行初始化流程。
   - 初始化未完成时，不进入简报生成流程。
2. 判定当前批次（固定 `Asia/Shanghai`）：
   - 09:00 批次：时间窗 `[前一天 18:00, 当天 09:00)`。
   - 18:00 批次：时间窗 `[当天 09:00, 当天 18:00)`。
3. 从公开热榜抓取候选热点，生成 `📌 重大事件`（建议 2-3 条）；每个事件仅保留“事件发展趋势关键点”，最多 3 条。
4. 从可选标签中选择 1-3 个 `news_label`，按标签分别调用 `news/search`（`label=${NEWS_LABEL}`，`limit=${SHENME_FETCH_LIMIT}`）拉取候选资讯。
5. 过滤候选：仅保留 `publish_time` 落在当前批次时间窗内的资讯。
6. 合并去重：按 `news_id` 去重；同一 `news_id` 多次出现时保留 `ingest_time` 更新的一条。
7. 兴趣度筛选：基于 `${PROFILE}` 识别用户关心内容，并结合“相关性、信息增量、事件影响度”排序；先按兴趣度降序，再按 `publish_time` 倒序。
8. 确认输出语言：按 `${LANGUAGE}` 生成日报（`zh-CN` 输出中文，`en-US` 输出英文）。
9. 生成 Brief，严格遵循 `{baseDir}/daily_example.md`：
   - 固定 section 顺序：标题 -> `📌 重大事件` -> `📌 为你关注`。
   - `📌 为你关注` 初次输出最多 5 条。

# Rules
## Parameter Rules
- `news_label` 可选值仅限：`财经`、`科技`、`教育`、`社会`、`娱乐`、`港澳台`、`国际关系`。
- 允许多标签检索；多标签场景必须先分别检索，再合并去重。
- `SHENME_FETCH_LIMIT` 建议大于等于 `5`。
- 当 `SHENME_FETCH_LIMIT < 5` 时，按实际可取数量输出并提示候选不足。
- `PROFILE` 用于定义用户偏好，兴趣筛选必须基于 `${PROFILE}` 执行。
- `LANGUAGE` 用于控制日报输出语言，建议值：`zh-CN` 或 `en-US`。
- `label` 和 `query` 二选一，至少填写一个。
- `label` 为 closed-domain，仅允许预定义标签值。
- `query` 为 open-domain，可传任意字符串，后端通过语义检索返回结果；若与 `label` 同时传入，优先按 `query` 检索。

## Format Rules
- 固定顺序：标题 -> `📌 重大事件` -> `📌 为你关注`。
- `📌 重大事件`：输出 2-3 条事件，每条必须为“编号 + 事件标题 + 1-3 条趋势关键点”。
- `📌 为你关注`：先输出“已选标签”行，再输出编号资讯；每条资讯为“标题 + 1-2 句摘要”。
- `📌 为你关注` 初次输出最多 5 条，禁止超过 5 条。
- 最终日报语言必须与 `LANGUAGE` 一致（`zh-CN` 中文，`en-US` 英文）。
- 禁止新增未定义 section（如“总结”“延伸阅读”“参考链接”）。
- 禁止把模板字段名原样输出（如 `${title}`）；必须替换为真实内容。

## Failure Fallback Rules
- 接口调用失败（网络或限流）：每次请求最多重试 3 次。
- 热榜抓取失败：`📌 重大事件` 输出“重大事件暂缺（热榜抓取失败）”，其余部分继续执行。
- 热榜信息不足：允许减少事件条目，但已输出事件仍需保证趋势关键点不超过 3 条，并标记“信息不完整”。
- 窗口内无命中资讯：`📌 为你关注` 输出“该时段无命中资讯”，不编造内容。
- 选定标签均无命中：允许更换为其他可选标签重试一次。
- 字段缺失（无 `news_id`、`title` 或 `publish_time`）：剔除该条。

## Forbidden Output
- 编造不存在的新闻或字段。
- 输出未经验证的“已推送成功”结论。
- 将“重大事件”误写为来自内部 API 或无来源信息。
