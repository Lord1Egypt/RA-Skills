# Fulcra Meeting Briefing

A ClawHub skill for generating private meeting briefings from Fulcra calendar data, optional CRM notes, and optional web research.

## What It Does

- Pulls upcoming meetings from an authenticated Fulcra account.
- Filters out personal blocks, solo calendar holds, internal-only events, and standing non-meeting blocks.
- Preserves exact calendar titles.
- Uses optional CRM files when configured.
- Adds public attendee/company research only when useful and allowed.
- Fails closed instead of producing generic filler.

## Setup

- Authenticate Fulcra through the CLI. Preferred command: `uv tool run fulcra-api`.
- Optional: set `FULCRA_MEETING_CRM_DIR` to a directory of CRM markdown notes.
- Optional: set `FULCRA_MEETING_BRIEFINGS_DIR` if generated briefings should be saved.

## Safety

Calendar, attendee, CRM, and briefing content are private. Do not include tokens, private locations, attendee emails, or private CRM notes in shared examples or public output.
