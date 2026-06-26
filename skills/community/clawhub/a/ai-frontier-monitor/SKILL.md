---
name: ai-frontier-monitor
description: "AI frontier intelligence briefing — aggregate, score, and deliver structured daily briefings from 5 tracks (RSS enterprise, 36kr hotlist, arXiv papers, GitHub Trending, Anthropic web search). Use when user mentions: AI前沿, 情报汇总, 每日情报, 行业动态, AI动态, 技术趋势, 行业信号, 今天有什么信号, AI动态汇总, frontier monitor, daily briefing AI, signal check, AI news, tech briefing."
---

# AI 前沿情报汇总

> 信息聚合 ≠ 信息堆砌。每日情报经筛选、评分、分层后输出，不做 50 条标题的噪音。

## When to Use

触发词（任意语言）：
- "AI 前沿" / "情报汇总" / "每日情报" / "frontier monitor" / "daily briefing" → 全量简报
- "今天有什么信号" / "signal check" / "快速扫描" / "what signals today" → 快速信号检测
- "arXiv 最新" / "论文追踪" / "paper tracker" / "latest papers" → 仅 arXiv 轨道
- "GitHub Trending" / "AI 热榜" / "trending AI" → 仅 GitHub 轨道

## Architecture: 5-Track Parallel

| Track | Source | Script | Priority |
|-------|--------|--------|----------|
| 🏢 Enterprise | 11 RSS feeds (OpenAI/AWS/Techmeme/...) | `{baseDir}/scripts/rss-crawler.py` then `{baseDir}/scripts/generate-briefing.py --candidates <path>` | ⭐⭐⭐⭐⭐ |
| 🇨🇳 China | 36kr Hotlist API | `curl https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json` | ⭐⭐⭐⭐ |
| 📚 Papers | arXiv cs.AI/cs.LG/cs.CL | `{baseDir}/scripts/arxiv-fetch.sh --category cs.AI --days 7 --max 10` | ⭐⭐⭐ |
| 🔥 GitHub | GitHub Trending (AI/ML) | `{baseDir}/scripts/github-trending-fetch.sh --period daily` | ⭐⭐⭐ |
| 🔍 Anthropic | Web search supplement | `web_search` tool | ⭐⭐⭐⭐⭐ |

> For full data source details, read `{baseDir}/references/data-sources.md`

## Workflow

### Step 1: Fetch All Tracks

```bash
# Track 1: RSS (run crawler first, outputs to {baseDir}/data/candidates/)
python3 {baseDir}/scripts/rss-crawler.py

# Track 2-4: Generate briefing (all tracks auto-fetched)
python3 {baseDir}/scripts/generate-briefing.py --mode full
```

Modes: `full` | `quick` | `arxiv` | `github`

### Step 2: Auto-Score & Tier

Each candidate without a score is auto-scored (0-5) by keyword matching across 4 dimensions:

| Dimension | Weight | What to look for |
|-----------|--------|-----------------|
| Enterprise landing | 40% | Real company name, deployment scale |
| Data support | 20% | Quantified metrics (% improvement, $ saved) |
| Learnability | 20% | Methodology, architecture, lessons learned |
| Novelty | 20% | New scene, new product, not old news |

Source bonus: OpenAI/AWS +1.0, Techmeme +0.5, PH/HN +0.3

Tiers are **dynamic** (based on actual score distribution, not hardcoded thresholds):
- 🔴 Core: top ~15% or ≥3.5 (max 3)
- 🟡 Worth watching: top ~30% or ≥2.5 (max 5)
- 🟢 Quick scan: ≥1.0 (max 8, 36kr first)

> For scoring keywords and signal detection rules, read `{baseDir}/references/scoring.md`

### Step 3: Detect Signals

Extract cross-track signals into 3 dimensions:
- 🛠 **Tech trends** — new models, architectures, frameworks, benchmarks
- 🏢 **Product launches** — new releases, open-source, GA announcements
- 💰 **Funding/M&A** — investments, acquisitions, IPOs

