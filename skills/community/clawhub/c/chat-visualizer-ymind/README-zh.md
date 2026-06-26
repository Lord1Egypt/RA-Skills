[English](README.md) | **中文**

# chat-visualizer-ymind

一个适用于 OpenClaw、Claude Code 和 Codex 的 AI agent skill。把任何 AI 对话可视化为结构化思维图 —— 提取推理路径、呈现思维阻力点、追踪想法的演化过程。

**核心理念：** 对话是线性的，思维不是。AI 对话里藏着大量洞察 —— 但它们散落在漫长的聊天线程里。你会忘记关键突破、重复走过的弯路、错过节点之间的连接。这个 skill 把你的思维外化：每一段对话，都变成一张可以导航的图，记录你真正想清楚了什么。

## 功能

分享一个对话链接 → 得到一张交互式力导向图：
- **推理节点** —— 从对话中提取事实、阻力、灵感和行动
- **思维转折检测** —— 对话在哪里发生了根本性的转变？
- **行动清单** —— 自动提取、按优先级排序、关联到具体的阻力上下文
- **D3.js 可视化** —— 暗色模式交互图，可以导出为单个 HTML 文件分享

![泰坦尼克号与功利性过滤器](assets/graph-demo.png)

## 快速开始

1. 安装 skill（见[安装](#安装)）
2. 把对话链接发给你的 agent：
   ```
   帮我可视化这个：https://chatgpt.com/share/xxx
   ```
3. agent 自动抓取对话、提取思维图、生成 HTML 文件
4. 打开 `graph.html` —— 浏览节点、追踪行动路径、导出洞察

**自动抓取**（分享链接 → agent 自动获取内容）：ChatGPT、Gemini、Claude、DeepSeek、豆包。

**粘贴模式**（没有分享链接？Ctrl+A → 复制 → 粘贴给 agent）：支持任何 AI 工具，不需要链接。

想支持其他平台的自动抓取？[提 issue](https://github.com/yslenjoy/chat-visualizer-ymind/issues)。

## 安装

### ClawHub

```bash
npx clawhub@latest install chat-visualizer-ymind
```

### 手动安装

#### OpenClaw

```bash
git clone https://github.com/yslenjoy/chat-visualizer-ymind.git ~/.openclaw/skills/chat-visualizer-ymind
```

#### Claude Code

```bash
git clone https://github.com/yslenjoy/chat-visualizer-ymind.git ~/.claude/skills/chat-visualizer-ymind
```

#### Codex

```bash
git clone https://github.com/yslenjoy/chat-visualizer-ymind.git ~/.codex/skills/chat-visualizer-ymind
```

## 输出结构

结果默认保存到 `~/ymind-ws/`（可通过 `YMIND_DIR` 覆盖）。每次运行生成一个独立文件夹 —— 你的个人思维图库。

```
~/ymind-ws/
  index.html                    ← 所有 session 的可视化时间线
  index.json                    ← 机器可读的 session 索引
  20260319-143021_chatgpt/
    raw_chat.json               ← 抓取的原始对话
    graph.json                  ← 提取的思维图数据
    graph.html                  ← D3.js 可视化（有 raw_chat.json 时左右分栏，左边原始对话）
    graph.png                   ← 截图
    meta.json                   ← provider、url、标题、创建时间
```

## 隐私

- **不存储 Cookie** —— 抓取使用全新浏览器上下文，不缓存任何会话数据
- **完全本地** —— 所有输出只保存在本机，不上传任何内容
- **数据不出本机** —— 所有对话数据仅保存在本地；渲染出的 HTML 通过 CDN 加载字体和可视化库（D3.js、html2canvas），需要联网才能正常显示
- 对话链接仅用于抓取你提供的公开分享页

## 处理流程

```
输入
  ├─ 分享链接  → scripts/run.sh fetch → fetch-chat.py → raw_chat.json
  └─ 粘贴文本  → 直接告诉 agent 对话内容（无需抓取）
        │
  [LLM] SKILL.md → 分析 → graph.json
        │
  scripts/run.sh render → render-html.py → graph.html + graph.png
        │
  （自动）重建 index.html + index.json  ← 你的完整 session 库
```

## 依赖

需要 Python 3.10+。

**最小安装**（粘贴模式）：无需安装任何依赖。

**完整功能**（自动抓取 URL + 截图）：
```bash
pip install requests playwright && playwright install chromium
```

## 许可证

MIT
