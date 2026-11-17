# ARI CLI 与 API 参考

仅在需要命令参数、响应字段或错误处理时读取本文件。

API 默认地址：`https://ari.funewa.com`（开发环境可用 `ARI_BASE_URL` 覆盖）。
认证头：`Authorization: Bearer ari_live_...`。统一 JSON 信封为
`{success, code, message, data, error, meta}`；SSE 分析由 CLI 聚合为同类 JSON。

`--compact` 输出单行 JSON，放在子命令前后都可以
（`ari.py --compact check` 与 `ari.py check --compact` 等价）。

## 版本与更新

CLI 在 User-Agent 里带自身版本（`ARI-Review-Skill/<version>`，与 `_meta.json` 一致）。
服务端在每个 API Key 响应上回 `X-ARI-Skill-Latest` / `X-ARI-Skill-Update-Url`；
本地版本更旧时，**任意命令**的输出都会多出一个顶层 `update` 字段：

```json
{"update": {"current": "1.0.4", "latest": "1.0.6", "url": "...", "message": "..."}}
```

`check` 还会额外读取免认证的 `/api/v1/public/config`，把完整的
`release: {latest, minSupported, url, notes}` 一并返回——Key 失效时也能拿到升级入口。

升级一律由用户通过原安装渠道完成。**CLI 不会下载或执行任何远端代码**，
也不要让 agent 代劳去取"新版文件"运行。

## 用户入口

- API Key：<https://ari.funewa.com/zh/account?ui=d47626f#api-keys>
- 充值/套餐：<https://ari.funewa.com/zh/billing>
- 产品管理：<https://ari.funewa.com/zh/products>
- 报告中心：<https://ari.funewa.com/zh/reports>

## CLI 命令

| 命令 | API | 是否可能扣点 |
|---|---|---|
| `setup` | auth/device/start + poll（免认证），浏览器授权后自动保存 Key | 否 |
| `configure` | 本地保存 Key | 否 |
| `check` | user/me + credits/balance | 否 |
| `products` | asins | 否 |
| `collect` | billing/pricing + credits/balance + collection/submit | 是；必须 `--confirm` |
| `status` | collection/status/{taskId} | 否 |
| `reviews` | reviews | 否 |
| `charts` | charts/stars·trend·keywords·flow | 否 |
| `quote` | analysis/quote | 否 |
| `analyze` | analysis/voc·insight·trend·variant·compare | 是；必须 `--confirm` |
| `deepdive` | products + charts + reviews + reports + VOC quote/analysis | 默认否；`--confirm` 才分析 |
| `reports` / `report` | reports | 否 |

运行 `python ari.py <命令> --help` 查看完整参数。

## 采集

`collect --asin B0... --site amz_us --pages 3` 只返回报价；确认后追加
`--confirm --wait`。请求字段：`asin, site, pageCount, filterByStar, sortBy, alias`。

- `pages`: 1–10，每页约 10 条。
- `filterByStar`: `all_stars|critical|positive|one_star|two_star|three_star|four_star|five_star`。
- `sortBy`: `recent|helpful`。
- **US 以外站点只能使用付费（addon）积点**，赠送的 plan 积点被排除。报价字段
  `usableBalance` 已按站点算好，`sufficient=false` 时不要确认——服务端会直接 402。
  报价还返回 `planCredits` / `addonCredits` / `siteNote` 供解释。
- `--wait` 轮询 `collection/status`，任务状态只有 `queued|running|done|failed`。
  瞬时错误会自动重试 3 次；仍失败或超时返回 `WAIT_TIMEOUT`，此时任务仍在后台，
  用 `status --task <taskId>` 查询，**不要重新提交采集**。

## 分析

先调用 `quote --type ...`。报价字段：
`type, basePrice, price, sampledReviews, totalReviews, balance, sufficient`。

- `voc`: Markdown VOC 报告，SSE 聚合后在 `data.content`，并归档。
- `insight`: 结构化消费者洞察，`data.result`，同时可能含流式说明 `content`。
- `trend`: 情感趋势解读，普通 JSON。
- `variant`: 颜色/尺寸等变体归因，普通 JSON；需足量变体评论。
- `compare`: 目标与竞品对比，**双方在库内各需 ≥10 条评论**（订阅关系不作强制校验，
  但 charts/reviews 等 0 积点端点仍要求订阅）。必须传 `--competitor`。

