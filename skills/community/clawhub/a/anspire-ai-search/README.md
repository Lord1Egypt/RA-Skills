<div align="center">

**English** | [中文](./README_CN.md)

</div>

---

# Anspire Search

> The next-generation real-time intelligent search engine built for the AI ecosystem.

An [OpenClaw](https://openclaw.ai) skill that brings [Anspire](https://aisearch.anspire.cn)'s real-time search directly into your AI agent — no browser, no scraping, one env var.

**MIT** · [![ClawHub](https://img.shields.io/badge/ClawHub-anspire--search-blue)](https://clawhub.ai/Anspire-AI/anspire-search) · [![Anspire](https://img.shields.io/badge/Powered%20by-Anspire-purple)](https://aisearch.anspire.cn)

### Why Anspire?

| Capability | Description |
|---|---|
| 🌐 Omni-channel Crawling | Parallel crawling across major search engines, encyclopedias, news, and academic sources in real time |
| 🧠 Multimodal Retrieval | Semantic parsing + cross-modal retrieval: text, images, video, news, flights, hotels |
| 🔗 Cross-domain Fusion & Cognitive Ranking | Hybrid cluster + federated learning framework for real-time indexing across encyclopedias, news, and academic resources |
| ⚡ Millisecond Knowledge Updates | Break through the information lag of traditional search systems |

### Installation

**Method 1 — ClawHub (recommended)**

```bash
clawhub install anspire-search
```

**Method 2 — Direct from GitHub**

Point OpenClaw directly at the SKILL.md in this repo:

```bash
openclaw skills add https://raw.githubusercontent.com/Anspire-AI/Anspire-search/main/SKILL.md
```

---

### Setup

**Option 1: Persistent Configuration (Recommended)**

Add the API key to your system so it loads automatically:

**macOS/Linux:**

```bash
# For zsh users (macOS default)
echo 'export ANSPIRE_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc

# For bash users
echo 'export ANSPIRE_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**

```cmd
# Set permanently (requires terminal restart)
setx ANSPIRE_API_KEY "your_key_here"

# Also set for current session (optional, for immediate use)
set ANSPIRE_API_KEY=your_key_here
```

**Option 2: Temporary Configuration (Current session only)**

```bash
# macOS/Linux
export ANSPIRE_API_KEY=your_key_here

# Windows (cmd)
set ANSPIRE_API_KEY=your_key_here

# Windows (PowerShell)
$env:ANSPIRE_API_KEY="your_key_here"
```

> ⚠️ Note: Temporary configuration will be lost when you close the terminal or open a new chat window

> Get your key at [aisearch.anspire.cn](https://aisearch.anspire.cn)

### Usage

**Option 1: Agent Mode (Automatic)**

Once installed, your OpenClaw agent automatically uses this skill when it needs live web information.

**Option 2: Direct Script Execution**

Use the provided wrapper scripts for manual searches:

```bash
# Python wrapper (recommended) - formatted output
python scripts/search.py "your search query" --top-k 10

# Python wrapper - JSON output
python scripts/search.py "your search query" --json

# Shell wrapper
./scripts/search.sh "your search query" 10
```

**Option 3: Direct API Call**

```bash
curl --silent --show-error --fail --location --get \
  "https://plugin.anspire.cn/api/ntsearch/search" \
  --data-urlencode "query=QUERY" \
  --data-urlencode "top_k=10" \
  --header "Authorization: Bearer $ANSPIRE_API_KEY" \
  --header "Accept: application/json"
```

### Output Format

```json
{
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com/page",
      "content": "Full article content...",
      "score": 0.997,
      "date": "2026-03-10T10:10:00+08:00"
    }
  ]
}
```

### When to Use

| Scenario | Example |
|---|---|
| 📰 Current events & news | "latest US tech regulations" |
| 📈 Market & industry updates | "NVIDIA stock news today" |
| 🔬 Research & fact-checking | "recent climate research 2026" |
| 🌍 Real-time facts | "current weather in Shanghai" |

### File Structure

```
anspire-search/
├── SKILL.md              # Skill documentation
├── .env.example          # Environment variable template
├── scripts/
│   ├── search.py         # Python wrapper (recommended)
│   └── search.sh         # Shell wrapper
├── README.md             # This file
└── README_CN.md          # Chinese README
```

### Requirements

| Requirement | Details |
|---|---|
| `ANSPIRE_API_KEY` | Required — get at [aisearch.anspire.cn](https://aisearch.anspire.cn) |
| `curl` | Required — pre-installed on macOS/Linux, available on Windows 10+ |
| `python3` | Optional — for using the Python wrapper script |

### License

MIT © [Anspire-AI](https://github.com/Anspire-AI) · [aisearch.anspire.cn](https://aisearch.anspire.cn)
