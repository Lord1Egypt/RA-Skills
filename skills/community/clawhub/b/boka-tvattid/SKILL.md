---
name: "boka-tvattid"
description: "Boka tvättid via bokatvattid.se: free slots, book, cancel, view bookings. Triggers: tvättid, tvättstuga, tvättbokning, gästlägenhet, laundry booking."
---

# Boka tvättid (tvättstugebokning)

Book laundry and guest-apartment times via Boka tvättid (bokatvattid.se / Visir) — works for any v1-mode building. Run every step through the bundled stdlib-only CLI `scripts/bokatvattid.py`: it handles login, room matching, URL encoding and confirmations. Raw endpoints live in `references/bokatvattid-api.md` — fallback/debugging only, for when the CLI cannot run.

## Commands

- `buildings <query>` — public building search → v2 id, name, city, v1 id
- `login` — verify credentials (prints userid and active room count)
- `rooms` — list rooms (id, name; the building's default marked)
- `slots [date]` / `free [date]` — all / only free slots
- `book <date> <HH:MM[,HH:MM…]>` — book slot(s); interactive confirmation unless `--yes`
- `cancel [date]` — cancel own bookings that date; interactive confirmation unless `--yes`
- `my` — list current bookings
- Date: defaults to today; accepts `imorgon`/`tomorrow`, `+N`, `YYYY-MM-DD`, `DD/MM` and more
- Options: `--pin`, `--building`, `--apartment`, `--room`, `--yes` (PIN resolution: `--pin` → env `BOKATVATTID_PIN` → `~/.config/bokatvattid/pin.txt`)

## Steps

1. Credentials: v1 buildingid, apartment number, 6-digit PIN — take them from the user's stored config, never hardcode anything here. Keep the PIN out of chat text and final reports; prefer config file or env over `--pin` (command-line args are visible in process lists).
2. Unknown building: `buildings <name>`, confirm the right hit with the user, note the v1 id. Only v1-mode buildings are supported; the tool flags others clearly.
3. `login`, then `rooms`, then `free <date>` to show availability. Rooms match by id or (part of) name; without `--room` the building's default room is used.
4. Book only after the user confirms room, date and time(s): `book <date> <HH:MM[,HH:MM]> --yes`. Report BookingID, room, date and slot(s) back.
5. Cancel only after user confirmation: `cancel <date> --yes`.
6. `my` lists current bookings.

## Security notes

- The legacy API's native form passes the PIN as a URL query parameter (the official web app does the same); the bundled CLI instead sends every call as POST with the PIN in the request body, so it never lands in a URL. Treat the PIN as sensitive regardless: config file or env, never chat text, logs or shell history.
- `--yes` skips the interactive book/cancel confirmation and is required in non-interactive runs. Never pass it without the user's explicit confirmation of that exact booking.
- Bookings and cancellations are real actions on the user's account. Confirm before acting; if fully booked the tool reports the queue option — never auto-join.

## Pitfalls

- Slot ids are per room and date — always book from a fresh `slots`/`free` output.
- Only v1-mode buildings work; the v2 REST surface (`/api/v2/auth/*`) rejects these logins.
- Guest apartments, where present, unlock with the same apartment PIN after booking.
- Building rules vary: booking window (~1 month ahead) and per-month limits (`BookPerMonth` in the room list). Respect any building-specific rules from user memory.
