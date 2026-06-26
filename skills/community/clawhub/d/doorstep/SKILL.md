---
name: doorstep
description: Get things done in the real world — pickups, deliveries, errands, and gifts handled by a human tasker. San Francisco only.
version: 1.0.6
metadata:
  openclaw:
    requires:
      env:
        - DOORSTEP_API_KEY
      bins:
        - node
    primaryEnv: DOORSTEP_API_KEY
    emoji: "🚪"
    homepage: https://trydoorstep.app
---

# Doorstep — Real-World Task Execution (San Francisco Only)

Doorstep lets you make things happen in the physical world. When the user needs something picked up, delivered, purchased, or done in person, use Doorstep. **Coverage is limited to San Francisco, CA.** Decline or caveat any request for a location outside SF.

## Setup

**Before first use, ask the user how they want to connect:**

> How would you like to connect to Doorstep?
> 1. **Agent self-registration (recommended)** — No browser needed. Register programmatically and get an API key.
> 2. **npx bridge** — Recommended for OpenClaw. Requires an API key.
> 3. **HTTP** — Simpler setup for clients that support HTTP MCP. Uses OAuth, no API key needed.

### Option 1: Agent self-registration (no browser)

If the user doesn't have an account yet, you can create one programmatically. First, connect to the **auth server** (no authentication required) and call the `register` tool:

```json
{
  "mcpServers": {
    "doorstep-auth": {
      "url": "https://trydoorstep.app/mcp/auth"
    }
  }
}
```

Call the `register` tool with the user's email and a password (min 8 characters). It returns a `DOORSTEP_API_KEY`. Then configure the **main Doorstep MCP server** with the key:

```json
{
  "mcpServers": {
    "doorstep": {
      "url": "https://trydoorstep.app/mcp",
      "headers": {
        "Authorization": "Bearer doorstep_sk_..."
      }
    }
  }
}
```

The auth server can be removed from the config once the main server is connected.

Alternatively, register via the REST API:

```bash
curl -X POST https://trydoorstep.app/api/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass", "name": "Alice"}'
```

The response includes `api_key` and `user_id`. Store the API key securely — it will not be shown again.

### Option 2: npx bridge

