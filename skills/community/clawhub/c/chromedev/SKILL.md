---
name: chromedev
version: 1.0.6
description: Use this skill when you need to access or control a live Chrome browser through the local Chrome DevTools MCP middleware at http://127.0.0.1:8787/mcp, especially for opening pages, extracting rendered content, interacting with DOM elements, taking snapshots, or collecting data from websites.
---

# chromedev

Use this skill when the user wants browser backed data from real web pages through the local `chrome-devtools-mcp` middleware running at `http://127.0.0.1:8787/mcp`.

This skill is for cases where rendered browser state matters, including JavaScript heavy sites, login state in the user's Chrome, interaction flows, screenshots, DOM snapshots, or page data that should come from the live browser instead of plain HTTP fetches.

Connection model
- `chromedev run` is the long lived daemon. It is the layer that keeps the upstream `chrome-devtools-mcp` process attached to Chrome.
- The bundled `http_mcp_call.mjs` script is intentionally short lived. Each invocation only sends a bounded MCP request to the local daemon.
- Do not try to keep a client side MCP HTTP session open in order to preserve Chrome authorization. Chrome authorization belongs to the daemon side connection, not to an individual skill invocation.
- If the daemon is healthy, short lived skill calls should not require Chrome to re-authorize on every request.

Primary behavior
- If the user gives a URL, open it and extract the page content.
- If the page is a list page, return the visible list content in order.
- If the task takes multiple browser steps, emit short progress updates while it runs.

This workflow is otherwise a black box to the user, so visible progress output is required.
Output is not optional in this skill.

## Output rules

1. If the user explicitly asks for 摘要, 总结, 要点, recap, summary, then produce a summary.
2. Otherwise, return extracted page content faithfully and concisely.
3. If paywall or login blocks full text, say what you can see and what is blocked.
4. If a chromedev MCP call fails with errors such as `Not connected`, first inspect with `chromedev doctor`. If it reports stale/orphan chromedev processes or the retry fails, run one recovery cycle with `chromedev stop --all`, then `chromedev run`, and retry the failed page operation once. Only report the error to the user if the retry also fails.

## Progress reporting

Do not send intermediate progress updates to Telegram or any other chat tool.
Focus on producing the final extracted answer or summary directly.
Current agent progress and final user facing answer must not trigger extra chat-tool delivery side effects.
When the final extracted answer or summary is ready, deliver the final answer once.
The final extracted answer or summary must not be streamed token by token.
Buffer the final answer first, then send it as one complete final output.

Timeline guarantee
- If a step fails, emit the failure status immediately and stop or recover.
- If a step is waiting on external input, emit the waiting status immediately when the wait begins.
- The final answer must be the terminal visible success output.
- The final answer must be sent in one completed block, not as a streaming preview.

Progress message constraints
- Never include the original URL, any raw link, or full page text in any auxiliary status text.
- Do not restate or recap completed progress steps after the final answer is ready.
- Do not append a trailing success/progress line after the final answer.
- Do not use streaming progress text as the vehicle for the final answer body.
- Do not call `openclaw message send` for this workflow.
- Do not send intermediate status messages to Telegram or any chat tool.
- The final extracted answer or summary itself should be the only user visible success output.
- The final extracted answer or summary must not be followed by any extra progress, recap, completion, or status line.
- The final extracted answer or summary must be delivered non-streaming.

Bad pattern, do not do this
- Do not send `完成`, `成功`, `已提取`, or similar status text after the final answer body.
- Do not use a progress update as the container for the final answer.
- Do not stream the final summary or final extracted answer line by line or token by token.
- Do not let the final answer remain inside a draft/preview message lifecycle.
- Do not call `openclaw message send` or any equivalent chat-tool delivery command during this workflow.

## Preconditions

