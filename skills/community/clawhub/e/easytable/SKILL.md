---
name: easytable
description: Use when the user wants to check restaurant availability or make, change, or cancel a table reservation at a restaurant that books through easyTable (a book.easytable.com/book/?id=<id> widget). Covers listing booking areas, dates and times, looking up existing bookings by phone, and creating/modifying/cancelling reservations.
---

# easyTable reservations

easyTable is a restaurant table-booking system. Each restaurant has a public
booking widget at `https://book.easytable.com/book/?id=<restaurantId>` — the
`id` is the only identifier (there's no login). This MCP drives that widget
through the user's own signed-in, Cloudflare-cleared browser tab via the
ContextMint Bridge extension (fetchproxy's browser extension); the site blocks any server-side request.

## Setup (one time)

1. Install the ContextMint Bridge browser extension from
   https://github.com/nullnet-app/contextmint-bridge/releases (Chrome: load the
   `contextmint-bridge-chrome-*.zip` unpacked; Safari: ships inside the ContextMint app,
   no public download yet — use Chrome for now). It is the renamed fetchproxy extension, same maintainer;
   source is public — build it or verify the zip with its published `.sha256`.
2. Open a booking widget in Chrome: `https://book.easytable.com/book/?id=<restaurantId>`.
   Let the page finish loading — its Cloudflare Turnstile check solves itself.
3. The first tool call prints a one-time pair code; approve it in ContextMint Bridge.

## Typical flow

1. `easytable_list_types` — the restaurant's booking areas (e.g. indoor, bar);
   note the `type` id.
2. `easytable_list_dates` — bookable dates for that `type` + party size.
3. `easytable_list_times` — time slots (HH:MM) for a chosen date.
4. `easytable_create_booking` — make the reservation (needs name + mobile).

To change or cancel, first `easytable_find_bookings` with the mobile the
booking was made under, then `easytable_modify_booking` /
`easytable_cancel_booking` with the returned booking id.

## Writes are confirmed first

`create`, `modify`, and `cancel` ask the user to confirm before anything is
sent: a confirmation prompt where the client supports one (unless the server
sets `MCP_CONFIRM_ELICITATION=off`). Otherwise the first
call sends nothing and returns `status: "confirmation-required"` with a
preview and a `confirmToken` — show the user the preview, and only after they
approve it in chat call again with the same arguments plus that `confirmToken`.
The token is single-use; a changed argument is refused as `DRAFT_CHANGED` with a
fresh preview (see `MCP_CONFIRM_MODE`).

`cancel` looks the booking up first (a read) and refuses a `bookingId` that
isn't one of that mobile's bookings; its preview's `booking` shows the matching
row (date, time, party) so the user can see which reservation they're cancelling.

`create` and `modify` submit a Cloudflare Turnstile token the MCP reads from
the widget tab's hidden input, so a `book.easytable.com/book/?id=<id>` tab must
be open and loaded when you confirm. The token is single-use and expires after
a few minutes; if a create fails on the token, reload the tab and retry.
If a create/modify comes back with an unknown outcome (a timeout, or a reply
easyTable didn't clearly accept or reject), the booking may already exist —
run `easytable_find_bookings` with the guest mobile before retrying.
`cancel` needs no token.

`modify` replaces the whole booking, and easyTable offers no way to read an
existing booking's email or comment back. Ask the user for the booking's current
email, comment (special requests, allergy notes) and company and pass them
through unchanged, or pass `''` to clear one on purpose; the preview lists what
will be cleared.

## In context groups

easyTable is a member of the **food** group. It has no canonical read: there is
no account to list subjects from, and every read needs a restaurant id (plus
the guest mobile for bookings), so it never answers a "what's new / due / on"
ask by itself. Its tools carry `lookup` hints (areas, dates, times, find
bookings) and `change` hints (create, modify, cancel), with the words people
say ("book a table", "cancel my reservation").

A compound ask such as "anything on tonight — and is there a table for four at
<restaurant> on Friday?" is answered by the group's other members for the
first half; the second half routes here as a lookup with the restaurant id.
Because every call rides the browser bridge, when no signed-in
book.easytable.com tab is connected the group answers that easyTable "needs
your browser open" rather than guessing.

## Notes

- Times are HH:MM; the widget internally uses minute-of-day.
- All reads and the whole booking flow are the user's own actions on their own
  browser session — no easyTable account or API key is involved.
