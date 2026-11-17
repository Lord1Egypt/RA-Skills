---
name: accesso-tickets
description: "Read accesso-powered mobile ticket links (accessoticketing.com media-engine URLs from confirmation emails) — order number, per-ticket product, participant, date/time, barcodes, Google Wallet passes — with curl."
---

# accesso tickets

For accesso Passport mobile-ticket links, which look like:

```
https://media-engine.<region>.accessoticketing.com/tickets/v1/<island>?oToken=A1:…&cToken=A1:…&merchant_id=<n>
```

Many venues deliver tickets this way (US National Whitewater Center, theme parks, festivals). The link arrives in the order-confirmation email, often behind a click-tracker — resolve that first with `curl -sSIL <tracking-url> | grep -i ^location`.

**No login, no browser bridge.** The `oToken` in the URL *is* the credential, and the page is plain-`curl` reachable server-side. Treat the URL as a secret: it grants anyone the order's tickets and barcodes. Never paste one into a file, a commit, or an issue.

## Core pattern

`references/parse-tickets.mjs` is dependency-free (no `node_modules`) and takes a URL, a file, or `-` for stdin:

```bash
P=~/.claude/skills/accesso-tickets/references/parse-tickets.mjs
node "$P" "$TICKET_URL" | jq .
```

Useful flags:

- `--barcodes <dir>` — write each ticket's barcode as a PNG (`ticket-<idx>-<ticketId>.png`; an existing file is never overwritten — a re-run writes `…-2.png`) and add `barcodeFile` to the output.
- `--terms` — include the (long, boilerplate, per-ticket-identical) `termsAndConditions`. Omitted by default.
- `--url <original-url>` — supply the source URL when parsing a saved file, so `googleWalletUrl` can be built.

Exit codes: `3` no tickets parsed (expired link, or layout drift — the message says which), `4` HTTP error fetching, `64` bad usage.

## Output

Top level: `orderNumber`, `island`, `merchantId`, `merchantLogo`, `ticketCount`, `declaredTicketCount`, `tickets[]`.

Per ticket: `index`, `ticketId`, `packageName`, `participant`, `additionalGuests[]`, `date`, `time` (absent on all-day items), `barcodeText`, `barcodeIsDataUrl`, `instructions`, `googleWalletUrl`, plus any other label/value pair the merchant rendered (commonly `guestNumber`, `webSalesId`).

Extra fields are harvested generically from the page's label/value markup rather than hardcoded, so a merchant with different detail rows still comes through. See `references/recipes.md` for jq recipes and the verified request shapes.

## Gotchas

- **An expired or invalid link returns HTTP 200**, not 4xx — the body just says "no tickets available to print on this order." Status alone never tells you the link is dead; the parser checks the body and says so.
- **Every ticket is rendered twice** (a mobile `ticket-item-container<N>` grouping and a `desktopTicketGrouping` one) sharing barcode element ids. Parse only the mobile blocks or you get doubles.
- **`ticketId` lives in neither rendering** — it is in the trailing "Register this ticket" modal section, one hidden input per ticket in ticket order. The parser maps it positionally and *omits* it (with a warning) if the counts disagree, rather than guessing.
- `date`/`time` are the merchant's local wall-clock strings (`MM/DD/YYYY`, `9:00 AM`) with no timezone. Don't convert them.
- Barcodes are inline base64 PNGs of the same order-level code (`%RC<order>`), not per-ticket unique on every merchant.

## In context groups

The accessoticketing MCP's tools sit in the **family** group (mcp-host context groups). It has **no canonical read**: it reads one order behind an emailed link, so it never answers the group's "what's new / what's due / what's on" fan-out, declares no subjects (an order link is not a listable set of people) and takes no date range. Its tools carry `lookup` hints (order, one ticket, Wallet passes, resolving a tracking link) and one `other` (saving barcode images), so a compound ask such as "what's on this weekend, and pull up the barcodes for our tickets" reaches it only for the tickets half, with the link. It needs no browser: no "needs your browser open" answer comes from this source.
