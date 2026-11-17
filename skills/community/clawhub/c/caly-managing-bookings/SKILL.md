---
name: managing-bookings
description: "Reviews and changes the user's Caly bookings: lists upcoming, past, cancelled or unconfirmed meetings, looks one up by attendee or time, reschedules it to a free slot, or cancels it through Caly's two-step confirmation. Use when the user asks 'what meetings do I have tomorrow', 'show my bookings with Sam', 'move my call with Alex to Friday', 'reschedule the 3pm', 'cancel my meeting with this client', or 'who cancelled this week'. Reads freely; reschedule and cancel notify attendees, so they are confirmed first."
---

# Caly: managing bookings

Find the right booking, then read, move or cancel it without surprising anyone.

## Connecting and calling the tools

Every tool in this skill comes from the `caly` MCP server, the Caly connector, and is written here as `caly:<tool>`.

- **Tools listed by name:** call them directly, for example `caly:list_bookings`.
- **Only `caly:search_tools` and `caly:execute_typescript` listed (Code Mode, the default):** call `caly:search_tools` first, then call each tool inside `caly:execute_typescript` as `external_<tool>` (for example `external_list_bookings`); the program must `return` its result.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call.
- **No `caly` tools at all:** Caly is not connected yet. Add the server as shown in https://github.com/DevinoSolutions/mcp-servers/tree/main/caly#install; it signs in with OAuth on first use.

A refused call throws an Error whose message starts with its code, for example `CONFIRMATION_REQUIRED:`.

## Tools you will use

- `caly:whoami`: the account and its time zone.
- `caly:list_bookings`: the user's bookings, filtered by `status` (upcoming, past, cancelled, unconfirmed, recurring), `attendeeEmail`, `attendeeName`, `eventTypeId`, or a window (`afterStart`, `beforeEnd`). Paginated with `take` and `skip`; check `pagination.hasNextPage`.
- `caly:get_booking`: one booking by `bookingUid`, with attendees, hosts, location and any cancellation or rescheduling details.
- `caly:find_available_slots`: free start times; pass `bookingUidToReschedule` when moving a booking so its own slot counts as free.
- `caly:reschedule_booking`: moves a booking to a new `start` (UTC ISO 8601), with an optional `reschedulingReason`. Caly creates a new booking with a new `uid` and notifies the attendees.
- `caly:cancel_booking`: cancels a booking and notifies its attendees. It cannot be undone and takes two calls (see the workflow).

## Workflow

### Reviewing bookings

1. Call `caly:whoami` for the time zone, then `caly:list_bookings` with the filters that match the question ("tomorrow" → `status: ["upcoming"]` plus a window; "with Sam" → `attendeeName` or `attendeeEmail`).
2. Follow `pagination.hasNextPage` with `skip` until the window is covered, or tell the user how many more there are.
3. List each booking with its time in the user's time zone, title, attendees and status. Call `caly:get_booking` only when the user wants one booking's details.

### Rescheduling

1. Identify exactly one booking and its `uid`. If several match, list them and ask which one.
2. Call `caly:find_available_slots` for its event type and the new day, passing `bookingUidToReschedule`. Use only a start time from the result.
3. Confirm with the user: the booking, the old time, the new time (in the user's and the attendee's time zone), and that Caly will notify the attendees. Wait for an explicit yes.
4. Call `caly:reschedule_booking` once. Report the new time and the new `uid`.

### Cancelling

1. Identify exactly one booking and its `uid`, and ask for a reason if the user has one.
2. Call `caly:cancel_booking` with the `bookingUid` (and `cancellationReason`). The first call does not cancel: it returns `CONFIRMATION_REQUIRED` with a `confirmToken`.
3. Show the user which booking will be cancelled (title, time, attendees) and that the attendees will be emailed. Wait for an explicit yes.
4. Call `caly:cancel_booking` again with the SAME arguments plus the `confirmToken`. Report that it is cancelled.

## Rules

- Never reschedule or cancel without the user's explicit yes to a summary that names the booking.
- Never pass a `confirmToken` the user has not seen the booking for, and never reuse one for a different booking.
- Set `cancelSubsequentBookings` only when the user clearly asks to cancel the rest of a recurring series.
- Always state the time zone next to every time you show.
