---
name: contentin-linkedin-leads
description: Work the people who engaged with the user's LinkedIn posts through ContentIn (Agent Pro or Pro plan). Use when the user asks who is engaging with them, which engagers fit their ideal customer, who to follow up with, or wants a comment reply or a connection note drafted for a specific person. Reads list_leads and list_my_comments, drafts text the user approves, never sends anything.
license: MIT
compatibility: Requires the ContentIn MCP server connected in the agent (https://mcp.contentin.io/mcp-server) and an Agent Pro or Pro plan. Network access to mcp.contentin.io.
metadata:
  author: ContentIn
  version: "1.0.0"
  homepage: https://contentin.io/linkedin-for-ai-agents/
---

# ContentIn leads

Use this skill when the user wants to turn engagement on their LinkedIn posts into conversations. It needs the Agent Pro or Pro plan. If `list_leads` or `list_my_comments` is refused with `needs_agent_pro_or_pro`, call `get_account_status`, tell the user the tool needs Agent Pro or Pro and that the other ContentIn tools still work, and stop. Do not quote prices or link to a checkout.

## What the data is

- `list_leads` returns people who engaged with THIS user's own posts: name, headline, LinkedIn profile, how they engaged, what they commented, which posts pulled them in, ContentIn's ICP fit score (`icp_score`, 0 to 100) and the user's lead status (`new`, `contacted`, `snoozed`, `dismissed`, `converted`).
- A single reaction creates a lead. A lead with no comment is normal.
- `icp_score` is ContentIn's estimate from the person's headline against the user's stated ideal customer. It is not verified data about who they are. `classified: false` with `icp_score: null` means ContentIn has not scored the lead yet; report it exactly that way, never as "poor fit". `icp_score_source: "user_override"` means the number is the user's own label.
- `list_my_comments` returns the comments the user left on other people's posts and what they got. Use it to see where the user is already in a conversation.
- Default results exclude `dismissed` leads. Ask for them explicitly only if the user wants them.

## Workflow: list, pick, draft, user sends

1. **List.** Call `list_leads` with the filter the user implies. Common calls: `sort: "icp_score"` with `min_icp_score: 70` for "who fits my ICP"; `interacted_since` set to the last 7 days with `sort: "last_interacted"` for "who engaged this week"; `status: ["new"]` for people not yet contacted; `search` for a name or company. Page with `before` / `before_id` when the user wants more. Profiles routinely hold thousands of leads, so keep `limit` small (10 to 20) and summarise.
2. **Pick.** Present a short table: name, headline, how they engaged, what they said, score (or "not scored yet"), status. Let the user choose who to approach. Do not rank unscored leads below scored ones; say they are unscored.
3. **Draft.** For the chosen person, draft one of:
   - a reply to their comment on the user's post,
   - a comment on something they posted (only if the user supplies that post's text; do not fetch other people's posts),
   - a short connection note or direct message.
   Call `get_voice_context` once so the draft sounds like the user and uses only the user's own facts. Reference what the person actually did (their comment, the post they engaged with). Keep it short, specific, no pitch in the first message unless the user asks for one.
4. **User sends.** Hand the text to the user to copy and post or send from their own LinkedIn account. ContentIn has no tool that sends comments or messages, and this skill must never try to automate that through any other tool or browser. Nothing goes out without the user's own hands.

## Rules

- Never send, post or queue a comment, message or connection request on the user's behalf. Draft only; the user sends.
- Do not scrape, fetch or enrich a lead from LinkedIn or other sites. Work with what `list_leads` returns and what the user tells you.
- LinkedIn's User Agreement and API terms restrict automated messaging and connection requests. Remind the user of this once when they first ask for outreach drafts, and decline requests to bulk-generate messages for sending by a bot.
- Keep lead data inside this conversation and the user's own tools. Do not paste it into web forms or third-party services unless the user explicitly asks and names the destination.
- Lead status changes (contacted, converted) are made by the user in ContentIn. If they tell you they contacted someone, say the status is updated in ContentIn, not by this skill.

## Example

User: "Who engaged with my posts this week that looks like a buyer? Draft a reply for the best one."

1. `list_leads` with `interacted_since` = 7 days ago, `sort: "icp_score"`, `limit: 10`.
2. Show the table. Note any unscored leads as "not scored yet".
3. The user picks a founder who commented on the pricing post. `get_voice_context` with `topic: "pricing post follow-up"`.
4. Draft a two-sentence reply to their comment that answers their point and asks one question. Hand it over for the user to post.
