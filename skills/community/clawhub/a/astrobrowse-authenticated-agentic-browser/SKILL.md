---
name: astrobrowse-authenticated-agentic-browser
description: "AstroBrowse - Authenticated Agentic Browser: Operate a real, authenticated web browser on the user's. Use when an agent needs astrobrowse authenticated agentic browser, astrobrowse authenticated agentic browser, post and schedule content across social media accounts, pull reports and update records in crms and erps, operate saas platforms and portals that have no api, fill and submit web forms on the user's behalf, close browser, browser session id through AgentPMT-hosted remote tool calls."
version: 1.0.3
homepage: https://www.agentpmt.com/marketplace/astrobrowse-authenticated-agentic-browser
compatibility: "Requires AgentPMT internal handler access through the external marketplace API. Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/astrobrowse-authenticated-agentic-browser"}}
---
# AstroBrowse - Authenticated Agentic Browser

## Freshness
Last updated: `2026-10-02`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Give your AI agent access to the websites and accounts you choose, without ever handing over your passwords. AstroBrowse runs a real, logged-in web browser on your behalf so your agent can work inside the tools you already use: social media, CRMs, ERPs, dashboards, and any SaaS platform or website, including the many that have no API. Save a login once and your agent can resume that session to post content, pull reports, update records, fill forms, download files, and complete multi-step tasks, all in a fresh, single-use browser that is wiped clean when the job is done. If a site ever needs a human touch, like a sign-in confirmation or a quick verification step, AstroBrowse hands you a link to step in for a moment and then lets your agent carry on. You stay in control of which accounts are connected and what the agent is allowed to visit.

## Product Instructions
### AstroBrowse - Authenticated Agentic Browser

Operate a real, logged-in web browser on the user's behalf. The user saves their logins once; you resume those sessions to work inside their accounts without ever seeing a password. Every session is single-use and isolated, and is wiped when you close it.

Full setup guide (Tailscale network egress, enabling the tool, saving a login): https://www.agentpmt.com/docs/tool-specific/astrobrowse

#### Workflow
1. `list_accounts` to see the user's saved logins.
2. `initialize_browser` with a stable `idempotency_key` (required, so a retry never starts a second session) plus `account_id` to resume a saved login, or omit `account_id` for a general-browsing session when the user's policy allows it. Returns a `browser_session_id`.
3. Operate the page with `run_steps` (including drag and tab switching), `extract_page`, `screenshot`, `start_recording` / `stop_recording`, `upload_file`, and `list_downloads` / `download_file`.
4. If a site needs a human (CAPTCHA, MFA, or an unusual login), call `request_user_takeover` then poll `wait_for_takeover`. The user steps in on the live session.
5. Always `close_browser` when finished.

`get_policy` tells you whether general browsing is allowed (`saved_only` | `open` | `open_with_allowlist`). Only the user can change the policy, from their dashboard; there is no agent action to change it.

#### Actions
- `list_accounts` — list saved logins. Call this first.
- `get_policy` — read the browsing policy. It is set only by the user from their dashboard.
- `initialize_browser` — required `idempotency_key`; optional `account_id`, `initial_url`, `region`. Omit `account_id` for a general-browsing session only when the user has enabled it.
- `run_steps` (`browser_session_id`, `steps[]`) — execute 1 to 20 validated steps per request. Supported actions: `goto`, `click`, `click_at`, `hover`, `drag`, `drag_by`, `fill`, `type_text`, `press`, `select`, `wait_for_load_state`, `wait_for_selector`, `wait_for_text`, `snapshot`, `find`, `extract_text`, `extract_html`, `screenshot`, `list_tabs`, and `switch_tab`. Read each result's `ok` and `error`; a batch can return a failed step while the tool call itself succeeds. JavaScript is not supported. Screenshot steps save PNGs to File Manager and return `artifact.file_id` and `artifact.signed_url`.
- `extract_page` (`browser_session_id`, `selector?`, `include_html?`) — return visible text or capped HTML.
- `screenshot` (`browser_session_id`) — save a PNG to File Manager and return `artifact.file_id` plus a fresh seven-day `artifact.signed_url`. Raw image base64 is not returned inline.
- `upload_file` (`browser_session_id`, `selector`, `file_ids[]`) — attach File Manager files to a matching `<input type=file>` on the active tab. Hidden inputs are supported; they do not need to be revealed or clicked first.
- `list_downloads` / `download_file` (`browser_session_id`, `download_name?`) — list completed downloads from any tab, including popup tabs, then save one to File Manager. Use the filename returned by `list_downloads` as `download_name`; wait and list again if the transfer is still in progress.
- `start_recording` (`show_cursor?`) / `stop_recording` — save an MP4 of the session to File Manager. Stop recording before closing.
- `request_user_takeover` (`reason`) / `wait_for_takeover` — hand the live session to the human, then poll for status.
- `status` — return sanitized live status without cookies or credentials.
- `close_browser` — release and wipe the session. Always call when done. Anonymous sessions are discarded because they have no saved login to persist.

