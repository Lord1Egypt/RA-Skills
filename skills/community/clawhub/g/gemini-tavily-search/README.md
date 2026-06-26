# gemini-tavily-search

An intelligent web search orchestration skill for AI agents.
This skill performs web search using a primary → fallback architecture:
Gemini (Google Search Grounding) → automatic fallback → Tavily
The agent always receives a unified, normalized JSON response, regardless of which provider handled the request.

## System Requirements

This skill executes shell scripts and requires the following system dependencies:

### Required CLI Tools

- **bash**
- **curl**
- **jq**

These tools must be available in your system PATH.

### Verify Installation

Run the following commands:

```bash
jq --version
curl --version
```

If both commands return a version number, the dependencies are correctly installed.

If a command is not found, install the missing tool before using this skill.

### Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install curl jq -y
```

### macOS (Homebrew)

```bash
brew install curl jq
```

### Windows

Recommended options:

- Use **WSL (Windows Subsystem for Linux)** and install via apt
- Or use **Git Bash** and ensure `jq` and `curl` are installed

For WSL:

```bash
sudo apt update
sudo apt install curl jq -y
```

## Architecture

User  
→ Agent  
→ gemini_tavily_search.sh  
  ├── Gemini (primary, with optional google_search tool)  
  └── Tavily (automatic fallback on any failure)  
  ↓  
Agent receives unified JSON  
↓  
User

## Core Behavior

- Gemini is always attempted first.
- Gemini decides whether web search is required.
- If web search is required, Gemini uses `google_search` grounding.
- Any failure condition (timeout, quota error, HTTP error, invalid JSON, API error object, etc.) triggers automatic Tavily fallback.
- Output format is consistent across providers.
- The agent does not need to know about fallback logic.

## When To Use

Use this skill when:

- Information is current or time-sensitive
- The user asks about news or recent events
- Real-time data is required
- Fact verification from authoritative sources is needed
- External knowledge beyond model training is required

## When NOT To Use

Do not use this skill when:

- The question is stable general knowledge
- Historical facts that do not change
- Conceptual explanations
- Code or local file operations
- Documentation already known
- Another more specific skill applies

## Installation

From the root repository:

```bash
npx skills add JoseArroyave/agent-skills --skill gemini-tavily-search
```

## Usage (CLI)

```bash
./scripts/gemini_tavily_search.sh '{"query":"Who won the euro 2024?"}'
```

## Input

The script expects a single JSON argument.

### Required

- `query` (string)

### Optional (forwarded to Tavily on fallback)

- `search_depth`
- `topic`
- `max_results`
- `time_range`
- `start_date`
- `end_date`
- `include_domains`
- `exclude_domains`
- `country`
- etc.

## Environment Variables

### Required for Gemini

- `GEMINI_API_KEY`
- `TAVILY_API_KEY`

### Optional

- `GEMINI_MODEL` (default: `gemini-2.5-flash-lite`)

Example configuration:

```json
{
  "env": {
    "GEMINI_MODEL": "gemini-2.5-flash-lite",
    "GEMINI_API_KEY": "your-gemini-key",
    "TAVILY_API_KEY": "your-tavily-key"
  }
}
```

## Output Format (Unified)

The script always returns structured JSON in the following format:

```json
{
  "provider": "gemini",
  "answer": "Main textual answer",
  "results": [
    {
      "title": "Source title",
      "url": "https://example.com",
      "snippet": "Relevant excerpt"
    }
  ],
  "used_web": true | false,
  "fallback": false
}
```

If Gemini answers without using web search:

```json
{
  "answer": "Main textual answer",
  "provider": "gemini",
  "fallback": false,
  "used_web": false,
  "results": []
}
```

If fallback occurs:

```json
{
  "provider": "tavily",
  "results": [...],
  "fallback": true,
  "used_web": true,
  "answer": null
}
```

If both providers fail:

```json
{
  "error": "tavily_failed",
  "provider": "tavily",
  "used_web": true,
  "fallback": true,
  "answer": null,
  "results": []
}
```

## Design Goals

- Deterministic fallback behavior
- Provider abstraction
- Stable JSON schema
- Agent-friendly integration
- Zero provider error leakage
- Minimal agent complexity

## Credits

This implementation is based on the structure and approach of the Tavily skills repository:

[https://github.com/tavily-ai/skills](https://github.com/tavily-ai/skills)

Core Tavily integration logic is derived from that repository, with additional routing logic added to introduce:

- Gemini-first classification
- Conditional Google Search Grounding
- Automatic provider failover
- Unified output normalization

This skill is self-contained and does not require the official Tavily skill to be installed separately.
