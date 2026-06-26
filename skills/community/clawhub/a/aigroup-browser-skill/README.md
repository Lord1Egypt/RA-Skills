# aigroup-browser-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-0ea5e9.svg)](./SKILL.md)
[![Browser Routing](https://img.shields.io/badge/Routing-CN%20%7C%20Global-10b981.svg)](./README.md)

> OpenClaw skill for driving the real browser on `spark`, with explicit mainland-China and international routing.

## Overview

`aigroup-browser-skill` is a focused OpenClaw skill for one job: when a user says "open this site in the browser", OpenClaw should use the live browser profiles on the host instead of substituting `web_fetch`, `search`, `canvas`, or `nodes`.

It is designed for deployments that need:
- separate CN and global browser profiles
- stable browser-based access to sites that do not behave well with pure HTTP fetches
- a structured JSON result containing the real page title and final URL
- simple agent routing for country-specific browsing behavior

## Highlights

- **Real browser open** instead of synthetic fetch-based substitutes
- **Dual-profile routing** for mainland Chinese and international destinations
- **Three modes**: `cn`, `global`, and `auto`
- **CDP-backed verification** so the result comes from the live browser session
- **Agent-friendly output** that is easy to summarize or chain into later steps

## Host assumptions

This skill expects the target host to already provide:
- `oc-cn`
- `oc-global`
- `oc-browser`
- CDP port `18810` for the CN profile
- CDP port `18800` for the global profile

## Quick Start

### Requirements

- Python 3
- `oc-cn`
- `oc-global`
- `oc-browser`

### Run directly

```bash
python3 scripts/open_page.py '{"url":"https://www.eastmoney.com/","mode":"cn"}'
python3 scripts/open_page.py '{"url":"https://huggingface.co/","mode":"global"}'
python3 scripts/open_page.py '{"url":"https://www.baidu.com/","mode":"auto"}'
```

## Recommended routing

- `mode=cn` for sites such as `eastmoney.com`, `baidu.com`, `bilibili.com`
- `mode=global` for sites such as `huggingface.co`, `github.com`, `openai.com`
- `mode=auto` only when the destination is ambiguous or you want hostname-based fallback routing

## Example outputs

### CN example

```json
{
  "ok": true,
  "mode": "cn",
  "port": 18810,
  "title": "东方财富网：财经门户，提供专业的财经、股票、行情、证券、基金、理财、银行、保险、信托、期货、黄金、股吧、博客等各类财经资讯及数据",
  "url": "https://www.eastmoney.com/"
}
```

### Global example

```json
{
  "ok": true,
  "mode": "global",
  "port": 18800,
  "title": "Hugging Face – The AI community building the future.",
  "url": "https://huggingface.co/"
}
```

## Why this exists

Many real-world sites do not behave well when handled through a plain fetch path alone. This skill gives OpenClaw a predictable browser-first path for browsing tasks where locality, profile state, region routing, or anti-bot behavior matter.

## Repository contents

```text
aigroup-browser-skill/
├── SKILL.md
├── README.md
├── LICENSE
└── scripts/
    └── open_page.py
```

## Development notes

The production deployment on `spark` now also uses the corrected slug `aigroup-browser-skill`, so the runtime name and the public repository name are aligned.

## License

MIT. See [LICENSE](./LICENSE).
