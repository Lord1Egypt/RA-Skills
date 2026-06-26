---
name: arxiv-digest
version: 1.0.1
description: "Daily AI/ML paper digest from HuggingFace Papers Trending with accessible interpretations. Fetch trending papers from arXiv, provide plain-language summaries, and support automated daily delivery. Use when: (1) asking for latest AI/ML papers or arxiv research (2) setting up paper digest notifications (3) explaining research in simple terms. Triggers on: arxiv, papers, 论文, trending, research news, 热门论文, latest papers, paper digest."
license: MIT-0
author: lifei68801
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      pypi: ["requests"]
    permissions:
      - "net:fetch:huggingface.co/papers/*"
    behavior:
      networkAccess: true
      modifiesLocalFiles: true
      description: "Fetches trending papers from HuggingFace Papers API. Stores history locally for deduplication. No authentication required. No sensitive data transmission."
initQuestions:
  - id: digest_time
    question: "What time should we deliver the daily digest? (Beijing time)"
    type: time
    default: "12:00"
  - id: categories
    question: "Which arXiv categories to follow? (comma-separated)"
    type: text
    default: "cs.AI,cs.CL,cs.LG"
    hint: "Popular: cs.AI(AI), cs.CL(NLP), cs.LG(ML), cs.CV(Vision), cs.RO(Robotics)"
  - id: paper_limit
    question: "How many papers per digest?"
    type: number
    default: 5
    min: 1
    max: 20
  - id: language
    question: "Language for paper interpretations?"
    type: select
    default: "zh"
    options:
      - value: zh
        label: 中文
      - value: en
        label: English
---

# arXiv Paper Digest

Daily AI/ML trending papers with accessible interpretations. Never miss important research again.

## What It Does

- **Fetch trending papers** from HuggingFace Papers Trending (real-time hot papers)
- **Smart ranking** by combining trending position, upvotes, and freshness
- **Plain-language summaries** - one-sentence takeaways, key innovations, why it matters
- **Automated delivery** via cron - daily QQ/Notion push
- **Deduplication** - tracks history, no repeats

---

## Quick Start

### Check Dependencies

```bash
python3 --version && curl --version
```

### Basic Usage

```bash
# Today's top 5 trending AI papers (Chinese)
python3 scripts/fetch_papers.py --days 1 --limit 5 --lang zh

# Custom categories
python3 scripts/fetch_papers.py --category cs.AI --category cs.CV --days 7 --limit 10

# Markdown output
python3 scripts/fetch_papers.py --days 1 --limit 5 --output markdown
```

### In OpenClaw Agent

Just say:
> "今天有什么热门 AI 论文"

The agent will automatically:
1. Fetch trending papers from HuggingFace
2. Rank by combined score
3. Generate accessible summaries

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `python3 scripts/fetch_papers.py --days 1 --limit 5` | Today's top 5 papers |
| `--category cs.AI --category cs.CL` | Custom categories |
| `--days 7` | Last 7 days |
| `--lang zh` | Chinese summaries (default) |
| `--lang en` | English summaries |
| `--output json` | JSON format |
| `--output markdown` | Markdown format |

---

## How It Works

### Ranking Algorithm

Papers sorted by **combined score**:

| Score Type | Range | Description |
|------------|-------|-------------|
| Position | 0-100 | Higher trending rank = higher score |
| Upvote | 0-50 | More community votes = higher score |
| Freshness | 0-30 | Newer papers get bonus |

This ensures **both latest and hottest** papers surface.

### Processing Pipeline

```
HuggingFace Papers API
         ↓
    Fetch Trending
         ↓
    Score & Rank
         ↓
    Deduplication (history file)
         ↓
    Generate Summaries
         ↓
    Output (JSON/Markdown)
```

---

## Interpretation Template

Each paper includes:

```markdown
### 📄 {Title}

**One-sentence summary**: {Core contribution, <20 words}

**Key innovations**:
1. {Technical breakthrough}
2. {Method improvement}

**Plain-language explanation**:
{200-300 words in everyday language}

**Why it matters**:
{50-100 words on practical significance}

---
```

---

## Cron Integration

Daily automated digest:

```json
{
  "name": "arxiv-daily",
  "schedule": { "kind": "cron", "expr": "0 12 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Use arxiv-digest skill. Fetch 5 papers, language zh. Push to QQ.",
    "deliver": true,
    "channel": "qqbot",
    "to": "YOUR_QQ_ID"
  }
}
```

---

## arXiv Categories

| Code | Field |
|------|-------|
| cs.AI | Artificial Intelligence |
| cs.CL | Natural Language Processing |
| cs.LG | Machine Learning |
| cs.CV | Computer Vision |
| cs.RO | Robotics |
| cs.NE | Neural Computing |
| stat.ML | Statistical ML |

Full list: https://arxiv.org/category_taxonomy

---

## File Structure

```
~/.openclaw/workspace/skills/arxiv-digest/
├── SKILL.md                    # This file
├── scripts/
│   └── fetch_papers.py         # Main fetch script
├── references/
│   └── digest-guide.md         # Interpretation patterns
└── memory/history/
    └── papers-trending-history.md  # Deduplication history
```

---

## Troubleshooting

### "No papers returned"

- HuggingFace API may be slow - retry in a few seconds
- Check network connectivity

### "Python module not found"

```bash
pip install requests
```

### "History file not found"

First run creates it automatically at `memory/history/papers-trending-history.md`

---

## Changelog

### v1.0.1 (2026-03-12)
- Security: Use requests library (preferred) to reduce false positives
- Security: Simplify User-Agent header
- Dependency: Added requests to pypi requirements
- Fallback: Still supports urllib if requests not installed

### v1.0.0 (2026-03-12)
- Initial release
- HuggingFace Papers Trending integration
- Combined score ranking (position + upvote + freshness)
- Chinese/English output support
- Deduplication history tracking

---

*Stay on top of AI research. Read less, learn more.*
