# bili-sunflower-publish

将 HTML 或 Markdown 内容一键发布到 Bilibili，支持 **专栏**（Article）和 **小站**（Tribee）两种目标。

## 功能

- 🔐 自动检测登录状态，未登录时提示手动登录
- 📝 智能标题处理：从 H1 提取标题、过长自动缩短、无意义标题自动生成建议
- 📄 支持 HTML 和 Markdown 两种输入格式
- 🖼️ 本地图片自动内联为 base64 data URI（HTML 和 Markdown 均支持）
- 🚀 一键发布，支持专栏发布设置（封面、定时、原创声明等）
- ⚡ 直接通过编辑器 API 注入内容，无系统剪贴板依赖

## 支持的发布目标

| 目标 | 说明 |
|------|------|
| **专栏 (Article)** | `member.bilibili.com` 长文章 |
| **小站 (Tribee)** | `bilibili.com/bubble` 社区帖子 |

## 前置条件

- **OpenClaw** 的 `openclaw` 浏览器 profile（Playwright 管理的浏览器）

## 触发词

以下关键词会自动激活此 Skill：

> 发布文章到B站 / 上传专栏 / 发B站文章 / 发小站帖子 / tribee发帖 / publish to Bilibili

## 工作流程

1. **导航 & 登录检查** — 打开对应编辑器页面，检测登录状态
2. **预处理 & 标题** — 运行预处理脚本（H1 提取、heading 提升、图片内联、HTML 空白清理）；验证标题
3. **插入文章正文** — HTML 通过 ClipboardEvent dispatch 注入，Markdown 通过 `editor.commands.importMarkdown` 注入
4. **发布** — 应用用户设置后点击发布按钮

## 文件结构

```
bili-sunflower-publish/
├── SKILL.md                         # Skill 定义与详细流程
├── README.md                        # English README
├── README_zh.md                     # 本文件（中文说明）
└── scripts/
    ├── preprocess_html.py           # HTML 预处理（H1、图片、空白）
    └── preprocess_md.py             # Markdown 预处理（H1、图片）
```

## 作者

**Vicky**
