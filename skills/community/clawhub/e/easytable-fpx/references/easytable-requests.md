# easyTable requests for fpx

Ready-to-run URLs for `fpx get '<url>' -p easytable -H 'X-Requested-With: XMLHttpRequest'`
(reads) and `fpx post-json`/`fpx get` (writes). All paths/params/field shapes
are transcribed from `src/client.ts`, `src/parse.ts`, `src/payload.ts`, and
`docs/EASYTABLE-API.md` — the same shapes the `easytable_*` MCP tools use.

Host: `https://book.easytable.com`. Every URL below needs `id=<placeId>`
(a.k.a. `place`) and `lang=<code>` (`en`, `se`, `da`, … — defaults to `en`).
Replace `1fdfc` with a real restaurant id from a
`book.easytable.com/book/?id=<id>` link.

Reads answer **HTML fragments**, not JSON — extraction below is `grep -oE`
against the exact attributes `src/parse.ts` selects on. These are compact
greps, not a full parser; for anything beyond simple extraction, read
`src/parse.ts`.

---

## 1. List booking areas/types (resolve this first)

```sh
fpx get 'https://book.easytable.com/book/ajax/types.asp?id=1fdfc&lang=en' \
  -p easytable -H 'X-Requested-With: XMLHttpRequest' \
  | grep -oE '<a[^>]*type=[0-9]+[^>]*>[^<]*</a>'
# <a href="#type=13991">Boka Inne</a>
```

The numeric value after `type=` in the `href` is the `type` id every later
call needs.

## 2. List bookable dates

Needs `type` (from §1) and `qty` (party size).

```sh
fpx get 'https://book.easytable.com/book/ajax/calendar.asp?id=1fdfc&lang=en&type=13991&qty=2' \
  -p easytable -H 'X-Requested-With: XMLHttpRequest' \
  | grep -oE '<span[^>]*class="[^"]*day[^"]*"[^>]*data-date="[0-9-]+"[^>]*>'
```

A `class` containing `av` = available; `closed`/`ua` = not. `data-note`
(when present) carries a note.

## 3. List time slots

Needs `type`, a `date` (ISO `YYYY-MM-DD`, from §2), and `qty`. Slot values
are **minute-of-day** (1035 → 17:15 — `hh=floor(m/60)`, `mm=m%60`).

```sh
fpx get 'https://book.easytable.com/book/ajax/times.asp?id=1fdfc&lang=en&type=13991&date=2026-08-01&qty=2' \
  -p easytable -H 'X-Requested-With: XMLHttpRequest' \
  | grep -oE '<span[^>]*class="[^"]*time[^"]*"[^>]*data-time="[0-9]+"[^>]*>'
```

## 4. Find existing bookings by phone

```sh
fpx get 'https://book.easytable.com/book/ajax/cancel-search.asp?id=1fdfc&lang=en&mobile=%2B46701234567' \
  -p easytable -H 'X-Requested-With: XMLHttpRequest' \
  | grep -oE 'data-booking="[^"]+"|data-id="[^"]+"|data-mobile="[^"]+"'
```

URL-encode the mobile (`+` → `%2B`). The booking id is on
`data-booking`/`data-id` (`easytable-mcp` prefers `data-booking`, falling
back to `data-id` — never `value`, which can be a button label).

## 5. Cancel a booking (no Turnstile — plain tokenless GET)

```sh
fpx get 'https://book.easytable.com/user/ajax/json_cancel_booking.asp?place=1fdfc&mobile=%2B46701234567&booking=<bookingId>' \
  -p easytable
```

The response is JSONP-wrapped (`callback([{Status,...}])`); unwrap and read
with:

```sh
sed -E 's/^[^(]*\(//; s/\);?[[:space:]]*$//' | jq '.[0] | {Status, errHtml, successHtml, confirmUrl}'
```

`Status: 1` = cancelled; `Status: 0` = rejected (see `errHtml`).

## 6. Create / modify a booking — payload shape (Turnstile caveat applies)

Harvest the three plain-text page-derived values first — these ARE
reachable via `fpx get` (they're server-rendered, unlike the Turnstile
token):

```sh
# bookingToken + cancellationtime, from the confirm.asp fragment:
fpx get 'https://book.easytable.com/book/ajax/confirm.asp?id=1fdfc&lang=en&type=13991&date=2026-08-01&time=1035&qty=2' \
  -p easytable -H 'X-Requested-With: XMLHttpRequest' > /tmp/confirm.html
grep -oE 'bookingToken\s*=\s*"[^"]+"' /tmp/confirm.html          # → {EB9351E5-...}
grep -oE 'id="cancellationtime"[^>]*value="[0-9]+"' /tmp/confirm.html  # → e.g. 180

# lcid, from the widget page HTML (language-dependent: se→1053, en→2057):
fpx get 'https://book.easytable.com/book/?id=1fdfc&lang=en' -p easytable \
  | grep -oE '\blcid\s*=\s*"?[0-9]+'
```

The **Turnstile token cannot be harvested through `fpx`** — the CLI has no
DOM-read verb. Manual workaround: with the widget tab open and loaded (past
the confirm step so Turnstile has rendered), open DevTools console on that
tab and run:

```js
document.querySelector('input[name="cf-turnstile-response"]').value
```

Copy that value in as `turnstileToken` below. It's single-use and expires in
~300s, so harvest it right before the POST.

POST body — the full 32-key `dataObj` (the endpoint 500s on a partial
payload; `time`/`persons` MUST be strings; omit `event`/`existing` when
unused):

```json
{
  "place": "1fdfc",
  "type": "13991",
  "date": "2026-08-01",
  "persons": "2",
  "time": "1035",
  "name": "Guest Name",
  "mobile": "+46701234567",
  "email": "",
  "room": "",
  "company": "",
  "address": "",
  "zip": "",
  "city": "",
  "country": "",
  "comment": "",
  "newsletter": 0,
  "newsletterrelated": 0,
  "lcid": "2057",
  "lang": "en",
  "ref": "",
  "cancellationtime": "180",
  "promocode": "",
  "groupRequestTerms": 0,
  "preorder": {},
  "tags": [],
  "amounttags": [],
  "customFields": [],
  "bookingInfo": [],
  "bookingToken": "{EB9351E5-...}",
  "botScore": 0,
  "websitePot": "",
  "turnstileToken": "<paste the harvested token>"
}
```

```sh
fpx post-json 'https://book.easytable.com/user/ajax/json_booking.asp' @/tmp/booking.json -p easytable \
  | sed -E 's/^[^(]*\(//; s/\);?[[:space:]]*$//' | jq '.[0] // .'
```

For **modify**, POST the same shape plus `"existing": "<existingBookingId>"`
to `https://book.easytable.com/user/ajax/json_modify_booking.asp`.

A `Status: 0` response with the token/bookingToken/cancellationtime fields
all present and non-empty means the request itself is malformed — re-check
the harvested values and the field types (`time`/`persons` as strings).
