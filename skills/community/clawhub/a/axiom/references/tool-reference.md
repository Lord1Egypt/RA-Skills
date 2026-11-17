# Axiom MCP tool reference

Five tools. Money fields are in dollars unless the field name ends in `Cents` (for example the `maxTipCents` input). An order is identified by its `orderID`; every order tool takes or returns it.

## `get_payment_method`

Returns the payment method saved in the user's Axiom account (brand and last 4 digits only) and whether account setup is complete. Optional before an order: `place_order` performs the same checks and its reply includes `paymentCard`. Use it when the user asks which payment method Axiom has on file.

- Parameters: none.
- Returns: `hasPaymentMethod`, `card {brand, last4}`, `accountSetupComplete`, `missingRequirements[]`, `setupUrl`, `userMessage`, and when setup is incomplete `agentInstructions` and `nextAction`. After setup, `heldPurchaseID` names an order Axiom is holding; this tool never starts it.

## `place_order`

Places an order. Axiom verifies the request against the user's intent and spending rules, then completes the store's checkout on the user's behalf in the background. Replies within about 25 seconds: long enough for a question about the product to come back in the same reply.

- Parameters: `userCommand` (near-verbatim), `merchant {merchantName, merchantURL}`, `itemName` (with variants), optional `itemSubtotal` (dollars), optional `intentContext {resolvedUserIntent, evidence[], resolutionSummary}`, optional `preferences {fulfillment, substitutionsAllowed, maxTipCents, notes}`.
- Returns: `status` (`in_progress`, `needs_answer`, `awaiting_approval`, `completed`, `needs_clarification`, `unavailable`, `mandate_denied`, `limit_reached`, `account_setup_required`, `email_verification_required`, `account_restricted`), `nextAction`, `userMessage`, `agentInstructions`, `isFinal`, `orderID` and `orderUrl` once an order exists, `paymentCard` when known, `question` and `options[]` for questions, `source` (`intent_sufficiency`, `purchase_request_resolution`, `review_demo_catalog`) on `needs_clarification`, `heldPurchaseID` when setup blocked the order, `resumedFrom` when a held order was placed.

## `get_order_status`

Where an order stands, by its `orderID`. Answers immediately. Call it when the user asks about an order, not on a schedule.

- Parameters: `orderID`.
- Returns: the same shape as `place_order`, with `status` one of `in_progress`, `awaiting_approval`, `needs_answer`, `completed`, `could_not_place`, `cancelled` (or `limit_reached` / `mandate_denied` for an order that never started). Plus `approvalLink` and `deadline` when `awaiting_approval`; `questionID`, `question`, `options[{optionID, label, description, amount, imageUrl, productUrl}]`, `allowFreeText`, and `deadline` when `needs_answer`; `receipt {items, taxesAndFees, discounts, shipping, total, orderNumber}` and `finalTotal` when `completed`; `reason` when the order ended without going through.

## `answer_order_question`

Sends the user's answer to a `needs_answer` question and continues the same order. Not for `needs_clarification` or `unavailable` from `place_order`.

- Parameters: `orderID`, `questionID`, and `selectedOptionID` and/or `userInput`.
- Returns: the same shape as `get_order_status` (usually `in_progress`, or `needs_answer` when another question follows).

## `list_orders`

The user's recent orders, newest first.

- Parameters: optional `limit` (1 to 100, default 20).
- Returns: `orders[]` with `orderID`, `status`, `merchant`, `description`, `total` (dollars), `currency`, `createdAt`, `orderUrl`; plus `count` and `total`.

## Field glossary

| Field | Where | Meaning |
|---|---|---|
| `userMessage` | every order response | Text for the end user. Relay as written. |
| `agentInstructions` | every order response | Guidance for you. Never show it. |
| `nextAction` | every order response | One of `none`, `ask_user_then_call_answer_order_question`, `ask_user_then_call_place_order`, `tell_user_unavailable`, `tell_user_complete`, `tell_user_failed`, `tell_user_denied`, `tell_user_limit_reached`, `open_setup_link_then_wait_for_user`, `tell_user_restricted`. |
| `orderID` | order responses, `list_orders` | The order. Pass it to `get_order_status` and `answer_order_question`. |
| `orderUrl` | order responses, `list_orders` | The Axiom page for this order. The link to share with the user. |
| `isFinal` | order responses | True once the order has ended, or when nothing was ordered. |
| `setupUrl` | `account_setup_required`, `email_verification_required`, `get_payment_method` | The Axiom setup page for this user, already inside `userMessage` on its own line. |
| `heldPurchaseID` | `account_setup_required`, `email_verification_required`, `get_payment_method` | The order Axiom is holding for 24 hours until setup completes. Nothing to pass back: the next `place_order` from this user places it. |
| `resumedFrom` | `place_order` | The `heldPurchaseID` this order picked up. The held order ran, not the arguments of the call that resumed it. |
| `approvalLink` | `awaiting_approval` | Where the user reviews and approves the order in Axiom. Axiom emails the same link. |
| `deadline` | `awaiting_approval`, `needs_answer` | When the order times out if nobody approves or answers. `userMessage` already says it in hours. |
| `paymentCard` | `place_order`, when available | `{brand, last4}` of the payment method that will be used. Omitted when Axiom could not read the saved card in time; that does not stop the order. |
