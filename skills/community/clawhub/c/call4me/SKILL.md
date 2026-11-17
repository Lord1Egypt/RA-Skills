---
name: call4me
description: "Your AI agent phones businesses for you: books, reschedules, cancels, asks, and waits on hold."
version: 1.0.0
homepage: https://call4.me
metadata:
  openclaw:
    homepage: https://call4.me
    emoji: "📞"
---

# call4me

[Website: call4me](https://call4.me) · [MCP setup](https://call4.me/mcp) · [Source skill](https://github.com/skeptrunedev/call4me/blob/main/chatgpt-plugin/skills/get-started/SKILL.md)

Your AI agent phones businesses for you: books, reschedules, cancels, asks, and waits on hold.

## Setup and pricing

Connect the remote MCP server at https://call4.me/mcp using streamable HTTP. Sign in through the browser with Google or X. No local server install is needed. A call4me account and prepaid credits are required to make calls; credits start at $10. The skill itself is free.

Before following the workflow, ensure the call4me MCP tools are connected and available. If they are not available, guide the user to [MCP setup](https://call4.me/mcp); do not pretend to place a call.

## Workflow

call4me phones businesses for the user: restaurant bookings, vet and salon appointments, car service and dealership questions, home services, flight changes, and questions for any business. A natural-sounding caller talks to the business and reports back with the outcome and a transcript.

1. Call `call4me_get_balance`. Show the balance and minutes left. If the account has call4me numbers, show them and suggest saving them as a contact named call4me: calls go out from these numbers, and businesses call back on them. If there are none yet, explain that a US number is assigned on the first call.
2. Call `call4me_get_profile`. If it is missing things, ask the user in one message for their full name, phone, email, and home address (and car details if they want car calls), then save the answers with `call4me_save_profile`. Skip anything they decline.
3. Ask what they want called for. Pick the category, call `call4me_get_requirements`, and ask in one message for everything it lists that you don't know yet. Find the business's number and check it is the right location.
4. Confirm with the user, then place the call with `call4me_place_call`. Follow it with `call4me_get_call` (wait_seconds: 30) until it finishes. If it shows an open question, the business is waiting on the line: answer right away with `call4me_answer_question`.
5. Tell the user the result in a line or two.

Only call businesses and services the user wants to reach, never personal numbers.
