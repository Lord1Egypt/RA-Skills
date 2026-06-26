---
name: doubao-chat-obtain
description: 读取豆包（Douyin/Doubao）对话页面的完整全文内容。用于读取豆包对话帖子（如 https://www.doubao.com/thread/xxx ），解决虚拟滚动容器导致的"只能读取第一屏"问题，提取完整文本保存到本地文件。此 Skill 应在用户分享豆包对话链接或要求读取豆包页面时触发。豆包页面采用虚拟滚动，内容初始不可见，必须通过 JavaScript 直接操作 DOM 元素提取。
agent_created: true
visibility: public
version: 1.0.0
---

# DoubaoChatObtain

读取豆包对话页面完整全文。

## 核心原理

豆包页面的 `body` 设置了 `overflow: hidden`，`window.scroll` 无效。真正的滚动区域是一个 `div.fixed` 容器，页面内容通过虚拟滚动加载（只渲染可视区域附近的内容）。直接用 `element.innerText` 可以一次性绕过虚拟滚动，提取已渲染的全部文本。

## 前置依赖

需安装 [agent-browser](https://www.npmjs.com/package/agent-browser)（Node.js CLI 浏览器自动化工具）：

```bash
npm install -g agent-browser
# 或项目级安装
npm install agent-browser
```

验证安装：
```bash
npx agent-browser --version
```

## 执行步骤

### 第一步：用 agent-browser 打开目标 URL

```bash
npx agent-browser open "<豆包对话URL>"
```

### 第二步：执行 JS 提取全文

在豆包页面内执行以下 JS，通过 `getComputedStyle` 遍历所有元素，找到真正的滚动容器，然后一次性提取 `innerText`：

```bash
npx agent-browser eval --json "(() => { const c = [...document.querySelectorAll('div')].find(el => { const s = getComputedStyle(el); return (s.overflowY==='auto'||s.overflowY==='scroll') && el.scrollHeight > el.clientHeight; }); return c ? c.innerText : 'NOT_FOUND'; })();" > /tmp/doubao_raw.json
```

**关键点**：`--json` 参数返回标准 `{"success":true,"data":{"origin":"...","result":"文本"}}` 格式，避免解析转义字符的问题。

### 第三步：解析并保存

使用内置脚本解析 JSON 并写入文件：

```bash
python3 scripts/parse_doubao.py --input /tmp/doubao_raw.json --output ./豆包对话全文.txt
```

## 已知限制与注意事项

1. **需要浏览器已打开豆包页面**：每次读取新对话前，需先 `agent-browser open <url>`。
2. **非登录用户**：可能看到"开始试用豆包"弹窗，读取内容通常不受影响。
3. **内容提取时机**：等待页面完全加载后再执行 JS，尤其是长对话帖子。
4. **多页对话**：某些帖子可能有翻页，滚动到底部后再执行 JS 提取。
5. **若 `eval --json` 返回 `NOT_FOUND`**：说明页面未完全加载，滚动到底部后重试。

## 输出

- 文件保存路径：`/Users/zen/WorkBuddy/Claw/中登日记自动化项目/豆包对话全文.txt`
- 字数通常在 5 万～15 万字之间（取决于对话长度）
- 建议：提取完成后，对照原文用 Read 工具浏览，确认关键段落位置后再进行后续分析。
