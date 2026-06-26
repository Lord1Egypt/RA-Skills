---
slug: browser-automation-skills
display-name: Browser Automation Skills
version: 1.0.0
description: Browser automation skills for AI models — navigate, screenshot, interact, scrape, debug, test, and record browser sessions. Controls local Google Chrome via CDP with visual overlay locking. 浏览器自动化技能包，让 AI 模型控制本地 Chrome。
license: MIT-0
---

# Browser Automation Skills / 浏览器自动化技能包

A set of Skills that teach AI models how to control the local Google Chrome browser.
Works with any model — via built-in `browser_subagent` or the bundled Playwright CLI script.

一组教会 AI 模型控制本地 Google Chrome 的技能包。
适用于任何模型 — 通过内置 `browser_subagent` 或自带 Playwright CLI 脚本。

## Included Skills / 包含的技能

| Skill | Description / 说明 | Invocation / 调用 |
|-------|-----------|------------|
| `navigate` | Open URLs, read page content / 打开网页、读取内容 | Auto + `/navigate` |
| `screenshot` | Capture visuals / 截图截屏 | Auto + `/screenshot` |
| `interact` | Click, type, fill forms / 点击、输入、表单 | Auto + `/interact` |
| `scrape` | Extract structured data / 数据抓取 | Auto + `/scrape` |
| `debug` | Inspect network, console / 网页调试 | Auto + `/debug` |
| `test` | Automated QA / 自动化测试 | `/test` only |
| `record` | Record sessions / 录制操作 | `/record` only |
| `browser-context` | API reference / API 参考 | Model only |

## Prerequisites / 前提条件

- **Google Chrome** installed locally / 本地安装 Chrome
- For Playwright CLI: `pip install playwright`
- Start Chrome: `chrome.exe --remote-debugging-port=9222`

## Quick Start / 快速开始

```bash
python scripts/browser.py status
python scripts/browser.py navigate https://example.com
python scripts/browser.py screenshot
python scripts/browser.py lock      # Visual overlay, block user input
python scripts/browser.py unlock    # Remove overlay, restore input
```

See [docs/api-reference.md](docs/api-reference.md) for full API documentation.
