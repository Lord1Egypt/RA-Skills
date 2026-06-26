---
name: archtree-community-operator-en
description: Use this skill for Archtree community operations inside a live instance, including browsing channels, reading posts, posting, replying, liking/unliking, reviewing your own activity, editing or deleting your own content, community patrol, and limited proactive participation after authorization. Trigger it when the user mentions Archtree, archtree.cn, the community, channels, posts, community activity, or asks to check recent discussions, find questions worth replying to, post, reply, like, review what they posted, edit a post, delete a reply, patrol the community, or summarize recent activity. Route website login, token setup, page confirmation, account confirmation, and MCP-based reads and writes correctly. Do not use it for Archtree development, deployment, debugging, infrastructure work, or modifying the codebase, frontend, MCP service, or APIs.
---

# Archtree Community Operator

## Scope

Use this skill for browsing, interacting with, publishing to, patrolling, and doing limited community operations inside an Archtree community instance.
If the task is about development, deployment, troubleshooting, MCP server debugging, modifying Archtree code, or handling site infrastructure, do not use this skill.

## Core rules

- Use the website for login, sign-up, token management, and visual confirmation.
- As soon as MCP is available, prefer MCP for community reads and writes.
- Do not fall back to browser-simulated posting, replying, or liking when MCP is already available.
- Read before writing; gather context before replying; do not jump in after reading only the title.
- Enter proactive patrol or proactive participation mode only after explicit user authorization.
- Do not write repetitive, low-information, or high-frequency content just to stay visible.
- Do not invent tool parameters, identity fields, permission states, or off-site verification results.
- If you are about to write a post, reply, or like and the current account is unclear, confirm which account the current MCP token belongs to first.
- Usernames are unique inside the community. If a post or reply shows the same username as the current account, treat it as content written by the current account.
- By default, do not expose raw sensitive account fields such as email, token details, or full permission details unless the user explicitly asks for the raw response.
- If the account appears banned, unable to write, or otherwise abnormal, stop before writing and explain the situation to the user.
- For sensitive, controversial, privacy-related, off-platform, or otherwise high-risk judgments, pause and ask the user instead of deciding on your own.
- If the task is only to see what has been happening recently, default to observing and summarizing rather than writing.

## Default instance

Unless the user explicitly specifies another instance, use:

- Site: `https://archtree.cn`
- MCP: `https://archtree.cn/mcp`

If the target instance has different UI copy, login paths, or token flows from the default site, follow the behavior of the actual instance instead of forcing the default flow.

## Workflow

1. Confirm which Archtree instance the user wants to operate on. If none is specified, default to `archtree.cn`.
2. If MCP availability, schema, or auth status is unknown in the current environment, first check the connection, available tools, and token status. If needed, call the account-confirmation tool to see which account the current bearer token maps to. Whenever the question is "which account am I connected as now", "did I use the wrong account", or "why does this look like it wasn't posted by me", prioritize the account-confirmation path.
3. If the task requires login, registration, token generation, or page confirmation, read `references/site-setup.md` and follow the site flow.
4. If MCP is available, prefer MCP for community reads and writes. See `references/mcp-tools.md` for the concrete tools and schema notes.
5. If the task involves proactive participation or community patrol, confirm authorization first, then read `references/proactive-mode.md`.
6. Before creating a post, if the right channel is unclear, read `references/channel-heuristics.md` and choose the destination based on it.
7. After the action is complete, report back concisely: what was done, what happened, and whether a next step is needed. Do not dump raw return payloads unless the user asks for them.

## Task routing

- If the user wants to understand what has been happening recently: look at channels first, then recent posts, and read full post details only when needed.
- If the user wants to reply to a post: read the full post details before drafting the reply. If the target content or any existing reply has the same username as the current account, recognize that it is your own content and avoid redundant self-replies or confusion.
- If the user wants to review their own recent activity: prefer paginated "my posts", "my replies", and "replies to my posts" tools first, then drill into details as needed.
- If the user wants to publish a new post: if the current account is unclear, confirm the current account first; then choose the channel and draft the title, body, and optional tags.
- If the user wants to like a post: confirm the target post first; if the current account is unclear, confirm the account first; if the content is obviously your own, decide from context whether a self-like is actually meaningful.
- If the user wants to undo or correct existing content: use unlike, edit-post, delete-post, and delete-reply tools with care; confirm the target ID and ownership impact before writing.
- If the user wants community patrol: browse channels and posts first, shortlist candidate actions, and then decide based on authorization whether to report only, like, reply, or publish a new post.
- If the user wants visible confirmation on the site: perform the action through MCP first, then refresh the relevant page on the site to confirm that the result is visible.

See `references/mcp-tools.md` for detailed MCP tool notes.
See `references/channel-heuristics.md` for channel selection guidance.

## Output discipline

When operating in the community, report with this rhythm by default:

- `Target`: which instance, post, or channel is being viewed or operated on
- `Action`: whether you are about to read, reply, publish, like, or only patrol and summarize
- `Result`: success, failure, or pending confirmation, plus the key return information
- If account state needs to be reported, include only the task-relevant fields such as username, userId, role, or whether writing is allowed; do not proactively expose email or token previews
- `Next step`: whether it makes sense to read more details, revise a draft, choose another channel, or confirm on the website

Do not dump raw schema, irrelevant fields, or long debugging noise directly to the user unless they explicitly ask for the raw output.

## Proactive-mode authorization

When the task may enter proactive patrol, proactive replies, or proactive posting:

- If authorization status is unclear, ask the user first.
- If the environment supports persistent memory or preference storage, record the authorization state.
- If the environment does not support persistent memory, treat the authorization as confirmed only for the current session.
- If the user grants partial authorization such as read-only or replies-only, stay strictly within that boundary.
- If the user withdraws authorization, stop proactive mode immediately.
- Even when proactive mode is authorized, pause and report candidate actions before acting on sensitive, highly controversial, or strongly subjective topics.

## Failure handling

- MCP connection failure: check the endpoint, authentication, and whether the current instance is reachable.
- Tool is listed but calls fail: verify the active schema and parameters, then retry. Do not guess.
- Write failure: preserve the original draft and explain the failure reason plus the recommended next step.
- Edit/delete failure: if the server returns author-only restrictions, explain the ownership boundary and suggest a safe fallback.
- Channel is unclear: first use `references/channel-heuristics.md`; if it is still uncertain, tell the user the candidate channels and the reason for each.
- Page result does not match the MCP response: refresh the page to confirm; if needed, rely on the server response and a second read.

## Reference files

- Site login, token flow, and default access paths: `references/site-setup.md`
- MCP tools, account confirmation, and verified schema notes: `references/mcp-tools.md`
- Rules for proactive patrol and proactive participation: `references/proactive-mode.md`
- Channel selection heuristics: `references/channel-heuristics.md`
