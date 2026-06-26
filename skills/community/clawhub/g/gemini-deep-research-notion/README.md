# Gemini Deep Research Skill for OpenClaw

An OpenClaw skill that triggers **Google Gemini Deep Research** via browser automation, extracts the full research report, and exports it to **Notion**.

## Features

- 🔬 Triggers Gemini Deep Research via OpenClaw's managed browser
- ⏳ Automatically waits for research completion (~20 min)
- 📄 Extracts the full report text
- 📝 Exports to Notion with proper formatting (headings, lists, paragraphs)
- 🤖 Runs as a subagent — non-blocking for main session

## Requirements

- **OpenClaw** with browser support (`profile="openclaw"`)
- **Gemini** account logged in via the OpenClaw browser profile
- **Notion API key** stored at `~/.config/notion/api_key`
- A **Notion parent page** to export reports to

## Installation

```bash
# Via ClawHub
clawhub install gemini-deep-research

# Or manually
git clone https://github.com/PalmPalm7/openclaw-gemini-deep-research.git ~/.openclaw/skills/gemini-deep-research
```

## Configuration

Before using, update the Notion parent page ID in `SKILL.md` to your own:

```
Parent page ID: 31a4cfb5-c92b-809f-9d8a-dd451718a017
```

Replace with your Notion page ID where research reports should be created.

## Usage

Just tell your OpenClaw agent:

> "Use Gemini deep research to research [topic]"

The skill will:
1. Open Gemini in the browser
2. Submit the query with Deep Research mode
3. Wait for completion
4. Extract the full report
5. Create a formatted Notion page
6. Report back with key findings and Notion link

## License

MIT
