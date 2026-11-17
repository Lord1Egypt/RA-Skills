---
name: commerceai-shopping
description: Search the US product catalog, compare products, and answer product questions through the CommerceAI MCP tool `shopping_agent`. Use when the user wants to find, compare, or ask about products to buy, such as "earbuds under $50" or "compare these two". Not for carts, orders, checkout, coupons, or markets other than US.
---

# CommerceAI shopping

CommerceAI exposes one MCP tool, `shopping_agent`, at `https://commerceai.ai/mcp/` (Streamable HTTP, header `Authorization: Bearer $COMMERCEAI_API_KEY`). If the tool is not connected, point the user to the setup steps at https://github.com/CommerceAI-ai/CommerceAI to add the server.

## When to call it

- The user wants product recommendations: "a standing desk for a small room under $300".
- The user wants to compare products you already showed: "compare the first two on weight".
- The user asks about a product you already showed: "does this one come with a charger?".
- The user refines an earlier search: "only ones in black".

Do not call it for carts, orders, order tracking, checkout, coupons or vouchers, store account sign-in, image input, or markets other than US. The tool refuses these.

## How to call it

1. First request: send `query` only. Put the user's full request in natural language, including budget, brand, and must-have features.
2. Follow-ups: send the new `query` with the `conversation_id` from the last line of the previous result.
3. To compare or ask about specific products, also send their `item_id` values (the `[pr_...]` at the start of each product line) in `selected_item_ids`, at most 10, together with the same `conversation_id`.
4. A call takes 20 to 40 seconds, up to about 2 minutes. Wait for it; do not call again in parallel for the same request.

## How to use the result

- The text result lists each product as `[item_id] name · price · rating/5 · merchant · purchase_url`, and comparisons as Markdown tables. Answer from it and keep the links, so the user can buy on the merchant's page.
- If the agent asks a clarifying question, relay it to the user and send their answer as the next `query` with the same `conversation_id`.
- If nothing matched, suggest loosening the budget, brand, or specs.
- Prices and availability can change. Tell the user to confirm the final price on the merchant's page.

## Errors

- HTTP 401: the API key is missing or invalid. Ask the user to set `COMMERCEAI_API_KEY`; never ask them to paste the key into the chat.
- `INSUFFICIENT_CREDITS`: tell the user to top up in the CommerceAI console.
- `RATE_LIMITED`, `SHARED_CAPACITY`, `UPSTREAM_TIMEOUT`: wait `retry_after_seconds` if given, retry at most twice.
- `CONVERSATION_EXPIRED`, `NOT_FOUND`, or a stale `item_id`: start a new search without `conversation_id`.

Each completed turn costs the user credits for its input tokens, output tokens, and tool calls (around 30 credits plus token usage; 1 credit = $0.001). `usage.credits_used` reports the exact amount. Refusals and errors are free.
