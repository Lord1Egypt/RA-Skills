# Flova Video Generator -- OpenClaw Skill

**English** | [中文](README.zh-CN.md) | [日本語](README.ja.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill Version](https://img.shields.io/badge/skill_version-0.2.9-green.svg)](SKILL.md)
[![ClawHub](https://img.shields.io/badge/ClawHub-marketplace-brightgreen.svg)](https://clawhub.ai/flova/flova-video-generator)
[![Flova](https://img.shields.io/badge/Flova-video_platform-00bcd4.svg)](https://www.flova.ai)

An [OpenClaw](https://openclaw.ai) skill that teaches AI agents to create, edit, and export videos through [Flova](https://www.flova.ai) -- the world's first all-in-one AI video creation platform that integrates ideation, storyboarding, filming, and editing to bring your creativity to life.

> *Everyone is their own creative director -- effortlessly craft brilliant stories.*

**Compatible with:** OpenClaw | Claude Code | Codex | Cursor | Windsurf | Cline | and more

## About

This is an [OpenClaw](https://openclaw.ai) skill -- a markdown-based instruction file that gives AI agents the ability to call the Flova API. After loading the skill, your AI assistant can create video projects, send creative instructions, handle file uploads, export finished videos, and manage subscriptions -- all through natural conversation. Works with any AI coding assistant that supports tool use or URL fetching.

## Installation

### Via ClawHub (Recommended)

Search for **flova** on [ClawHub](https://clawhub.ai/flova/flova-video-generator) and click install, or use the CLI:

```bash
openclaw skills install flova-video-generator
```

### Chat with Your AI Assistant

Send this message directly to your AI assistant:

> Learn https://s.flova.ai/SKILL.md and follow the Skill instructions to create a video.

## Quick Start

1. **Get an API Token:** Visit [flova.ai/openclaw](https://www.flova.ai/openclaw/?action=token)
2. **Set the environment variable:**
   ```bash
   export FLOVA_API_TOKEN="your_token_here"
   ```
   Or simply send your token to your AI assistant and it will help you configure it.
3. **Start creating:** Just tell your AI assistant what video you want!

## Features

- **Natural language video creation** -- describe what you want, get a video
- **File uploads** -- attach images, videos, audio, and documents
- **Export & download** -- export finished videos and download project assets
- **Project management** -- list, resume, and switch between video projects
- **Subscriptions & credits** -- check status, subscribe to plans, buy credits

## Workflow Overview

```
Create project -> Chat (describe your video) -> Stream response (SSE)
    -> Export video -> Poll status -> Get video URL
```

All creative interactions (writing scripts, choosing models, editing storyboards, etc.) go through the conversational `/chat` endpoint -- no separate endpoints needed.

## Repository Structure

| File | Description |
|---|---|
| `SKILL.md` | Skill definition with API reference and workflow instructions |
| `api_curl_commands.md` | Debug curl commands for manual API testing |
| `LICENSE` | MIT License |

## API Endpoints

| Endpoint | Description |
|---|---|
| `POST /user` | Get user profile and credits |
| `POST /create` | Create a video project |
| `POST /projects` | List existing projects |
| `POST /project_info` | Get project metadata and storyboard |
| `POST /chat_history` | Get conversation history (paginated) |
| `POST /upload` | Upload a file (image, video, audio) |
| `POST /chat` | Send a creative instruction |
| `POST /chat_stream` | Consume SSE response stream |
| `POST /export_video` | Start video export |
| `POST /export_status` | Poll export progress |
| `POST /download_all` | Download project resources |
| `POST /download_status` | Poll download progress |
| `POST /products` | List available plans and credit packs |
| `POST /subscribe` | Start subscription checkout |
| `POST /credits_buy` | Buy credits |

## Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/your-change`)
3. Make your changes and submit a Pull Request

**Note:** `SKILL.md` must use ASCII-only characters.

## Links

- [Flova Platform](https://www.flova.ai)
- [Pricing & Plans](https://www.flova.ai/pricing/)
- [Documentation](https://www.flova.ai/docs/)
- [Token Management](https://www.flova.ai/openclaw/?action=token)

## License

[MIT](LICENSE)
