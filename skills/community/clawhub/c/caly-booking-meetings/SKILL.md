---
name: booking-meetings
description: "Books a meeting in Caly on one of the user's event types: finds a free slot, collects the attendee's details and the event type's required booking questions, confirms with the user, then creates the booking so Caly sends the invites. Use when the user asks 'book a call with Sam on Tuesday at 3', 'schedule a 30 minute intro with alex@example.com', 'put a meeting on my calendar with this client', or picks a slot found earlier. Writes data and emails the attendee, so it always confirms first."
---

# Caly: booking meetings

Create one confirmed booking in Caly, with the right event type, time, time zone and attendee.

## Connecting and calling the tools

Every tool in this skill comes from the `caly` MCP server, the Caly connector, and is written here as `caly:<tool>`.

- **Tools listed by name:** call them directly, for example `caly:create_booking`.
- **Only `caly:search_tools` and `caly:execute_typescript` listed (Code Mode, the default):** call `caly:search_tools` first, then call each tool inside `caly:execute_typescript` as `external_<tool>` (for example `external_create_booking`); the program must `return` its result.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call.
- **No `caly` tools at all:** Caly is not connected yet. Add the server as shown in https://github.com/DevinoSolutions/mcp-servers/tree/main/caly#install; it signs in with OAuth on first use.

A refused call throws an Error whose message starts with its code, for example `INVALID_INPUT:`.

## Tools you will use

- `caly:whoami`: the account this connection acts as, with its time zone.
- `caly:list_event_types`: the user's event types with id, title and length.
- `caly:get_event_type`: one event type in full, including `bookingFields` (the booking questions an attendee must answer).
- `caly:find_available_slots`: free start times for an event type between two dates.
- `caly:create_booking`: books the meeting (`eventTypeId`, `start` as UTC ISO 8601, `attendee` with `name`, `timeZone` and usually `email`, optional `guests`, `lengthInMinutes`, `bookingFieldsResponses`). Caly sends the confirmation emails and calendar invites.

## Workflow

1. Call `caly:whoami` and `caly:list_event_types`. Pick the event type from the user's words; ask if it is ambiguous.
2. Collect the attendee: name, email, and their time zone. If the user does not know the attendee's time zone, ask; do not assume it is the user's.
3. Call `caly:get_event_type` and read `bookingFields`. Ask the user for any required answer you do not have yet.
4. Call `caly:find_available_slots` for the requested day. Use only a start time that appears in the result. If the requested time is not free, say so and offer the nearest free slots instead.
5. Show a summary and wait for an explicit yes: event type, date and time in both the user's and the attendee's time zone, length, attendee name and email, guests, and that Caly will email the invite.
6. After the yes, call `caly:create_booking` once with the slot's `start` in UTC and the collected details.
7. Report the result: the booking's title, time, status (some event types need the host to confirm, so it may be unconfirmed), meeting URL or location, and its `uid`, which reschedules and cancellations need.

## Rules

- Never call `caly:create_booking` without the user's explicit confirmation of the summary in step 5.
- Never retry a failed `caly:create_booking` blindly; read the error, fix the input, and confirm again if anything changed.
- Never invent an attendee email. Book only with details the user gave.
- To move or cancel an existing meeting, use the `managing-bookings` skill instead of creating a second booking.