- Check the npm published version once at the start of the session with `npm view @mallocfeng/chromedev version`. Then check the local CLI version with `chromedev version`. If `chromedev` is missing, the local version command is unavailable, or the npm version is newer than the local version, install the explicit npm version with `npm install -g @mallocfeng/chromedev@<npm-version>`, then continue. Do not repeat this check for every page task unless a command call fails.
- Check whether the local middleware is already running on `127.0.0.1:8787`. If it is not running, start it automatically with `chromedev run`, then re-check the endpoint before using MCP tools.
- If the endpoint exists but MCP calls fail with `Not connected` or similar connection/binding errors, run `chromedev doctor` first. If there are orphan/multiple `chrome-devtools-mcp` processes or the retry fails, run one recovery cycle: `chromedev stop --all` → `chromedev run` → retry once.
- On first connection, Chrome may show a remote debugging authorization prompt. Wait up to 30 seconds for the user to approve it.
- Treat HTTP session errors and Chrome attachment errors differently. A missing MCP HTTP session does not by itself mean Chrome authorization was lost.

Quick endpoint check
```bash
curl -i http://127.0.0.1:8787/mcp
```

A response like `400 Bad Request` with `No sessionId` means the endpoint exists and is healthy.
This is expected because the daemon serves short lived stateless HTTP requests while keeping the upstream Chrome connection alive in the background.

## Workflow

1. Confirm the latest npm version once per session with `npm view @mallocfeng/chromedev version`, then compare it with `chromedev version`. If the local command is missing, too old to print a version, or older than npm, force install the explicit npm version with `npm install -g @mallocfeng/chromedev@<npm-version>`.
2. Confirm the middleware is running. If not, run `chromedev run` and then re-check `http://127.0.0.1:8787/mcp`.
3. Connect to `http://127.0.0.1:8787/mcp`.
4. If any MCP tool call fails with connection-style errors such as `Not connected`, `target closed`, or similar startup/binding failures, run `chromedev doctor` to check for stale daemon state or multiple DevTools clients. Then try exactly one recovery cycle if needed: `chromedev stop --all` → `chromedev run` → retry the original page operation once.
5. If the user explicitly provided a URL, open the target page first with `new_page`. Do not try to recover by opening a blank page or any synthetic page.
6. For explicit URL tasks, do not call `list_pages` before the first `new_page`.
7. After `new_page`, assume the new tab is already the selected page. Do **not** call `list_pages/select_page` unless `take_snapshot/evaluate_script` fails with a "no selected page" or similar error.
8. If the user did not provide a URL and wants the current page or an existing tab, then inspect current pages and select the right page.
9. Prefer `evaluate_script` for a **fast, bounded** extraction (title/byline/time/body) first, then fall back to `take_snapshot` when the DOM is hard to parse or blocked.
10. Use `wait_for` only when the page is still loading and you know a stable text or UI state to wait on (keep it short).
11. Return extracted data, not protocol noise.
12. Once the final answer body is ready, buffer the full final answer and deliver only that final answer as one complete non-streaming output.

## How to interpret requests

When the user gives a URL, treat it as a request to read that page.

- Open the target page directly first.
- Do not attempt recovery by opening `about:blank` or any placeholder page.
- Do not inspect existing pages before the first `new_page` for explicit URL tasks.
- If the user asks for summary, return a summary.
- If the user asks for page content, return extracted content.
- If the user asks for list content, return the visible list items in order.

## Preferred tool order

- For explicit URL tasks: `new_page`.
- Then: `evaluate_script` (fast extract, keep output bounded).
- Fallback: `take_snapshot` (slower, but robust when the DOM is messy).
- For current-page or existing-tab tasks: `list_pages`, then `select_page`.
- `wait_for` only when you have a reliable, small string to wait on.
- `take_screenshot` only when visuals matter.

## Command line client

The npm package includes a reusable request client exposed through:
- `chromedev call <tool_name> [json_arguments]`

It connects to the local HTTP MCP endpoint and calls one tool.
Prefer `chromedev call` because it uses the request client bundled with the installed npm package and does not depend on the current skill directory containing a scripts folder.

This skill source also includes the same reusable script for development:
- `scripts/http_mcp_call.mjs`

The script is not the persistent connection holder. It is only a request client for the already running local daemon.

When using `chromedev call`, the npm package's bundled dependencies should be used automatically. Only install `@modelcontextprotocol/sdk` in the current workspace if you intentionally run `scripts/http_mcp_call.mjs` directly and the dependency is missing.
```bash
WORKSPACE="$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)"
cd "$WORKSPACE" && npm install @modelcontextprotocol/sdk
```

