---
name: axiom_wallet
description: Use Axiom Wallet via MCP to manage payment methods, review account activity, and complete user-requested purchases through Axiom's server-managed browser checkout.
metadata:
  {
    'openclaw':
      {
        'homepage': 'https://clawhub.ai/axiom-wallet/axiom',
        'requires': { 'bins': [{ 'name': 'mcporter', 'version': '>=0.8.0' }] },
      },
  }
---

# Axiom Wallet

Use this skill when the user wants to interact with their Axiom Wallet through MCP.

Axiom Wallet can be used to:

- check the payment method on file
- review recent transactions
- start a server-managed browser checkout for a user-requested purchase (charged to the card on file)

The Axiom MCP endpoint is:

`https://mcp.useaxiom.ai/mcp`

## When to use this skill

Use Axiom Wallet when the user asks you to:

- buy or pay for something with Axiom
- check their Axiom payment method or account info
- inspect recent Axiom transactions

Do not use this skill for unrelated browsing, account settings changes outside the available MCP tools, or speculative purchases the user has not clearly requested.

## Authentication

For the full authentication guide, see [`references/authentication.md`](references/authentication.md).

**Quick summary:**

1. Register Axiom: `mcporter config add axiom --url https://mcp.useaxiom.ai/mcp`
2. Start auth: `mcporter auth axiom --reset --oauth-timeout 300000 --log-level info` (runs in background, prints the OAuth URL)
3. Parse the OAuth authorize URL from mcporter's log output
4. Navigate to that URL with a headless browser: `agent-browser open "<URL>"` (or `browser-use open "<URL>"`)
5. Read the **activation URL** from the rendered page: `agent-browser eval "document.querySelector('a[href*=\"activate\"]')?.href"`
6. Send the activation URL to the user to approve on their phone
7. mcporter completes the OAuth exchange automatically when the user approves
8. Verify: `mcporter call axiom.get_payment_method`

> **Important:** The OAuth authorize URL and the activation URL are different. The agent navigates to the authorize URL; the user opens the activation URL. Never send the authorize URL to the user. See the auth doc for examples of both.

To clear cached tokens: `mcporter auth axiom --reset`

Starting a purchase and submitting a clarification require the `payments:write` OAuth scope; polling
purchase status requires `payments:read`. If a purchase tool is rejected for insufficient scope,
reset auth and reconnect so the client requests the current scope set.

## Available tools

- `get_payment_method` — returns the card on file (brand and last 4 digits only). Use this to verify a payment method exists before attempting a purchase.
- `list_transactions` — lists recent transactions (optional `limit`, most recent first).
- `make_purchase` — the purchase entry point. Validates the request, resolves product/variant availability when possible, creates the intent mandate, and starts Axiom's server-managed browser checkout. Requires `userCommand` (near-verbatim), `merchant` (`merchantName`, `merchantURL`), `itemName`, optional `itemSubtotal`, and optional `preferences`. Returns immediately with `status` — never waits on the browser pipeline.
- `get_purchase_status` — polls a browser purchase started by `make_purchase`. Pass `browserPurchaseSessionID` and omit `timeoutMs` (or use the longest timeout your client supports). It blocks until the next parked or terminal status change, then returns it: public `progressStage` / `progressLabel`, approval links, clarification requests, terminal outcomes, receipt, and cart details. It does not stream incremental progress — call it again in a loop. End-to-end purchases often take around 10–15 minutes.
- `submit_purchase_clarification` — submits the user's answer when `get_purchase_status` returns `status: "awaiting_user_input"`. Pass `browserPurchaseSessionID`, `userInputRequest.requestID`, and either `selectedOptionID`, `userInput`, or both. Then continue polling `get_purchase_status`.
- `get_transaction` — fetches a single transaction by ID, including its status, merchant, amount, approval state, receipt, and audit trail. Use it to revisit a completed purchase or inspect history.

## Making a purchase

Axiom runs the entire checkout server-side. You resolve the request and start it; Axiom handles cart acquisition, checkout, contact/shipping entry, delivery selection, payment authorization, card entry, order-outcome detection, and receipt capture. You never see or enter card details.

1. Verify payment method.
   - Call `get_payment_method` so the user can confirm which card on file will be charged.
   - If no payment method exists, tell the user to add a card in their Axiom account settings and stop.

