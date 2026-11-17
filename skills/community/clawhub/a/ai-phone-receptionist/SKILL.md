---
name: ai-receptionist
description: "Give a business a phone number that an AI answers: a greeting that says it is an AI, opening hours, messages taken with a full transcript, and follow-up by ticket or email. Use when the person wants an AI receptionist, a virtual receptionist, a phone answering line or missed calls handled. Runs on Conecto, a paid service: numbers from $2.00 a month and $0.25 per started minute, on credit the owner bought. US and Canada numbers."
metadata:
  openclaw:
    homepage: https://conecto.chat/solutions/ai-receptionist?from=clawhub
---

# AI receptionist

This skill lets you, the agent, give a small business a phone number that answers its calls. Conecto hears the caller and speaks. You choose the number, the greeting, the hours and the voice, and after each call you get the whole transcript to act on. The phone line runs on Conecto's servers and reaches you as tools on one MCP server.

Conecto is a paid service, and the phone is the one part of it that free credit does not pay for. The owner has to add money once before you can rent a number (see Money).

## Two ways the line answers

- Taking messages. This is the default. The line greets the caller, asks for their message, name and number, and you get the transcript when the call ends.
- Answering live. Each thing the caller says is sent to an https endpoint, with the conversation so far, and the endpoint answers with what to say within about 2.5 seconds. After 8 seconds without an answer the line takes a message instead. Choose this only if the person runs an endpoint that answers that fast. This skill does not set one up.

Either way the greeting tells callers they reached an AI, and Conecto first plays a short notice that the call is recorded and transcribed.

## Connect once

If `openclaw mcp status` already lists `conecto`, skip this section.

Ask the person to run these in a terminal, or run them yourself if they say so:

```bash
openclaw mcp add conecto \
  --url https://api.conecto.chat/v1/mcp \
  --transport streamable-http \
  --auth oauth
openclaw mcp login conecto
openclaw mcp doctor conecto --probe
```

`openclaw mcp login conecto` opens Conecto's sign-in in the browser. A new business creates its account first at https://conecto.chat/account/signup?from=clawhub-ai-receptionist. On the sign-in page the person ticks the areas you may use, for this skill Phone, and Help desk if messages should become tickets, and allows it. You then run on a key of your own that the owner can revoke. No key goes in this skill or in an environment variable. `doctor --probe` should list the `phone_` tools.

## Set up the line

1. Find a number. `phone_search_numbers` lists numbers the business can rent right now, with the monthly price and a quote for each. Pass `area_code` or `city` for a local number. It is free, and a quote lasts 30 minutes.
2. Rent it. Show the person the number and its monthly price, and wait for a yes. Then pass the quote to `phone_rent_number`. The call pays the first month, and the number renews monthly from the balance. If it answers `payment_required`, the balance is still free credit and the owner has to top up once.
3. Say how it answers. `phone_setup_assistant` sets the greeting, the hours, the voice and whether the line takes messages or answers live. The first time, pass `greeting` and `timezone`. The greeting must say the caller reached an automated line or an AI, for example "Hi, you've reached Halverson Cycle. This is our automated line: how can we help?" A greeting without that is refused with `greeting_needs_ai_disclosure`.
4. Check it. `phone_get_assistant` shows whether the numbers are answering right now, and if not, why. It also lists the voices.

The business can keep its own number and forward it to the rented one.

## After each call

- `phone_list_calls` lists calls, newest first: who, when, how long and what each cost, missed ones included.
- `phone_get_call` returns one call with its whole transcript.
- `account_events` reports `phone.message_left` and `phone.call_ended` as calls end.
- With `open_tickets` set in `phone_setup_assistant`, each message left opens a help desk ticket with the transcript, for $0.01.

Then do what the caller asked for: tell the owner, open a ticket, or note the call on the customer's record. Ask before you email or call anyone back.

## Money

- A number costs $2.00 to $25.00 a month, quoted per number.
- An answered call costs $0.25 per started minute. While a call runs, the line holds the longest call the settings allow at that rate.
- Setting up costs $0.001. A message filed as a ticket costs $0.01. Reading calls and transcripts is free.
- A message taken while the balance is empty is free.
- The phone runs only on credit the owner bought. The $1.00 of free credit and the bonus on a first top-up pay for Conecto's other tools, not for numbers or minutes.
- Only a person adds money, on the account page (https://conecto.chat/account), from $5.00 plus a fee of 7% + $0.35.
- A call that fails costs nothing. Every reply from a tool carries `cost_usd` and `balance_usd`.

## Before you act

- Ask before you rent a number, since it renews every month, and before you release one with `phone_release_number`, since that gives it back for good.
- Ask before you change the greeting or the hours.
- Never write a greeting that passes the line off as a person.
- The owner can make chosen tools wait for a person's approval. Such a call answers `approval_required`, and the request goes to the approver.

## Limits

- Agents can rent numbers where the carrier asks for no identity documents, which includes the US and Canada. For other countries `phone_search_numbers` says why not.
- An account rents up to 5 numbers.
- If the balance runs short at renewal, the number has 7 days of grace and is then released.
- This skill covers incoming calls.

## More

- Every phone tool with its inputs, an example and its errors: https://conecto.chat/tools/phone.md
- Every error code: https://conecto.chat/docs/errors.md
- Prices: https://conecto.chat/pricing.md
- Terms: https://conecto.chat/terms
