# Podcast and YouTube Support Design

## 背景

`follow-news` 当前通过多个 Python fetcher 收集 RSS、Twitter/X、Web、GitHub、GitHub Trending 和 Reddit 数据，再由 `scripts/merge-sources.py` 统一打分、去重、按 topic 聚合。这个架构的边界比较清晰：fetcher 只产结构化数据，最终摘要由 digest prompt 和 agent 生成。

这次要增加 podcast 支持，并参考 `follow-builders` 中的两个设计信号：

- `prompts/summarize-podcast.md`：基于 transcript 生成独立成文的 podcast 摘要，强调 takeaway、speaker context、具体洞察和短引用。
- `feed-podcasts.json`：已抓取后的 episode artifact，字段包括 `source`、`name`、`title`、`guid`、`url`、`publishedAt` 和完整 `transcript`；当前样例是 YouTube episode。

因此首版不能只把 podcast 当作普通 RSS。它需要支持 YouTube metadata 和 transcript 获取，同时保持 pipeline 的可降级能力。

## 目标

- 新增 `podcast` source type，支持普通 podcast RSS 和 YouTube playlist/channel/video URL。
- 新增 podcast fetcher，统一输出 episode metadata，并在可用时附带 transcript。
- 支持 YouTube metadata 和 transcript 获取，但 transcript 获取失败不能导致整个 pipeline 失败。
- 将 podcast episode 合入现有 merge、scoring、dedup 和 topic grouping 流程。
- 在 digest prompt 中新增 podcast remix 输出规则，复用 transcript 生成高质量摘要。
- 保持 Python 3.8+ 和当前“可选依赖增强、缺失时降级”的项目风格。

## 非目标

- 首版不做音频下载。
- 首版不做音频转写或 speech-to-text。
- 首版不在 fetcher 内调用 LLM。
- 首版不要求 CI 或用户环境必须安装 YouTube transcript 工具。
- 首版不改变现有 RSS、Twitter/X、Web、GitHub 或 Reddit 的行为。

## 推荐方案

采用 Hybrid 方案：把 podcast 作为独立 source type，同时把 transcript 作为增强字段，而不是 fetch 成功的硬前置条件。

数据路径：

```text
config/defaults/sources.json or workspace overlay
  -> scripts/fetch-podcast.py
  -> podcast.json
  -> scripts/merge-sources.py
  -> quality scoring, deduplication, topic grouping
  -> digest prompt Podcast Remix section
```

`fetch-podcast.py` 只负责抓取和规范化数据。它不负责总结 transcript。摘要仍由 digest prompt 使用合并后的 JSON 数据生成，这符合现有架构中“pipeline 产数据，agent 写报告”的职责边界。

## 配置模型

新增 source type：

```json
{
  "id": "training-data-podcast",
  "type": "podcast",
  "name": "Training Data",
  "enabled": true,
  "priority": true,
  "url": "https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8",
  "platform": "youtube",
  "topics": ["llm", "ai-agent"],
  "transcript": {
    "enabled": true,
    "backend": "auto",
    "languages": ["en", "zh", "zh-Hans"]
  }
}
```

普通 podcast RSS 也走同一个 source type：

```json
{
  "id": "dwarkesh-podcast",
  "type": "podcast",
  "name": "Dwarkesh Podcast",
  "enabled": true,
  "priority": true,
  "url": "https://example.com/feed.xml",
  "platform": "rss",
  "topics": ["llm", "frontier-tech"],
  "transcript": {
    "enabled": false
  }
}
```

字段语义：

- `url`：source 入口。YouTube 可为 playlist、channel 或单个 video；RSS 为 feed URL。
- `platform`：`youtube`、`rss` 或 `auto`。缺省可按 URL 推断。
- `transcript.enabled`：是否尝试抓 transcript。
- `transcript.backend`：首版支持 `auto` 和 `yt-dlp`。后续可扩展其他 backend。
- `transcript.languages`：字幕语言优先级。缺省为 `["en", "zh", "zh-Hans"]`。

## Episode 输出结构

`podcast.json` 使用与其他 fetcher 类似的 `sources` 包装结构。每个 episode 规范化为 article-compatible shape：

