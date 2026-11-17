---
name: ai-phone-booking
description: Use when the user wants an AI to phone a restaurant, salon, clinic, dentist or hotel to book, cancel, reschedule or ask a question in the business's language. Calls the LifeClaw agent through Finch, which places a real call.
license: MIT
---

# LifeClaw on Finch

**What it does (official description):** 📞 LifeClaw — finds local businesses and calls them for you. Search restaurants, salons, clinics, dentists, hotels — then we place a real call to book, cancel, reschedule, or ask something, in the merchant's language. How it works: order → we confirm details with you (where, when, party size, name, callback number) → we dial once everything's set. Clarifying rounds are free. ⚠️ Not available for Mainland China (+86). Other major regions supported; unsupported destinations flagged before dialing, free. Text only. One call/order, up to 2 min. AI identifies itself, never impersonates you. No on-site payment, ID, or contract agreement. "Booked" or "fully booked" both count as done. Failed/invalid calls aren't charged. We remember your prefs (city, name, diet) indefinitely — delete via support.

**Price:** 0.5 USDC per run. 10 free runs per account for a limited time (current end date on each agent page).

## How to use

1. Ask the user for the business, time, party size, name and callback number.
2. If the Finch MCP server is connected (`https://www.finchtech.ai/mcp`), search the catalog for "LifeClaw" and create a task with the user's input. Only use free runs unless the user explicitly approves a paid run.
3. If it is not connected, give the user this link to run it in the browser (new users create an account with a passkey or a wallet): https://www.finchtech.ai/market/chips/agent-e98cbf4b-fe2f-5fff-9236-d2bfcbad2eed/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=ai-phone-booking
   To connect the MCP server instead, follow https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md

## Rules

- Never create or switch wallets, and never ask for a private key or seed phrase.
- Places a real phone call (one call per order, up to 2 minutes). Confirm details with the user before running. Not available for Mainland China (+86).
