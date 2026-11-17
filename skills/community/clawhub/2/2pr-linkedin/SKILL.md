---
name: 2pr-linkedin
description: Write, schedule and publish LinkedIn posts in your own voice, reply to comments and read post analytics through 2pr.io. Use when the user wants a LinkedIn post drafted or rewritten, a carousel or image post, a post scheduled or published, replies to comments on their posts, or to know which posts performed and when to post.
version: 1.0.0
metadata:
  openclaw:
    emoji: "💼"
    homepage: https://2pr.io
---

# LinkedIn with 2pr.io

[2pr.io](https://2pr.io) is a LinkedIn content tool. This skill drives the 2pr.io MCP server, which acts on the user's real LinkedIn account. Drafting is safe to repeat; publishing, scheduling, replying and deleting are public and need the user's explicit yes.

## Setup

Add the 2pr.io remote MCP server to your agent:

- URL: `https://2pr.io/api/mcp` (Streamable HTTP)
- Auth: OAuth 2.1. The first tool call opens a "Sign in with 2pr" window. There is no API key or environment variable to set, and access can be revoked in 2pr.io under Preferences.

The user needs a 2pr.io account on the Pro or Team plan with their LinkedIn connected. If a tool says the plan does not include a feature, tell the user and link https://2pr.io/pricing.

Data goes only to `https://2pr.io/api/mcp`, which talks to LinkedIn (and X, if connected) through their official APIs. Privacy policy: https://2pr.io/privacy. Full tool list: https://2pr.io/docs/mcp.

## Writing and publishing a post

1. **Pick the profile.** Call `profile_list` first. Most tools need a `profile_id`. If the user manages more than one profile, ask which one before drafting.
2. **Load the voice.** Call `persona_get` so the draft sounds like the user, not like a generic LinkedIn post. Only change the persona with `persona_appendDirective` or `persona_replace` when the user asks for a lasting style change.
3. **Find an angle (optional).** When the user has a topic but no angle, call `viral_search` for proven posts on that topic and borrow the structure, never the words. `inspiration_getTopics` suggests topics from the user's niche.
4. **Draft.** Call `draft_create` with the user's idea. It returns three variants of the same angle and a link that opens the draft in the 2pr.io editor. Show the variant that fits best and the link.
5. **Refine.** Use `draft_refine` for edits ("shorter", "stronger hook", "less salesy"). Use `draft_get` to re-read a draft before acting on it.
6. **Add media (optional).** `media_generateImage`, `media_uploadFromUrl` and `draft_attachImages` / `draft_attachMedia` attach images, carousels or video.
7. **Ship it.** Only after the user confirms the final text:
   - `post_schedule` for a future time. Suggest a slot from `analytics_getPostingTimes` when the user has no preference.
   - `post_publish` to post now.
   - `x_publish` / `x_schedule` to cross-post to X when the user asks.

## Replying to comments

1. Call `profile_list` to get the `profile_id`.
2. Call `engage_refreshPosts` if the inbox looks stale, then `engage_getInbox` to list comments waiting for a reply.
3. Call `engage_draftReplies` for suggested replies in the user's voice. Show them grouped by post.
4. Post with `engage_postReply` or react with `engage_setReaction` only after the user approves that specific reply.

## Reading analytics

- `analytics_getProfileStats`: follower and impression trends.
- `analytics_getPostStats`: per-post performance. Lead with the best and worst post and one concrete reason each did what it did.
- `analytics_getPostingTimes`: when this audience is most active.

Report numbers as they come back. Do not estimate or fill gaps; if data is missing for a period, say so.

## Rules

- Never call `post_publish`, `post_schedule`, `x_publish`, `x_schedule`, `engage_postReply` or `post_delete` without an explicit yes from the user for that exact item.
- Show the final text before publishing. Do not silently edit it after approval.
- Check `post_list` before scheduling on a day that already has a post.
- Adding or removing prospects (`outbound_addProspect`, `outbound_removeProspect`) changes the user's saved list, so confirm first.
