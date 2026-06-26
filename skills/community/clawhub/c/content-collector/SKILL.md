---
name: content-collector
version: 2.0.0
description: >
  个人内容收藏与知识管理系统。收藏、整理、检索、二创。
  Use when: (1) 用户说"收藏"/"存一下"/"记录下来"/"save"/"bookmark"/"clip",
  (2) 用户要求搜索之前收藏的内容,
  (3) 用户要求基于收藏内容生成社交媒体文案(二创),
  (4) 用户提到"之前看过一个..."/"上次收藏的..."等回忆性检索。
  已支持来源:博客、X/Twitter、网页、B站/YouTube/抖音/小红书视频。
  NOT for: 纯个人笔记(直接写文件)、长文写作(用 internal-comms/docx)、
  公众号发布(用 wemp-ops)、小红书发布(用 xiaohongshu-ops)。
---

# Content Collector - 个人内容收藏系统

收藏好内容 → 结构化整理 → 关键词检索 → 二次创作

## 数据位置

- **主存储**: `<WORKSPACE>/collections/`（articles/ tweets/ videos/ wechat/ ideas/）
- **Obsidian 同步**: `<YOUR_OBSIDIAN_VAULT>/收藏/`（每次收藏同时写入）
- **索引**: `collections/index.md` + `collections/tags.md`（自动维护）

## 收藏工作流

### Step 0: 去重（每次必做）
有 URL 时: `obsidian search query="<domain/path>" total`（去掉 `https://` 前缀）或 `grep -rl "<url>" collections/`
返回 > 0 → 已收藏，终止。返回 0 → 继续。

### Step 1: URL 路由
按 URL 匹配处理路径。详见 `references/url-routing-and-site-specs.md`。

| URL 模式 | category | 处理方式 |
|----------|----------|---------|
| 内网域名 | articles | Chrome Relay，不调 web_fetch |
| `arxiv.org/abs/*` | articles | 提取 abstract/authors |
| `github.com/*/*` | articles | README + stars/language |
| `mp.weixin.qq.com` | wechat | 优先 browser |
| `youtube.com/watch*` | videos | Supadata transcript |
| B站 | videos | `video_transcribe.sh` 本地转录 |
| 小红书/抖音(视频) | videos | `video_transcribe.sh` 本地转录 |
| `x.com/*/status/*` | tweets | 提取互动数据，thread 展开 |
| 其他 | articles | 默认流程 |

### Step 2: 内容提取

**文章/网页:**
1. `supadata_fetch.py web <url>`（降级: `web_fetch`）
2. Schema.org 提取 — 详见 `references/schema-extraction-spec.md`
3. 插图提取+下载（**必做**）— 详见 `references/image-extraction-spec.md`
4. 主题关键词提取 — 详见 `references/theme-extraction-spec.md`

**视频:**
1. 元数据: `supadata_fetch.py metadata <url>` 或 `bilibili_extract.py <url>`
2. 转录: `bash scripts/video_transcribe.sh <url>`（自动检测平台和字幕源）
3. 精彩片段提取(≥10min) — 详见 `references/highlight-extraction-spec.md`
4. 主题关键词提取

**推文/短内容:** 直接提取文本+互动数据

### Step 3: 写文件
1. 生成 `collections/{category}/YYYY-MM-DD-slug.md`（格式见下方 Schema）
2. 内容概览图(>1000字文章) — 详见 `references/content-overview-spec.md`
3. 同步到 Obsidian — 详见 `references/obsidian-integration.md`
4. `obsidian daily:append content="- 📌 收藏了 [[{标题}]]({source})| {一句话摘要}"`
5. 更新 `index.md` + `tags.md`

### Step 3.5: 微信图片缓存（wechat 类必做）
如果 URL 是微信公众号（`mp.weixin.qq.com`），写完收藏文件后运行：
`bash scripts/cache-wechat-images.sh <刚写入的收藏文件>`
下载微信 CDN 图片到本地 `collections/images/<slug>/`，防止图片过期 404。

