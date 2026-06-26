# Article-to-HTML

OpenClaw Skill：将文章/推文转化为手机可读的 HTML 信息图，自动匹配视觉风格，截图即用。

## 效果

给 bot 发一个链接或一段文字，自动生成信息图：

```
文生图 https://x.com/xxx/status/xxx
```

## 特点

- **AI 自由设计** — 不套模板，根据内容调性自动选择视觉方向
- **手机适配** — 1080px 画布，字号 ×3 设计，手机上清晰可读
- **后处理兜底** — 自动修复 CSS 边距、溢出、字号等常见问题
- **9 种灵感方向** — 商务简报、暗色科技、杂志编辑、手账笔记、报纸新闻等

## 文件结构

```
├── SKILL.md                 # 入口：工作流 + 设计理念
├── rules/
│   ├── 01-技术底线.md        # 字号、宽度、overflow 硬约束
│   ├── 02-截图流程.md        # Chrome DevTools 截图步骤
│   └── 03-风格灵感.md        # 9 种视觉方向灵感参考
├── scripts/
│   ├── fix-html.js          # CSS 后处理修复
│   └── post-process.sh      # 一键后处理（fix + 字号兜底）
├── templates/               # 9 个 HTML 模板（灵感参考）
└── docs/                    # 快速开始、设计规范
```

## 安装

复制到 OpenClaw skills 目录：

```bash
cp -r . ~/.openclaw/skills/article-to-html
```

## 技术底线

生成的 HTML 必须遵守：

| 规则 | 值 |
|------|-----|
| 容器宽度 | `width: 1080px`（不用 max-width） |
| 容器高度 | `min-height: 1440px`（不用 height） |
| H1 字号 | ≥ 72px |
| 正文字号 | ≥ 30px |
| 最大栏数 | 2 栏 |
| overflow | 禁止 hidden |

详见 `rules/01-技术底线.md`。

## License

MIT
