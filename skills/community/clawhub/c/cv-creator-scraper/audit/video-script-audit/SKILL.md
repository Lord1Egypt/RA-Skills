---
name: video-script-audit
description: |
  CreatiVault 短视频拆解与脚本审核。适用于 TikTok 单条视频、Instagram Reels、YouTube Shorts
  及本地视频的分镜拆解、开场钩子、选题与痛点、内容结构、卖点植入、行动引导（CTA）、评分和优化建议。
  支持按品牌 Brief 检查符合度，在有匹配案例时提供对标结果，也可逐条审核多条视频并汇总为回填表。
  使用本地 video_audit_*.mjs 调用 CreatiVault OpenAPI；本地视频先用 media_upload.mjs 上传。
compatibility: Node.js 20.6+
metadata:
  layer: audit
  parent: creator-scraper-cv
---

# 短视频拆解与脚本审核

用 CreatiVault OpenAPI 提交任务、查询进度和获取结果。用户明确要求非 API 分析时，可按其要求处理。其他情况下以接口结果为准，失败时说明可核实的原因。

## 输入与提交

| 场景 | 输入 | 执行 |
|------|------|------|
| 拆解已发布视频 | 一条可访问的 TikTok 视频、Instagram Reels 或 YouTube Shorts 链接 | 用 `video_audit_submit.mjs` 传 `video_url` |
| 发布前自审 | 本地 MP4、MOV、AVI、MKV 或 WEBM 文件的绝对路径，单个文件最大 500 MB | 用 `media_upload.mjs` 传 `file_path`，再将返回的完整 `data.oss_url` 原样传给 `video_audit_submit.mjs` 的 `oss_url` |

上传会生成公开可访问的素材地址。审核时使用完整的 CreatiVault HTTPS 素材地址 `oss_url`。每次提交恰好选择 `video_url` 或 `oss_url` 中的一项。提交成功后保留 `data.task_id`。接口返回的 `estimated_time_seconds` 为参考值。

社媒链接由脚本和后端分别校验，接受以下格式：

| 平台 | 视频链接格式 |
|------|--------------|
| TikTok | `https://www.tiktok.com/@{用户名}/video/{数字ID}` |
| YouTube Shorts | `https://www.youtube.com/shorts/{视频ID}`，或 Shorts 的 `https://youtu.be/{视频ID}` |
| Instagram Reels | `https://www.instagram.com/reel/{短码}`，也接受 `/reels/{短码}` 和包含视频的 `/p/{短码}` |

收到 TikTok 分享短链时，请用户提供展开后的完整视频链接。收到 YouTube `/watch`、抖音或达人主页链接时，说明接受的链接格式并请用户提供对应短视频链接。

### 可选参数

| 参数 | 用法 |
|------|------|
| `brief` | 提交品牌 Brief 原文用于符合度检查 |
| `enable_benchmark` | 传 JSON 布尔值 `true` 启用案例对标。有匹配案例时返回对比结果 |
| `audit_mode` | `high`（默认）或 `low` |
| `campaign_id` | 已知活动 ID 时可一并传入 |

任务归属以 API Key 绑定身份为准。旧调用方传入的 `url` 和 `oss_url_override` 仍可分别映射到 `video_url` 和 `oss_url`。新调用统一使用当前字段。已有任务直接使用原 `task_id` 查询，避免重复提交。

以下命令从本子 Skill 目录运行。先替换示例中的素材路径、链接和任务编号。

```bash
# 已发布视频，可附 Brief 或启用对标
node ../../scripts/video_audit_submit.mjs '{"video_url":"https://www.tiktok.com/@creator/video/7648432916250250526","brief":"品牌要求自然演示产品使用场景","enable_benchmark":true}'

# 本地视频，第二步使用第一步返回的 data.oss_url
node ../../scripts/media_upload.mjs '{"file_path":"/path/to/draft.mp4"}'
node ../../scripts/video_audit_submit.mjs '{"oss_url":"https://oss.creativault.tech/media_ingestion/uploads/example/draft.mp4","brief":"发布前自审"}'
```

## 任务状态与错误处理

用 `video_audit_poll.mjs` 自动轮询，默认每 10 秒查询一次，最多 40 次，完成后自动获取结果。可用 `interval` 和 `max_attempts` 调整本次轮询，或传 `fetch_result: false` 仅等待终态。需要查一次状态时用 `video_audit_status.mjs`，查已完成任务的报告时用 `video_audit_result.mjs`。

```bash
node ../../scripts/video_audit_poll.mjs '{"task_id":"550e8400-e29b-41d4-a716-446655440000"}'
node ../../scripts/video_audit_status.mjs '{"task_id":"550e8400-e29b-41d4-a716-446655440000"}'
node ../../scripts/video_audit_result.mjs '{"task_id":"550e8400-e29b-41d4-a716-446655440000"}'
```

