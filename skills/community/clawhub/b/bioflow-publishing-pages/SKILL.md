---
name: publishing-pages
description: "Publishes or schedules a BioFlow page's draft so it goes live, after showing a preview of what changes and getting the user's confirmation. Use when the user asks to 'publish my page', 'go live', 'push my changes live', 'schedule my page to go live Monday at 9am', 'make my link in bio public', or 'update the live page'. Needs the workspace publishing setting plus a two-step confirmation."
---

# Publish a BioFlow page

Take the draft live, now or at a set time, through BioFlow's two-step publish. The first call only previews; the user's confirmation is what commits.

## Connecting and calling the tools

Every tool in this skill comes from the `bioflow` MCP server, the BioFlow connector, and is written here as `bioflow:<tool>`.

- **Tools listed by name:** call them directly, for example `bioflow:page.list`.
- **Only `bioflow:search_tools` and `bioflow:execute_typescript` listed (Code Mode, the default):** call `bioflow:search_tools` first, then call each tool inside `bioflow:execute_typescript` as `external_` plus the tool name with dots swapped for underscores (for example `external_page_list` for `bioflow:page.list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `bioflow:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects BioFlow and approves that scope.
- **No `bioflow` tools at all:** BioFlow is not connected yet. Install the BioFlow power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `bioflow:page.list`: find the page and its public URL.
- `bioflow:page.get`: the draft and published summaries, so you can describe what differs.
- `bioflow:page.publish`: publish the draft now. Two-step: a call without `confirmToken` returns a preview of exactly what would go live plus a short-lived `confirmToken` and publishes nothing; a second call carrying that token commits.
- `bioflow:page.schedule_publish`: schedule the draft to publish at `startsAt`, an ISO 8601 timestamp in the future. Same two-step contract: the first call schedules nothing and returns a preview and `confirmToken`; the second call carries the same `startsAt` plus the token.

## Workflow

1. Call `bioflow:page.list` and confirm which page the user means.
2. Call `bioflow:page.get` and summarize what is in the draft but not yet live.
3. For a scheduled publish, resolve the time to a full date and time in the user's timezone, state it, and convert it to an ISO 8601 `startsAt`.
4. Call `bioflow:page.publish` or `bioflow:page.schedule_publish` without a `confirmToken`. Nothing goes live on this call.
5. Show the user the preview the tool returned, in plain words: which blocks are added, changed, or removed, and the page title. For a schedule, repeat the time.
6. Ask for an explicit yes. Do not treat silence, "ok, looks fine", or an earlier request as confirmation.
7. After a clear yes, call the same tool again with the `confirmToken`. Report the result and the page's public URL.

## Rules

- The preview is the expected first response, not a failure. Never say "publish did nothing" after step 4.
- Never pass a `confirmToken` the user has not approved in this conversation, and never reuse a token.
- The token expires after 10 minutes. An expired, malformed, or mismatched token is refused with `CONFIRM_TOKEN_INVALID`, and a draft change in between is refused with `STALE_SNAPSHOT`. In either case start again at step 4 and show the new preview.
- On `DANGEROUS_OPS_DISABLED`, publishing is turned off for the workspace. Give the user the settings link from the response (Settings, Connected AI apps) and stop. Only the user can turn it on.
- If the publish tools are missing, the user did not grant the `publish` scope. Say so and tell them to reconnect with it.
