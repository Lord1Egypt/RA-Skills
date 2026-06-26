---
name: fulcra-meeting-briefing
description: "Generate private meeting briefings from Fulcra calendar data with optional CRM notes and web research."
homepage: https://fulcradynamics.com
---

# Fulcra Meeting Briefing

Use this skill when the user wants upcoming-meeting prep, same-day meeting intel, next-day meeting briefings, attendee research, or CRM-assisted relationship context.

## Inputs

- Fulcra calendar events from the authenticated Fulcra CLI or API.
- Optional CRM notes supplied by the user, a configured CRM directory, or files already in the current workspace.
- Optional web research when the user asks for it or the CRM context is too thin.

## Workflow

1. Get calendar events for the requested window with the Fulcra CLI or API.
2. Qualify only meaningful meetings:
   - include external meetings with attendees plus a meeting link or non-home location
   - exclude solo blocks, personal appointments, health appointments, family events, internal-only events, and standing non-meeting blocks
   - preserve the exact calendar title
3. Identify the primary attendee from organizer, external attendees, title, email domain, or user-provided context.
4. Build the briefing from available evidence:
   - confirmed meeting facts: title, time, participants, location/link presence
   - relationship context from CRM or prior notes
   - company/domain context from attendee emails
   - public research only when allowed and useful
5. Fail closed when context is too thin. Do not post filler. Return a short diagnostic privately or say no reliable briefing could be generated.
6. Save output only when the user asks or a local workflow has an explicit destination.

## Output

Keep briefings concise and useful:

- who the person is
- why the meeting likely matters
- relationship or prior-context notes
- company or market context
- Fulcra-relevant angle, if any
- concrete questions or follow-ups

## Privacy

- Calendar, attendee, CRM, location, and briefing content are private.
- Do not expose real calendar details, locations, private CRM notes, or attendee contact details in public examples.
- Do not assume a local CRM path, local scripts, private credentials, or Arc-specific infrastructure.
- Keep auth tokens out of chat. Device-code URLs are okay only when the user explicitly needs to authenticate.

## Generic Integration Notes

- Preferred CLI base command: `uv tool run fulcra-api`.
- Use a configured CRM path only if one is provided, for example `FULCRA_MEETING_CRM_DIR`.
- Use a configured output path only if one is provided, for example `FULCRA_MEETING_BRIEFINGS_DIR`.
- Local Arc scripts may be useful examples, but ClawHub users should not need `projects/meeting-briefer/` or Arc's private CRM.
