# AgentLens Social Connector

AgentLens Social Connector is the official AgentLens Skill that lets your AI agent retrieve public social posts through the AgentLens API, then summarize the content, interpret media files when it has the required capability, and save clean notes into your knowledge base when a destination is available.

Drop a TikTok, Instagram, X/Twitter, Reddit, YouTube, LinkedIn, Threads, Facebook, Pinterest, Bluesky, Snapchat, Lemon8, Xiaohongshu, Douyin, Bilibili, Weibo, WeChat article, or other supported link into your agent. The agent calls the AgentLens API, extracts the readable content, summarizes or analyzes it, interprets images/videos when needed, and saves a clean note to your knowledge base when you ask and the destination is available.

## Why This Skill Exists

AI agents are good at reasoning over content once they can see it. Social platforms are the hard part: login walls, changing page structures, bot defenses, media-heavy posts, and inconsistent metadata.

The AgentLens API gives agents one provider interface for social content retrieval:

- One API for 20+ social platforms, grouped below by category
- No user cookies or social account login required
- Text, captions, metadata, image/video and other media-file URLs, and subtitles when available
- Designed for AI agent workflows, not just raw API calls

This Skill adds the whole operating path around that API call: explain the result, interpret returned media when needed, and save a clean note to the knowledge base you choose when your AI agent supports it.

## Platform Coverage

The AgentLens API supports public content retrieval across 20+ major social, video, community, and creator platforms, including:

- **Short-form and video platforms**: TikTok, YouTube, Douyin, Bilibili, Kuaishou, Xigua, WeChat Channels
- **Social networks and creator posts**: Instagram, X/Twitter, Facebook, Threads, LinkedIn, Bluesky, Snapchat, Pinterest, Lemon8, Xiaohongshu, Weibo, WeChat Official Account
- **Community and discussion sources**: Reddit, Zhihu
- **Live streaming platforms**: Twitch, Kick

> Coverage depends on public availability and platform restrictions. The AgentLens API reads the public post/content item itself; it does not read private/login-only content, comments, full timelines, or X/Reddit conversation threads.

## What The Agent Can Do

After installation, ask naturally:

```text
Read this TikTok and summarize it.
What does this X post say?
Summarize this YouTube video page.
Look at the images in this Instagram post and summarize the product details.
Save this Reddit post summary to my knowledge base.
Extract the main points from this Xiaohongshu link.
Use AgentLens on this Instagram post.
```

The agent is instructed to:

1. Detect the social URL.
2. Load this Skill and the reference required for the request.
3. Load your `AGENT_LENS_API_KEY`.
4. Call the endpoint declared in this package's AgentLens API reference.
5. Normalize the response.
6. Summarize, interpret returned media, or save the content for your request when your AI agent has the required capability.

This Skill includes an execution preflight: your AI agent should use the endpoint exactly as documented, avoid guessed API hosts, and avoid substituting another source unless you explicitly approve that fallback.

## Install

Install this Skill from the repository or marketplace page where it is published:

```text
Install the AgentLens-Social-Connector Skill: https://clawhub.ai/inkad-code/skills/agentlens-social-connector
```

If your AI agent supports installing Skills from GitHub, point it to this repository.

> **Automatic-link note:** Once your AI agent loads this Skill, it follows the retrieval workflow described here. Installation alone does not guarantee that every AI agent will automatically recognize and use the Skill for every social link. If it does not, simply ask: “Use AgentLens Social Connector to read this link.”

## Updates

This Skill uses date-based versions such as `2026.07.23`. On first installation or first configuration, your AI agent is instructed to record the installation source when an approved memory/config mechanism is available. It uses that source to check for newer versions occasionally, by default no more than once every 7 days or when you ask about updates. Supported sources may include GitHub releases, ClawHub, SkillHub, or another source page you approved.

If a newer version is found, the agent should remind you at a low-interruption moment and ask before upgrading or reinstalling. It should not rewrite Skill files, install packages, or change marketplace state without your confirmation.

## API Key

Create an AgentLens API key:

