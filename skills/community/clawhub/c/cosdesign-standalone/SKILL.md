---
name: cosdesign
description: |
  设计风格精准复刻工具 — 通过 Jina Reader / WebFetch / WebSearch 浏览目标网页，
  自动提取色彩体系、字体排版、间距系统、布局结构、组件风格，输出可执行的设计规范文档。
  支持单页分析、多站对比、风格定义输出（Design Token / CSS Variable / Tailwind Config）。
  Precise design replication tool — crawl any website via Jina/WebFetch, extract color palette,
  typography, spacing, layout patterns, and output actionable design specifications.
keywords:
  - cosdesign
  - 设计复刻
  - 设计分析
  - design-system
  - design-token
  - color-palette
  - typography
  - 色彩提取
  - 字体分析
  - 排版分析
  - 布局分析
  - web-design
  - CSS变量
  - Tailwind配置
  - 风格定义
  - 设计规范
  - 网页设计
  - UI分析
  - 视觉风格
  - Jina
  - WebFetch
  - 设计对比
  - component-style
  - spacing-system
requirements:
  node: ">=18"
  binaries:
    - name: node
      required: true
      description: "Node.js runtime >= 18"
metadata:
  openclaw:
    homepage: "https://github.com/Cosmofang/cosdesign"
    author: "Cosmofang"
    runtime:
      node: ">=18"
    env:
      - name: JINA_API_KEY
        required: false
        description: "Jina Reader API key for enhanced crawling. Free tier works without key."
---

# CosDesign — 设计风格精准复刻

> 给我一个 URL，还你一套完整的设计规范

---

## Purpose & Capability

CosDesign 是一个**设计风格逆向工程工具**，能从任意网页 URL 中提取完整的视觉设计体系。

**核心能力：**

| 能力 | 说明 |
|------|------|
| 色彩提取 | 从网页中提取主色、辅色、背景色、文字色、渐变色，输出 HEX/RGB/HSL |
| 字体分析 | 识别 font-family、font-size 层级、font-weight、line-height、letter-spacing |
| 间距系统 | 提取 padding/margin/gap 规律，归纳为 4px/8px 栅格体系 |
| 布局结构 | 分析页面 grid/flex 布局、断点、容器宽度、响应式策略 |
| 组件风格 | 按钮、卡片、导航栏、表单等常见组件的视觉参数 |
| 风格定义输出 | 生成 CSS Variables / Design Tokens JSON / Tailwind Config |
| 多站对比 | 同时分析 2-3 个 URL，输出风格差异对比表 |
| 设计报告 | 生成完整的 HTML 设计规范文档（含色卡、字体样本、间距示意） |

**能力边界（不做的事）：**
- 不做 UI 设计或出图（只分析，不创作）
- 不抓取需要登录的页面内容
- 不提取图片资源或下载字体文件
- 不修改目标网站的任何内容

---

## Instruction Scope

**在 scope 内：**
- "分析这个网页的设计风格" / "提取这个 URL 的配色方案"
- "帮我复刻这个网站的设计规范"
- "对比这两个网站的设计风格"
- "提取这个页面的字体排版系统"
- "生成 Tailwind 配置来匹配这个设计"
- "输出 CSS 变量 / Design Token"

**不在 scope 内：**
- "帮我设计一个网页"（CosDesign 分析设计，不创作设计）
- "下载这个网站的图片"（不做资源抓取）
- "修改这个网站的样式"（只读分析，不修改）
- "分析这个 APP 的设计"（仅支持 Web URL，不支持移动端截图分析）

---

## Credentials

| 操作 | 凭证 | 说明 |
|------|------|------|
| 网页抓取（Jina Reader） | `JINA_API_KEY`（可选） | 免费层无需 key；有 key 可提升速率限制 |
| 网页抓取（WebFetch） | 无 | Claude 内置工具，无需凭证 |
| 网页搜索（WebSearch） | 无 | Claude 内置工具，无需凭证 |

