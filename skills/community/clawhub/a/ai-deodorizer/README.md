# Ai-Deodorizer

> Remove signs of AI-generated writing. Make text sound natural and human.
> **Version 2.0.0**

[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue)]()

**Ai-Deodorizer** is an OpenClaw Skill that transforms AI-generated text into natural, human-like writing. Based on 25 AI writing pattern detectors + two-round rewriting strategy + Soul injection principles. Supports **both English and Chinese** content.

## Disclaimer

**Disclaimer**:
This project is 99% AI-generated. The AI's owner has no programming background. Please evaluate the project's feasibility before use.

---

## Features

- **25 AI Pattern Detectors** — covers content, language, style, communication, and filler patterns
- **Two-Round Rewriting** — pattern fix → anti-AI audit for maximum "humanness"
- **Soul Injection** — not just cleaning, adds human voice and personality
- **Chinese Language Support** — built-in Chinese AI vocabulary table (25 terms)
- **English Language Support** — built-in English AI vocabulary table (20 terms)
- **Three Strength Modes** — light / medium / strong, adjust rewriting depth
- **Zero Cost** — runs on MiniMax API, no third-party paid services
- **OpenClaw Native** — designed as an OpenClaw Skill for seamless workflow integration

## Quick Start

### Prerequisites

- Python 3.8+
- MiniMax API Key ([Get one here](https://platform.minimaxi.com/))

### Installation

```bash
# Clone the repo
git clone https://github.com/xx235300/ai-deodorizer.git
cd ai-deodorizer

# Install dependencies
pip install -r scripts/requirements.txt

# Set your API key
export MINIMAX_API_KEY="your_api_key_here"
```

### Usage

```bash
# Basic usage
python scripts/humanize.py --input "此外，该研究具有重要意义..."

# From file
python scripts/humanize.py --file ./input.txt

# With output file
python scripts/humanize.py --input "YOUR TEXT" --output ./output.txt

# Strength modes
python scripts/humanize.py --input "YOUR TEXT" --mode light   # minimal changes
python scripts/humanize.py --input "YOUR TEXT" --mode medium  # balanced (default)
python scripts/humanize.py --input "YOUR TEXT" --mode strong  # maximum humanization
```

## How It Works

### Two-Round Rewriting

**Round 1 — Pattern Fix**
Detects and fixes 25 common AI writing patterns including:
- Significance inflation, promotional language, vague attributions
- AI vocabulary (此外 → 还有, 由此可见 → 所以)
- Rule of three abuse, em dash overuse, filler phrases

**Round 2 — Anti-AI Audit**
Asks: "What still looks AI?" and fixes remaining tells.

Adds **Soul** — real opinions, varied rhythm, first-person voice, acknowledgment of complexity.

## 25 AI Writing Patterns

| Category | Patterns |
|----------|----------|
| Content | Significance inflation, notability name-dropping, superficial -ing analyses, promotional language, vague attributions, formulaic challenges |
| Language | AI vocabulary, copula avoidance, negative parallelisms, rule of three abuse, synonym cycling, false ranges |
| Style | Em dash overuse, boldface overuse, inline-header lists, title case headings, emoji abuse, curly quotes |
| Communication | Chatbot artifacts, cutoff disclaimers, sycophantic tone |
| Filler & Hedging | Filler phrases, over-hedging, generic positive conclusions, zombie templates |

**English AI Patterns** — See [METHODOLOGY.md](METHODOLOGY.md) Section 8 for English-specific vocabulary and sentence patterns.

## Examples

### Example 1: Business Writing

**AI-generated (before):**
> 此举标志着公司在数字化转型道路上迈出了关键一步。此外，该战略将为其在竞争激烈的市场中奠定坚实基础，具有重要的战略意义。

**After humanizing:**
> 这个决定是公司推出自有技术品牌的开始。之前犹豫了很久，主要担心资源分散。现在看，团队已经准备好了。

### Example 2: Academic Writing

**AI-generated (before):**
> 本研究深入探讨了机器学习在医疗诊断中的应用。研究表明，该技术具有重要的临床价值，值得广泛关注。

**After humanizing:**
> 我们分析了2019-2023年间50家医院的影像数据，发现AI辅助读片的漏诊率降低了约15%。这个效果比我预期的要好。但样本主要是三甲医院，基层医院的效果还需要验证。

## Documentation

- [SKILL.md](SKILL.md) — OpenClaw Skill definition
- [METHODOLOGY.md](METHODOLOGY.md) — Complete methodology (25 patterns, prompts, Chinese AI vocabulary)
- [EXAMPLES.md](EXAMPLES.md) — Before/after examples for each pattern category

## OpenClaw Skill Installation

Copy the `skills/ai-deodorizer/` directory to your OpenClaw skills folder:

```bash
cp -r skills/ai-deodorizer ~/.openclaw/skills/
```

## Contributing

Issues and pull requests welcome. If you find additional AI writing patterns or have better humanization strategies, please share.

## Changelog

### v2.0.0 (2026-03-30)

- Added English AI writing patterns table (Section 8 in METHODOLOGY.md)
- SKILL.md now embeds full two-round rewriting prompts
- Strength Modes documentation improved (light / medium / strong)
- SKILL.md frontmatter added `version: 2.0.0`

### v1.0.0 (2026-03-27)

- Initial release
- 25 AI writing pattern detectors
- Two-round rewriting strategy
- Chinese language support
- Python CLI tool

## License

MIT License — see [LICENSE](LICENSE) for details.
