# Deep Research Skill for Claude Code

[English](README.md) | [中文](README_zh.md)

> If you find this project helpful, please give it a star! :star:

![Architecture](architecture.png)

Automatic deep research skill for Claude Code and AI agents. Multi-round search with multi-source verification, outputs structured reports.

## Use Cases

- **Concept Research**: Understanding tech principles, learning new concepts
- **Tool Comparison**: Evaluation, competitor analysis
- **Trend Tracking**: Industry dynamics, event analysis
- **Deep Investigation**: Topic research, information gathering

## Installation

```bash
git clone https://github.com/Pancat009/auto-deep-research-skill
cd auto-deep-research-skill
cp env.example .env
```

Configure API Key (at least one):
- Tavily: https://tavily.com
- Jina Reader: https://jina.ai/reader

## Usage

```bash
# Make scripts executable
chmod +x scripts/*.sh
```

Trigger command:
```
/auto-deep-research your research question
```

## Output Files

Each research creates `output/{topic-slug}/`:
- `state.json` - Execution state (iteration, subproblem progress)
- `memo.json` - Structured research notes
- `sources.json` - Source list
- `report.md` - Final report

## File Structure

```
auto-deep-research-skill/
├── SKILL.md              # Skill definition
├── README.md             # Chinese
├── README_en.md          # English
├── env.example           # Env variable example
├── scripts/
│   ├── search.sh         # Search script
│   └── read_page.sh      # Page reading script
├── references/
│   ├── conflict-detection.md
│   └── source-trust.md
└── evals/
    └── evals.json
```

## Version

v0.0.1 - Initial release