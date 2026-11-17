# accesso ticket recipes

All shapes below were captured live against a real accesso order
(`media-engine.na3.accessoticketing.com`, island `accesso155`, 12 tickets).
Replace `$TICKET_URL` with the link from the confirmation email — never commit one.

```bash
P=~/.claude/skills/accesso-tickets/references/parse-tickets.mjs
```

## Resolve a tracked link first

Confirmation emails wrap the link in a click-tracker (SendGrid `…/ls/click?upn=…`, etc.):

```bash
curl -sSIL "$TRACKED_URL" | grep -i '^location:' | tail -1
```

Take the final `media-engine.*/tickets/v1/*` URL. Keep the whole query string —
`oToken` **and** `cToken` are both required.

## Everyday queries

```bash
# One line per ticket: who, when, what
node "$P" "$TICKET_URL" 2>/dev/null \
  | jq -r '.tickets[] | [.date, (.time // "all-day"), .participant, .packageName] | @tsv' \
  | column -t -s $'\t'

# Group by participant
node "$P" "$TICKET_URL" 2>/dev/null \
  | jq -r '.tickets | group_by(.participant)[] | "\(.[0].participant): \(map(.packageName) | join(", "))"'

# Just the timed items (the ones with a start time you must not miss)
node "$P" "$TICKET_URL" 2>/dev/null | jq '[.tickets[] | select(.time)] | map({time, participant, packageName})'

# Distinct products and counts
node "$P" "$TICKET_URL" 2>/dev/null | jq -r '.tickets | group_by(.packageName)[] | "\(length)x \(.[0].packageName)"'

# Order header
node "$P" "$TICKET_URL" 2>/dev/null | jq '{orderNumber, island, merchantId, ticketCount}'

# Per-product instructions (deduped — merchants repeat them on every ticket)
node "$P" "$TICKET_URL" 2>/dev/null \
  | jq -r '[.tickets[] | {packageName, instructions}] | unique_by(.packageName)[] | "## \(.packageName)\n\(.instructions)\n"'
```

## Barcodes

```bash
node "$P" "$TICKET_URL" --barcodes ~/Desktop/tickets >/dev/null
open ~/Desktop/tickets   # macOS
```

Each file is `ticket-<index>-<ticketId>.png`. The scannable value is also in
`barcodeText` (e.g. `ID %RC<order-number>`) if you'd rather regenerate the code yourself.

## Google Wallet passes

Verified endpoint — returns `{"jwt": "..."}` at HTTP 200:

```
GET https://media-engine.<region>.accessoticketing.com/google-wallet/v1/<island>/<oToken>/<ticketId>
```

The page sends an `X-ACCESSOPASSPORT-ORIGIN: <store-origin>` header; it is **not**
required (a bare curl returns 200). Turn a JWT into a save link with Google's
standard form, `https://pay.google.com/gp/v/save/<jwt>` (verified: resolves, and
prompts Google sign-in as expected):

```bash
node "$P" "$TICKET_URL" 2>/dev/null | jq -r '.tickets[] | select(.googleWalletUrl) | "\(.ticketId)\t\(.googleWalletUrl)"' \
| while IFS=$'\t' read -r id url; do
    jwt=$(curl -sS "$url" | jq -r .jwt)
    printf '%s\thttps://pay.google.com/gp/v/save/%s\n' "$id" "$jwt"
  done
```

These URLs embed the order token — treat the output as secret.

## Page structure (why the parser looks the way it does)

Server-rendered HTML, no JSON store, no bot wall, no auth beyond the URL tokens.

- `span.ticketHeader__orderNumber` → `Order #  <n>` (a `span`, not a `div`).
- `img.ticketHeader__merchantLogo` → `…/assets/<island>/images/…`, the island fallback.
- Mobile grouping: `div#ticket-item-container<N>[data-ticketidx][data-totaltickets]`, one per ticket,
  containing `.ticket__packageName`, `.ticket__customerName`, `.ticket__barcodeText` and
  `img#barcode<N>` (inline base64 PNG).
- The expandable detail panel `#flip-ticket-info-container<N>` is a **sibling** of that block, not a
  child — both hang off `#ticket-grouping-container`. Guest Number, Web Sales ID, Instructions and
  Terms all live in the panel, so they have to be paired back by index. (A text-slicing parser like
  the `.mjs` here picks them up incidentally because the panel falls between two ticket boundaries;
  anything walking the DOM must join them explicitly.)
- Detail rows are generic pairs: `div.gap-font--overline` (label) + `div.gap-font--body-2` (value) —
  this is how `Date`, `Time`, `Guest Number`, `Web Sales ID` all arrive. Harvest them generically.
- Long-form panels: `div.flipTicket__content-heading` + `div.flipTicket__content` → `Instructions:`, `Terms and Conditions:`.
- `div#desktop-ticket-section.desktopTicketGrouping` repeats **all 12 tickets** with
  `desktopTicket__*` classes and the *same* `img#barcode<N>` ids. Bound parsing above it.
- Hidden `input#ticketId` / `#oToken` / `#merchantId` appear only in the trailing
  per-ticket "Register this ticket" modal forms, after the desktop grouping.

## Failure modes

- **Expired/invalid token → HTTP 200** with body `"We are sorry, but there are no tickets available to print on this order."`
  Confirmed by probing a bogus `oToken`. Never gate on status code alone.
- Merchant detail rows differ by venue; unknown labels are camel-cased into the ticket
  object rather than dropped, so new rows appear automatically.
- If `ticketId` is `null` and stderr warned about a count mismatch, the registration-modal
  section changed shape — re-check before trusting any `googleWalletUrl`.

## Not covered here

The same platform runs a separate **accesso Passport store API** at
`https://ecomm.api.<region>.accessoticketing.com/api/request/<service>` (POST; ~150 services
including `GetMerchantPackageList`, `GetParkHours`, `GetEventCalendarDates`, `CP_Login`,
`GuestOrderSearch`, `GuestViewOrder`, cart/purchase). It is server-side reachable (a malformed
request returns 400, not a bot wall) but needs merchant identification captured from a live
store session, and credentials for anything account-scoped. Out of scope for this skill.
