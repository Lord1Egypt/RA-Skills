---
name: "article-tuwen"
description: "One-shot pipeline: raw material → 4000-word article → 5-9 social cards + text summary. Invoke when user says '转写成图文' or '转换成图文' with URLs/files/text. Do NOT use for original writing, video, or plain-text formatting."
---

# Article Tuwen — 素材转图文一条龙

## 任务
只做一件事：接收素材（URL/文件/文本），全自动产出5-9张图文卡片+压缩文字稿。不做原创写作、不做视频、不做纯文字排版、不做单步中间产物交付。

## 输出格式

```
C:\Users\Administrator\Desktop\<slug>公众号配图\
├── p1.png ~ pN.png        # 5-9张 (1080×1440)
├── <slug>-article.md       # 长文源文件
├── <slug>-文字稿.txt       # ≥800字≤1000字
└── used-images.json        # 图片来源记录
```
飞书云盘同步文件夹（手机端访问）

## 规则

1. **零确认**：全流程4 Phase无用户确认环节。素材摄入→长文撰写→排版渲染→截图交付，一条龙不停顿
2. **多样性轮换**：每次运行读取`history.json`，封面搜索词/封底搜索词/主题色/布局序列必须与最近3次不同。8封面词+8封底词+5主题池，按序轮换
3. **截图前杀进程**：截图前必须`Stop-Process python`，确认HTTP服务器指向当前项目目录，截图后验证文件大小与上次不同
4. **字号铁律**：正文≥30px，辅助≥26px，元信息≥22px。禁止inline font-size覆盖。所有内页标题统一.h-md(52px)
5. **密度铁律**：活跃构图≥78%画布高度。填不满时追加callout/数据行/注释行。Pull Quote页禁止justify-content:center

## 示例

**输入**：用户说"转写成图文" + 粘贴3个MiMo相关URL
**输出**：9张PNG + mimo-article.md + mimo-文字稿.txt → 桌面mimo公众号配图/ + 飞书云盘URL。封面用"data center"（轮换池第2个），主题用"ink-classic"（轮换池第2个），布局M02,M11,M09,M06,M05,M07,C01,M10,M15