### Step 4: 关联匹配
运行 `bash scripts/post-collect.sh <刚写入的收藏文件>`
脚本自动匹配活跃项目和相关收藏，更新 frontmatter 的 related_projects。
如有相关收藏，在回复中附带提及。
仍需手动匹配 `collections/topics/topic-pool.md` → 追加到 `temp/handoffs/collector-to-writing.md`

## 写文件前自检

每次写 collections/ 文件前，确认以下步骤已完成。缺项标注 `incomplete: true`，不允许静默跳过。

- 去重 ✓ → 内容提取 ✓ → 插图(文章类,必做) ✓ → 主题关键词 ✓ → 写文件 ✓ → Obsidian同步 ✓ → Daily Note ✓
- 写 tags 前运行 `bash scripts/normalize-tags.sh <tag1> <tag2> ...` 检查是否有已有近似 tag，优先复用已有 tag 名称

## 存储 Schema

文件命名: `YYYY-MM-DD-slug.md`

```yaml
---
title: ""
source: ""
url: ""
author: ""
date_published: ""
date_collected: ""
tags: []
category: "articles|tweets|videos|wechat|ideas"
language: "zh|en"
summary: ""
themes: []              # 5-7 个概念切面
schema_type: ""         # Schema.org @type（可选）
schema_data: {}         # ≤10 key-value（可选）
incomplete: false
# 视频专属
duration: ""
platform: ""
bvid: ""
stats: {}
subtitle_source: ""     # native_cc|whisper
highlights: []          # 精彩片段
related_projects: []
---
```

### 内容结构
- **内容概览**（Mermaid，>1000字触发）
- **核心观点**（3-7个要点）
- **精彩片段**（视频≥10min）
- **要点摘录**（blockquote 金句）
- **热门评论精选**（视频类）
- **我的笔记**
- **原文摘要**（200-500字）

### 英文内容
默认 storytelling 翻译风格。术语参照 `<WORKSPACE>/references/glossary-ai-zh.md`，首次出现 `中文(English)` 格式。

## 检索

1. 标签: `tags.md`
2. 全文: `grep -ril "keyword" collections/`
3. 返回匹配列表 + 摘要

## 二创

按选题从收藏库筛选素材，交给 `xiaohongshu-ops` 或 `wemp-ops` 处理。本 skill 只负责供料。

## 工具脚本

| 脚本 | 用途 |
|------|------|
| `scripts/supadata_fetch.py web\|transcript\|metadata <url>` | Supadata API 抓取 |
| `scripts/bilibili_extract.py <url>` | B站元数据 |
| `scripts/video_transcribe.sh <url>` | 视频转录（自动检测平台） |
| `scripts/sync_to_obsidian.py` | 批量同步到 Obsidian |
| `scripts/cache-wechat-images.sh <file>` | 微信 CDN 图片本地缓存 |
| `scripts/normalize-tags.sh <tag1> <tag2> ...` | 标签归一化去重 |
| `scripts/post-collect.sh <file>` | 收藏后自动关联分析 |

## 🔴 Final: 机械验证（不可跳过）

通知用户前运行：
```bash
bash scripts/skill-verify.sh content-collector <collections-file-path>
# 例: bash scripts/skill-verify.sh content-collector collections/wechat/2026-04-23-xxx.md
```
- ✅ ALL PASSED → 回复用户收藏结果
- ❌ FAILED → 按输出补齐缺失项（Obsidian 同步/插图/index.md 等），重新验证直到通过

绝不在验证未通过时回复用户"已完成"。

## 收藏结果通知

- 成功: `📌 已收藏:<标题>\n核心:<一句话摘要>\n标签:<3-5个标签>`
- 重复: `📌 已存在:<标题>(之前已收藏过)`
- 失败: `❌ 收藏失败:<URL>\n原因:<失败原因>`

## 下一步建议（条件触发）

| 触发条件 | 推荐 |
|---------|------|
| 与公众号选题方向高度相关 | 用 wemp-ops 写 |
| 适合小红书短图文 | 用 xiaohongshu-ops 改写 |
| 某博主收藏 ≥3 条 | 用 x-profile-deep-dive 画像 |
| 涉及技术方案/架构决策 | 存到 memory 做长期参考 |
