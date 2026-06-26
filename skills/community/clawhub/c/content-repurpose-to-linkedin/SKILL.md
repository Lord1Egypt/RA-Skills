---
name: content-repurpose-to-linkedin
description: Turn source content into polished LinkedIn posts and publish them with confirmation. Uses ClawLink to discover LinkedIn tools and publish posts after user approval.
---

# Content Repurpose to LinkedIn

![Content Repurpose to LinkedIn](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/linkedin.svg)

Turn source content into polished LinkedIn posts and publish them through ClawLink. Use this skill when users want to transform articles, notes, or other content into professional LinkedIn posts.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=content-repurpose-to-linkedin) for hosted connection flows and credentials so you do not need to configure LinkedIn API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect LinkedIn |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect LinkedIn |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ LinkedIn API      │
│   (User Chat)   │     │   (OAuth)    │     │ (Posts/Content)  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect LinkedIn  │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ LinkedIn │
   │  File    │           │ Auth     │           │ Profile │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for LinkedIn posting again."

## Good Trigger Phrases

- "Turn this article into a LinkedIn post"
- "Repurpose my notes into 3 LinkedIn post options"
- "Draft a founder update for LinkedIn"
- "Rewrite this thread for LinkedIn and post it"
- "Take this blog post and make it into a short professional post"
- "Create a LinkedIn post from this content"

## Workflow

### 1. Understand the Source and Goal

Ask for:
- the source content
- the target audience
- the tone
- whether the goal is reach, authority, storytelling, or announcing something
- whether the user wants one post or several variants

If the source is long, first summarize the key ideas before drafting.

### 2. Pull Out the Strongest Angle

Do not just compress content. Choose the best LinkedIn angle:
- opinion
- lesson learned
- founder update
- case study
- contrarian insight
- practical checklist
- behind-the-scenes story

If there are several possible angles, give the user 2-3 options first.

### 3. Draft for LinkedIn, Not for Blogs

Good LinkedIn posts are usually:
- shorter than the source
- hook-first
- easy to scan
- written in plain language
- built around one idea

Prefer:
- a strong opening line
- short paragraphs
- one concrete takeaway
- a simple CTA when useful

Avoid:
- sounding robotic
- stuffing hashtags
- preserving blog structure
- making unsupported claims

### 4. Offer Variants Before Publishing

When the user has not specified a format, generate 2-3 options such as:
- concise and professional
- personal/founder voice
- tactical/educational

Let the user choose or edit one before posting.

### 5. Discover the Live LinkedIn Tools

1. Call `clawlink_list_integrations` to confirm LinkedIn is connected.
2. Call `clawlink_list_tools` with integration `linkedin`.
3. If the exact posting tool is unclear, call `clawlink_search_tools` with a short query such as `create post`, `publish text post`, or `organization post`.
4. Call `clawlink_describe_tool` before any publish, comment, or delete action.
5. Use the returned schema and guidance as the source of truth.

### 6. Preview and Confirm

Before any publish action:
1. Show the final post text exactly as it will appear.
2. Confirm whether it should publish to a personal profile or organization if relevant.
3. Call `clawlink_preview_tool` first when available.
4. Execute with `clawlink_call_tool` only after explicit confirmation.

## Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=linkedin and connect LinkedIn.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Good Workflow Behavior

- Suggest edits to improve clarity before posting.
- Preserve claims and facts from the source; do not invent outcomes or metrics.
- Ask if the user wants a CTA, hashtags, or a shorter version.
- If the user wants several posts from one source, make them meaningfully different.
- If the post is for a company page, verify the target entity before publishing.

## Rules

- Always use ClawLink tools for LinkedIn publishing. Do not ask for separate LinkedIn credentials.
- Do not invent LinkedIn tool names or schemas. Use the live ClawLink catalog in the current turn.
- Ask for confirmation before publishing, commenting, or deleting any LinkedIn content.
- Never publish a draft automatically just because the user asked for help writing it.
- If LinkedIn is not connected, direct the user to https://claw-link.dev/dashboard?add=linkedin.

## Example Prompts

- Turn this blog post into 3 LinkedIn post options for startup founders.
- Rewrite these product notes into one polished LinkedIn launch post.
- Take this long transcript and create a short authority-building LinkedIn post.
- Draft a LinkedIn post from these bullet points, then ask me before posting it.

## Notes

- LinkedIn integration slug is `linkedin`.
- Tool names may include `create_post`, `organization_post`, `share_post`, or similar — discover the exact name from the live catalog.
- LinkedIn API requires specific permissions for organization posting — verify the connected account has appropriate access.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration linkedin`. |
| Missing connection | LinkedIn is not connected. Direct the user to https://claw-link.dev/dashboard?add=linkedin. |
| `Write rejected` | User did not confirm publishing. |
| `InvalidArgument` | Invalid parameter. Review the tool schema with `clawlink_describe_tool`. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

## Resources

- [LinkedIn API Documentation](https://developer.linkedin.com/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=content-repurpose-to-linkedin
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Twitter/X](https://clawhub.ai/hith3sh/twitter-social) — For Twitter posting
- [Facebook](https://clawhub.ai/hith3sh/facebook-pages) — For Facebook posting
- [Instagram](https://clawhub.ai/hith3sh/instagram-business) — For Instagram posting

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=content-repurpose-to-linkedin)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
