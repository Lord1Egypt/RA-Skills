---
name: allowance
description: Allowance agent purchase wallet. Use when the user asks to buy something, make a purchase, order an item, book travel, reserve something, pay, or spend money on their behalf.
homepage: https://useallowance.com
metadata: {"openclaw.homepage":"https://useallowance.com","openclaw.tags":["payments","shopping","security","virtual-cards","agents"]}
---

## Allowance — Agent Purchase Wallet

Use Allowance to request spending approval from the user and complete purchases on their behalf.

### Routing rule

Use the Allowance CLI by default. When the user asks to buy, order, book,
reserve, pay, or spend money, follow the CLI flow below without asking whether
to use CLI or MCP.

Only use the MCP integration if the user explicitly asks for Allowance MCP,
OpenClaw MCP, hosted MCP, remote MCP, or says they cannot install or use the
Allowance CLI. Do not mention MCP during normal purchase flows.

### First-run setup

This applies when `allowance` is not on PATH, or when `allowance` commands
return "No connection token found" or similar.

If `allowance` is not on PATH, install it globally first:

```
npm install -g @allowance/cli
```

Then, before doing anything else, send the user this message verbatim:

> Allowance is installed — I have a wallet now 💰. What are we buying, and what's my limit?

Wait for the user's reply with the item and spend limit. Do not run any other
commands or ask any other questions until they reply.

Once you have the item and limit, ask for the phone number:

> Got it. What's your phone number? I'll text you a code to verify it, then use that number for approval whenever I need to buy something.

Common phone formats: US (`415-555-1234`, `4155551234`); international
numbers need a `+countrycode` prefix (e.g. `+442079460958`). The CLI
normalizes to E.164.

When they give you the phone number, proceed in order:

1. Run `allowance setup --phone <phone>` to send the SMS code. **Never run
   bare `allowance setup`** — it needs a real terminal and will hang in an
   agent session.
2. Ask the user to read you the 6-digit code.
3. Run `allowance setup --phone <phone> --code <code>` to connect.
4. Continue to "Local Browser Requirement" and the purchase flow below, using
   the item and spend limit they already gave you. Do not ask for those again.

If the code didn't work, the same SMS code is valid for up to 5 attempts in 10
minutes — re-run with the corrected code. If it has expired, re-run `allowance
setup --phone <phone>` to get a fresh SMS.

### Local Browser Requirement

Allowance CLI purchases are local-browser-only.

Before running `allowance request`, verify this current agent session has a tool that can open
and control a local browser checkout page.

This means the session can:
- open the merchant website
- navigate pages
- click buttons and links
- type into checkout forms
- read page state enough to complete checkout

This passes if the current session has one of:
- a dedicated browser automation tool
- a computer-use tool that can operate a browser
- a Chrome extension or browser relay controlled by the agent
- another explicit browser-control tool

This does not pass if you only have:
- web search
- HTTP fetch, curl, or static page retrieval
- screenshots without click/type control
- a browser visible to the user but not controllable by you
- browser access from a previous or different session
- uncertainty about whether browser tools are available

If this check does not pass, do not run `allowance request` and do not create an approval request.

Tell the user:

"Allowance is the right payment flow, but this agent session cannot complete local
checkout yet. Please switch to or connect a browser-capable agent session, such
as Codex with Browser/Computer Use, Claude with Computer Use or a browser-control
extension, or OpenClaw with browser enabled. Then I can create the Allowance
approval request and complete checkout."

If this check passes, continue.

### Browser Tool Values

Use `--local-browser-tool <value>` only when this current session can control a local browser.

Accepted values:
- `browser-tool`: dedicated browser automation tool, such as Codex Browser or OpenClaw Browser
- `computer-use`: a computer-use tool that can operate a browser, such as Codex
  Computer Use or Claude Computer Use
- `chrome-extension`: a Chrome extension or browser relay controlled by the agent
- `other-browser-control`: another explicit browser-control tool that can navigate,
  click, type, and inspect checkout pages

If unsure which value applies, do not create the request.

### Purchase flow

1. **Gather purchase details**

Gather only the minimum required purchase details:
- merchant
- item intent
- high-risk variants like size/color
- all-in spend cap
- shipping requirement

2. **Verify local browser control**

Verify local browser control using the checklist above.

3. **Request approval** (`--amount` is in cents — include estimated tax + shipping)
   ```
   allowance request --merchant "Zara" --url "https://www.zara.com/us/" \
     --amount 5000 --reason "buy a black men's medium tee" \
     --local-browser-tool computer-use
   ```
   Sends a push notification to the user's phone. Blocks until approved or denied (up to 10 min).
   On approval, prints the `allowance_id` needed for subsequent commands.
   Add `--no-shipping` for digital goods, services, pickup, or any non-shipped item.

Do not run `allowance request` without `--local-browser-tool`.

