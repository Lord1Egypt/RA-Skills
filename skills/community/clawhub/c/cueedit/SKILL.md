---
name: cueedit
description: Run Instagram and Facebook Pages from the agent with CueEdit (cueedit.io). Use when the user wants to reply to Instagram or Facebook comments, DM everyone who commented a keyword like "LINK" on a reel, set up a comment-to-DM auto reply (ManyChat-style keyword automation), pause or resume an Auto DM rule, find unanswered comments, or message a Facebook Page commenter on Messenger. Triggers on "instagram", "reel", "auto dm", "comment reply", "manychat", "dm everyone who comments", "comment to dm", "facebook page comments".
license: MIT
compatibility: Needs network access to https://www.cueedit.io. Works through the CueEdit MCP server (OAuth or API key) or plain HTTPS with the CUEEDIT_API_KEY environment variable and Node 18+.
metadata: {"author":"IndianAppGuy","version":"1.0.0","homepage":"https://www.cueedit.io/?ref=skill","openclaw":{"emoji":"📩","homepage":"https://www.cueedit.io/?ref=openclaw","primaryEnv":"CUEEDIT_API_KEY","requires":{"bins":["node"],"env":["CUEEDIT_API_KEY"]},"envVars":[{"name":"CUEEDIT_API_KEY","required":true,"description":"CueEdit API key (ce_live_...) from cueedit.io Settings > API keys"}]},"hermes":{"tags":["instagram","facebook","social-media","auto-dm"],"category":"social-media"}}
required_environment_variables:
  - name: CUEEDIT_API_KEY
    prompt: CueEdit API key (ce_live_...)
    help: Create one at https://www.cueedit.io/dashboard/settings under API keys
    required_for: the CLI path (not needed if the CueEdit MCP server is connected with OAuth)
---

# CueEdit: let the agent run Instagram and Facebook Pages

CueEdit connects to the user's own Instagram professional account and Facebook Pages through Meta's official APIs. With it you can:

- read posts and comments, and find the ones nobody has answered yet
- reply to comments in public
- DM the person who commented (Instagram private reply / Facebook Messenger private reply)
- create Auto DM rules: "when someone comments LINK on this reel, DM them the link", then pause or resume them

Writes (reply, DM, rules) need a CueEdit Pro plan. Reads work on the free plan.

## 1. Connect (pick ONE path)

Rule: if the `CUEEDIT_API_KEY` environment variable is set (check with `test -n "$CUEEDIT_API_KEY" && echo set`), use path B. Otherwise use path A. If an MCP call is blocked or fails and the key is set, switch to path B.

**A. MCP server (when the agent has the CueEdit MCP connected).**
URL: `https://www.cueedit.io/api/mcp/mcp` (streamable HTTP).
- OAuth: just add the URL. The agent opens a CueEdit sign-in, the user clicks Allow.
- API key: send `Authorization: Bearer $CUEEDIT_API_KEY` as a header.
Tool names: `list_accounts`, `list_posts`, `list_comments`, `reply_to_comment`, `send_dm`, `schedule_reel`, `list_scheduled_posts`, `cancel_scheduled_post`, `list_autodm_rules`, `create_autodm_rule`, `set_autodm_rule_status`, `list_facebook_pages`, `list_facebook_posts`, `list_facebook_comments`, `reply_to_facebook_comment`, `send_facebook_dm`.

**B. REST with an API key (any agent that can run a shell).**
The user creates a key at https://www.cueedit.io/dashboard/settings → API keys and sets `CUEEDIT_API_KEY=ce_live_…`. Then use the bundled CLI (no install, Node 18+):

```bash
node scripts/cueedit.mjs accounts
node scripts/cueedit.mjs posts --limit 5
node scripts/cueedit.mjs comments <media_id> --unhandled
```

Every MCP tool below has a CLI twin, so the workflows in section 4 work on both paths:

| MCP tool | CLI |
|---|---|
| `list_accounts` / `list_facebook_pages` | `accounts` / `fb-pages` |
| `list_posts` / `list_facebook_posts` | `posts` / `fb-posts` |
| `list_comments` / `list_facebook_comments` | `comments <media_id> --unhandled [--keyword LINK --all-pages]` / `fb-comments <post_id> …` |
| `reply_to_comment` / `reply_to_facebook_comment` | `reply <comment_id> --text "…"` / `fb-reply …` |
| `send_dm` / `send_facebook_dm` | `dm <comment_id> --text "…"` / `fb-dm …` |
| `create_autodm_rule` / `list_autodm_rules` / `set_autodm_rule_status` | `rule-create --dm "…" --keywords LINK --media <id>` / `rules` / `rule-status <id> active\|paused` |

Add `--account <id>` (Instagram) or `--page <id>` (Facebook) when several are connected. Run `node scripts/cueedit.mjs help` for every flag. The full endpoint list is in [references/api.md](references/api.md). Never print, log or echo the API key, and never ask the user to paste it into chat if they can set the env var themselves.

**No account yet?** Send the user to https://www.cueedit.io/signup?ref=skill to sign up, connect Instagram (and optionally a Facebook Page), then create the key or approve the OAuth screen.

If a list call returns `connect_url`, nothing is connected yet: show that link, ask the user to connect, and stop.

