# cgartlab-search

A **harness-agnostic** unified search skill. One entry point routes a query to the best
backend(s) and returns normalized, source-attributed results that the model turns into a
cited summary. Works in any agent harness that can make HTTP calls (DSH, Claude Code,
Codex, opencode, ...), including restricted-egress environments via web_fetch.

## Backends

| Backend | Best for | Transport | Key |
|---|---|---|---|
| bing (cn.bing.com RSS) | general web, facts, query news | curl + web_fetch | none |
| context7 | library/framework/API docs | curl + web_fetch | none |
| qqnews (腾讯新闻热榜) | latest/hot Chinese news | curl + web_fetch | none |
| hupu (虎扑足球) | 足球/体育 news | curl + web_fetch | none |
| so (Stack Overflow) | dev Q&A / error fixes | curl + web_fetch | none |
| github | repo/tool discovery | curl + web_fetch | none |
| hn (Algolia) | tech community signal | curl + web_fetch | none |
| brave | general web / news (quality) | curl only (header auth) | BRAVE_SEARCH_API_KEY |
| exa | deep research / semantic | curl only (POST + auth) | EXA_API_KEY |
| tencent (official CLI) | 中文新闻搜索 + 热点榜 | local `tencent-news-cli` binary | owned by the CLI (`apikey-set`) |
| zhihu (official OpenAPI) | 中文全网 / 知乎讨论 | curl + web_fetch | ZHIHU_API_KEY |

## Requirements

- **Normal harness**: a shell with `curl` (macOS/Linux/Windows 10+) — all backends.
- **DSH / restricted egress**: the harness's `web_fetch` tool — all key-less backends.
  See `references/backends.md` for the verified host-reachability map.
- **`scripts/search.mjs`**: Node 18+ (zero dependencies, uses global `fetch`).
- **`scripts/search.sh`**: a working `python3` **or** `python` — the script probes both
  (plus `$PYTHON`) and verifies real output, because on Windows `python3` can be a
  Microsoft Store alias stub that exits 0 while printing nothing.
- **`tencent` backend**: the local `tencent-news-cli` binary (see `references/backends.md`).
  Nothing else needs any install.

## Install

Copy the `cgartlab-search/` folder into your harness's skill directory:

- DSH: `~/.dsh/skills/`
- Claude Code: `~/.claude/skills/` or project `.claude/skills/`
- Others: see your harness's skill docs.

## Keys

Key-less backends need nothing. For brave/exa/tencent/zhihu set env vars
(`BRAVE_SEARCH_API_KEY`, `EXA_API_KEY`, `TENCENT_NEWS_KEY`, `ZHIHU_API_KEY`) or place a
`secrets.json` next to SKILL.md (see `secrets.example.json`). `secrets.json` is gitignored.

## Usage

Ask in natural language — "查一下 ...", "搜搜最新足球比赛新闻", "最近有什么重大新闻",
"React 的 use() 怎么用", "全面调研 ...". The skill triggers and routes automatically.
Direct invocation: `node scripts/search.mjs <backends> "<query>" --limit 5`.

Before committing, run the local gate — it is the same checks as `.github/workflows/ci.yml`,
so it works even where Actions is unavailable:
`bash scripts/gate.sh` (add `--smoke` to actually hit every backend once).

## Status (verified 2026-10-23)

- **9 of 11 backends live**: bing, context7, qqnews, hupu, so, github, hn (key-less) plus
  zhihu (official OpenAPI) and tencent (official CLI) — all smoke-tested end to end.
- **brave / exa**: wired via curl but need keys (none configured here) and are unreachable
  from DSH's GFW-like egress.
- Both entry points (`search.mjs`, `search.sh`) were verified per-backend on Windows;
  `search.sh` also needed a Python-interpreter probe and stdin-based `secrets.json`
  loading (native Python cannot read MSYS-style paths).
## 发布与版本

- 当前版本 **0.1.1**（`0.x` 表示尚未稳定：指令、文件约定与后端清单都可能变更）。
- **版本源**：`SKILL.md` frontmatter 的 `metadata.version`（唯一权威）。
- 变更记录见 `CHANGELOG.md`；发布流程与三道闸见 `docs/RELEASING.md`。
- tag 命名 `v<version>`，与 `metadata.version` 逐字一致（如 `v0.1.0`）。