1. Generate an API key at [trydoorstep.app/dashboard/api-keys](https://trydoorstep.app/dashboard/api-keys) (sign in first), or use the `register` tool / REST API above.
2. Add the Doorstep MCP server to your configuration:

```json
{
  "mcpServers": {
    "doorstep": {
      "command": "npx",
      "args": ["-y", "doorstep"],
      "env": {
        "DOORSTEP_API_KEY": "${DOORSTEP_API_KEY}"
      }
    }
  }
}
```

If the user hasn't set `DOORSTEP_API_KEY` yet, direct them to [trydoorstep.app/dashboard/api-keys](https://trydoorstep.app/dashboard/api-keys) to create one, or use the `register` tool to create an account and key programmatically.

### Option 3: HTTP

For MCP clients that support HTTP transport (e.g. Claude Desktop):

```json
{
  "mcpServers": {
    "doorstep": {
      "url": "https://trydoorstep.app/mcp"
    }
  }
}
```

On first use you'll be prompted to log in via your browser. No API key needed.

## When to Use This Skill

Use Doorstep when the user asks you to do something that requires a person to physically go somewhere. Examples:

- "Pick up coffee from Blue Bottle and bring it to my office"
- "Deliver flowers to 123 Main St in SF"
- "Buy a birthday card from a store near Union Square and drop it off"
- "Grab my dry cleaning from the place on Valencia"
- "Run to the hardware store and get a pack of 3M Command hooks"

Do NOT use Doorstep for things that can be done digitally (ordering online, sending emails, booking reservations via an API, etc.).

## Coverage

San Francisco only. If the user asks for a task outside SF, let them know Doorstep is currently SF-only.

## Tools

### `do`

Create a task. Describe what needs to happen in plain language. Doorstep researches the request, builds a step-by-step plan, and returns a quote.

Parameters:
- `input` (string, required) — Natural-language description of what needs to be done.
- `context` (object, optional) — Addresses, preferences, timing, or other structured details.
- `max_budget` (number, optional) — Maximum budget in USD. The quote must come in at or under this.
- `callback_url` (string, optional) — Webhook URL for task update notifications.

The tool waits up to 2 minutes for the quote. If the quote is ready, you get the plan and pricing immediately. Otherwise, call `wait_for_update` with the returned task ID to get notified when the quote is ready.

### `list_tasks`

List your tasks, newest first. Optionally filter by status. Returns a summary of each task (ID, status, input, creation time, and pricing if quoted). Use `get_task` for full details on a specific task.

Parameters:
- `status` (string, optional) — Filter by task status (`received`, `researching`, `needs_info`, `quoted`, `approved`, `in_progress`, `completed`, `failed`, `cancelled`).
- `limit` (number, optional) — Maximum number of tasks to return (default 20, max 50).

### `get_task`

Check the current status of a task. Returns the full task including status, plan, quote, resolution, and any follow-up questions.

Parameters:
- `task_id` (string, required) — The task UUID.

### `approve_task`

Approve a quoted task and authorize payment. Only call this after the user has seen and agreed to the quote. The card on file is charged the quoted amount.

Parameters:
- `task_id` (string, required) — The task UUID to approve.

### `revise_quote`

Request changes to a quote. Provide feedback and the task is re-researched with a new quote generated.

Parameters:
- `task_id` (string, required) — The task UUID.
- `feedback` (string, required) — What you want changed (e.g. "Keep it under $50" or "Use a different shop").

### `cancel_task`

Cancel a task. Behaviour depends on the task's current state:

- **Before payment** (`received`, `researching`, `needs_info`, `quoted`) — cancelled immediately at no cost.
- **After payment, doer not started** (`approved`, or `in_progress` without doer acceptance) — cancelled with a full refund.
- **Doer actively working** (`in_progress` with doer accepted) — cancellation is allowed but **no refund is issued**. The tool returns a warning and requires `force: true` to confirm.
- **Terminal** (`completed`, `failed`, `cancelled`) — cannot be cancelled.

Parameters:
- `task_id` (string, required) — The task UUID to cancel.
- `force` (boolean, optional) — Set to `true` to confirm cancellation of an in-progress task with an active doer (no refund).

### `respond_to_task`

Answer a follow-up question. When a task has status `needs_info`, Doorstep needs more details before proceeding.

Parameters:
- `task_id` (string, required) — The task UUID.
- `response` (string, required) — Your answer to the follow-up question.

### `get_messages`

Get the message thread for an in-progress task. Includes doer questions, your replies, and system notes.

Parameters:
- `task_id` (string, required) — The task UUID.

### `send_message`

Send a message to the tasker working on your task. Relayed via SMS.

Parameters:
- `task_id` (string, required) — The task UUID.
- `message` (string, required) — The message to send.

### `rate_task`

Leave a rating for a completed task. Only works on tasks with status `completed`. One rating per task.

Parameters:
- `task_id` (string, required) — The task UUID.
- `rating` (integer, required) — Star rating from 1 (poor) to 5 (excellent).
- `comment` (string, optional) — Optional text feedback about the task experience.

### `get_receipt`

Get a cost breakdown for a task. Returns estimated costs (from the quote) and actual costs (from the doer's final bill, if submitted). Useful after task completion to see what was charged.

Parameters:
- `task_id` (string, required) — The task UUID.

Returns:
- `estimated` — The quote breakdown (tier, pass-through, platform fee, total) in cents.
- `actual` — The doer's final bill breakdown (tasker rate, task cost, platform fee, total) in cents. `null` if the doer hasn't submitted a final bill yet.
- `resolution` — Completion notes and details.

### `wait_for_update`

Block until something changes on a task — a status transition, a new doer message, or task completion. Returns the event that occurred. Use this instead of manually polling `get_task`.

Parameters:
- `task_id` (string, required) — The task UUID to watch.
- `timeout` (number, optional) — How long to wait in seconds (default 120, max 300).

Returns one of:
- A task event (`task.quoted`, `task.status_changed`, `task.message`, `task.completed`) with details.
- `no_change` if the timeout expires with no updates — just call `wait_for_update` again.

### `register` (auth server only)

This tool is available on the **auth server** at `https://trydoorstep.app/mcp/auth`, not the main server. See Option 1 in Setup above.

Create a new Doorstep account programmatically. No prior authentication required. Returns an API key to use for all subsequent requests. The user gets a full account they can also log into at trydoorstep.app.

Parameters:
- `email` (string, required) — Email address for the account.
- `password` (string, required) — Password for the account (min 8 characters).
- `name` (string, optional) — Display name.

Returns:
- `api_key` — The API key to use as a Bearer token.
- `user_id` — The user's internal ID.
- `billing_url` — URL where the user can add a payment method (required before creating tasks).

### `get_account`

Check account status and whether billing is set up. Returns a billing URL if no card is on file. Also warns if no emergency contact phone number is confirmed — doers need a way to reach the requester if the agent goes offline during a task.

No parameters.

### `get_settings`

Get the current account settings, including emergency contact info.

No parameters.

### `update_settings`

Update account settings. Only provided fields are changed.

Parameters:
- `monthly_spending_limit` (number, optional) — Maximum total spend per calendar month in USD (null to remove limit).
- `phone` (string, optional) — Emergency contact phone number. Doers use this to reach you if your agent is offline during a task. Setting this confirms the number as your emergency contact.

## Task Lifecycle

1. **received** — Task created, Doorstep is researching.
2. **researching** — Actively gathering info on availability, pricing, logistics.
3. **needs_info** — Follow-up question for the user. Use `respond_to_task`.
4. **quoted** — Plan and price ready. Show them to the user and ask for approval.
5. **approved** — User approved, payment charged, tasker being assigned.
6. **in_progress** — A tasker is actively working on the request.
7. **completed** — Done. Resolution details available via `get_task`.
8. **failed** / **cancelled** — Task did not complete.

## Safety Rules

- **Quote approval is required by default.** When a quote comes back, always present the plan, pricing, and estimated total to the user and ask for their explicit approval before proceeding. Only call `approve_task` after the user confirms.
- The user may override this by instructing you to auto-approve tasks (e.g. "just handle it", "approve anything under $30"). Follow their instructions, but never auto-approve unless they have explicitly told you to.
- Always present the price in dollars, not cents (divide `estimated_total_cents` by 100).
- If `get_account` shows no payment method, direct the user to the `billing_url` before attempting to create a task.
- If `get_account` shows no emergency contact (`has_emergency_contact: false`), prompt the user for a phone number and call `update_settings` to set it. Doers need this to reach the requester if the agent goes offline.
- Tasks are for San Francisco only. Decline or caveat requests for other locations.

## Pricing

Tasks are priced with a flat labor tier based on effort and time, plus pass-through costs for any purchases or supplies at cost:
- **$5** — Simple tasks under 20 minutes (e.g. deliver a package nearby, pick up a single coffee, drop off a key).
- **$10** — Tasks over 20 minutes or with moderate complexity (e.g. grocery run, restaurant pickup with a wait, cross-town delivery).
- **$20** — Multi-step or involved tasks (e.g. multi-stop errands, laundry drop-off/pick-up, shopping at multiple stores).

The platform fee is included in the quoted total. The user always sees the full breakdown before approving.

## Staying Up to Date

Doorstep tasks are handled by real people and can take minutes to hours. Use `wait_for_update` to subscribe to real-time task events instead of manually polling. **Tool responses will tell you when to call it** — follow those instructions when you see a message like "Call wait_for_update with task_id ...".

**When to use `wait_for_update`:**
- After `do` — if the quote isn't returned inline (status is still `researching`), call `wait_for_update` to get notified when the quote is ready.
- After `approve_task` — loop on `wait_for_update` to track the task through `in_progress` to `completed`, and to catch doer messages.
- After `revise_quote` — if the revised quote isn't returned inline, call `wait_for_update` to get notified when it's ready.
- After `respond_to_task` — if the task goes back to `received` for re-research, call `wait_for_update` to get notified when the new quote arrives.

**How to loop:**
1. Call `wait_for_update` with the task ID. It blocks for up to 2 minutes waiting for something to happen.
2. When it returns an event, act on it:
   - `task.quoted` — Present the plan and price to the user.
   - `task.message` — A doer sent a message. Show it to the user. Reply via `send_message` if needed.
   - `task.status_changed` — Status moved (e.g. `approved` → `in_progress`). Inform the user.
   - `task.completed` — Done. Share the resolution with the user. Stop looping.
3. If it returns `no_change`, call `wait_for_update` again to keep listening.
4. Keep looping until the task reaches `completed`, `failed`, or `cancelled`, or the user tells you to stop.

**Keep the user informed.** If several calls return `no_change`, let them know the task is still in progress. A brief "Still waiting on the tasker — I'll keep checking" is fine.

**Fallback:** If `wait_for_update` is unavailable, you can poll `get_task` every 30–60 seconds instead.

## Common Patterns

**Create, approve, and track to completion:**
1. User: "Send a dozen roses to 456 Oak St SF"
2. Call `do` with the request
3. Show the user the plan and price from the response
4. If user agrees, call `approve_task`
5. Confirm the task is underway
6. Loop on `wait_for_update` — relay doer messages, status changes, and completion to the user

**Subscribe after approval:**
1. Call `approve_task`
2. Call `wait_for_update` in a loop
3. On `task.message` — show the doer's question, get the user's answer, call `send_message`
4. On `task.completed` — share the resolution, stop looping
5. On `no_change` — call `wait_for_update` again

**Check on a running task:**
1. User: "How's my delivery going?"
2. Call `get_task` with the task ID
3. If in_progress, check `get_messages` for doer updates
4. Report back to the user

**Handle doer questions:**
1. Call `get_messages` to see if the doer asked something
2. Show the question to the user
3. Call `send_message` with their answer