## Common commands

Check and install the latest published `chromedev`
```bash
REMOTE_VERSION="$(npm view @mallocfeng/chromedev version 2>/dev/null || true)"
LOCAL_VERSION="$(chromedev version 2>/dev/null | sed -E 's/^.*@([0-9]+\.[0-9]+\.[0-9]+).*$/\1/' || true)"

if [ -z "$REMOTE_VERSION" ]; then
  echo "Could not read @mallocfeng/chromedev version from npm"
elif [ -z "$LOCAL_VERSION" ] || node -e 'const [l,r]=process.argv.slice(1); const a=l.split(".").map(Number); const b=r.split(".").map(Number); process.exit(b[0]>a[0] || (b[0]===a[0] && b[1]>a[1]) || (b[0]===a[0] && b[1]===a[1] && b[2]>a[2]) ? 0 : 1)' "$LOCAL_VERSION" "$REMOTE_VERSION"; then
  npm install -g "@mallocfeng/chromedev@$REMOTE_VERSION"
  hash -r 2>/dev/null || true
fi
```

Start the service if the endpoint is not already listening
```bash
curl -s -o /dev/null http://127.0.0.1:8787/mcp || chromedev run
```

Recover from a stuck/not-connected session
```bash
chromedev doctor
chromedev stop --all
chromedev run
```

List current pages
```bash
chromedev call list_pages
```

Open a page
```bash
chromedev call new_page '{"url":"<URL>","timeout":30000}'
```

For explicit URL tasks, do this first. Do not begin by opening `about:blank` or any recovery page.

Get a snapshot
```bash
chromedev call take_snapshot
```

Extract title and a bounded article body (fast path)
```bash
chromedev call evaluate_script '{"function":"() => {\n  const pick = () => document.querySelector(\"article\") || document.querySelector(\"main\") || document.body;\n  const el = pick();\n  const text = (el?.innerText || \"\").replace(/\\s+\\n/g, "\\n").trim();\n  return {\n    title: document.title,\n    url: location.href,\n    byline: document.querySelector(\"[data-testid=byline]\")?.innerText || document.querySelector(\".byline\")?.innerText || \"\",\n    time: document.querySelector(\"time\")?.getAttribute(\"datetime\") || document.querySelector(\"time\")?.innerText || \"\",\n    text: text.slice(0, 20000),\n    textLength: text.length\n  };\n}"}'
```

Note: never forward raw URL in Telegram progress messages.

Wait for specific text
```bash
chromedev call wait_for '{"text":["<TEXT>"],"timeout":30000}'
```

## Extraction guidance

- Fast path first: use `evaluate_script` to extract a bounded body string (e.g. `article`/`main` innerText) plus title/byline/time, then summarize from that.
- Fallback: use `take_snapshot` for readable page content and structure when extraction is blocked or the DOM is hard to parse.
- Use `evaluate_script` for precise fields, arrays, links, prices, tables, or JSON shaped output.
- Use `wait_for` only if a page is visibly still loading and you know a reliable text to wait on.
- For list pages, preserve order and return item text and link targets.
  - Link targets are allowed in the final user facing extraction output.
  - Link targets are never allowed in Telegram progress messages.
- For article pages, extract title, author, publish date when visible, then the article body text.

## Operational notes

- Keep browser state intact unless the user asked for navigation or interaction.
- If a tool call hangs near connection start, assume Chrome may be waiting for the authorization dialog.
- Prefer returning concise extracted data over full raw snapshots unless the user asked for raw output.
- Do not expose the local MCP endpoint outside `127.0.0.1`.
- Do not treat a per call MCP HTTP session as the source of truth for Chrome attachment. The daemon process is the long lived connection holder.
- Do not send Telegram progress updates during this workflow.
- Do not send a final Telegram/chat-tool success status after the final extracted answer or summary is ready.
- In Telegram-like channels with stream previews, never stream the final answer through the preview channel; finalize the content first and then send the final answer once.
