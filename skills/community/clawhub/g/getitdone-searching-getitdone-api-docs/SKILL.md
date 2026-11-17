---
name: searching-getitdone-api-docs
description: "Answers questions about the GetItDone developer API from its own documentation. Use when the user asks 'what does the 429 problem code mean in the GetItDone API', 'how do I authenticate against the GetItDone API', 'how does this GetItDone REST endpoint work', 'where is the GetItDone API reference', 'how do I connect an integration to GetItDone', or wants GetItDone developer docs. Reads documentation only."
---

# GetItDone developer docs lookup

Answer developer questions from GetItDone's published documentation, with links, instead of from memory.

## Connecting and calling the tools

Every tool in this skill comes from the `getitdone` MCP server, the GetItDone connector, and is written here as `getitdone:<tool>`.

- **Tools listed by name:** call them directly, for example `getitdone:list_tasks`.
- **Only `getitdone:search_tools` and `getitdone:execute_typescript` listed (Code Mode, the default):** call `getitdone:search_tools` first, then call each tool inside `getitdone:execute_typescript` as `external_<tool>` (for example `external_list_tasks`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `getitdone:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects GetItDone and approves that scope.
- **No `getitdone` tools at all:** GetItDone is not connected yet. Install the GetItDone power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

If the tool list shows only `getitdone:search_tools` and `getitdone:execute_typescript`, the server is in Code Mode: call the operation below inside `getitdone:execute_typescript` as `external_search_docs`.

- `getitdone:search_docs`: ranked results from GetItDone's developer documentation (REST operations, error and problem codes, guide pages), each with its public URL and, for guide and error pages, a Markdown-twin URL.

## Workflow

1. Turn the question into a short query: the operation name, the status or problem code, or two or three keywords.
2. Call `getitdone:search_docs`.
3. If the top result is a guide or error page and the snippet is not enough, fetch its Markdown-twin URL to read the full page.
4. Answer in a few sentences. Quote the exact field names, codes, and paths from the docs.
5. End with the public URL of each page you used.

## Rules

- `getitdone:search_docs` searches GetItDone's developer documentation, not the user's tasks or workspace notes. For task content, use `investigating-tasks`.
- If nothing relevant comes back, say the docs do not cover it. Do not fill the gap with guessed endpoints or fields.
- Keep API keys and tokens out of examples. Use placeholders.
- This skill only reads the docs. Never call `getitdone:create_task`, `getitdone:update_task`, `getitdone:complete_task_occurrence`, `getitdone:link_task_dependency`, or `getitdone:archive_task` from it.
