# Boka tvättid — legacy (v1) API reference

Source: web app at https://prod.bokatvattid.se (Flutter), compiled `main.dart.js`. Generic: works for any v1-mode building; no building-specific constants below.

## Building resolution (before login, if the v1 id is unknown)

- `GET https://api.visirsolutions.com/api/v2/public/buildings/search?q=<name>` → `{"data":[{"id":"<v2_id>","name":"<Byggnadsnamn>","city":"<Stad>"}],"meta":{"total":1}}`
- `GET https://api.visirsolutions.com/api/v2/public/buildings/lookup?building_id=<id>` → `{"data":{"id":"<v2_id>","backend_mode":"v1","v1_building_id":"<v1_id>",…}}`
- Use `v1_building_id` for all legacy calls when `backend_mode` = "v1". Other modes are out of scope (`/api/v2/auth/login`, untested).

## Base

All booking calls: `POST https://prod.bokatvattid.se/api/api2` with `method=<METHOD>&<params>&lang=1` as a form-encoded request body (`Content-Type: application/x-www-form-urlencoded`).
- POST keeps credentials (PIN, token) out of URLs — query strings end up in server/proxy access logs; request bodies normally do not.
- The endpoint also accepts its native web-app form — everything in the URL query string, no body — but prefer POST. URL-encode values either way.
- Same host as the web app (prod.bokatvattid.se). `/api/phone?method=…` exists for messaging (e.g. `getTotalUnReadMessageV2`) — not needed for booking.

## Auth

- `checkLogin2` with body params `buildingid=<v1 id>`, `pincode=<PIN>`, `apartmentnumber=<apt>` → `{"error":0,"body":{"Token":"…","ApartmentID":<id>,"LaundryRoomDefaultID":<id>,"TotalLaundryRoom":6,…}}` (example shape)
- Later calls add body params `token=<Token>` and `userid=<ApartmentID>`.
- `error:0` = success. Max 2 login attempts, then report to user (PIN may have been changed; user can change it in the app; always 6 digits).

## Methods

| Method | Key params | Returns |
|---|---|---|
| checkLogin2 | buildingid, pincode, apartmentnumber | Token, ApartmentID, LaundryRoomDefaultID |
| getLaundryRoomList | token, userid, buildingid, v=3 | rooms[] (LaundryRoomID, LaundryRoomName, IsActive, IsDefault) |
| getLaundryRoomSlots | token, userid, laundryid, day, month, year | {data: room, calendar: slots} |
| getMyBooking | token, userid, start=0, limit=50 | data[] (bookings), total, reminder |
| getCalendarData | token, userid, laundryid, year, month | per-day {booked, freeslot, date, publishdate, isdisable, totalSlots, bookedSlots, isqueue} |

## Rooms — always from getLaundryRoomList (never hardcode)

Room ids and names differ per building. Filter `IsActive=1` (an inactive LaundryRoomID=0 entry can appear), use `IsDefault` as the default room, and match rooms by id or name.

## Booking3

Params: `laundryid`, `timeslot=<slotid[,slotid…]>`, `day`, `month`, `year`, `rebook=0`, plus the device block `devicemodel=BokaTvattidV2%20Web&firmware=web&appid=0&curday=&devicetoken=`.
- Book: `rebook=0&timeslot=<ids>`
- Cancel: `rebook=1&timeslot=` (empty)
- Success: `error:0`, `body` = BookingID (book) / `0` (cancel). `error:100` = fully booked → queue path (`body.Content`); do not auto-join queue.

## Slot shape (getLaundryRoomSlots)

`{"id":12345,"NumberQueue":0,"name":"07:00 - 09:00","isBook":0,"isOwner":0,"apartmentID":"","aptbook":"","isDisable":0}`
- Typically 8 slots/day, 07:00–23:00, 2 h blocks (varies per building). Free = `isBook=0 && isDisable=0`. `isOwner=1` = own booking. `isDisable=1` = past or not yet published.

## Gotchas

- The legacy buildingid is the v1 id (from lookup `v1_building_id`), not the v2 search id.
- Slot ids are per room+date; multiple slots join with commas in `timeslot`.
- Tokens appear short-lived; on auth errors redo checkLogin2 once.
- v2 REST `/api/v2/auth/exchange` rejects live v1 tokens — do not use the v2 surface for v1 buildings.
- v2 login `/api/v2/auth/login` 401s for v1-mode buildings.
- Guest apartments, where present, unlock with the same apartment PIN after booking.
- Booking window opens ~1 month ahead (observed: next-month slots opened early in the prior month).
- System per-building limits come from the room list (e.g. `BookPerMonth`: max bookings per month).
