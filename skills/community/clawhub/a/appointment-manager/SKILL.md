---
name: appointment-manager
description: Books, tracks, and reminds you about every appointment. Use when a user wants to book, log, or be reminded about any appointment.
license: MIT
compatibility: Requires lobstrkit with Exine browser for online booking. Phone-only providers use call script workflow.
allowed-tools: web_fetch web_search
metadata:
  openclaw.emoji: "📅"
  openclaw.user-invocable: "true"
  openclaw.category: life-admin
  openclaw.tags: "appointments,booking,reminders,calendar,health,dentist,doctor"
  openclaw.triggers: "book appointment,book me a,I need an appointment,remind me about,dentist,doctor"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/appointment-manager


# Appointment Manager

Every appointment has three problems: booking it, remembering it, and following up after.
This skill handles all three.

---

## File structure

```
appointment-manager/
  SKILL.md
  appointments.md    ← all appointments, status, full lifecycle
  providers.md       ← known providers with booking method, contact, notes
  config.md          ← reminder preferences, delivery settings
```

---

## The lifecycle

```
Request → Research → Book → Confirm → Remind (24h) → Remind (2h) → Attend → Follow-up
```

The skill owns every stage except the ones that need a phone call.
For those, it does everything up to handing you the number and the script.

---

## Booking methods

**Online booking (handled automatically):**
Agent uses the browser tool to find and complete the booking.
No action required from the user beyond the initial request.

**Phone-only providers (handled up to the call):**
Agent finds the number, identifies the best time to call,
drafts a script with all the information needed, and sends it ready to use.
The call is the user's — everything else is handled.

**Manual logging:**
User booked it themselves. Agent logs it and sets up the reminder chain.
`/appt log [description] [date/time]`

---

## Setup flow

### Step 1 — Reminder preferences

Ask once. Store in config.md. All future appointments use this.

Default chain:
- 24 hours before: full reminder with address, what to bring, journey time
- 2 hours before: short nudge with location
- 15 minutes before: final ping (off by default — ask if they want it)

Also ask: follow-up prompt after appointment? Default on.
"[APPOINTMENT] is done — anything to note?"

### Step 2 — Location

Ask for home location / postcode if not already in USER.md.
Used for: journey time estimates, finding local providers.

### Step 3 — Calendar

If Google Calendar is connected: ask if they want appointments added automatically.
Default: yes.

### Step 4 — Write config.md

```md
# Appointment Manager Config

## Reminder chain
24h: true
2h: true
15min: false
follow_up: true

## Location
home: [address / postcode]

## Calendar sync
google_calendar: true

## Delivery
channel: [CHANNEL]
to: [TARGET]
```

---

## Booking flow — online provider

When user says "book me a dentist appointment" or "I need a GP appointment next week":

### Step 1 — Identify the provider

Check providers.md for a preferred or previously used provider.
If found: confirm with user — "Use [PROVIDER] again, or try somewhere new?"
If not found: ask for their preferred provider, or offer to find one nearby.

**Finding a provider (if needed):**
```
web_search: "[appointment type] near [location]"
```
Present top 3 options with: name, address, distance, rating, booking method.
User picks. Store in providers.md.

### Step 2 — Find the booking page

```
web_fetch: [provider website]
```
Look for: online booking link, booking system (Doctolib, Zocdoc, Calendly, proprietary).
If booking system found: proceed to Step 3.
If no online booking: proceed to phone-only flow.

### Step 3 — Check availability

Use browser tool to navigate the booking system.
Find available slots. Check against user's calendar if connected.

Ask the user: "Any preference on day or time? Morning or afternoon?"
Default: next available slot that doesn't conflict with calendar.

Present top 3 options:
```
Available slots:
1. Tuesday 15 April — 10:30am
2. Wednesday 16 April — 2:15pm
3. Friday 18 April — 9:00am

Which works?
```

### Step 4 — Complete the booking

Navigate and complete the booking in the browser.
Fill in required details (name, DOB, reason for visit — ask user if needed).
Get confirmation number or confirmation email.

Confirm to user:
```
✅ Booked: Dentist — Dr. [NAME] / [PRACTICE]
Tuesday 15 April at 10:30am
[ADDRESS]
Confirmation: #[REF]

Reminders set: Monday 14 April (24h) and Tuesday at 8:30am (2h).
Added to Google Calendar. ✓
```

Log to appointments.md and update providers.md with booking details.

### Step 5 — Register reminder cron jobs

For each reminder in the chain, register an isolated cron job:

```json
{
  "name": "Appt Reminder 24h — [TYPE] [DATE]",
  "schedule": { "kind": "at", "at": "[24h before appointment ISO timestamp]" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "deleteAfterRun": true,
  "payload": {
    "kind": "agentTurn",
    "message": "Send 24h appointment reminder. Read {baseDir}/appointments.md for [appointment ID]. Send reminder with address, what to bring, journey time.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>" }
}
```

Repeat for 2h reminder. Store cron job IDs in appointments.md.

---

## Booking flow — phone-only provider

When the provider has no online booking:

### Step 1 — Find the number

```
web_fetch: [provider website]
web_search: "[provider name] phone number"
```
Extract: main booking number, best time to call, any notes ("call after 9am", "press 2 for appointments").

### Step 2 — Draft the call script

Generate a complete script ready to use:

