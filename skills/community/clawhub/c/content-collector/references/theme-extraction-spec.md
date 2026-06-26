# 主题关键词提取规范

**目标**:为每篇收藏内容提取 5-7 个精细概念切面,辅助选题和二创时快速判断"这篇可以从哪些角度写文章"。

## 与 tags 的区别

| | tags | themes |
|---|---|---|
| 粒度 | 大类(AI、产品) | 具体概念(Prompt 工程范式、用户分层策略) |
| 用途 | 检索/分类 | 选题/二创灵感 |
| 数量 | 3-5 | 5-7 |

## 触发条件
- **所有内容类型**(文章、视频、推文、笔记),只要有足够文本(≥ 200 字)
- 可以在生成 summary + tags 的同一步 AI 调用中一起提取,不需要额外调用

## 提取方式

使用以下 prompt(或合并到内容提取步骤中):

```xml
<task>
<role>You are an expert content analyst and semantic keyword extraction specialist.</role>
<languageRequirement>IMPORTANT: You MUST generate all keywords in Chinese. Technical terms keep English in parentheses.</languageRequirement>
<context>
Title: {title}
Source: {source}
Author: {author}
</context>
<goal>Extract 5-7 core conceptual themes that precisely capture the main topics discussed.</goal>
<instructions>
  <item>Each keyword/phrase must be 2-6 Chinese characters (or 1-3 English words for technical terms).</item>
  <item>Each keyword must capture a meaningfully different angle, stakeholder, problem, or method.</item>
  <item>Specificity over Generality: "用户分层策略" > "用户运营".</item>
  <item>Cover different facets: challenges, solutions, frameworks, stakeholders, outcomes.</item>
  <item>Avoid synonyms or adjective swaps of earlier keywords.</item>
</instructions>
<qualityControl>
  <item>Would each theme alone spark a specific article idea?</item>
  <item>Are any two themes essentially the same concept reworded?</item>
</qualityControl>
<outputFormat>Return a JSON array of strings: ["theme1","theme2",...]. No markdown.</outputFormat>
<content><![CDATA[
{content_text_first_3000_chars}
]]></content>
</task>
```

## 写入格式

**frontmatter**:
```yaml
themes: ["Prompt工程范式", "AI Agent架构", "用户意图识别", "工具调用策略", "上下文窗口优化"]
```

## 降级
- 内容太短(< 200 字)→ 跳过
- AI 提取失败 → 跳过,用 tags 替代
- 输出不是数组 → 跳过
