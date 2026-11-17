---
name: editing-page-drafts
description: "Edits the draft of a BioFlow link-in-bio page: adds, changes, removes, or reorders links, images, products, newsletter signups, booking embeds, and other blocks, renames a page, or creates a new page. Use when the user asks to 'add a link to my YouTube channel', 'update my bio link page', 'rename my page title', 'move the newsletter block to the top', 'remove this link', 'create a new link in bio page', or edit their creator landing page. Changes the draft only; never publishes."
---

# Edit a BioFlow page draft

Make the user's page changes on the draft. The live page does not change until the user publishes through the `publishing-pages` skill.

## Connecting and calling the tools

Every tool in this skill comes from the `bioflow` MCP server, the BioFlow connector, and is written here as `bioflow:<tool>`.

- **Tools listed by name:** call them directly, for example `bioflow:page.list`.
- **Only `bioflow:search_tools` and `bioflow:execute_typescript` listed (Code Mode, the default):** call `bioflow:search_tools` first, then call each tool inside `bioflow:execute_typescript` as `external_` plus the tool name with dots swapped for underscores (for example `external_page_list` for `bioflow:page.list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `bioflow:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects BioFlow and approves that scope.
- **No `bioflow` tools at all:** BioFlow is not connected yet. Install the BioFlow power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `bioflow:page.list`: the account's pages with slug, public URL, and publish status.
- `bioflow:page.get`: one page's draft and published summaries, the ordered block list, and the `expectedUpdatedAt` snapshot token every write needs.
- `bioflow:page.create`: create a new page.
- `bioflow:page.update_draft`: change page-level fields on the draft, such as the title.
- `bioflow:page.add_block`: append a block to the draft. Returns the new block id.
- `bioflow:page.remove_block`: remove named blocks from the draft. It refuses full-page clears.
- `bioflow:page.reorder_blocks`: change the order of the draft's blocks.

## Workflow

1. Call `bioflow:page.list`. If the account has more than one page and the user did not name one, ask which.
2. Call `bioflow:page.get` and show the current block order in one short list so the user can refer to blocks by position or name.
3. Restate the change in one line ("Add a link block 'YouTube' to https://youtube.com/@name at the end"). For `bioflow:page.remove_block` and `bioflow:page.update_draft`, which delete or overwrite draft content, wait for the user's explicit yes before the write.
4. Call `bioflow:page.get` again right before each write and pass its fresh `expectedUpdatedAt`. Then call the write tool.
5. After each write, report what changed in the draft and the new block id where one was returned.
6. When the user is done, say the changes are in the draft only and offer the `publishing-pages` skill.

## Rules

- Never call `bioflow:page.publish` or `bioflow:page.schedule_publish` from this skill.
- On `STALE_SNAPSHOT`, nothing was written. Call `bioflow:page.get`, show the user what changed, and repeat the write only if it still makes sense.
- Do not invent URLs, product details, or handles. Ask for the link when a block needs one.
- To empty a page, remove blocks by name one at a time after the user confirms the list. There is no clear-all operation.
- If the write tools are missing, the user did not grant the page write scope. Say so and tell them to reconnect with it.
