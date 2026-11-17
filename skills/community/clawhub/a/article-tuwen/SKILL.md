---
name: "article-tuwen"
version: "1.1.2"
slug: "article-tuwen"
displayName: "Article Tuwen"
summary: "素材转图文一条龙：URL/文件/文本 → 长文 + 5-9张社交卡片 + 文字稿"
license: "MIT-0"
description: "One-shot pipeline: raw material → 4000-word article (with web search enrichment) → 5-9 social cards + text summary. Invoke when user says '转写成图文' or '转换成图文' with URLs/files/text. Local files are created on desktop. Cloud sync is opt-in only. Do NOT use for original writing, video, or plain-text formatting."
---

# Article Tuwen — 素材转图文一条龙

## 任务
接收素材（URL/文件/文本），产出5-9张图文卡片+压缩文字稿。不做原创写作、不做视频、不做纯文字排版。

## 数据处理声明

触发本技能后，以下操作会自动执行：
- **网络请求**：WebFetch抓取URL素材；WebSearch搜索补充信息进行事实核查；从图片源下载封面/封底图片
- **本地文件创建**：在桌面创建输出文件夹，写入PNG图片、MD文章、TXT文字稿
- **子技能调用**：调用transcript-crafter（长文撰写）和xhs-crafter（排版截图），子技能的具体行为见各自技能声明

以下操作需要用户确认：
- **云上传**：飞书云盘同步是可选步骤，执行前必须征得用户明确同意。如果素材包含敏感/机密信息，应提醒云上传风险
- **不传输原始素材**：飞书云盘仅上传生成的PNG和文字稿，不上传原始素材文件

## 权限声明

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| 网络访问 | ✅ | WebFetch抓取URL素材；WebSearch搜索补充信息；下载封面/封底图片；用户确认后上传飞书云盘 |
| 文件读写 | ✅ | 读取用户提供的文件；写入桌面输出目录和项目临时目录 |
| 环境变量 | ❌ | 不读取任何环境变量 |
| subprocess | ✅ | 调用xhs-crafter执行截图、lark-cli上传飞书（可选） |
| 外部 API | ✅ | lark-cli飞书API（可选，需用户确认） |

## 架构：编排层，非执行层

article-tuwen是**编排技能**，自身不执行内容生产，而是调度两个子技能：

```
article-tuwen（编排层）
│
├── 子技能1: transcript-crafter — 长文撰写
│   路径: <transcript-crafter技能安装目录>
│   职责: 10维度提取→人设适配→框架→5工具搜索补充→重构撰写
│   产出: <slug>-article.md（2500-4000字，增量密度≥70%）
│
├── 子技能2: xhs-crafter — 排版渲染
│   路径: <xhs-crafter技能安装目录>
│   职责: HTML排版→截图→文字稿压缩
│   产出: 5-9张PNG + <slug>-文字稿.txt
│
└── article-tuwen自身 — 编排+多样性+交付
    职责: 多样性轮换、字号/密度铁律、截图安全、本地交付
```

## 触发边界

**触发条件**（必须同时满足）：
- 用户明确说"转写成图文"或"转换成图文"
- 用户提供了素材：URL、文件路径、或粘贴文本

**不触发**：
- 用户只说"写文章"、"排版"而没有"图文"关键词
- 用户只提供URL但没有说"转写/转换成图文"
- 普通对话中提到"图文"但无转换意图

## 输出格式

```
<桌面输出目录>\<slug>公众号配图\
├── p1.png ~ pN.png        # 5-9张 (1080×1440)
├── <slug>-article.md       # 长文源文件
├── <slug>-文字稿.txt       # ≥800字≤1000字
└── used-images.json        # 图片来源记录
```
飞书云盘同步为可选项，需用户确认后执行。

## 规则

1. **本地零确认，云上传需确认**：Phase 1-3全自动执行无需确认。Phase 4飞书云上传前必须询问用户"是否同步到飞书云盘？"，用户同意才执行
2. **调用transcript-crafter**：Phase 1必须调用transcript-crafter技能的完整8步流程（10维度提取+5工具搜索补充+事实核查），禁止用简化版内嵌逻辑替代。产出文章增量密度必须≥70%
3. **用户已有转写稿时跳过Phase 1**：如果用户说"不用转写"或提供了已有的转写稿MD文件，直接进入Phase 2-4
4. **多样性轮换**：每次运行读取`history.json`，封面搜索词/封底搜索词/主题色/布局序列必须与最近3次不同。8封面词+8封底词+5主题池，按序轮换
5. **截图**：调用xhs-crafter执行HTML截图，截图后验证文件大小与上次不同
6. **字号铁律**：正文≥32px，辅助≥28px，元信息≥24px。禁止inline font-size覆盖。所有内页标题统一.h-md(52px)
7. **密度铁律**：活跃构图≥78%画布高度。填不满时追加callout/数据行/注释行。Pull Quote页禁止justify-content:center

## 示例

**输入**：用户说"转写成图文" + 粘贴3个MiMo相关URL
**Phase 1**：调用transcript-crafter → 产出mimo-article.md（增量密度≥70%，含5工具搜索补充数据）
**Phase 2-3**：多样性轮换→排版渲染→截图
**Phase 4**：本地交付到桌面 → 询问用户是否云上传
**输出**：9张PNG + mimo-article.md + mimo-文字稿.txt → 桌面mimo公众号配图/（+ 飞书云盘URL，如用户确认）

**输入**：用户说"转换成图文，不用转写" + 提供已有MD文件
**Phase 1**：跳过（用户已有转写稿）
**Phase 2-4**：多样性轮换→排版渲染→截图→本地交付→询问云上传