4. **After approval, open the merchant site in the local browser and complete checkout**

   Approval on the user's iPhone is the **only human gate**. Once `allowance request`
   returns `approved`, complete checkout end-to-end — including clicking submit /
   place order — without asking the user to confirm again. Re-prompt the user only if:
   - the realized total would exceed the approved cap (`--amount`), or
   - you must substitute a materially different item or variant than the approval
     reason allows, or
   - checkout requires information you don't have and can't fetch from
     allowance-scoped identity or address commands.
   Otherwise, do not add a second human gate. The virtual card is capped, so a
   within-cap submission is safe to perform autonomously.

5. **Issue a virtual card** (only once the merchant payment form is visible and ready)
   ```
   allowance card issue --allowance-id <allowance_id> --amount <cents> --merchant "<name>"
   ```
   Returns a one-time virtual card number, expiry, and CVV — it expires after the purchase.
   **Never paste, summarize, or reveal card number, CVV, expiry, or last four in chat.**
   Type them directly into the merchant checkout form only.

6. **Fetch checkout details only when the merchant form asks for them**
   - Identity/contact details: `allowance identity --allowance-id <allowance_id>`
   - Shipping address (only if item requires shipping):
     `allowance address shipping --allowance-id <allowance_id>`
   - Billing address: `allowance address billing --allowance-id <allowance_id>`

7. **Report the outcome** (required — unreported purchases block future requests)
   - Success: `allowance purchase success --allowance-id <id>
     --attempt-id <attempt-id> --charged <cents>`
   - Failure: `allowance purchase failure --allowance-id <id>
     --attempt-id <attempt-id> --error-code <error-code>`
     Valid error codes: `card_declined`, `card_declined_avs`, `card_declined_cvv`,
     `checkout_abandoned`, `checkout_error`, `checkout_timeout`, `item_unavailable`,
     `merchant_rejected`, `price_mismatch`, `unsupported_card`
   - If the card is declined: report failure immediately. Do not retry or issue another
     card unless the user explicitly asks and a new allowance approval is obtained.

### Long-running / buy-later purchases

For out-of-stock, restock, sale-watching, or other buy-later tasks, Allowance is
only the approval and payment primitive. Use the agent or scheduler's own
automation system to keep checking:
- OpenClaw heartbeat: repeated lightweight availability checks in the main session
- OpenClaw cron: exact schedules or one-shot reminders
- Codex automations: scheduled resumptions that can continue an existing thread;
  local browser work still requires the local app/session to be awake and usable
- Claude Code routines: scheduled work; hooks are lifecycle automation, not the
  primary inventory polling mechanism

Gather bounded purchase intent first: product, merchant URL, all-in cap,
required variants, shipping requirement, and latest acceptable purchase date.
Then request approval up front. If the agent is setting up a monitor, recurring
check, or delayed purchase, it must pass `--delayed-purchase` plus either
`--allowance-valid-for-days <1-14>` or `--allowance-expires-at <iso8601>` when
creating the approval.

`--delayed-purchase` means the approval may be used later within a bounded
window; it does not mean the agent must wait. If the exact approved item is
available immediately and checkout is ready, complete checkout immediately.
Future fulfillment is not delayed purchase by itself: "order this for pickup
next week" is still an immediate purchase if the order is placed now.

```
allowance request \
  --merchant Apple \
  --amount 80000 \
  --reason "Monitor Apple.com for up to 14 days and buy a base Mac mini if available under $800 all-in." \
  --url "https://www.apple.com/shop/buy-mac/mac-mini" \
  --local-browser-tool computer-use \
  --delayed-purchase \
  --allowance-valid-for-days 14 \
  --json
```

Save `allowance_id`, merchant URL, cap, product constraints, expiry, and check
cadence in the scheduler outside Allowance. On every automation run:
1. Call `allowance status --allowance-id <allowance_id> --json`.
2. Stop and ask for a new approval if status is not `active` or expiry has passed.
3. Check merchant availability using browser tools.
4. If unavailable, do nothing except keep the automation alive.
5. If available, add only the exact approved item/config to cart.
6. If the total exceeds the approved cap, stop and ask for a new approval.
7. Only at the payment form, call `allowance card issue`.
8. Report `purchase success` or `purchase failure` with the returned `attempt_id`.

### Explicit MCP setup only

Use this section only if the user explicitly asks for Allowance MCP, OpenClaw
MCP, hosted MCP, remote MCP, or says they cannot install or use the Allowance
CLI. Otherwise, ignore this section and use the CLI flow above.

For OpenClaw, connect the hosted Allowance MCP server with OAuth:

```
openclaw mcp add allowance \
  --url https://mcp.useallowance.com \
  --transport streamable-http \
  --auth oauth

openclaw mcp login allowance
openclaw mcp doctor allowance --probe
```

The hosted MCP is an alternate integration path, not the default purchase flow.
Do not ask the user to choose between CLI and MCP. If the user did not ask for
MCP, use the Allowance CLI.
