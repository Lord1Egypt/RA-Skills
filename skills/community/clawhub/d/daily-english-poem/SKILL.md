---
name: daily-poem
description: 每日英语诗歌推送。每天从多个英文诗歌网站抓取当日推荐诗歌（Poem of the Day），包含诗歌全文、作者介绍和深度赏析，推送至飞书。触发词：每日诗歌、英文诗歌推送、poem of the day、daily poem。
---

# 每日英语诗歌推送（Daily Poem）

每天自动从多个英文诗歌网站抓取当日推荐诗歌（Poem of the Day），生成包含全文、作者介绍和深度赏析的推送内容，发送至飞书。

## 数据源（多源降级策略）

按优先级依次尝试，直到成功获取为止：

1. **poemanalysis.com/poem-of-the-day/** — 最佳来源，自带分析
2. **poets.org/poem-a-day** — Academy of American Poets
3. **poems.com/** — Poetry Daily
4. **discoverpoetry.com/poems/poem-of-the-day/** — 备用来源

使用 `web_fetch` 工具依次访问每个 URL，直到获取到有效内容。

## 核心流程

### 步骤 1：抓取诗歌

依次访问上述 URL，使用 `web_fetch` 获取页面内容。从页面中提取：
- 诗歌标题
- 作者姓名
- 来源网站
- 完整诗歌正文
- 已有的分析内容（如有）

### 步骤 2：补充作者信息

如果来源网站未提供足够的作者背景信息，搜索补充：
- 国籍
- 代表作品
- 重要奖项
- 当前职务

### 步骤 3：撰写赏析

### 步骤 4：发送推送

使用 `message` 工具发送到飞书（channel: feishu）。

## 推送格式（英文内容，三级分层排版）

📜 POEM OF THE DAY — [Date]

▌ 基本信息
━━━━━━━━━━━━━━━━
Title: [诗名]
Poet: [作者]
Source: [来源网站]

▌  Poem
━━━━━━━━━━━━━━━━
（完整诗歌正文）

▌ ABOUT THE POET
━━━━━━━━━━━━━━━━
（3-5句：国籍、代表作品、重要奖项、当前职务）

▌ READING & APPRECIATION
━━━━━━━━━━━━━━━━
（4-6段深度分析）
· Form & Structure
（诗体、韵式、 stanza 结构、节奏特点）

· Themes
（2-4个主题，每个附具体诗句为证）

· Imagery & Language
（意象系统、修辞手法、关键字词分析）

· Historical Context
（创作背景、文学史定位）

· Resonance
（当代意义、为何今天仍然重要）

## 排版规则

- 每级标题独占一行
- 分区之间空一行
- 正文段落之间空一行
- 赏析子标题用 `·` 标记，不加粗
- 诗歌正文保持原貌，适当分段
- 不用 markdown 表格（飞书不支持）

## 赏析写作准则

- 有判断力：不只描述，要评价"好在哪里"
- 有深度：挖结构层面的巧思，不只停留于情感描述
- 有证据：每个论点附具体诗句为证
- 拒绝套话：避免"beautiful""moving""deep"等空泛词汇
- 音韵分析：如果诗歌有明显的韵式或节奏特点，必须分析

## 定时任务配置

```
cron: 15 8 * * * @ Asia/Shanghai
session: main
wakeMode: now
delivery: systemEvent → main session
```

## 依赖

- `web_fetch` 工具（用于抓取诗歌网站）
- `message` 工具（用于飞书推送）

## 注意事项

- 如果所有源都失败，在飞书发送失败通知
- 诗歌正文保持原文格式，不要改写
- 作者传记信息从可靠来源获取（如 poets.org、Wikipedia）