**不做的事：**
- 不存储、传输或记录任何 API 凭证
- 不访问需要登录的页面
- 所有分析均为只读操作，不对目标网站产生任何影响

**最小配置：** 完全无需凭证即可使用。`JINA_API_KEY` 仅在需要高频抓取时可选配置。

---

## Persistence & Privilege

| 路径 | 内容 | 触发条件 |
|------|------|---------|
| `data/analysis-history.json` | 历次分析记录（URL + 时间戳 + 摘要） | 每次分析完成后追加 |
| stdout | 设计规范文本 / JSON / HTML | 脚本运行时输出 |

**不写入的路径：**
- 不修改系统配置或 shell 环境
- 不创建 cron 任务
- 不写入用户项目目录（除非用户明确指定输出路径）

**权限级别：**
- 以当前用户身份运行，不需要 sudo
- 仅读取网页公开内容，不做任何写入或修改

**卸载：** 删除 skill 目录即可，无残留配置。

---

## Install Mechanism

### 标准安装

```bash
clawhub install cosdesign
```

### 手动安装

```bash
cp -r /path/to/cosdesign ~/.openclaw/workspace/skills/cosdesign/
```

### 验证安装

```bash
node ~/.openclaw/workspace/skills/cosdesign/scripts/analyze.js https://example.com
# 应输出：该 URL 的设计分析 prompt
```

### 可选配置

```bash
# 如需 Jina 高频抓取（可选）
export JINA_API_KEY=<your-jina-api-key>
```

---

## 使用方法

```bash
# 单页分析 — 提取完整设计规范
node scripts/analyze.js <url>

# 指定分析维度
node scripts/analyze.js <url> --focus color        # 仅色彩
node scripts/analyze.js <url> --focus typography    # 仅字体
node scripts/analyze.js <url> --focus layout        # 仅布局
node scripts/analyze.js <url> --focus components    # 仅组件

# 多站对比
node scripts/compare.js <url1> <url2> [url3]

# 输出格式
node scripts/export.js <url> --format css-vars     # CSS 变量
node scripts/export.js <url> --format tokens        # Design Tokens JSON
node scripts/export.js <url> --format tailwind      # Tailwind Config
node scripts/export.js <url> --format html-report   # 完整 HTML 报告

# 风格定义
node scripts/define-style.js <url>                  # 输出风格定义文档
```

---

## 输出示例

### 色彩体系
```
Primary:    #1a73e8 (Google Blue)
Secondary:  #34a853 (Green)
Background: #ffffff / #f8f9fa
Text:       #202124 / #5f6368
Accent:     #ea4335 (Red)
Border:     #dadce0
```

### 字体排版
```
H1: Google Sans, 36px/44px, 400, #202124
H2: Google Sans, 24px/32px, 400, #202124
Body: Roboto, 14px/22px, 400, #5f6368
Caption: Roboto, 12px/16px, 400, #80868b
```

### Design Tokens (JSON)
```json
{
  "color": {
    "primary": { "value": "#1a73e8" },
    "secondary": { "value": "#34a853" },
    "bg-default": { "value": "#ffffff" },
    "text-primary": { "value": "#202124" }
  },
  "font": {
    "heading": { "value": "'Google Sans', sans-serif" },
    "body": { "value": "'Roboto', sans-serif" }
  },
  "spacing": {
    "xs": { "value": "4px" },
    "sm": { "value": "8px" },
    "md": { "value": "16px" },
    "lg": { "value": "24px" },
    "xl": { "value": "32px" }
  }
}
```

---

## 📁 文件结构

```
cosdesign/
├── SKILL.md
├── package.json
├── _meta.json
├── .clawhub/origin.json
├── data/
│   └── analysis-history.json
├── references/
│   └── extraction-guide.md
└── scripts/
    ├── analyze.js          # 单页设计分析
    ├── compare.js          # 多站风格对比
    ├── export.js           # 设计规范导出（CSS/Token/Tailwind/HTML）
    └── define-style.js     # 风格定义文档生成
```

---

*Version: 1.0.0 · Created: 2026-04-10 · Author: Cosmofang*
