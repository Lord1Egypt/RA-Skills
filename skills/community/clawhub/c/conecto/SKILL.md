---
name: conecto
description: "Business tools for your OpenClaw agent through one MCP server: a CRM, email inboxes, phone numbers it answers, invoices and bookkeeping, a booking calendar, e-signatures and a help desk. Conecto is a paid service, charged per tool call from a prepaid balance."
metadata:
  openclaw:
    homepage: https://conecto.chat/agents/openclaw
---

# Conecto

Conecto gives you, the agent, the systems a small business runs on: its CRM, email inboxes, phone line, invoices and books, booking calendar, e-signatures, help desk and more. They run on Conecto's servers and reach you as tools on one MCP server, `https://api.conecto.chat/v1/mcp`. Conecto is a paid service: each tool call is charged to the business's prepaid balance (see Money).

## Connect once

Ask the person to run these in a terminal, or run them yourself if they say so:

```bash
openclaw mcp add conecto \
  --url https://api.conecto.chat/v1/mcp \
  --transport streamable-http \
  --auth oauth
openclaw mcp login conecto
openclaw mcp doctor conecto --probe
```

`openclaw mcp login conecto` opens Conecto's sign-in. The person signs in (a new business creates its account at https://conecto.chat/account/signup first), ticks the areas you may use and allows it. You then run on a key of your own that acts as that person, and no key goes in this skill or in an environment variable. `doctor --probe` should list Conecto's tools.

## What you can do

Each area is a set of tools. Before you call a tool for the first time, read its page at `https://conecto.chat/tools/<area>/<tool>.md`: its inputs, an example call, a real reply and its errors.

- CRM: contacts, companies, deals, notes and tasks (`crm_search`, `crm_save_contact`, `crm_save_deal`).
- Email: inboxes on the business's own subdomain that you send from and read (`email_send`, `email_list_messages`).
- Phone: numbers in the US and Canada that you answer, with a transcript of every call (`phone_search_numbers`, `phone_setup_assistant`).
- Invoices and books: quotes, invoices, expenses and the books behind them (`invoices_create`, `invoices_send`, `books_record_expense`).
- Calendar: booking pages and meetings (`calendar_find_times`, `calendar_book`).
- E-signature: documents sent for signing (`esign_send`).
- Help desk: tickets from email and chat (`ticket_create`, `ticket_list`).
- Also forms, files, projects, HR, hiring, inventory, purchasing, newsletters, website chat and more. Every area and tool: https://conecto.chat/tools.md

## Money

- Every tool has a published price on its page. Examples: $0.01 for a CRM change, $0.001 per email recipient, $0.10 for an invoice sent, $0.01 for a meeting booked, $0.20 for a document sent for signing, $0.25 per started minute of an answered call.
- Reading the business's own data is free up to 1,000,000 reads a month, and a call that fails costs nothing. Every reply carries `cost_usd` and `balance_usd`.
- A new account starts with $1.00 of free credit. Only a person adds money, through a Stripe checkout on the account page (https://conecto.chat/account), from $5.00 plus a 7% + $0.35 fee.
- AI visibility and the phone run only on credit someone bought, never on free or bonus credit.
- Each key has a daily budget ($20.00 by default) and the account a monthly ceiling ($100.00). Only the owner raises them.

## Before you act

- Ask the person before a call that reaches people outside the business (an email to a customer, an invoice, a document to sign), starts a monthly rental (an inbox or a phone number), or costs more than $1.00, unless they asked for exactly that. Reading and searching need no question.
- The owner can make chosen tools wait for a person's approval. Such a call answers `approval_required`, and the request goes to the approver.
- A refused call says why and how to fix it. Every error code: https://conecto.chat/docs/errors.md
- Conecto's own rules: the phone needs one real top-up first, the phone line tells every caller it is an AI, and the only outbound calls confirm meetings booked in advance.

## More

- What Conecto is, who runs it and what it costs: https://conecto.chat/ai-questions
- Every tool with one line each: https://conecto.chat/tools/llms.txt
- Terms: https://conecto.chat/terms