| 返回 | 处理 |
|------|------|
| `data.status` 为 `pending`、`queued` 或 `processing` | 保留任务编号并继续查询。以 `status` 判断任务状态，`progress` 只用于展示 |
| `data.status` 为 `completed` | 取回结果并核对 `data.audit_result` |
| `data.status` 为 `failed` 或 `failure_stage: audit_task` | 原文反馈 `data.error_message` 或脚本提取的 `error`，结合实际原因说明如何处理 |
| `data.status` 为 `skipped` | 报告任务被跳过。轮询脚本只识别 `completed` 和 `failed`，如有轮询超时，单次查状态确认 |
| `failure_stage: local_validation` 或请求失败 | 从 stdout 或 stderr 获取 `error`、`reason` 和具体错误码。无效链接或参数修正后再提交 |
| `failure_stage: poll_timeout` | 说明本次等待结束，保留任务编号并用状态脚本确认进度。超时本身无法确定任务结果 |

外层 `success` 只代表接口调用成功。即使状态查询返回 `success: true`，也要按实际任务状态处理。端点特有的错误说明见[错误码](../../references/error-codes.md#video-script-audit-errors)。`40002` 表示结果尚不可取，先查询状态。`40003` 表示已完成任务没有可读取的结果。向用户说明后再决定是否重新提交。计费用量按接口实际返回展示。只有 `40201` 表示 CreatiVault 积分不足，`quota_remaining` 表示剩余请求次数。

## 可用结果

结果载荷位于 `data`。分析主体在 `data.audit_result`。只展示实际返回的字段，空分数留空，保留接口实际返回的 0 分。对于本地上传的视频，账号背景和社媒表现指标为 `not_applicable`，可直接展示素材内容分析。

| 结果 | 数据来源 |
|------|----------|
| 分镜、时间轴、内容结构、选题 | `audit_result.storyboard`，包括 `shots`、`timeline`、`script_structure` 和 `content_theme` |
| 开场钩子、用户痛点、情绪、卖点呈现 | `audit_result.viral_factors` 下的 `hook_analysis`、`pain_point_targeting`、`emotional_value` 和 `selling_point_integration` |
| 行动引导（CTA） | `audit_result.viral_factors.conversion_completeness` 中的 `has_clear_cta`、`cta_position` 和 `cta_strength`，作为内容分析展示 |
| 综合评分、诊断、优化建议 | `audit_result.scores`、`diagnosis_level` 和 `suggestions`。可用分项包括钩子、节奏、卖点、创意和制作，范围为 0–10 |
| 品牌 Brief 符合度、案例对标 | `audit_result.content_audit.brief_compliance` 和 `audit_result.benchmark_comparison`，有返回值时展示 |
| 视频表现、达人背景 | `audit_result.video_metrics` 和 `audit_result.creator_metadata`，社媒数据可用时展示 |
| 标签、内容类型、结构化作品分析 | `data.hashtags`、`data.content_type_label`、`data.content_type_reason`、`data.structured_analysis`。达人类型按 `audit_result.creator_metadata.creator_type` 展示 |
| HTML 报告链接 | `data.html_report_url`，有返回值时提供 |

`video_metrics.comments_cnt` 是视频评论数。输出时保留这一指标的含义。文案可结合实际返回的口播和字幕分镜说明。若 `confidence.requires_human_review` 为 `true`，在报告中提示需要人工复核。

## 多条视频与回填表

多条视频分别提交，每条保留自己的输入和任务编号。按实际配额分批提交或并发查询，某条失败或暂未完成时仍可交付已完成结果。按视频列出失败原因或仍待查询的任务编号。

批量结果或用户要求回填表时，输出可复制到飞书的 Markdown 表格。可以包含平台、达人 ID、主页、达人类型、视频链接、内容类型、作品分析、结构拆解、核心标签和 HTML 报告链接。达人 ID、主页以及报告链接使用已知来源或实际返回值，缺失时留空。作品分析可用 `structured_analysis` 的场景与痛点、拍摄亮点和 CTA 亮点。结构拆解可汇总开场、主体、行动引导和分镜。

## 与其他子 Skill 衔接

- 需要找适合拆解的素材时，用[视频检索](../../discovery/video-search/SKILL.md)选择已收录视频。
- 拆解后需要查看发布达人的资料时，用[达人搜索](../../discovery/creator-search/SKILL.md)按实际平台和账号标识查找。
- 需要联系达人时，使用[邮件建联](../../outreach/creator-outreach/SKILL.md)确认收件名单和内容后发送。

接口字段和错误处理可参考 [API Reference](../../references/api-reference.md)。