SSE 聚合结果字段：`meta, content, result, reportId, creditsUsed`。
只有 `insight` 会发 `result` 事件；`voc` / `compare` 的 `reportId` 由 CLI 在分析完成后
回查报告列表补上，此时带 `reportIdSource: "reports-lookup"`。

Free 套餐的 AI 分析被强制降级到轻量模型，且受全局限流保护——报告深度与付费档不同，
必要时说明这一点。

## 免费数据字段

- `products`: `asins[], count, limit`；元素含 `asin, site, alias, collectionStatus,
  lastCollectedAt, reviewCount, variantCount`。**只包含主品**，作为竞品添加的 ASIN
  不在其中（但它们的 charts/reviews 依然可读）。
- `reviews`: `reviews[], total, page, pageSize`；每条含标题、正文、星级、日期、
  verifiedPurchase、helpfulCount、attributes。
- `charts stars`: `stars[1★..5★], total, avgStar`。
- `charts trend`: 按月评论数、平均星级、低星数。
- `charts keywords`: `keywords[]`。
- `charts flow`: 场景/问题等流向结构；为空时不要补造。
- `charts` / `deepdive` 额外返回 `_window: {days, note}`，`days=0` 表示全部历史；
  非 0 时所有图表只统计最近 N 天，解读必须带上该窗口。

## 聚合命令的失败语义

`charts` 和 `deepdive` 会并发调多个端点。任一子请求失败时，最外层就是
`success:false`，并给出 `failedParts:[{part, code, message}]`（如 `charts.trend`、
`analysis`），成功的部分仍保留在 `data` 里。只能使用成功的那部分，缺失的数据不得推断。

`deepdive` 找不到主品订阅时不会直接报错：仍返回 charts/reviews/reports，
并在 `productNote` 里说明；此时即使传了 `--confirm`，AI 分析也会降级为只报价、不扣点。

## 错误处理

| 状态/错误码 | 动作 |
|---|---|
| 401 / `ARI_UNAUTHENTICATED` | Key 无效或已撤销；去用户中心重建 |
| 402 / `ARI_INSUFFICIENT_CREDITS` | 停止付费操作；展示已有结果并引导充值 |
| 403 / `ARI_EMAIL_NOT_VERIFIED` | 去用户中心验证邮箱 |
| 403 / `ARI_FORBIDDEN`（含配额字样） | 已达套餐可订阅 ASIN 上限；引导删除旧 ASIN 或升级套餐 |
| 403 / `ARI_FORBIDDEN`（其他） | 该 ASIN 不在当前账户订阅内；或 API Key 无账户/支付/后台权限 |
| 422 / `ARI_INSUFFICIENT_REVIEWS` | 先增加采集页数；不把小样本包装成确定结论 |
| 202 / `ARI_COLLECTING` | 采集中且数据不足，**未扣点**；按提示秒数等待后重试 |
| 429 / `ARI_RATE_LIMITED`（含「免费版 AI 分析」） | 套餐级限流；引导升级或稍后再试，不要连续重试 |
| 429 / `ARI_RATE_LIMITED`（其他） | 降低并发后再试；不要并发轰炸 |
| `ARI_STREAM_INTERRUPTED` | 分析流中断，**服务端可能已扣点并归档**；先 `reports --asin <ASIN> --limit 1` 核对，没生成才可重试 |
| `NETWORK_ERROR` / `WAIT_TIMEOUT` | 同上：付费命令一律先核对再决定是否重跑 |
| `ARI_PARTIAL_FAILURE` | 聚合命令部分失败；见 `failedParts`，只用成功的部分 |
| 426 / `ARI_SKILL_TOO_OLD` | 当前版本低于服务端最低支持版本，付费操作被禁止；引导用户更新，免费查询不受影响 |

CLI 网络错误和 HTTP 错误均返回结构化 JSON，不应从报错文本臆测业务数据。
