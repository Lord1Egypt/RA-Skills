# ICS Calendar Invite Format

## Template

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//[BUSINESS_NAME]//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:[BOOKING_ID]@[DOMAIN]
DTSTAMP:[NOW_UTC]
DTSTART:[START_UTC]
DTEND:[END_UTC]
SUMMARY:Confirmed Appointment - [SERVICE]
DESCRIPTION:Your appointment at [BUSINESS_NAME] is confirmed.
ORGANIZER;CN=[BUSINESS_NAME]:mailto:[FROM_EMAIL]
ATTENDEE;CN=[CUSTOMER_NAME];ROLE=REQ-PARTICIPANT:mailto:[CUSTOMER_EMAIL]
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR
```

## Date Format

All dates in ICS must be UTC in the format: `YYYYMMDDTHHMMSSZ`

Example: `20260403T063000Z` = April 3 2026, 6:30 AM UTC

## Timezone Conversion (Melbourne Example)

Melbourne is UTC+10 (AEST) or UTC+11 (AEDT).

DST rules:
- Starts: First Sunday of October (clocks forward, UTC+11)
- Ends: First Sunday of April (clocks back, UTC+10)

To convert Melbourne local → UTC:
- During AEDT (Oct–Apr): subtract 11 hours
- During AEST (Apr–Oct): subtract 10 hours

Example: April 3 2026, 5:30 PM Melbourne (AEDT) → subtract 11h → April 3, 6:30 AM UTC

## Calculating DTEND

Use the service duration to calculate the end time:

```
DTEND = DTSTART + service_duration_in_minutes
```

Common durations should be configured per business in TOOLS.md.

## Escaping Text

ICS text fields must escape these characters:
- `\` → `\\`
- `;` → `\;`
- `,` → `\,`
- Newlines → `\n`

## Line Length

ICS lines must not exceed 75 octets. Fold long lines by inserting `\r\n ` (CRLF + space).

## Attaching to Email

Base64-encode the .ics content and attach with:
- Filename: `appointment.ics`
- MIME type: `text/calendar`
- Disposition: `attachment`
