# Calendars and Events

Calendar writes are the only ones in this skill that send mail to other people as a side effect. Read the participant list before touching anything.

**Before writing an event**, read `timezone` from `~/Clawic/data/fastmail-api/config.yaml` (falling back to `~/Clawic/profile.yaml`, then UTC) and the calendar ids in `## Account Map` of `memory.md`. **After turning a confirmation email into an event**, write the reservation to the shared `~/Clawic/data/bookings/<year>.md` keyed by its locator — one row, updated in place if the confirmation is re-sent (`memory-template.md`). The event lives in the calendar; the booking record is what survives the calendar.

**Contents:** [Capability and Calendars](#capability-and-calendars) · [The Event Object](#the-event-object) · [Time, Which Is the Hard Part](#time-which-is-the-hard-part) · [Recurrence](#recurrence) · [Participants and Scheduling Mail](#participants-and-scheduling-mail) · [Reading a Range](#reading-a-range) · [From Confirmation Email to Event](#from-confirmation-email-to-event) · [Deleting](#deleting)

## Capability and Calendars

Calendars are a separate capability with its own URN, its own scope on the token, and its own per-account availability — read all three from the session (`session.md`). A token scoped to mail only produces `unknownCapability` on the first calendar call, which is a scope answer, not an auth one.

`Calendar/get` lists the calendars: `id`, `name`, `color`, `isVisible`, `isSubscribed`, `myRights`. Two facts that decide what is possible:

- **An account usually has several calendars**, including subscribed read-only ones (holidays, a shared team calendar). Writing to the wrong one is silent.
- **`myRights`** on the calendar governs write, and on a shared calendar it commonly permits reading and not writing. Check before building the event, not after.

Record each calendar id, its name, and the `myRights` verdict in the calendars sub-table of `## Account Map` in `~/Clawic/data/fastmail-api/memory.md`, in the same turn you read them.

## The Event Object

`CalendarEvent` objects follow JSCalendar (RFC 8984), which is not iCalendar with different spelling — several concepts differ deliberately.

| Property | Note |
|---|---|
| `title` / `description` | Plain text |
| `start` | **Local wall time**, `2026-09-03T14:00:00`, with no offset and no `Z` |
| `timeZone` | IANA name (`Europe/Madrid`); `null` means floating time |
| `duration` | ISO 8601 duration (`PT1H30M`) — **there is no end property** |
| `showWithoutTime` | `true` for all-day events; `duration` is then whole days (`P1D`) |
| `calendarIds` | Map of calendar id → `true`, same set shape as `mailboxIds` |
| `participants` | Map of participant id → object with `email`, `roles`, `participationStatus` |
| `recurrenceRules` / `recurrenceOverrides` | See below |
| `status` | `confirmed` · `cancelled` · `tentative` |
| `freeBusyStatus` | `busy` · `free` — what other people's availability views see |
| `alerts` | Map of alert id → trigger; relative (`-PT15M`) or absolute |
| `uid` | Stable across systems; how the same event is recognized after an export/import round trip |

Patch semantics are the same as everywhere else: `{"participants/p1/participationStatus": "accepted"}` changes one thing, a whole-property write replaces the map (`requests.md`).

## Time, Which Is the Hard Part

- **`start` is wall time and `timeZone` interprets it.** `2026-09-03T14:00:00` with `Europe/Madrid` is 2pm in Madrid whatever the reader's zone. Writing `14:00:00Z` into `start` is not a UTC event, it is a malformed value.
- **A floating event (`timeZone: null`) means 9am wherever you are.** Correct for "morning routine", wrong for a meeting, and the difference only shows up when someone travels.
- **All-day is `showWithoutTime: true`**, not midnight-to-midnight. Midnight events shift a day across a timezone change; all-day events do not.
- **The configured `timezone` is an assumption, so state it.** "Booked Thursday 14:00 Europe/Madrid" is verifiable; "booked Thursday at 2" is not.
- Duration, not end time. Converting an end time to a duration across a DST boundary is where an hour goes missing — compute in the event's own timezone.

## Recurrence

A recurring series is **one object**, not many.

- `recurrenceRules` holds the pattern: `frequency`, `interval`, `byDay`, `count` or `until`.
- `recurrenceOverrides` is a map keyed by the **original occurrence's start value**, each entry a patch applied to that one occurrence.
- Changing one occurrence = writing an override. Creating a separate event instead produces a duplicate that the series still generates underneath.
- Cancelling one occurrence = an override with `"excluded": true`. Deleting the object deletes the whole series, including the past.
- Changing the series while overrides exist can orphan them: an override keyed to a start time the new rule no longer generates simply never applies. When the pattern changes materially, read the overrides first and say which ones will be lost.
- "This and all future" is not a JMAP operation. It is: bound the existing series with `until`, then create a second series for the new pattern. Two objects, both of which need writing.

## Participants and Scheduling Mail

**This is the part that emails people.** An event with participants is a scheduling object; adding, removing, or rescheduling triggers iTIP messages to attendees.

| Change | Who hears about it |
|---|---|
| Adding a participant | That person gets an invitation |
| Changing `start`, `duration`, or location | Every participant gets an update |
| Removing a participant | That person gets a cancellation |
| Setting `status: "cancelled"` | Everyone gets a cancellation |
| Editing `description` or `alerts` | Usually nobody — but "usually" is not a guarantee to make on the user's behalf |
| Your own `participationStatus` | The organizer gets your reply |

Before patching any event that has participants: read the list, say who will be notified, and get confirmation for anything beyond a private field. A "quick fix" to a meeting time is a message to eight people, some of whom will reply.

Being the organizer versus an attendee changes what is permitted: an attendee can change their own `participationStatus` and little else, and attempts to reschedule someone else's event fail or produce a counter-proposal depending on the server.

## Reading a Range

- `CalendarEvent/query` with a filter on `after` / `before` returns events overlapping the window.
- **Recurring events expand within the window** when the query is asked to expand them; without expansion you get the series object once, whose `start` may be years ago. "Nothing on Tuesday" derived from an unexpanded query is a wrong answer, not an empty one.
- For a free/busy question, `freeBusyStatus` and `status: "cancelled"` both matter: a cancelled event that is still on the calendar is not a conflict.
- Fetch `id`, `uid`, `title`, `start`, `timeZone`, `duration`, `status`, `participants` and skip the rest; descriptions are long and rarely needed for a scheduling answer.

## From Confirmation Email to Event

The common workflow, and the one with a durable output:

1. Find the confirmation (`search.md`), fetch the body, extract: what, when, timezone, location, locator, provider.
2. **Resolve the timezone from the content, not from the user's default.** A flight departing 07:15 is local to the departure airport; a hotel check-in is local to the hotel.
3. Create the event with `uid` left to the server, and put the locator in `description` — that is what makes the event findable later.
4. Write the booking row to `~/Clawic/data/bookings/<year>.md`: locator, provider, what, dates, status, and that it came from mail (`memory-template.md`).
5. If the confirmation is later amended, update **both** the event and the booking row. Two records that disagree are worse than one.

Cancellations are an update in both places — `status: "cancelled"` on the event, a status change with the date on the booking row. A deleted row cannot explain the refund three months later.

## Deleting

| Intent | Operation |
|---|---|
| Remove one occurrence | Override with `"excluded": true` |
| Cancel a meeting others are attending | `status: "cancelled"` — this notifies them; destroying the object may not |
| Remove a private event entirely | `CalendarEvent/set` `destroy` |
| End a recurring series going forward | Set `until` on the rule; keeps the history |

`destroy` on a calendar event is permanent and there is no Trash. For anything with participants, cancel rather than destroy: destroying can leave the event on their calendars forever with no cancellation ever sent.
