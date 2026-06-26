# Artidrop Skill for OpenClaw

Publish AI-generated content to shareable URLs from any OpenClaw conversation.

## What It Does

When a user asks OpenClaw to publish, share, or host generated content, this skill instructs the agent to use the [Artidrop CLI](https://www.npmjs.com/package/artidrop) to publish it as a live web page and return the URL.

Supported formats: HTML, Markdown, and multi-file sites (directories or ZIP archives).

## Prerequisites

1. **Node.js** — already included in OpenClaw
2. **Artidrop API key** — sign in at [artidrop.ai](https://artidrop.ai), go to Settings > API Keys, and create one

## Installation

### From ClawHub

```bash
clawhub install artidrop
```

### Manual

Copy the `artidrop/` folder into one of:

- `<your-workspace>/skills/` — project-specific
- `~/.openclaw/skills/` — available to all projects

### Configuration

Add your API key to your OpenClaw environment:

```yaml
# In your openclaw config or .env
ARTIDROP_API_KEY=sk-your-api-key-here
```

## Usage

Just ask OpenClaw naturally:

- *"Generate a report on last month's sales and publish it as a web page"*
- *"Create an HTML dashboard for this data and give me a shareable link"*
- *"Publish these meeting notes as a Markdown page"*

OpenClaw will generate the content, pipe it through the Artidrop CLI, and return the URL.

## Publishing This Skill to ClawHub

```bash
clawhub publish ./skills/artidrop \
  --slug artidrop \
  --name "Artidrop" \
  --version 1.0.0 \
  --tags latest
```
