---
name: analyzing-page-performance
description: "Reports how a BioFlow link-in-bio page performs and who it captured: views, link clicks, CTR, top links, referrers, tip revenue, newsletter and lead signups, contacts, and uploaded files. Use when the user asks 'how did my page do last month', 'who signed up through my page', 'which links get the most clicks', 'where does my traffic come from', 'show my bio link analytics', or 'list my leads'. Read-only."
---

# BioFlow page insights

Read the workspace's analytics, captured leads, and uploaded files, and turn them into a short, honest report. Read only.

## Connecting and calling the tools

Every tool in this skill comes from the `bioflow` MCP server, the BioFlow connector, and is written here as `bioflow:<tool>`.

- **Tools listed by name:** call them directly, for example `bioflow:page.list`.
- **Only `bioflow:search_tools` and `bioflow:execute_typescript` listed (Code Mode, the default):** call `bioflow:search_tools` first, then call each tool inside `bioflow:execute_typescript` as `external_` plus the tool name with dots swapped for underscores (for example `external_page_list` for `bioflow:page.list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `bioflow:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects BioFlow and approves that scope.
- **No `bioflow` tools at all:** BioFlow is not connected yet. Install the BioFlow power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `bioflow:analytics.summary`: aggregated views, clicks, CTR, top links, referrers, and tip revenue for the workspace.
- `bioflow:contacts.list`: the leads the page has captured, with how each was captured (for example a newsletter signup or a file gate).
- `bioflow:file.list`: the files uploaded to the account.
- `bioflow:page.list`: page names and public URLs, so numbers can be tied to a page.

## Workflow

1. Agree the window (default: the last 30 days). Call `bioflow:analytics.summary` for it.
2. Report in this order: views, clicks, CTR, the top links with their click counts, the top referrers, then tip revenue if there is any.
3. If the user asks about signups or leads, call `bioflow:contacts.list` and give the count, the split by capture method, and the most recent entries.
4. If the user asks about files or gated downloads, call `bioflow:file.list` and list the files by name.
5. Close with at most three concrete suggestions drawn from the numbers, such as moving the most clicked link higher. Offer the `editing-page-drafts` skill to make the change.

## Rules

- Only report numbers the tools returned. If a metric is not in the response, say it is not available.
- Do not compare against industry benchmarks; there are none in the data.
- Contacts are personal data. Show only what the user asked for, and do not copy the full list into the chat unless they ask.
- This skill only reads. Never call `bioflow:page.create`, `bioflow:page.update_draft`, `bioflow:page.add_block`, `bioflow:page.remove_block`, `bioflow:page.reorder_blocks`, `bioflow:page.publish`, or `bioflow:page.schedule_publish` from it.
