# AITuber Skill for AI Agents

Add AI video creation capabilities to Claude Code, Cursor, OpenClaw, Codex, and other AI coding agents. This skill teaches your AI agent how to create fully produced videos with AI narration, visuals, and synced captions for YouTube Shorts, TikTok, Instagram Reels, and long-form content.

[AITuber](https://aituber.app) | [API Documentation](https://aituber.app/api) | [MCP Server](https://github.com/aituberapp/aituber-mcp) | [Get API Key](https://app.aituber.app/dashboard/api-keys)

## What your agent learns

When you install this skill, your AI agent gains knowledge of the full AITuber video creation pipeline:

- **Pick a voice** from 1,300+ AI voices (filter by gender, accent, age, language)
- **Generate videos** from a script or idea with AI narration, visuals, and captions
- **Choose visual styles** from 27+ options (photorealistic, anime, cinematic, 3D Pixar, and more)
- **Use templates** like skeleton (X-ray viral format) and character-driven stories
- **Export to MP4** and get a download URL
- **Check credits** and subscription status
- **Support any format** including YouTube Shorts (9:16), standard YouTube (16:9), and square (1:1)

## Install

**Claude Code:**

```bash
npx skills add aituberapp/ai-video-skill
```

**Cursor:**

Copy the `SKILL.md` file to your project's `.cursor/skills/` directory.

**OpenClaw:**

Add this repository to your OpenClaw agent configuration:

```
aituberapp/ai-video-skill
```

**Manual install (any agent):**

Download `SKILL.md` and place it where your AI agent reads skill files.

## How it works

1. **Install the skill** using the command above
2. **Get an API key** from [app.aituber.app/dashboard/api-keys](https://app.aituber.app/dashboard/api-keys)
3. **Ask your agent** to create a video, and it knows exactly which API endpoints to call, what parameters to use, and how to handle the full workflow

### Example prompts

> "Create a 60-second YouTube Short about 5 mind-blowing facts about the ocean"

> "Make a skeleton-style video about what happens if you eat 100 bananas"

> "Find me a calm British female voice and create a meditation video"

> "Generate a faceless narration video about the history of coffee with cinematic visuals"

## Skills vs MCP Server

| | Skill | MCP Server |
|---|---|---|
| **What it provides** | Knowledge and instructions | Typed tools the AI calls directly |
| **How it works** | Agent reads SKILL.md and makes API calls | Agent calls MCP tools which proxy to the API |
| **Best for** | Coding agents that support skills | Any MCP-compatible client |
| **Install** | `npx skills add aituberapp/ai-video-skill` | `npx -y @aituber/mcp-server` |

For the best experience, use both together. The skill provides context and the MCP server provides execution.

- **MCP Server**: [github.com/aituberapp/aituber-mcp](https://github.com/aituberapp/aituber-mcp) | [npm](https://www.npmjs.com/package/@aituber/mcp-server)

## API Endpoints

The skill covers all 7 AITuber API endpoints:

| Endpoint | Description |
|----------|-------------|
| `GET /voices` | Browse 1,300+ AI voices with filters (public, no auth needed) |
| `POST /videos/generate` | Create a video from a script or idea |
| `GET /videos` | List all your videos |
| `GET /videos/{id}` | Get video details and generation status |
| `GET /subscription` | Check your plan, credits, and billing info |
| `POST /exports` | Start rendering a video to MP4 |
| `GET /exports/download` | Get a temporary download URL for the MP4 |

## Supported video types

| Type | Description |
|------|-------------|
| **Faceless narration (images)** | AI images with Ken Burns animation, narration, and captions |
| **Faceless narration (video clips)** | AI-generated video clips instead of images |
| **Stock footage** | Real stock footage matched to narration |
| **Skeleton template** | Viral "what happens if..." X-ray style |
| **Character template** | Character-driven story format |

## Links

- [AITuber](https://aituber.app) - AI video creation tool
- [API Documentation](https://aituber.app/api) - Interactive API reference
- [MCP Server](https://github.com/aituberapp/aituber-mcp) - MCP server for Claude, Cursor, OpenClaw
- [Dashboard](https://app.aituber.app/dashboard) - Manage videos and billing
- [API Keys](https://app.aituber.app/dashboard/api-keys) - Create and manage your API keys

## License

MIT
