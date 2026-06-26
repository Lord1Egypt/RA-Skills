# 🔍 Free Keyword Miner for OpenClaw

**Zero-cost keyword research** — Google PAA, Autocomplete, Reddit & Bing. No Ahrefs/SEMrush needed.

## ✨ Features

- 📰 **Google People Also Ask** — Scrape real user questions
- 🔤 **Google Autocomplete** — Long-tail keyword suggestions
- 💬 **Reddit Mining** — Extract pain points and discussions
- 🔎 **Bing Related Searches** — Alternative keyword sources
- 📊 **Auto Clustering** — Group keywords by topic
- 💡 **Topic Generation** — Ready-to-use content ideas

## 🚀 Quick Start

```bash
# Install dependencies
pip install people-also-ask beautifulsoup4 requests

# Run keyword research
python3 keyword_miner.py --seed "your keyword" --sources all --output results.json
```

## 📋 Output

```json
{
  "seed_keyword": "adult products for couples",
  "google_paa": ["question1", "question2"],
  "autocomplete": ["suggestion1", "suggestion2"],
  "reddit_topics": [{"title": "...", "score": 100}],
  "clusters": [{"name": "cluster1", "keywords": [...]}],
  "topic_ideas": ["How to...", "Best ..."]
}
```

## 🎯 Use Cases

- SEO keyword research (free alternative to paid tools)
- Content strategy planning
- User pain point discovery
- Competitor content gap analysis
- Blog topic generation

## 🛠️ Installation for OpenClaw

```bash
npx clawhub@latest install free-keyword-miner
```

*Coming soon to ClawHub — currently requires GitHub account age > 14 days*

## 📄 License

MIT