#### Working with complex pages
- Start with `snapshot` to read roles and accessible names, or use `find` to search visible text and accessible names. Prefer `role` plus `name` over generated CSS classes. Name matching is a substring by default; set `name_exact: true` when several elements have similar names.
- For canvas drag and drop, identify the source with `selector` or `role`/`name`, then use `drag` with `target_selector`, `target_role`/`target_name`, or viewport `target_x` and `target_y`. Coordinates are useful when a canvas has no accessible drop target. `drag_by` remains available for relative movement.
- Use `list_tabs` after an action opens a new tab, then `switch_tab` with its `tab_index`. Subsequent steps, extraction, screenshots, and file uploads use the selected tab.
- File pickers may hide their file input. Use `upload_file` with the input selector and File Manager `file_ids`; selecting files through the native picker is unnecessary.
- After an export, call `list_downloads` until the completed filename appears, then `download_file`. Downloads opened in popup tabs are included.
- If a step fails, inspect that step's `error` and take a fresh `snapshot` or `list_tabs` before retrying. Missing, hidden, disabled, ambiguous, and timed-out targets report diagnostic details.

#### Safety and execution rules
- Do not attempt to execute JavaScript, inject scripts, access browser internals, or bypass the supported action grammar.
- Each `run_steps` request must contain 1 to 20 steps. Split longer workflows across requests and re-check page state between requests.
- Prefer selectors tied to stable labels, roles, names, or IDs. Use extraction and screenshots to confirm state before consequential actions.
- Use human takeover for CAPTCHA, MFA, login confirmation, or any action that requires the user's judgment.
- Artifact actions (`screenshot`, `download_file`, `stop_recording`, `upload_file`) run inside a workflow with budget context.
- Credentials are never exposed to the agent.
- Sessions are single-use and isolated; closing wipes them.

Full setup and configuration guide: https://www.agentpmt.com/docs/tool-specific/astrobrowse

## When To Use
- Use this skill for `AstroBrowse - Authenticated Agentic Browser` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: astrobrowse   authenticated agentic browser, astrobrowse authenticated agentic browser, post and schedule content across social media accounts, pull reports and update records in crms and erps, operate saas platforms and portals that have no api, fill and submit web forms on the user's behalf, close browser, browser session id.
- Supported action names: `close_browser`, `download_file`, `extract_page`, `get_policy`, `heartbeat`, `initialize_browser`, `list_accounts`, `list_downloads`, `request_user_takeover`, `run_steps`, `screenshot`, `start_recording`, `status`, `stop_recording`, `upload_file`, `wait_for_takeover`.

## Use Cases
- Post and schedule content across social media accounts
- Pull reports and update records in CRMs and ERPs
- Operate SaaS platforms and portals that have no API
- Fill and submit web forms on the user's behalf
- Download invoices statements and files from web apps
- Log in to accounts without sharing passwords with the agent
- Automate multi-step workflows on logged-in websites
- Capture screenshots and screen recordings of web sessions
- Hand off to a human for sign-in or verification steps
- Extract data from pages behind a login
- Edit designs using drag and drop and manage multiple tabs

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `16`.
x402 availability: not enabled for this product.