If both paths are available (an MCP connection AND `CUEEDIT_API_KEY`), they may be signed in to different CueEdit users. When the account the user names is missing from one, check the other before saying it is not connected.

## 2. Always start here

1. `list_accounts` (Instagram) and/or `list_facebook_pages` (Facebook). Note `plan` and `can_send`.
2. If more than one account or Page comes back, ask which one, and pass its `account_id` / `page_id` on every later call.
3. If `can_send` is false, say writes need CueEdit Pro (https://www.cueedit.io/pricing?ref=skill) and continue with reads only.

## 3. Safety rules (non-negotiable)

- **Show, then ask.** Before ANY reply, DM or rule change, show the user the exact text and the target (account, post, how many people). Wait for an explicit "yes". A yes covers that one batch, not future ones.
- **Instagram link-DM limit.** Send at most ~50 DMs that contain a link per Instagram account per day from the agent, even though the API allows more. Instagram flags accounts that send many link DMs in a short burst. For bigger lists, do 50 today and offer to continue tomorrow, or set up an Auto DM rule (it sends as comments arrive, which Instagram treats as normal replies).
- **Stop at the first refusal.** If any DM or reply fails (401, 402, 429, 502, or a Meta error such as "user cannot receive messages"), stop the batch, report what was sent and what failed, and ask before continuing. Only two errors may be skipped while you keep going: `already_dmed` (409) and `comment_too_old` (422).
- **Pace writes.** Leave about 5 seconds between DMs in a batch.
- **Only DM people who commented.** Meta allows one private reply per comment, within 7 days of the comment. Never try to DM people who did not comment, and never use `force` unless the user asks for a second DM to the same person.
- **Own accounts only.** Act only on accounts the signed-in user connected. Never test on a client's account.

## 4. Workflows

### "DM everyone who comments LINK" (Auto DM rule)
1. `list_posts` and let the user pick the reel (or "all posts").
2. Draft the DM: one short line + the link. Optional public reply ("Sent, check your DMs") and optional follow gate (`require_follow`).
3. Show: keyword(s), match mode (contains vs exact), posts, DM text, public reply text. Get a yes.
4. `create_autodm_rule` with `keywords: ["LINK"]`, `trigger_mode: "keyword"`, `match_mode: "any"`, `media_ids: [<id>]`, `dm_message`, and if wanted `auto_reply_enabled: true` + `comment_replies: [...]` (up to 3, one picked at random).
5. `list_autodm_rules` to confirm it is `active`. The rule only catches NEW comments.
6. Offer the catch-up: people who already commented in the last 7 days are not covered by the rule; run the next workflow for them.

### Catch up: reply to and DM people who already commented
1. `list_comments` with `media_id` and `unhandled_only: true`; page through `next_cursor`. Filter by keyword yourself if needed (case-insensitive contains).
2. Report: total, how many match, how many are `dm_eligible` (7 days or newer, not yet DMed).
3. Show the exact DM text and public reply text, plus the count (cap at 50 link DMs today). Get a yes.
4. For each eligible comment: `send_dm`, then (if wanted) `reply_to_comment`. ~5 s apart. Stop at the first real refusal.
5. Report: sent, skipped (too old / already DMed), failed.

### Reply to comments
1. `list_comments` with `unhandled_only: true`.
2. Draft replies (match the user's tone; short; no hashtags). Show them as a numbered list. Get a yes, or edits.
3. `reply_to_comment` for each approved one.

### DM one commenter
Find the comment with `list_comments`, show the DM, get a yes, `send_dm`. If it returns 422 `comment_too_old`, explain Meta's 7-day window; a public reply is still possible.

### Facebook Pages
Facebook Page messaging is still waiting on Meta App Review, so Facebook replies and DMs only work for CueEdit accounts that Meta has approved for testing; if they fail with a permissions error, say that plainly. Same flows with `list_facebook_pages` → `list_facebook_posts` → `list_facebook_comments` → `reply_to_facebook_comment` / `send_facebook_dm` (the DM lands in the commenter's Messenger, one per comment, 7-day window). Auto DM rules are Instagram only today.

### Not supported yet
Reel scheduling: the server still lists `schedule_reel`, `list_scheduled_posts` and `cancel_scheduled_post`, but scheduled reels cannot publish today (a Meta publishing permission is pending). Do not use them; tell the user to post the reel in Instagram and come back for the comment and DM side.

## 5. Errors

| Code | Meaning | What to do |
|---|---|---|
| 401 `unauthorized` | Bad or missing key | Ask the user to create a key or reconnect OAuth |
| 402 `upgrade_required` | Free plan | Writes need Pro: https://www.cueedit.io/pricing?ref=skill |
| 409 `already_dmed` | This comment already got a DM | Skip |
| 422 `comment_too_old` | Older than Meta's 7-day private-reply window | Skip; public reply still works |
| 429 `rate_limited` | Hourly cap (600/h) | Stop, retry in an hour |
| 502 `instagram_error` / `facebook_error` | Meta refused | Stop the batch, show the message; if it has `reconnect_url`, show it |

## 6. Examples

See [references/examples.md](references/examples.md) for five real prompts and the outputs they produced.