```json
{
  "title": "Waymo's Dmitri Dolgov: 20 Million Rides and the Road to Full Autonomy",
  "link": "https://www.youtube.com/watch?v=...",
  "date": "2026-05-04T20:05:00+00:00",
  "guid": "a6ff5c8c-47f4-11f1-a8a5-03b48837c50f",
  "topics": ["llm", "ai-agent"],
  "show_name": "Training Data",
  "platform": "youtube",
  "transcript": "Speaker 1 | 00:02 - 00:17 ...",
  "transcript_status": "ok"
}
```

当 transcript 不可用时，episode 仍然输出：

```json
{
  "title": "Episode title",
  "link": "https://www.youtube.com/watch?v=...",
  "date": "2026-05-04T20:05:00+00:00",
  "guid": "youtube:VIDEO_ID",
  "topics": ["llm"],
  "show_name": "Training Data",
  "platform": "youtube",
  "transcript_status": "missing",
  "transcript_error": "No subtitle track found"
}
```

`merge-sources.py` 合并后会补充：

```json
{
  "source_type": "podcast",
  "source_name": "Training Data",
  "source_id": "training-data-podcast",
  "quality_score": 7
}
```

## YouTube Backend

YouTube 支持分为 metadata 和 transcript 两层。

metadata：

- 优先使用 `yt-dlp` 展开 playlist/channel/video，因为 YouTube feed 不一定稳定暴露完整 episode 信息。
- 如果 `yt-dlp` 不可用，可对明确的 YouTube feed URL 做轻量 RSS fallback。
- 所有 metadata 抓取都受 `--hours` cutoff 限制。

transcript：

- `backend = auto` 时按可用能力选择 backend。
- 首版首选 `yt-dlp` CLI 下载人工字幕或自动字幕。
- 字幕语言按 `transcript.languages` 顺序尝试。
- transcript 下载失败、字幕不存在、命令超时、JSON 解析失败，都只影响该 episode 的 `transcript_status`。

推荐状态枚举：

```text
ok
disabled
missing
backend_unavailable
timeout
parse_error
error
```

## 缓存策略

新增 podcast cache，避免 cron 重复展开 playlist 和重复下载字幕。

建议路径：

```text
/tmp/follow-news-podcast-cache.json
```

缓存内容分两类：

- metadata cache：按 source URL、platform 和 hours window 缓存短期展开结果。
- transcript cache：按 episode guid 或 YouTube video id 缓存 transcript 和状态。

缓存规则：

- transcript 成功结果可长 TTL 缓存。
- transcript 失败结果使用短 TTL 缓存，避免每天重复请求不可用字幕。
- `--no-cache` 绕过 cache。
- `--force` 忽略已有 output file，但不必强制清空 transcript cache；是否绕过 transcript cache 由 `--no-cache` 控制。

## 失败降级

失败降级是首版设计的核心约束。

- 单个 source metadata 抓取失败：该 source 输出 `status = error`，其他 source 继续。
- 单个 episode transcript 抓取失败：episode 继续输出，并带 `transcript_status` 和短错误信息。
- transcript backend 不可用：podcast fetcher 仍可输出 metadata。
- podcast step 失败：`run-pipeline.py` 记录该 step 错误，但其他 source step 继续执行。
- merge 层缺少 `podcast.json` 时，podcast input count 记为 0。

这样可以支持 YouTube transcript 能力，同时不让字幕可用性拖垮整个 daily digest。

## Merge 与打分

`merge-sources.py` 新增 `--podcast` 输入，并把 podcast episode 当作普通 article 参与现有流程：

- `source_type = podcast`
- `source_name = source.name`
- `source_id = source.source_id`
- `topics` 沿用 episode topics
- `quality_score` 使用现有 priority 和 recency 逻辑

额外加分建议：

- priority podcast source 沿用现有 priority bonus。
- `transcript_status == "ok"` 且 transcript 长度达到最小阈值时增加小 bonus，例如 `+2`。

不建议首版为 podcast 引入复杂的单独排序系统。Podcast Remix section 可以在 prompt 层从 merged JSON 中筛选 top podcast episodes。

## Digest 呈现

普通 topic section：

- podcast episode 可以作为普通条目出现。
- 无 transcript 或 transcript 太短时，只按普通 item 展示。

固定 Podcast Remix section：

