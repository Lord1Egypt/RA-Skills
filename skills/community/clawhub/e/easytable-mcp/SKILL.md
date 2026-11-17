---
name: easytable-mcp
description: Use when the user wants to check restaurant availability or make, change, or cancel a table reservation at a restaurant that books through easyTable (a book.easytable.com/book/?id=<id> widget). Covers listing booking areas, dates and times, looking up existing bookings by phone, and creating/modifying/cancelling reservations.
---

# easyTable reservations

easyTable is a restaurant table-booking system. Each restaurant has a public
booking widget at `https://book.easytable.com/book/?id=<restaurantId>` — the
`id` is the only identifier (there's no login). This MCP drives that widget
through the user's own signed-in, Cloudflare-cleared browser tab via the
fetchproxy bridge; the site blocks any server-side request.

## Setup (one time)

1. Install the fetchproxy browser extension (https://github.com/chrischall/fetchproxy).
2. Open a booking widget in Chrome: `https://book.easytable.com/book/?id=<restaurantId>`.
   Let the page finish loading — its Cloudflare Turnstile check solves itself.
3. The first tool call prints a one-time pair code; approve it in the extension.

## Typical flow

1. `easytable_list_types` — the restaurant's booking areas (e.g. indoor, bar);
   note the `type` id.
2. `easytable_list_dates` — bookable dates for that `type` + party size.
3. `easytable_list_times` — time slots (HH:MM) for a chosen date.
4. `easytable_create_booking` — make the reservation (needs name + mobile).

To change or cancel, first `easytable_find_bookings` with the mobile the
booking was made under, then `easytable_modify_booking` /
`easytable_cancel_booking` with the returned booking id.

## Writes are confirm-gated

`create`, `modify`, and `cancel` do nothing without `confirm: true` — they
return a dry-run preview first. Re-run with `confirm: true` to apply.

`create` and `modify` submit a Cloudflare Turnstile token the MCP reads from
the widget tab's hidden input, so a `book.easytable.com/book/?id=<id>` tab must
be open and loaded when you confirm. The token is single-use and expires after
a few minutes; if a create fails on the token, reload the tab and retry.
`cancel` needs no token.

## Notes

- Times are HH:MM; the widget internally uses minute-of-day.
- All reads and the whole booking flow are the user's own actions on their own
  browser session — no easyTable account or API key is involved.
