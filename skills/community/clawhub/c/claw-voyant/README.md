# ClawVoyant 🕶️

**ClawVoyant** is a YouTube search and transcript extraction engine. While it functions as a standalone library, it's primarily designed to empower OpenClaw agents with the ability to "see" and "hear" YouTube content.

## 🚀 ClawHub Quick Install

To add this capability to your OpenClaw agent via ClawHub:

```bash
clawhub install clawvoyant
```

## Features
- **Stealth Discovery**: Disks anonymous YouTube video searches via DuckDuckGo—no API keys required.
- **Transcript Extraction**: Detailed, full-text transcripts pulled directly from the YouTube Transcript API.
- **OpenClaw Native**: Comes with a pre-configured MCP server and `.skill` definition for instant deployment.

## Installation

ClawVoyant is intended to be cloned and installed locally until officially released on PyPI.

```bash
git clone https://github.com/Of-Arte/clawvoyant.git
cd clawvoyant
bash install.sh
```

### Local Dev Setup
If you want to use the package in developer mode:
```bash
pip install -e .
```

### MCP Server (for Claude Desktop/Other MCP clients)
Add this to your configuration:
```json
{
  "mcpServers": {
    "clawvoyant": {
      "command": "python",
      "args": ["-m", "clawvoyant.mcp_server"]
    }
  }
}
```

## Usage
### As a Library
```python
from clawvoyant import ClawVoyant

cv = ClawVoyant()
results = cv.search("OpenClaw tutorial")
if results:
    transcript = cv.get_transcript(results[0]['url'])
    print(transcript)
```

### As an OpenClaw Skill
In your OpenClaw workspace, you can import it as a skill:
`clawhub import clawvoyant`

## License
MIT
