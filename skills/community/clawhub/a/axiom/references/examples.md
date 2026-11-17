# Worked examples

Each example shows the user's words, what the model does, and why.

## 1. Clear request: place the order

User: "Order a 25 lb bag of Acana Adult Recipe dog food from Chewy."

All four pre-flight boxes are checked (store, product, variant = size, intent to buy). Call `place_order`:

```json
{
  "userCommand": "Order a 25 lb bag of Acana Adult Recipe dog food from Chewy.",
  "merchant": { "merchantName": "Chewy", "merchantURL": "https://www.chewy.com" },
  "itemName": "Acana Adult Recipe dry dog food, 25 lb bag"
}
```

Response `status: "in_progress"`, `nextAction: "none"`. Relay `userMessage` (it names the payment method on file and the tracking link) and you are done. Axiom emails the user when the order is confirmed.

No extra confirmation question is needed here: the user asked for a specific item, and Axiom applies their spending rules and requests their approval if the order requires it.

## 2. Vague request: ask first, do not call

User: "Get me some running shoes from On."

Product and required variants (model, size, width, color) are unknown. Do **not** call `place_order`. Ask one question:

"Sure. Which On model, and what size and color? If you have a product link, paste it."

Only after the user answers do you call `place_order`.

## 3. Terse contextual request: resolve from context, include evidence

Earlier in the conversation the user bought "Big Moods Possum Dumpster Fire Sticker" from bigmoods.com. Now: "Get that sticker again."

Resolve from context and pass `intentContext`:

```json
{
  "userCommand": "Get that sticker again.",
  "merchant": { "merchantName": "Big Moods", "merchantURL": "https://bigmoods.com/products/possum-dumpster-fire-sticker" },
  "itemName": "Possum Dumpster Fire Sticker",
  "intentContext": {
    "resolvedUserIntent": "User wants to reorder the Big Moods Possum Dumpster Fire Sticker they bought earlier in this conversation.",
    "evidence": ["Earlier turn: user asked to buy the Possum Dumpster Fire Sticker from bigmoods.com and the order completed."]
  }
}
```

## 4. A question before the order exists: call `place_order` again

`place_order` returns:

```json
{ "status": "needs_clarification", "source": "purchase_request_resolution",
  "question": "Which size?", "options": [{ "optionID": "m", "label": "M", "amount": 125 }, { "optionID": "l", "label": "L" }],
  "nextAction": "ask_user_then_call_place_order",
  "userMessage": "Before I can place this order, I need one more detail: Which size?\n1. M ($125.00)\n2. L" }
```

Relay `userMessage`. User says "Large." Call `place_order` again with `itemName: "… size L"`. Do not call `answer_order_question`; there is no order yet.

## 5. A question about an order: `answer_order_question`

`place_order` (or a later `get_order_status`) returns `status: "needs_answer"`, `orderID: "transaction:1"`, `questionID: "browserpurchaseinput:1"`, options Black / White, and `userMessage` with the question and the numbered options.

Relay it. User says "Black." Call:

```json
{ "orderID": "transaction:1", "questionID": "browserpurchaseinput:1", "selectedOptionID": "option-black" }
```

The reply is usually `in_progress`: relay it and you are done.

## 6. Approval

`get_order_status` returns `status: "awaiting_approval"` with `approvalLink` and `userMessage` "We've emailed you to approve your $123.45 order for … Once you approve, we'll finish it and email you when it's confirmed. You can also approve it here: https://app.useaxiom.ai/approvals/…"

Relay it and stop. The user approves in Axiom; Axiom finishes the order and emails them.

## 7. The user asks how it went

User: "Did my Chewy order go through?" Call `get_order_status` with the `orderID` (or find it with `list_orders`).

`status: "completed"` returns `userMessage` "Your Chewy order is confirmed: order 1234567, $61.18 total. Receipt: https://app.useaxiom.ai/transactions/…". Relay it, optionally with a one-line summary of `receipt.items`.

`status: "in_progress"` means it is still being placed: relay `userMessage` and say Axiom will email when it is confirmed.

## 8. Lost order ID

The conversation was long and you no longer have the `orderID`. Call `list_orders`, find the order by store and date, and pass its `orderID` to `get_order_status`.
