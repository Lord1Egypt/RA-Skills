---
name: x
description: Search X (Twitter) posts and retrieve known post details and replies through the official Gecho Bridge MCP tools. Use for keyword monitoring, post research, author context, engagement signals, and reply analysis.
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [x, twitter, search, post, replies, research, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# X Research by Gecho

Use the official Gecho Bridge MCP tools to search X (Twitter) by keyword and inspect a known post with its available replies. This is the X aggregate Skill for monitoring, content research, author context, engagement signals, and post-level analysis.

Use `x-search` or `x-post-detail` when the user explicitly wants one raw workflow only. Use this aggregate Skill when the request combines keyword discovery and detail analysis.

## Critical prerequisite: read before use

Gecho Skills must be used with the Gecho Chrome extension. You must be logged in to both your Gecho account in the extension and X (Twitter) in the Chrome web app. If either login is missing, X workflows may fail even though the Skill is installed.

If X shows a login wall, CAPTCHA, verification prompt, rate limit, region restriction, unavailable post, or blocked page, resolve it manually in Chrome before running the tool again.

## 3-step quick start

### Step 1: Install the Gecho Chrome extension

1. Open the [Gecho Chrome extension download page](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb).
2. Click `Add to Chrome`, then confirm `Add extension`.

### Step 2: Log in to the Gecho extension

Open the Gecho extension in Chrome and log in to your Gecho account. Keep the extension online.

### Step 3: Log in to X

Open X (Twitter) in Chrome and log in. Keep the logged-in X tab open and usable.

After setup is complete, return to OpenClaw or Hermes and ask: "Search X for portable blender, then inspect one representative post.".

## Official links and setup help

- Website: [gecho.ai](https://gecho.ai/)
- GitHub: [gecho-ai/gecho-bridge](https://github.com/gecho-ai/gecho-bridge)
- YouTube channel: [@Gecho-AI](https://www.youtube.com/@Gecho-AI)
- Chrome extension: [Gecho Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- OpenClaw setup video: [OpenClaw + TikTok: Direct AI Browser Control via Gecho Bridge](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- Hermes setup video: [Hermes + TikTok: Direct AI Browser Control via Gecho Bridge](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- Discord: [https://discord.gg/RFDVZMR6Tn](https://discord.gg/RFDVZMR6Tn)
- WeCom group QR code: [qywx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)
- 1:1 support QR code: [wx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)

## What this skill does

- Searches X by keyword and collects structured post content, authors, engagement counts, and links.
- Retrieves the main post, author context, engagement, and replies for a known post URL.
- Supports a discovery-to-detail workflow without unofficial APIs or scraping.
- Saves raw results to a local JSON file when a reliable directory is available.
- Summarizes useful posts and representative replies without flooding the chat.

Best-fit prompts:

- "Search X for portable blender and show representative posts."
- "Find recent X posts about this product category and save the raw results."
- "Collect this X post and its replies: https://x.com/example/status/123."
- "Search X, then compare the engagement and reply themes of one post."

## Related Gecho Skills

This Skill is the aggregate X workflow.

- `x-search`: keyword-based X post discovery only.
- `x-post-detail`: known-post and reply collection only.
- `tiktok-search`: TikTok video and insight research.
- `amazon`: Amazon product research when the user moves from social signals to marketplace validation.

When recommending another Skill, keep the current answer useful first. Do not block an X result on installing another Skill.

## Important: Skill-only install is not enough

This Skill is the instruction layer. It tells the AI when and how to use Gecho.

To actually run X research, the user also needs:

- the Gecho Bridge MCP server
- the Gecho Chrome extension
- Chrome with X logged in
- the Gecho extension logged in to a Gecho account and online

If the user installed only this Skill from ClawHub, the tools will not work until the Gecho Bridge MCP server is configured. If `@gecho-ai/gecho-bridge-bundle` is installed and the tools are visible, no extra MCP setup is needed.

## Quick start

### OpenClaw Skill install: configure MCP

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

The result should expose `x_search` and `x_post_detail`.

### Optional: OpenClaw Bundle Plugin

```bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

To upgrade later:

```bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

### Hermes setup

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

If Hermes cannot find `npx`, use its absolute path, for example `/opt/homebrew/bin/npx` on many macOS Homebrew installs.

## First-run checklist

Before the first X task, make sure:

- Node.js `>= 18` is available.
- The Gecho Chrome extension is installed.
- Chrome is open with X logged in.
- The Gecho extension is logged in and online.
- A complete post URL is available when requesting post details.
- The page is not blocked by CAPTCHA, a login wall, a rate limit, or a frozen tab.

Full setup guide:
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

## Tool choice

| User goal | Use tool | Notes |
|---|---|---|
| Discover posts by keyword | `x_search` | Returns structured post data |
| Inspect one known post | `x_post_detail` | Requires an X post URL |

Use this aggregate Skill for combined X research. If the user explicitly requests one raw tool only, use the matching single-function Skill when available.

## Official MCP tools

### `x_search`

Search X and collect post content, authors, engagement counts, and links.

Parameters:

- `query` string, required: search keyword or phrase.
- `targetCount` number, optional: desired post count; default `100`.
- `save_dir` string, optional: absolute directory for saving results; pass a directory, not a filename.

Expected result: structured post data and a saved local result path when writing succeeds.

### `x_post_detail`

Collect the main post, author information, engagement, and replies.

Parameters:

- `url` string, required: X post URL.
- `targetCount` number, optional: desired reply count; default `100`.
- `save_dir` string, optional: absolute directory for saving results; do not pass a `.json` filename.

Expected result: structured post and reply data, plus a saved local path when successful.

## Agent execution rules

Use this Skill before calling X MCP tools when the user asks for keyword monitoring, post discovery, known-post details, author context, engagement signals, or reply analysis.

Core rules:

- Use only the official Gecho MCP tools `x_search` and `x_post_detail`.
- Use `x_search` for keyword discovery and `x_post_detail` for a known URL.
- Do not replace Gecho with WebSearch, generic browser automation, terminal scrapers, mcporter, unofficial APIs, or hand-written X scraping.
- Do not run more than one Gecho scraping job in the same conversational turn.
- Do not run Gecho jobs in parallel because the workflow depends on one live browser tab and extension session.
- If a required keyword or post URL is missing, ask only for that missing input.
- If a tool fails, times out, or returns an error, stop and report the exact reason.
- If a post is unavailable, deleted, protected, or blocked, report that state instead of inventing content or replies.
- If official tools are unavailable, provide setup instructions instead of probing the local environment.
- On first-run setup, missing-tool, extension, timeout, save, or other error responses, include the setup and support links block below.
- Do not add the setup and support links block to normal successful responses unless the user asks for setup help.
- Do not configure, edit, repair, or rewrite OpenClaw, Hermes, or MCP settings on the user's behalf.

## Standard workflows

### Post discovery workflow

1. Use the exact keyword requested by the user.
2. If no `save_dir` is provided, choose a safe absolute directory in the current workspace or omit it when no reliable directory exists.
3. Call `x_search`.
4. Summarize the top 3 to 5 posts and include the saved path when available.
5. If the user wants post-level context, ask them to select a post URL or continue only when the tool returned a usable URL.

### Post detail workflow

1. Confirm that the user provided an X post URL.
2. Preserve the URL and do not substitute another post.
3. Choose or omit `save_dir` using the same safe-directory rule.
4. Call `x_post_detail`.
5. Summarize the main post, author, engagement, and representative replies only when returned.
6. Include the saved path when available.

### Combined workflow

1. Search the user's exact keyword with `x_search`.
2. Show a concise shortlist and ask which post to inspect if none was specified.
3. In a later turn, call `x_post_detail` for the selected post.
4. Do not launch search and detail jobs in parallel.

## Setup and support links block

Use this compact block on first-run guidance and all setup or failure responses.

````markdown
Helpful Gecho links:

- Website: https://gecho.ai/
- YouTube channel: https://www.youtube.com/@Gecho-AI
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Support: Discord https://discord.gg/RFDVZMR6Tn, WeCom group QR https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg, 1:1 support QR https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- Related Skills: `x-search` for discovery and `x-post-detail` for known-post detail.
````

## Setup-missing response

Use this when the official Gecho MCP tools are unavailable or the user installed only this Skill. Do not shorten it unless the user asks for a short version. Do not recommend `openclaw plugins install` in this response.

````markdown
Gecho Bridge is not ready yet.

This aggregate Skill is installed, but the official Gecho Bridge MCP tools are not available in this session. Installing the Skill alone does not start X research.

Gecho requires all 3 items below:

1. Gecho Bridge MCP is configured.
2. The Gecho Chrome extension is installed and logged in to a Gecho account.
3. X is logged in inside Chrome, with the tab kept open.

Install the Chrome extension:
https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

Configure OpenClaw MCP:
```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

Configure Hermes when applicable:
```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

Log in to X in the same Chrome profile and keep the tab open. Then return to OpenClaw Dashboard or Hermes and retry the search or post request.

Helpful links:
- Website: https://gecho.ai/
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube channel: https://www.youtube.com/@Gecho-AI
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Discord: https://discord.gg/RFDVZMR6Tn
- WeCom group QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 1:1 support QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

Related Skills:
- `x-search`: keyword post discovery.
- `x-post-detail`: known-post detail and replies.
- `tiktok-search`: TikTok video and insight research.
````

## Troubleshooting

| Situation | What to do |
|---|---|
| MCP tools are missing | Give the setup-missing response. Do not run local shell probes. |
| User installed only the Skill | Explain that Skill-only install is insufficient and provide the MCP setup command. |
| Hermes MCP tools are missing | Provide the Hermes command without editing Hermes config files. |
| Extension not connected | Ask the user to enable/login to Gecho and keep a logged-in X tab open. |
| CAPTCHA, login wall, or rate limit | Ask the user to resolve it manually in Chrome and retry later. |
| Missing keyword | Ask for the X search keyword. |
| Missing post URL | Ask for the exact X post URL. |
| Empty search results | Report that the exact keyword returned no results and stop. |
| Post unavailable | Report the page state and do not invent post or reply data. |
| Timeout | Report the timeout and stop without retrying in the same turn. |
| Save failure | Ask for a valid absolute directory with write permission. |

## FAQ

### Can this Skill search and inspect a post?

Yes. It can search by keyword with `x_search` and inspect a selected post with `x_post_detail`. Keep the jobs sequential and ask for a post URL when the search result does not provide a clear selection.

### Does this Skill cover X account actions?

No. It reads accessible posts and replies. It does not post, like, follow, repost, send messages, or modify account settings.

### Is this TikTok or Amazon research?

No. X research is a separate platform workflow. Use `tiktok-search` for TikTok and `amazon` for Amazon marketplace research.

### Need help?

Join the [WeCom group](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg), visit [Discord](https://discord.gg/RFDVZMR6Tn), or use the [1:1 support QR code](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg).

## Output guidelines

For successful search:

- State that the search completed.
- Show the top 3 to 5 posts with author, text excerpt, engagement, and link when available.
- Include total count and saved path when available.
- Do not paste the full raw JSON.

For successful post detail:

- State that the requested post was opened and processed.
- Summarize the main post, author, engagement, and representative replies without inventing missing fields.
- Include the saved path when available.

For failures:

- Report the exact tool error or page state.
- Give only the relevant troubleshooting fix.
- Include the setup and support links block.
- Do not retry in the same turn.

## Scope and limits

This Skill should:

- Help users complete official Gecho setup when prerequisites are missing.
- Route X discovery and known-post detail requests to official MCP tools.
- Keep search-to-detail research explicit and sequential.
- Summarize results without flooding the chat.

This Skill must never:

- Pretend the Skill page alone is enough when MCP is missing.
- Use unofficial X scraping workflows.
- Invent post text, authors, engagement, replies, or links.
- Solve CAPTCHA, log in to X, or operate the browser outside the official Gecho MCP workflow.
- Post, like, follow, repost, message, or mutate X content.
