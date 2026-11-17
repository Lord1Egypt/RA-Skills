---
name: e-signature
description: "Send PDFs for e-signature from OpenClaw and track who has signed: contracts, NDAs, waivers and forms, to up to 10 signers, with reusable templates and reminders. Use when the person wants a document signed, asks whether it is signed, or wants signers reminded. Runs on Conecto, a paid service with $1.00 of free credit: a signature request costs $0.20 and reading is free."
metadata:
  openclaw:
    homepage: https://conecto.chat/tools/esign?from=clawhub
---

# E-signature

This skill lets you, the agent, send a PDF to people to sign and follow it until everyone has signed. Each signer gets an email with their own link and signs in the browser by drawing or typing. When the last one signs, everyone gets the signed PDF with a signing certificate. The signing runs on Conecto's servers and reaches you as tools on one MCP server.

Conecto is a paid service. Each tool call is charged to the business's prepaid balance, and a new account starts with $1.00 of free credit (see Money).

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

`openclaw mcp login conecto` opens Conecto's sign-in in the browser. A new business creates its account first at https://conecto.chat/account/signup?from=clawhub-e-signature. On the sign-in page the person ticks the areas you may use, for this skill E-signature, Files and Documents, and allows it. You then run on a key of your own that the owner can revoke. No key goes in this skill or in an environment variable. `doctor --probe` should list the `esign_` tools.

## Get the PDF into the file store

`esign_send` takes a PDF that is already in the business's file store. Pick the route that fits:

- The person has the document. Call `files_upload_link` and give them its `page_url`. They open it and drop the file, up to 25 MB. The link works once, for an hour.
- You write the document. `documents_create_pdf` makes a PDF from Markdown or HTML and stores it, for $0.005.
- The document is at a public https link. `files_upload` with `url` fetches and stores it, for $0.001.

Never type a PDF out as base64.

## Send it

`esign_send` needs the `file_id`, a `title` the signers see, and 1 to 10 `signers`, each with a name and an email.

- With no `fields`, a signature page is added at the end with a signature and date line for each signer. Start with this.
- With `fields`, you place each one yourself: page, x, y, width and height in percent of the page from its top-left corner. A signature field of about 30 by 5 fits a line. Every signer needs a signature field. The kinds are signature, initials, name, date, text and checkbox.
- Signers are emailed all at once (`parallel`) or one after another (`sequential`).

Before you send, tell the person who will be emailed and what the title is, and wait for a yes.

## Follow it

- `esign_get` shows each signer's status: waiting, to sign, opened, signed or declined. Once everyone has signed it returns the signed PDF with a download link.
- `esign_list` lists requests, newest first, optionally of one status.
- `esign_remind` emails everyone who still has to sign, at most once a day, for $0.02.
- `esign_signing_link` gives one signer's link, for someone signing in person on a tablet or phone.
- `esign_cancel` stops a request before everyone has signed. Signers are told and their links stop working.
- `account_events` reports `esign.signed` after each signature, `esign.completed` when everyone has signed and `esign.declined` if someone declines.

## Documents that go out often

`esign_save_template` saves a PDF once with its fields placed per signer role, such as Customer and Company. `esign_send_template` then sends it to new signers, one per role, with no fields to place again. It can send up to 50 requests in one call, for example the same NDA to every new contractor. An account keeps up to 100 templates.

## Money

- A signature request costs $0.20, from a template too. Up to 10 signers are one request.
- A reminder costs $0.02. Saving a template costs $0.001.
- Reading, signing links and cancelling are free, up to 1,000,000 reads a month for the account.
- A call that fails costs nothing. Every reply from a tool carries `cost_usd` and `balance_usd`.
- The $1.00 of free credit covers about four signature requests with their uploads.
- Only a person adds money, on the account page (https://conecto.chat/account), from $5.00 plus a fee of 7% + $0.35.

## Before you act

- Ask before every `esign_send`, `esign_send_template` and `esign_remind`. They email people outside the business.
- Reading a request's status needs no question.
- The owner can make chosen tools wait for a person's approval. Such a call answers `approval_required`, and the request goes to the approver.

## Limits

- PDFs only. Convert other files with `documents_convert_to_pdf` first.
- Up to 10 signers on a request. A PDF with too many pages is refused with `too_many_pages`.
- Signers sign by drawing or typing in the browser. This skill does not say what kind of signature a contract needs under the law that applies to it. Ask the person when that matters.

## More

- Every e-signature tool with its inputs, an example and its errors: https://conecto.chat/tools/esign.md
- Every error code: https://conecto.chat/docs/errors.md
- Prices: https://conecto.chat/pricing.md
- Terms: https://conecto.chat/terms