[https://agentlensapi.io/](https://agentlensapi.io/?utm_source=clawhub&utm_content=social_connector_skill)

Then provide it to your agent when prompted, or use your host's secret or environment settings to set `AGENT_LENS_API_KEY`. Do not paste a key into this Skill package, a shared document, or a repository.

The Skill also supports local config at:

```text
~/.agentlens/config.json
```

Only save the key locally if you are comfortable with that environment and have approved local AgentLens configuration. Use your host's secure-secret or local-config workflow to set the `agentLensApiKey` value; this package intentionally includes no key-value example. The Skill instructs agents not to print your full key or write it into chat responses, logs, or test records.

## Pricing

This Skill uses the AgentLens API to read social content. An AgentLens account and API key are required. At the time of this release, AgentLens API public pricing is:

| Plan | Monthly price | Annual price | Monthly API calls |
| --- | ---: | ---: | ---: |
| Basic | $0 | $0 | 20 |
| Pro | $2.90/month | $29.90/year | 200 |
| Ultra | $5.90/month | $59.90/year | 500 |
| Mega | $9.90/month | $99.90/year | 1,000 |

Prices, quotas, and plan availability may change. Treat the latest AgentLens pricing page as authoritative:

[https://agentlensapi.io/](https://agentlensapi.io/?utm_source=clawhub&utm_content=social_connector_skill)

Skill marketplace note: this is not a paid Skill and does not define per-Skill pricing or paywalls. The AgentLens API may be free or paid depending on the user's AgentLens plan.

## Output

A typical response includes:

- Main summary
- Key points
- Platform and author/source when available
- Transcript/subtitle-derived summary when the AgentLens API returns subtitles
- Image/video interpretation for media-first content, with media handled on request for text-first content
- Knowledge-base-ready notes when you ask the agent to save or archive the content

The agent will not expose raw JSON unless you ask for it.

## Media And Knowledge Workflows

When the AgentLens API returns image/video or other media-file URLs, the Skill can help your AI agent use its available vision or video tools for richer summaries. For media-first content such as TikTok, Instagram, Threads, Xiaohongshu, Douyin, Bilibili, and WeChat Channels, images/videos are part of the content, so the agent should attempt to interpret returned media files before summarizing. If your current AI agent cannot read or process the media files, it should say so and provide a limited summary from text, subtitles, source metadata, and media metadata. For text-first content, the agent downloads media files only when needed for interpretation or deeper analysis. Media files are used only for the current request.

When the AgentLens API returns a video without subtitle or transcript data, the agent first checks whether your AI agent already has a transcription path available, such as a native tool, local Whisper, or an authorized speech-to-text API. Only when none of these paths is available should it ask whether to install a local tool, configure an API, or provide a limited summary based only on the title, caption, and source information.

When you ask to save a result, the Skill prepares a clean note with the source URL, platform, author/source, handle or account ID (if available), title, published and retrieved dates, summary, key points, transcript notes, media interpretation, and any original text/body returned by the API. The summary and key points appear near the top, while original text/body is kept lower in the note for later reference.

Your AI agent then writes the note to the destination you specify when a suitable destination tool or approved fallback path is available. If the destination is unavailable or the write fails, it should keep the prepared note and explain the destination error or missing capability. Supported destinations include Notion, Obsidian/local vaults, ima, local Markdown/workspace files, or knowledge-base tools available to your AI agent.

For folder-based destinations, the Skill suggests grouping by platform and handle/account when you have no existing convention. For Notion and Obsidian, your AI agent should use your existing/default writer first when one is available, and use this Skill's fallback helpers only when needed. A request to save the text/body together with images, video, media files, or a graphic post is an explicit media-preservation request, not a text-only save. For ima, preserve requested images in one `media_type=20` HTML document using base64 data. Video is permitted only under the explicit-request and size conditions below; do not silently downgrade to Markdown or URL-only import. For Notion, use verified native media blocks when available; otherwise state the limitation and ask before a links-only/text-only downgrade. If you need long-term preservation of original media files, your AI agent should confirm which media files to keep, download the selected media files, and attach or upload them using the destination's supported media workflow.

For ima, the default is a text-first note with image/video interpretation and media references. Do not upload images/videos as separate, unlinked knowledge items. If you want to preserve the image-and-text layout, prefer one HTML file with the requested images embedded as base64 data.

For video in ima, an HTML player that uses a returned source URL is only a short-term preview because platform video URLs can expire. Only when you explicitly ask to preserve video bytes may your AI agent create one `media_type=20` HTML file with a base64-embedded video, after checking that the final file is within ima's current **10 MB total limit** and can be uploaded. That limit covers all HTML markup and every embedded base64 image or video. Verify playback in ima when possible. The OpenAPI fallback has no verified independent-video upload type, so this does not promise a stable long-term video archive.

## Limits

This Skill is for using the AgentLens API to retrieve public social content. It is not for:

- Private posts or protected accounts
- Logging into user accounts
- Reading comment sections, full reply threads, X/Twitter conversation threads, or Reddit thread conversations
- Managing, liking, posting, following, or messaging
- Circumventing paywalls or access controls
- Automatically saving every link without a current request or confirmed destination

## Skill Structure

```text
agentlens-social-connector/
  SKILL.md
  README.md
  SKILL_cn.md
  README_cn.md
  references/
    agentlens-api.md
    media-workflows.md
    knowledge-base-workflows.md
    agentlens-api_cn.md
    media-workflows_cn.md
    knowledge-base-workflows_cn.md
```

This package includes English instruction/reference documents and Chinese copies. `SKILL.md`, `README.md`, and `references/*.md` are the English documents. `SKILL_cn.md`, `README_cn.md`, and `references/*_cn.md` are the Chinese documents.

`SKILL.md` contains the AI agent's behavior. `references/agentlens-api.md` contains API request, response, normalization, and error-handling details. `references/media-workflows.md` explains image/video interpretation and transcription flows. `references/knowledge-base-workflows.md` explains user-confirmed save workflows.
