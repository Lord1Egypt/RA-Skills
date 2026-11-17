# Data Formats — Money, Time, IDs, Text

## Money

- Integer minor units are common (Stripe: `amount: 500` = $5.00) but not universal — PayPal uses decimal strings (`"5.00"`). Check the service section before converting.
- Zero-decimal currencies have no minor unit: in JPY, `amount: 500` means ¥500, not ¥5.00 — blind cents conversion overcharges 100×. Check the currency's exponent (ISO 4217); never assume 2.
- Never float arithmetic on money (0.1 + 0.2 ≠ 0.3 in binary floats): integers of minor units or a decimal type.
- An amount without its currency field is not a value — send and store them together.

## Timestamps

- Unix seconds vs milliseconds: 10 digits = seconds, 13 = milliseconds (holds until 2286). A milliseconds value parsed as seconds lands ~50,000 years out — sanity-check magnitude on ingest.
- ISO 8601 without an offset is ambiguous: some APIs mean UTC, some mean account-local time. Always SEND with an explicit `Z` or offset; on receive, check the service docs before assuming.
- Date-only values (`2026-07-23`) shift a day when parsed as midnight-local then converted across timezones — keep dates as dates, never promote them to datetimes.
- JWT `exp`/`iat` are Unix seconds (→ `auth.md` JWT).

## IDs

- 64-bit numeric IDs exceed JavaScript's 2^53−1 safe-integer ceiling and `JSON.parse` rounds them silently — Twitter ships `id_str` for exactly this. Treat every ID as an opaque string: never parse it, never do arithmetic, never rely on its format staying stable.
- IDs are case-sensitive; a case-insensitive database collation "finds" the wrong record.
- Don't build ordering on ID sequence — sort keys are explicit fields; sequential-looking IDs are an implementation detail.

## Text and Encoding

- Length limits count in different units: bytes vs code points vs UTF-16 units — one emoji is 1 grapheme, 2 UTF-16 units, 4 UTF-8 bytes. "Max 280 characters" means one specific unit; check which before truncating client-side.
- Normalize to NFC before comparing or deduping: "é" has two encodings that render identically and compare unequal.
- Null vs absent vs empty in PATCH: JSON Merge Patch semantics (RFC 7396) — `null` clears the field, absent leaves it unchanged. Serializers that drop null fields make clearing impossible; use a client that preserves explicit nulls.
- Form-encoded and legacy APIs deliver booleans and numbers as strings (`"true"`, `"0"`) — and the string `"0"` is truthy in most languages. Coerce explicitly at the boundary.

## Standard Formats to Send

| Kind | Format | Example |
|---|---|---|
| Phone | E.164 | `+14155550100` |
| Country | ISO 3166-1 alpha-2 | `ES` |
| Currency | ISO 4217 | `EUR` |
| Language | BCP 47 | `es-MX` |
| Timestamp | ISO 8601 with offset, or Unix seconds — per the API | `2026-07-23T10:00:00Z` |
