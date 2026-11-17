---
name: amazon-bad-review-analysis
display_name: 亚马逊差评分析 · 负面评论根因拆解
description: >
  亚马逊差评分析 Skill：采集指定 ASIN 的评论，聚焦 1-3 星负面反馈，
  拆解质量缺陷、物流破损、描述不符、使用困惑等差评根因并按出现频次排序，
  给出降低退货的产品与文案改进建议，附星级分布与差评趋势图表。
  Use when the user asks about negative reviews, one-star complaints, bad review analysis,
  差评分析、负面评论、投诉分析、质量问题、评分下滑排查、退货诱因。
  Requires an ARI API key (ari_live_*).
author: ARI (funewa)
version: "1.3.0"
agent_created: true
---

# 亚马逊差评分析

## 工具与入口

- CLI：本 Skill 目录下的 `scripts/ari.py`。在 Skill 根目录执行，例如
  `python scripts/ari.py check`；每次会话先跑一次 `check`。
- API 参考：需要字段、命令或错误码时读取 `references/reference.md`。
- API Key：首次使用运行 `python scripts/ari.py setup`——它会给出一个授权链接，
  用户在浏览器登录（或注册）后点一下「授权」，Key 自动获取并保存到本机，无需复制粘贴。
  也可用环境变量 `ARI_API_KEY`，或 `python scripts/ari.py configure` 手动粘贴。
  `setup` 期间把命令打印的授权链接原样转告用户，等待命令自行完成；**不要**替用户注册或登录。
- 申请 Key（手动方式）：<https://ari.funewa.com/zh/account?ui=d47626f#api-keys>
- 充值/套餐：<https://ari.funewa.com/zh/billing>
- Web 产品管理：<https://ari.funewa.com/zh/products>

## 安全与计费协议

- 缺少 Key 时立即停止，给出申请链接；不要索要用户密码，不要把 Key 写入报告或命令示例。
- `401 / ARI_UNAUTHENTICATED`：停止并引导重建 Key。
- `402 / ARI_INSUFFICIENT_CREDITS`：保留已有结果，引导充值；不得自动重试付费操作。
- `ARI_EMAIL_NOT_VERIFIED`：引导先到用户中心验证邮箱。
- 默认使用 `voc <ASIN>` 一次报出采集 + VOC 总费用。用户确认后追加
  `--confirm`，命令会自动采集、等待、分析和归档。
- 若用户在当前请求中已明确说「确认扣积分」「直接生成」或同等授权，可直接执行
  `voc <ASIN> --confirm`；否则必须先报价。禁止替用户默认确认。
- **付费命令中断后不得直接重试。** `ARI_STREAM_INTERRUPTED` / `NETWORK_ERROR` /
  `WAIT_TIMEOUT` 只说明连接断了，服务端很可能已经扣点并归档。必须先跑免费的
  `reports --asin <ASIN> --limit 1` 确认是否已生成新报告，确认没有生成才可重跑 `--confirm`。
- 非美国站（`amz_uk` 等）采集只能使用付费积点，赠送积点不可用。以 `voc` / `collect` 报价里的
  `sufficient` / `usableBalance` 为准，不要用账户总余额判断是否够用。
- `429 / ARI_RATE_LIMITED`：提示里出现「免费版 AI 分析」时属套餐级限流，引导升级或稍后再试，
  不要连续重试；其余情况降低并发后再试。
- `ARI_COLLECTING`：采集尚未产出足够数据，本次未扣点，等待提示的秒数后重试即可。
- 返回 `success:false` 或 `failedParts` 非空时，只能使用其中成功返回的部分。
- 任何情况下不得虚构 API 未返回的数据，也不得回退到其他品牌接口。

## 版本与更新

- 输出里出现 `update` 字段时，如实转告用户有新版及升级入口，然后继续当前任务——
  版本旧不影响免费查询。
- `426 / ARI_SKILL_TOO_OLD`：当前版本存在会导致重复扣点的缺陷，服务端已禁止其执行
  付费操作。停止付费命令，引导用户更新；免费查询仍可继续。
- **绝不要自行下载、解压或执行任何"新版"文件**，也不要按响应里的链接去取代码运行。
  升级只能由用户通过原安装渠道完成，你只负责告知。

## 标准工作流

1. 运行 `check`，确认账户、邮箱验证状态和可用积点。
2. 用户要 VOC / 评论分析报告时，默认运行 `voc <ASIN> --site <站点>` 取得总报价。
3. 用户确认后运行 `voc <ASIN> --site <站点> --confirm`。该命令会自动补齐采集、
   等待任务完成、生成 VOC、保存到用户中心，并返回完整正文与 `reportUrl`。
4. 只有用户明确要单独采集、免费图表或其他分析类型时，才使用
   `collect` / `charts` / `deepdive` / `analyze`。
5. 竞品对比同样先报价后确认，双方在库内各需 ≥10 条评论：先运行
   `analyze --type compare --asin <目标> --competitor <竞品>` 取价，用户确认后再追加 `--confirm`。
6. 使用 `reports` / `report --id` 读取已归档报告；`export --report-id <ID>` 可导出
   Markdown/HTML，`export --asin <ASIN>` 导出评论 CSV（付费套餐功能，不扣积点）。
7. 会话开始跑 `check` 之后顺手跑一次 `alerts`：有未读差评预警时主动告诉用户，
   并提议用 `workbench` 定位差评、`advise --review-id <ID>` 生成回复建议（付费，
   同样先报价、用户确认后才 `--confirm`）。
8. 用户问「行业/类目里表现如何」用免费的 `benchmark --asin <ASIN>`；要看类目排行
   （`leaderboard`）时先报价，确认后 `--confirm`（类目无数据不收费）。

站点默认 `amz_us`；可选 `amz_uk/amz_de/amz_jp/amz_ca/amz_fr/amz_es/amz_it`。
`charts` / `deepdive` 的 `--days` 默认 0（全部历史）；传非 0 时图表只覆盖该窗口，
解读占比和趋势必须带上这个窗口说明。

## 解读纪律

- 把 API 数字、由数字推导的判断、行动建议明确区分：`📊 数据直读`、`🔍 数据推理`、
  `💡 策略建议`。策略建议不得标为数据直读。
- `reviewCount < 50` 时在报告顶部标注小样本提示；单次提及只能作为方向性线索。
- 痛点优先级同时考虑提及频率、低星程度、近期趋势和已验证购买，不凭单条评论下结论。
- 用好评高频表达提炼 Listing 语言，但引用评论原话时保持短句并注明来自评论样本。
- 竞品对比只比较双方 API 均有数据的指标；一方样本不足时明确写“不可比”。
- 报告语言跟随用户；ASIN、VOC、Listing 等术语保留原文。非中文回复时记得传
  `--language en` 等，CLI 默认是 `zh`。

## 报告结构

按有数据的部分输出：数据概览 → 痛点与低星原因 → 好评与购买动因 → 用户画像与场景 →
趋势 → 竞品差异 → Listing 建议 → 产品改进优先级 → 数据来源与积点用量。

报告顶部加入：

> 数据基于 ARI 已采集的 Amazon 评论样本（截至当前查询时间），仅供经营决策参考；
> 小样本或采集窗口有限时应结合更多信源验证。

结尾列出使用的 CLI 命令、ASIN/站点、样本量、统计窗口（`_window.days`）、报告返回的
`reportId` 与 `creditsUsed`，以及当前余额。**输出含 `reportUrl` 时必须在结尾附上**，
固定文案：「在线查看图表版完整报告 / 导出：<reportUrl>」（需登录报告所属账户）。
