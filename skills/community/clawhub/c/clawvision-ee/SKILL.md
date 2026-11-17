---
name: "clawvision-ee"
description: "ClawVision East Edition 1.0.7 (中文版) — 本地导出工具。读取你选择的 OpenClaw 会话历史，使用本地 LLM 总结，并写入 HTML、Markdown、PowerPoint 和 PNG 导出文件到本地磁盘。需要权限：读取会话历史、列出会话、本地文件读写、执行本地 Python/Playwright 脚本、本地 LLM 推理。数据不会发送到外部 API。"
metadata:
  version: 1.0.8
  author: Maximius
  tags: [visualization, summary, html, sessions, codex, markdown, powerpoint, aesthetic, presets, chinese, 中文, east-edition]
  homepage: https://github.com/monaxamo/clawvision-ee
  license: MIT
  icon: clawvision_demo_zh.png
allowed-tools:
  - sessions_history
  - sessions_list
  - write
  - read
  - exec
  - node_inference
user-invocable: true
---

# ClawVision East Edition 1.0.8（中文版）

把任意 OpenClaw 会话变成一张可分享的视觉摘要卡片 —— 类似 Codex `$visualize`，但完全本地运行。同时导出 Markdown 与重新设计的品牌化 PowerPoint。

## 1.0.7 更新内容

- 安装页描述进一步明示：本 skill 会读取你选择的 OpenClaw 会话历史，并通过本地 LLM 总结后写入 HTML / Markdown / PowerPoint / PNG 导出文件。
- 移除未使用的 `skill_workshop` 权限。
- 修复 CSS 变量：生成 HTML 正确包含每个预设的 `:root` 颜色变量，标签页、卡片、导出按钮、主题切换均可正常渲染。
- 新增「摘要设计规范」步骤：先确认语言、视觉预设、强调色、字体、布局与导出格式，再渲染。
- 5 套视觉预设：`minimal`、`editorial`、`retro`、`luxury`、`playful`，同时影响 HTML 与 PPTX 的色彩、字体、圆角与阴影。

## 何时使用

仅在用户明确要求生成可视化/可导出摘要时激活，例如：

- “为这次对话生成一张 ClawVision 摘要卡片。”
- “把当前 OpenClaw 会话导出成 HTML/PNG/Markdown/PPT。”
- “根据刚才的聊天做一份视觉一页纸。”
- “用 ClawVision 总结会话 `<id>`。”

请求模糊时，先询问用户确认意图与范围。

## 何时不要使用

- 不要响应泛泛的“总结”或“记个笔记”。
- 如果会话可能包含机密、凭证、个人数据或内部标识符，先征得用户明确同意；否则停止或仅做不导出的泛化总结。

## 工作流程

1. 确认用户意图。若请求模糊或会话可能敏感，先征得明确同意。
2. 选择会话：用户说“这次对话”时使用当前会话；提到其他会话时用 `sessions_list` 按 ID 或标签查找。
3. 拉取历史：`sessions_history(includeTools=false, limit=200)`。
4. 构建纯文本转录：每条消息格式为 `\n\n<角色>: <内容>`。
5. 执行「摘要设计规范」（见下文）。默认：语言随会话、预设 `minimal`、强调色 `#2a9df4`、字体 `Inter`、布局 `card-based`、导出全部格式。先展示规范，让用户可修改。
6. 通过 `node_inference` 发送下方的中文总结提示词，解析返回的 JSON。
7. 运行 `scripts/generate_visual.py --summary <json文件> --output <目录> --png --md --pptx --lang zh --preset <预设>`，生成：
   - 自包含 HTML（中/英/俄语言切换 + 浅色/深色主题切换）
   - 每个标签页一张 PNG
   - Markdown 摘要
   - 品牌化 PowerPoint
8. 向用户展示输出路径；若节点已连接，可提议用 `canvas` 打开 HTML。

## 摘要设计规范

生成前先输出以下规范并请求确认或覆盖：

```text
摘要设计规范
==============
1. 会话语言：[zh | en | ru]
2. 视觉预设：[minimal | editorial | retro | luxury | playful]
3. 主强调色：#HEX
4. 字体：[Inter | Georgia | Space Grotesk | Playfair Display | Nunito | 其他]
5. 布局策略：[card-based | editorial-column | retro-grid | luxury-spaced | playful-stacked]
6. 导出格式：[html | png | md | pptx | all]
```

### 预设指南

| 预设 | 适用场景 | 强调色示例 | 圆角 | 阴影 | 字体 |
|---|---|---|---|---|---|
| `minimal` | 简洁技术摘要 | 蓝/灰 | 中 | 轻 | Inter / 系统字体 |
| `editorial` | 长文洞察、文章 | 酒红/藏青 | 小 | 平 | Georgia / 衬线 |
| `retro` | 怀旧、游戏、老网页 | 橙/棕 | 大 | 硬 | Space Grotesk |
| `luxury` | 金融、高端产品 | 金/黑 | 极小 | 柔 | Playfair Display |
| `playful` | 教育、社交、引导 | 紫/绿 | 巨大 | 弹 | Nunito |

## 总结提示词（通过 node_inference 发送）

```text
你是一名对话总结器。阅读下面的 OpenClaw 转录，只返回一个 JSON 对象，不要 markdown：

{
  "title": "简短中文标题",
  "subtitle": "一句话背景",
  "main_takeaway": "最重要的结论",
  "format_takeaway": "讨论是如何组织的",
  "next_takeaway": "下一步该做什么",
  "flow": [
    {"label": "步骤 1", "sub": "发生了什么"},
    {"label": "→", "sub": ""},
    {"label": "步骤 2", "sub": "发生了什么"}
  ],
  "metrics": [
    {"title": "目标", "text": "..."},
    {"title": "方法", "text": "..."},
    {"title": "产出", "text": "..."}
  ],
  "dos": ["好的做法 1", "好的做法 2"],
  "donts": ["风险 1", "风险 2"],
  "checklist": [
    {"text": "事项名称", "status": "ready|pending|blocked"}
  ],
  "next_steps": ["行动 1", "行动 2"]
}

转录：
{{transcript}}
```

## 输出规则

- HTML 必须自包含：内联 CSS 与 JS，无外部资源。预设字体使用 Web 安全回退栈。
- 提供中/英/俄语言切换器与浅色/深色主题切换。
- 生成内容与会话语言一致；中文版默认中文输出。
- PowerPoint 使用与 HTML 卡片相同的品牌色、预设与卡片布局。
- 默认输出目录 `workspace/visualized/`；若不可写则回退到用户偏好目录。
- 绝不导出会话中的秘密、密码、令牌或私人标识符。

## 安全

- 访问会话历史或写入输出文件前，先确认意图与范围。
- 若会话可能敏感，先询问用户；若拒绝，则停止或仅做不导出的泛化总结。
- 不要向外部 API 发送转录。
- 分享前检查生成的文件。

## 路线图

- **ClawVision 中文版 1.0.7** — 当前稳定版：中文工作流、明示权限、CSS 变量修复、摘要设计规范、5 套 HTML/PPTX 视觉预设。
- **ClawVision 中文版 2.0** — 计划：会话分析（消息统计、工具使用、主题/实体提取、洞察、纯 CSS 图表）。
