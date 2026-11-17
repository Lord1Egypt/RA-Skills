# Troubleshooting

## Authentication expired or failed

Your MCP client will prompt for sign-in again. Complete it, then retry the tool call. Placing an order and answering a question require the `payments:write` scope; checking and listing orders require `transactions:read`. If a tool is rejected for insufficient scope, disconnect and reconnect Axiom so the client requests the current scope set.

## `account_setup_required` or `email_verification_required`

The user still needs to confirm their email, add a card, a phone number, or a shipping address. `userMessage` already says what is needed and carries the setup link; relay it word for word with the link on its own line. Axiom holds the order for 24 hours (`heldPurchaseID`). When the user says they're done, call `place_order` again with the same details: the held order is placed and the reply carries `resumedFrom`. Do not call again before the user says so.

## `account_restricted`

Orders are unavailable for this account. Relay `userMessage` (it tells the user how to reach support) and stop; do not retry.

## `needs_clarification` keeps coming back

The resolved fields are still ambiguous. Ask the user for the exact missing detail named in `question`, fold the answer into `itemName` (or `merchant`), and call `place_order` once more. Do not loop on `place_order` without a new answer; orders are limited.

## `limit_reached`

Relay `userMessage` exactly. Do not retry, reword the request, or estimate a reset time.

## `mandate_denied`

The request did not pass Axiom's intent or order-policy check (for example, a store or product outside Axiom's policy, or a command that was not clearly a request to buy). Relay the reason and stop. Do not retry the denied request.

## `awaiting_approval`

Send the `approvalLink` and stop. The user approves the order in Axiom; Axiom has emailed them the same link and finishes the order once it is approved. Checking again does not speed anything up.

## The order is `in_progress` for a long time

That is normal: some orders are finished by Axiom's team, and the reply says roughly when. Axiom emails the user when it is confirmed. Relay the latest `userMessage` if the user asks; do not check repeatedly.

## Order `could_not_place` or `cancelled`

Normal outcomes. Relay `userMessage` (it includes the reason when one is safe to share and the Axiom link). Ask the user how they want to proceed.

## Tool call returned `isError: true`

A transport or validation error, not an order outcome. Read `error` and `message`, fix the input (for example, a wrong `orderID` or an invalid store URL), and retry once. If it persists, tell the user Axiom is temporarily unavailable.

## Order not found

`get_order_status` or `answer_order_question` says the order was not found: check the `orderID` from the `place_order` reply, or find it with `list_orders`.

## `answer_order_question` says there is no open question

The question was already answered (perhaps from Axiom's email) or replaced. Call `get_order_status` to see where the order stands.