2. Resolve the purchase request.
   - Keep `userCommand` near-verbatim from the user — it is the audit/intent record. Don't paraphrase, and don't fold resolved specifics into it (those go in `itemName` / `merchant.*`).
   - Resolve `merchant.merchantName`, `merchant.merchantURL`, and `itemName` as specifically as your context allows (prior turns, profile, memory). Never invent.
   - Prefer a product detail URL when the user gave one or you can defend one; otherwise use the merchant homepage URL you have.
   - Include required variants in `itemName` when known (size, color, storage, flavor, quantity, etc.).
   - Pass `itemSubtotal` (dollars, pre-shipping/tax/fees) when the user states a budget or the price is already known; it caps the line-item total at payment time.
   - Don't invent missing product-critical details. The flow can return a clarification or unavailable response before opening a browser session.

3. Call `make_purchase`.
   - If `status: "running"`, save `browserPurchaseSessionID` and `transactionID`, then call `get_purchase_status`.
   - If `status: "needs_clarification"`, present `question` and any `options` to the user verbatim. If `source: "intent_sufficiency"` or `source: "purchase_request_resolution"`, fold the user's answer into the resolved fields and call `make_purchase` again.
   - If `status: "unavailable"`, present `reason`, `question`, and any `options` / `availableOptions` to the user. Only call `make_purchase` again after the user chooses an available option or changes the request.
   - If `status: "mandate_denied"`, tell the user the returned `reason` and stop. This is a normal domain outcome, not an MCP tool failure.
   - If `status` is `failed`, `cancelled`, or `human_needed`, surface the returned `reason` / `message`. These are normal terminal outcomes, not MCP tool failures.

4. Poll `get_purchase_status`.
   - Continue polling until `status` is `completed`, `awaiting_approval`, `awaiting_user_input`, `human_needed`, `failed`, or `cancelled`.
   - For `running`, use `progressStage` and `progressLabel` for user-facing progress. Do not expose or infer internal browser task/phase names.
   - For `awaiting_approval`, send the user `approvalLink` and continue polling after they approve.
   - For `awaiting_user_input`, present `userInputRequest.question` and any `userInputRequest.options` to the user, then call `submit_purchase_clarification` with `browserPurchaseSessionID`, `userInputRequest.requestID`, and the selected option or free-text answer.
   - For `completed`, summarize `receipt`, `finalTotal`, and `cart`. Cart amounts are already public dollar values; do not expect raw cents fields.
   - For `human_needed`, `failed`, or `cancelled`, tell the user what happened from the returned `reason` / `message`.

## Safety and behavior rules

- Verify a payment method is on file before starting a purchase.
- Never claim a purchase succeeded unless `get_purchase_status` returns `completed`.
- If spending rules, approval requirements, or policy checks block the purchase, stop and tell the user what happened.
- If `make_purchase` returns `mandate_denied`, stop and tell the user the reason — do not retry with reworded inputs to work around the denial.
- Never bypass approval flows; send the user the `approvalLink` and wait for them to approve.
- Never expose OAuth tokens, session details, cookies, or browser state.
- Never fabricate merchant, amount, tax, shipping, receipt, or transaction details — report only what the tools return.

## Troubleshooting

### `mcporter` not found or outdated

`mcporter` ≥0.8.0 must be installed and available on PATH. Check with `mcporter --version`. OpenClaw checks required binaries at skill load time.

### Auth expired or failed

Reset and re-run the auth flow:

```bash
mcporter auth axiom --reset
```

### Cross-device approval timed out

Start a fresh auth flow and send the new approval link or activation code.

### No payment method on file

Tell the user to add a card in their Axiom account settings and stop.

### Purchase needs your approval

`get_purchase_status` returned `awaiting_approval` with an `approvalLink`. Send the user the link and keep polling; the flow resumes after they approve.

### Mandate denied

`make_purchase` returned `mandate_denied` — e.g. the merchant is in a prohibited category, or the request was not clearly a purchase. Tell the user the returned reason and stop. Do not re-run with reworded inputs.

### Purchase failed or needs a human

`get_purchase_status` returned `failed`, `cancelled`, or `human_needed`. Surface the returned `reason` / `message` to the user; these are normal terminal outcomes, not MCP tool failures.