### Step 4: Render Briefing

Strict format — emoji headers, tiered sections, signal summary. Output in **Chinese** (中文为主). Total ≤ 16 items across all tiers.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI 前沿情报 · {Day} {Date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 数据源：11 RSS + 36kr + arXiv + GitHub + Anthropic
   候选：{N} 条 | 高质量：{M} 条 | 阈值：核心≥{X} / 关注≥{Y}

## 🔴 核心情报（{N} 条）
### 1. {Title}
🔗 {Link}
💡 启示：{One-line insight}

## 🟡 值得关注（{N} 条）
1. **{Title}**
   🔗 {Link}

## 🟢 快速浏览（{N} 条）
• [{Title}]({Link})

## 📚 arXiv · 论文追踪（≤3 篇）
**{Title}** — {Authors} | {Date}
摘要：{Abstract[:150]}... → {Link}

## 🔥 GitHub Trending · AI（≤3 个）
**{Repo}** ({Lang}) +{TodayStars}⭐ → {Link}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 今日信号
🛠 技术趋势：{signal}
🏢 产品发布：{signal}
💰 资本动向：{signal}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ {HH:MM} | ai-frontier-monitor v3.0
```

### Step 5: Deliver & Archive

1. **Reply in conversation** — 直接在当前对话输出简报
2. **Push to Feishu** — 通过 `message` 工具发送到飞书（channel: feishu, to: user ID）
3. **Save to file** — 将完整简报保存为 Markdown 文件到：
   ```
   {baseDir}/data/briefings/{YYYY-MM-DD}-frontier-briefing.md
   ```
   保存时覆盖当日内容。

## Data Directory

All runtime data is stored under `{baseDir}/data/`:

```
{baseDir}/data/
├── candidates/          # RSS 爬取的候选条目 (JSON)
│   └── *_candidates.json
├── briefings/           # 生成的简报 (Markdown)
│   └── YYYY-MM-DD-frontier-briefing.md
└── rss-state.json       # RSS 爬取状态
```

> `{baseDir}` is the skill root directory containing this SKILL.md. All paths use `{baseDir}` for portability.

## Edge Cases

| Situation | Action |
|-----------|--------|
| No candidates (RSS empty) | Run with 36kr + arXiv + GitHub only, skip RSS section |
| arXiv API timeout (>30s) | Skip paper section, log warning |
| GitHub fetch fails | Skip trending section, log warning |
| 36kr API 404 (no data yet) | Skip 36kr items in quick scan |
| Zero high quality items (<2 at ≥2.5) | Return `NO_REPLY` instead of empty briefing |
| Same company appears in multiple sources | Deduplicate, keep highest-scored entry |
| First run (no data dir) | Auto-create `{baseDir}/data/` and subdirectories |

## Skill Integration

| Skill | Role |
|-------|------|
| **wechat-curator** | WeChat articles → 🟢 Quick scan supplement |
| **zsxq-helper** | Zsxq content → independent push (not in main briefing) |
| **rss-crawler.py** | RSS fetching engine (11 sources) — now included in `{baseDir}/scripts/` |

## Configuration

Edit `{baseDir}/references/BRIEFING_CONFIG.md` to customize:
- Quantity limits per tier
- Data source on/off switches
- Signal detection thresholds
- Delivery target (Feishu user ID / Discord channel / etc.)

## Quality Gates

- Max 16 items per day (3+5+5+3 papers)
- `NO_REPLY` when <2 quality candidates
- Deduplicate same company/product, keep highest score
- 3 consecutive days below 3 core items → trigger keyword review

## Dependencies

- **Python 3.8+** with `feedparser` (for RSS crawling)
- **bash** (for arXiv/GitHub fetch scripts)
- **curl** (for 36kr API)
- **web_search** tool (for Anthropic track)

---

_Last updated: 2026-05-09 | v3.0_
