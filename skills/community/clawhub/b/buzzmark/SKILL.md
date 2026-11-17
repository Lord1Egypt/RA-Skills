---
name: buzzmark
description: Write, plan and schedule social media posts in a business's own voice with Buzzmark's MCP server. Use when the user wants post ideas, posts for Instagram, LinkedIn, Facebook, X, Threads or TikTok, a week of posts planned around their best times, a check on how much a post sounds like their brand, or what worked this month.
version: 1.1.0
homepage: https://buzzmark.ai
clawdis:
  primaryEnv: BUZZMARK_API_KEY
  envVars:
    - name: BUZZMARK_API_KEY
      required: false
      description: Personal Buzzmark API key, sent as a Bearer header by agents that can't sign in with OAuth, and read by the Buzzmark CLI. Made on the AI apps page in Buzzmark.
  homepage: https://buzzmark.ai
---

# Buzzmark

Buzzmark is a ghostwriter that writes, plans and schedules social media posts for founders and growing businesses. It reads the business's website and products first, so the first post already sounds like them, and keeps learning from what they publish and how they edit its drafts.

This skill connects your agent to Buzzmark's remote MCP server, or to the same tools through the Buzzmark CLI, and tells it how to use them well.

## Setup

1. Sign up at [buzzmark.ai/signup](https://buzzmark.ai/signup). New users get 7 days free. Connect at least one social account in Buzzmark.
2. Add the MCP server `https://buzzmark.ai/mcp` (Streamable HTTP) to your agent. Claude and Claude Code use Claude's own address, `https://buzzmark.ai/mcp/claude`: it serves every tool except the two Claude can't use, `create_image` and `add_media_from_chat`.
   - Agents with OAuth sign in on their own the first time a tool runs: the user approves on a Buzzmark page. There is no key to copy.
   - Agents without OAuth send a personal API key as `Authorization: Bearer $BUZZMARK_API_KEY`. The user makes one on the [AI apps page](https://buzzmark.ai/app/ai-apps) and can revoke it there.
3. Check the connection: call `list_social_sets`. It returns the user's social sets and their ids.

Claude Code:

```bash
claude mcp add --transport http buzzmark https://buzzmark.ai/mcp/claude
```

Any app with an MCP config file:

```json
{
  "mcpServers": {
    "buzzmark": {
      "type": "http",
      "url": "https://buzzmark.ai/mcp",
      "headers": { "Authorization": "Bearer ${BUZZMARK_API_KEY}" }
    }
  }
}
```

Leave out `headers` when the app signs in with OAuth. Steps for Claude, ChatGPT, Grok and Cursor are at [buzzmark.ai/ai-apps](https://buzzmark.ai/ai-apps).

## Without an MCP client: the command line

An agent with a shell that can't add an MCP server runs the same tools with the Buzzmark CLI (Node.js 22 or later). It reads the key from `BUZZMARK_API_KEY` and nowhere else: never put the key on the command line.

```bash
npx buzzmark list-social-sets
npx buzzmark help save-draft
npx buzzmark save-draft --social-set-id 12 --text "We open at 8 tomorrow."
npx buzzmark schedule-post --post-id 42 --when best_time
npx buzzmark upload ./launch.png --post-id 42
```

- Each command is one of the tools below, with dashes: `schedule-post` runs `schedule_post`. `npx buzzmark tools` lists every one and `npx buzzmark help <tool>` shows its flags.
- Plain inputs are flags (`--post-id 42`, a list as `--account-ids 3,4`). Nested ones, like a thread or a week of posts, go in as JSON with `--input '{...}'`, or `--input -` to read it from stdin.
- `upload` adds a file from this machine to the user's Library, and with `--post-id` to that draft.
- The answer is JSON on stdout. An error is JSON on stderr with a `message`, and the exit code says what kind: 1 the tool said no (tell the user its reason), 2 a wrong command, 3 a missing or refused key, 4 too many calls, 5 Buzzmark couldn't be reached.

Everything below works the same way from the command line.

## The words Buzzmark uses

- **Social set**: a group of connected social accounts with one brand voice, one time zone and weekly posting slots. Almost every tool needs a `social_set_id`.
- **Hive profile**: the brand's voice, learned from its website, products and published posts. A founder can have a personal one next to the company's.
- **Buzz**: a post. A draft, a scheduled post and a published post are all Buzzes.

## How to work with it

**Start every session with `list_social_sets`.** If the user has more than one set, ask which business or accounts they mean before writing anything. Use the ids the tools return. Never guess an id.

**Find ideas.** `get_post_ideas` finds angles in this week's news for the brand's sector.

**Write.** `write_posts` writes 1 to 5 posts in the brand's voice and checks every post against Buzzmark's writing rules. Prefer it over writing the text yourself: the voice is the point. It saves nothing, so pass the text you keep to `save_draft`, which makes a draft (or updates one with `post_id`) and says what a platform would refuse before you schedule. `rewrite_post` improves a post, `check_post` scores any post from 0 to 100 against the voice and says what to fix, and `adapt_for_platforms` gives a draft its own version for each platform. `list_brand_profiles` shows the brands and their voices when the user has more than one.

**Add a first comment.** `save_draft` takes `first_comment`: a comment posted under the post the moment it goes out, on LinkedIn, Instagram (not a story), Facebook and Threads. It's the place for a link or the hashtags, so the post itself stays clean. When the user wants a link in a post for those platforms, put it in the first comment unless they ask for it in the post. Other platforms leave the comment out. Limits: 500 characters on Threads, 1,250 on LinkedIn, 2,200 on Instagram, 5,000 on Facebook. An empty string removes it; leaving it out keeps the draft's comment as it is.

**Tag people and brands.** On X, Threads, Instagram and TikTok write `@handle`. On LinkedIn write the profile or page link in brackets, `@[https://www.linkedin.com/company/<slug>]` or `@[https://www.linkedin.com/in/<id>]`, and LinkedIn shows its own name for it. On Facebook a mention stays plain text. A brand profile with accounts needs none of this: write its name, and its first mention is tagged on each platform where it has an account.

**Add a picture.** The server lists the picture tools your app can use: `create_image` makes one, `add_media_from_url` takes a public link, `create_upload_link` gives the user a link for a file on their computer or phone (then `add_uploaded_media`), and `add_media_from_chat` takes a file attached in the chat. Each says what a platform would refuse.

**Schedule.** Show the user the final text and the time before you schedule. `get_best_times` says when the set's posts do best. `schedule_post` puts one draft on the calendar and `schedule_posts` puts several. `reschedule_post` moves one, `unschedule_post` takes one back to drafts, and `delete_draft` removes a draft. Times are on the social set's clock: give a time without an offset and it means the set's local time.

**Plan a week.** `create_weekly_content_plan` builds 7 days of posts from the set's slots, best times and history. Afterwards, offer to save the posts as drafts and schedule them.

**See what worked.** `list_posts` and `get_post` read posts, `get_post_stats` lists a social set's recent published posts with their numbers, best first, and `get_insights` says what worked this month.

## What it can't do

- Post right away. The most an agent can do is schedule. Every scheduled post stays on the user's Buzzmark calendar, where they can change or remove it before it goes out.
- Delete a scheduled or published post, reach accounts that aren't connected to this Buzzmark account, or change the account itself (plans, billing, sign-in, deleting it).

Say so plainly and send the user to [buzzmark.ai/app/settings](https://buzzmark.ai/app/settings).

When a tool says a limit was reached, tell the user what ran out and when it starts again.

## Things to ask

- "Find me post ideas from this week's news in my sector."
- "Write 3 LinkedIn posts about what we shipped this week, then give X its own version."
- "Draft a LinkedIn post about our new guide and put the link in the first comment."
- "How much does this post sound like my brand? Fix what doesn't."
- "Plan next week around my best posting times and schedule it."
- "Make a picture for this post."
- "What worked on Instagram this month?"

## Links

- Buzzmark: [buzzmark.ai](https://buzzmark.ai)
- Setup guides: [buzzmark.ai/ai-apps](https://buzzmark.ai/ai-apps)
- Every tool and its inputs: [buzzmark.ai/ai-apps/mcp](https://buzzmark.ai/ai-apps/mcp)
- The CLI: [docs.buzzmark.ai/ai-apps/cli](https://docs.buzzmark.ai/ai-apps/cli)
- Support: support@buzzmark.ai

Buzzmark is made by Piik Labs AB in Göteborg, Sweden.