- 新增 `🎙️ Podcast Remix`。
- 只选择 `source_type == "podcast"` 且 `transcript_status == "ok"` 的 top N episode，默认 1-3 个。
- 摘要参考 `summarize-podcast.md`，但适配当前中文 digest：
  - 写成独立中文段落，不使用“本期节目讨论了”这类元叙述。
  - 包含核心 takeaway。
  - 点出 speaker 或 guest 背景。
  - 提炼 2-4 个具体、反直觉或可操作洞察。
  - 至少包含一个短引用。
  - 保留 source link。

transcript 是未信任输入，只能用于摘要内容，不能拼进 shell 参数、邮件 subject 或文件路径。

## CLI 与 Pipeline 变更

新增脚本：

```text
scripts/fetch-podcast.py
```

命令形态：

```text
python3 scripts/fetch-podcast.py --defaults config/defaults --config workspace/config --hours 336 --output /tmp/td-podcast.json --verbose
```

`scripts/run-pipeline.py` 需要：

- 新增 `Podcast` step。
- `--skip` 和 `--only` 支持 `podcast`。
- merge 参数新增 `--podcast`.
- source health 输入新增 `--podcast`，或使用 flexible loader 识别 podcast source list。

`scripts/merge-sources.py` 需要：

- 新增 `--podcast` 参数。
- `input_sources` 增加 `podcast_episodes`。
- `output_stats` 保持现有结构。

## 文档与配置校验

需要同步：

- `config/schema.json`：允许 `type = podcast`，定义 `platform`、`url`、`transcript`。
- `scripts/validate-config.py`：识别 podcast source，并要求 `url`。
- `README.md`、`README_CN.md`：更新 source count、pipeline 图、环境变量和 podcast 能力说明。
- `SKILL.md`：更新 metadata、source 列表说明、script 文档和安全说明。
- `references/digest-prompt.md`：新增 Podcast Remix section 和 podcast input stats。

可选工具说明：

```text
yt-dlp
```

`yt-dlp` 应作为 optional binary，不作为必需依赖。没有它时，YouTube transcript 能力降级。

## 测试策略

自动化测试不应依赖真实 YouTube 网络访问或真实字幕可用性。

单元测试：

- podcast source schema validation。
- `validate-config.py` 接受 `type = podcast`。
- YouTube URL platform inference。
- YouTube metadata fixture normalization。
- RSS podcast fixture normalization。
- transcript backend 不存在时输出 `backend_unavailable`，source 不失败。
- transcript 抓取失败时 episode 仍输出。
- transcript cache hit 时不重复调用 backend。
- podcast article 合入 merge 后 `source_type`、`source_name`、`source_id` 和 `quality_score` 正确。
- transcript-ready episode 获得 podcast bonus。

集成式测试：

- fixture `podcast.json` 输入 `merge-sources.py`，验证 `input_sources.podcast_episodes` 和 topic grouping。
- `run-pipeline.py --only podcast` 参数解析正确。
- `run-pipeline.py --skip podcast` 不影响其他 steps。
- README、README_CN 和 SKILL 中的 source counts 与默认配置保持同步。

手工验证：

```text
python3 scripts/fetch-podcast.py --hours 336 --output /tmp/td-podcast.json --verbose --force
python3 scripts/merge-sources.py --podcast /tmp/td-podcast.json --output /tmp/td-merged.json --verbose
python3 scripts/run-pipeline.py --only podcast --debug --force --output /tmp/td-merged.json
python3 -m unittest discover -s tests -v
```

## 风险与缓解

- YouTube 字幕不稳定：把 transcript 作为增强字段，失败时降级。
- `yt-dlp` 版本差异：只依赖稳定 CLI 输出，并通过 fixture 测试 normalization。
- transcript 过长：fetcher 只保存原始 transcript；digest prompt 负责选择 top N，避免整份 digest 被 podcast 占满。
- 去重误伤：podcast link 通常是 YouTube URL，标题可能与普通新闻相似；首版复用现有 URL/title dedup，必要时后续再为 podcast 调整阈值。
- 运行时间变长：限制 podcast source 并发、设置 per-command timeout，并缓存 transcript。

## 已确认决策

首版按以下决策落地：

- YouTube transcript backend 使用可选 `yt-dlp` CLI。
- 不做音频下载和音频转写。
- transcript 获取失败不影响 episode metadata 输出。
- Podcast Remix section 默认显示 1-3 个 transcript-ready episodes。
- `fetch-podcast.py` 不调用 LLM。
