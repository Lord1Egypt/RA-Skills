# 精彩片段提取规范

**目标**:从长视频转录中自动筛选 3-5 个最值得看的精华时间段,帮助用户快速定位价值内容。

## 触发条件
- 视频时长 ≥ 10 分钟
- 有完整转录文本(whisper 或 native_cc)
- < 10 分钟的短视频跳过此步骤

## 提取方式

使用以下 prompt 提取精彩片段(遵循 `~/.openclaw/workspace/references/prompt-engineering-template.md` 的 XML 结构化范式):

```xml
<task>
<role>You are an expert content curator selecting the most valuable moments from a video transcript.</role>
<languageRequirement>IMPORTANT: You MUST generate all content in Chinese.</languageRequirement>
<context>
Title: {video_title}
Speaker: {video_author}
Duration: {duration}
</context>
<goal>From this {duration} video, select the 3-5 most compelling moments worth watching.</goal>
<instructions>
  <item>Each highlight must be a contiguous segment of 45-90 seconds.</item>
  <item>Title must be specific and ≤15 characters. No generic titles like "重要观点".</item>
  <item>Quote must be an exact verbatim match from the transcript.</item>
  <item>Timestamps in [MM:SS-MM:SS] format.</item>
  <item>Insight explains in one sentence why this moment matters.</item>
  <item>Distribute highlights across the full video timeline - don't cluster in the opening.</item>
  <item>Focus on: contrarian insights, vivid stories, data-backed arguments, practical frameworks, memorable quotes.</item>
</instructions>
<qualityControl>
  <item>Are highlights distributed across the video (beginning, middle, end)?</item>
  <item>Does each highlight stand alone without needing context?</item>
  <item>Is the quote a verbatim match from the transcript?</item>
</qualityControl>
<outputFormat>Return strict JSON: [{"title":"string","start":"MM:SS","end":"MM:SS","quote":"exact transcript text","insight":"one sentence why this matters"}]. No markdown.</outputFormat>
<transcript><![CDATA[
{transcript_with_timestamps}
]]></transcript>
</task>
```

## 写入格式

**frontmatter**:
```yaml
highlights:
  - title: "片段标题"
    start: "12:30"
    end: "13:45"
    quote: "原文引用"
    insight: "为什么值得看"
```

**正文**(在「核心观点」之后、「要点摘录」之前):
```markdown
## 精彩片段

> AI 从 {duration} 视频中筛选的 {N} 个最值得看的片段

**1. [{start}-{end}] {title}**
> {quote}

{insight}
```

## 降级
- 转录文本过短(< 500 字)→ 跳过
- AI 提取失败 → 跳过,不阻塞收藏流程
- 产出不满 3 个 → 有几个写几个