- `close_browser` (action slug: `close-browser`): Release the session: it is wiped and destroyed. Always call this when finished. Price: `5` credits. Parameters: `browser_session_id`.
- `download_file` (action slug: `download-file`): Persist a file the browser downloaded into the File Manager (size-capped, requires workflow budget context). Pass download_name from list_downloads, or omit it to save the most recent download. Price: `5` credits. Parameters: `browser_session_id`, `download_name`.
- `extract_page` (action slug: `extract-page`): Extract visible text (or HTML) from the active page or a selector. Price: `5` credits. Parameters: `browser_session_id`, `include_html`, `selector`.
- `get_policy` (action slug: `get-policy`): Read the user's browsing policy (saved-only vs general browsing). The policy is set only by the human from their dashboard; there is no agent action to change it. Price: `5` credits. Parameters: none.
- `heartbeat` (action slug: `heartbeat`): Refresh the runtime session's 10-minute idle deadline before long non-browser work. It never extends the 30-minute hard cap. Price: `5` credits. Parameters: `browser_session_id`.
- `initialize_browser` (action slug: `initialize-browser`): Start a fresh, single-use, isolated browser session. Pass a stable idempotency_key (required) so a retry never starts a second session. Provide account_id to resume a saved login, or omit account_id for a general-browsing session (allowed only when the user has enabled general browsing). Call list_accounts first. Price: `5` credits. Parameters: `account_id`, `idempotency_key`, `initial_url`, `region`.
- `list_accounts` (action slug: `list-accounts`): List the user's saved AstroBrowse logins (accounts). Call this first to find a saved site before initialize_browser. Price: `5` credits. Parameters: none.
- `list_downloads` (action slug: `list-downloads`): List files the browser has downloaded in this session (name, size, type) so you can pick one to save with download_file. Price: `5` credits. Parameters: `browser_session_id`.
- `request_user_takeover` (action slug: `request-user-takeover`): Ask the human to take over the live browser (e.g. CAPTCHA, MFA, unusual login UI). Holds the session open past the idle timeout. Use ONLY when the agent cannot proceed automatically. Price: `5` credits. Parameters: `browser_session_id`, `reason`.
- `run_steps` (action slug: `run-steps`): Run bounded browser steps in an initialized session, including navigation, role/name targeting, drag and drop, accessible-name search, screenshots, and tab listing or switching. Price: `5` credits. Parameters: `browser_session_id`, `steps`.
- `screenshot` (action slug: `screenshot`): Capture a PNG screenshot and save it to your File Manager (requires workflow budget context). The image is NOT returned inline; the response has artifact.file_id and a fresh artifact.signed_url for viewing or analysis. Price: `5` credits. Parameters: `browser_session_id`.
- `start_recording` (action slug: `start-recording`): Start an MP4 screen recording of the session. show_cursor controls whether the cursor appears in the video. Price: `5` credits. Parameters: `browser_session_id`, `show_cursor`.
- `status` (action slug: `status`): Return the session's sanitized live status (no cookies). Price: `5` credits. Parameters: `browser_session_id`.
- `stop_recording` (action slug: `stop-recording`): Stop the recording and save the MP4 to your File Manager (requires workflow budget context). The video is NOT returned inline; the response has artifact.file_id — fetch it from the File Manager to view the recording. Call before close_browser. Price: `5` credits. Parameters: `browser_session_id`.
- `upload_file` (action slug: `upload-file`): Attach File Manager files to one input[type=file] on the active tab. Hidden file inputs are supported; pass a selector and file_ids. Price: `5` credits. Parameters: `browser_session_id`, `file_ids`, `selector`.
- `wait_for_takeover` (action slug: `wait-for-takeover`): Poll the session status after request_user_takeover. Price: `5` credits. Parameters: `browser_session_id`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "astrobrowse-authenticated-agentic-browser"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "astrobrowse-authenticated-agentic-browser"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "astrobrowse-authenticated-agentic-browser"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "astrobrowse-authenticated-agentic-browser"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "astrobrowse-authenticated-agentic-browser"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "astrobrowse-authenticated-agentic-browser"
  }
}
```

## Call This Tool
Product slug: `astrobrowse-authenticated-agentic-browser`

Marketplace page: https://www.agentpmt.com/marketplace/astrobrowse-authenticated-agentic-browser

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AstroBrowse---Authenticated-Agentic-Browser",
    "arguments": {
      "action": "close_browser",
      "browser_session_id": null
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "astrobrowse-authenticated-agentic-browser",
  "parameters": {
    "action": "close_browser",
    "browser_session_id": null
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `close_browser` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/astrobrowse-authenticated-agentic-browser
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