```
📞 Call script — [PROVIDER]

Number: [PHONE NUMBER]
Best time to call: [TIME — e.g. "weekday mornings, lines open 8am"]
[Any navigation notes — "Press 2 for appointments"]

---

When they answer:

"Hi, I'd like to book an appointment for [REASON / TYPE].

My name is [USER NAME].
Date of birth: [DOB if medical]
[Any other required details]

I'm available: [USER'S AVAILABILITY — pulled from calendar or asked]

Do you have anything [morning/afternoon] in the next [timeframe]?"

---

Once booked, log it: /appt log [type] [date/time]
```

Send the script to the user's channel. Everything they need is in one message.

### Step 3 — Set a call reminder

If the user hasn't logged the appointment within 2 days:
"Did you manage to call [PROVIDER]? If you've booked, just log it and I'll set up reminders."

---

## Appointment types and prep notes

The skill knows what different appointments typically require.
The 24h reminder includes type-specific prep notes.

**Medical / GP:**
- Bring: [any referral letters, current medication list, insurance card if applicable]
- Note: arrive 5-10 minutes early if first visit
- Journey: [estimated travel time from home]

**Dentist:**
- Avoid eating 1 hour before if possible
- Bring: [dental insurance card if applicable]
- Journey: [estimated travel time]

**Optician:**
- Bring: current glasses/contact lenses
- Note: driving after eye test may not be possible if drops are used

**Haircut / beauty:**
- Bring: reference photos if you have a specific style in mind
- No special prep

**Specialist / hospital:**
- Bring: referral letter, any previous test results, medication list, insurance card
- Note: allow extra time for registration
- Journey: [hospital can be large — check which department and entrance]

**Custom:**
For appointment types not in the library, ask the user once: "Anything specific to bring or prepare?"
Store in providers.md for future bookings at the same provider.

---

## appointments.md structure

```md
# Appointments

## [APPOINTMENT ID] — [TYPE] — [PROVIDER]
Date: [DATE TIME]
Duration: [if known]
Address: [full address]
Booked via: [online / phone-script / manual]
Confirmation: [reference number or email confirmation]
Status: upcoming / completed / cancelled / rescheduled
Reminder jobs: [24h cron ID] [2h cron ID]
Prep notes: [what to bring, any specific notes]
Follow-up: [none / [specific follow-up required]]
Calendar event: [Google Calendar event ID if synced]
Notes: [anything else]
```

---

## providers.md structure

```md
# Providers

## [PROVIDER NAME]
Type: [dentist / GP / optician / etc]
Address: [full address]
Phone: [number]
Best time to call: [if phone-only]
Booking method: [online — [URL] / phone-only / mixed]
Booking system: [Doctolib / Zocdoc / proprietary / etc]
Last visit: [date]
Notes: [any useful info — "Dr. [NAME] is preferred", "parking on site", etc]
```

providers.md grows over time. Every new provider is stored.
Future bookings at the same provider skip the research step entirely.

---

## Reminder formats

### 24h reminder

```
📅 [TYPE] tomorrow — [DAY] at [TIME]

📍 [PROVIDER NAME]
[ADDRESS]

🕐 Journey: [X] min from home — leave by [TIME]

📋 Bring:
• [Item from prep notes]
• [Item]

[Any specific notes for this appointment]
```

### 2h reminder

```
⏰ [TYPE] in 2 hours — [TIME] at [PROVIDER]
Leave by [TIME] to arrive on time.
```

### 15min reminder (if enabled)

```
⏰ [TYPE] in 15 minutes.
```

### Follow-up prompt (1h after end time)

```
Done with [TYPE]? Anything to note — results, next steps, follow-up needed?

Reply /appt done [ID] [notes] or just tell me what happened.
```

---

## Reschedule flow

`/appt reschedule [appointment]`

1. Cancel existing reminder cron jobs
2. Navigate back to booking system (for online bookings)
3. Find new slot — present options
4. Complete reschedule
5. Update appointments.md
6. Register new reminder cron jobs
7. Update Google Calendar event

---

## Cancellation flow

`/appt cancel [appointment]`

1. Cancel reminder cron jobs (delete them)
2. Ask: "Do you want me to cancel with the provider too, or just remove your reminders?"
3. If cancelling with provider: navigate to online cancellation or provide phone number + cancellation script
4. Update appointments.md status to "cancelled"
5. Update Google Calendar event

---

## Management commands

- `/book [description]` — start booking flow
- `/appt list` — all upcoming appointments with dates
- `/appt today` — anything today
- `/appt log [type] [date/time]` — manually log a booked appointment
- `/appt done [appointment] [notes]` — mark complete with follow-up notes
- `/appt cancel [appointment]` — cancel appointment and reminders
- `/appt reschedule [appointment]` — reschedule flow
- `/appt history` — past appointments log
- `/appt history [provider]` — past visits to one provider
- `/appt providers` — list of known providers

---

## What makes it good

The phone-script for phone-only providers is the most underrated feature.
It removes the only thing the skill can't do automatically — the call itself —
by making the call as easy as possible. Number, navigation instructions, exact words to say.
The user spends 3 minutes on hold instead of 20 minutes procrastinating.

The providers.md memory compounds.
The second time you book at the same dentist, there's no research, no finding the number,
no remembering which booking system they use.
The skill knows. It just asks "same place?" and proceeds.

The 24h reminder with journey time is the one people notice.
"Leave by 9:45 to arrive on time" is more useful than "appointment at 10:30."
