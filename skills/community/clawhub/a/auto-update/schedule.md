# Schedule Contract - Auto-Update

This document defines the local schedule state.

## Required Facts

- timezone
- discovery cadence
- apply cadence
- quiet hours
- scheduler type
- who may edit the scheduler
- no-op behavior

## Good Entries

- "Timezone: Europe/Madrid."
- "OpenClaw applies daily at 04:00 local time."
- "Skills discover daily, apply only once backups finish."
- "Scheduler edits require approval."

## Bad Entries

- "Run updates at night."
- "Use whatever scheduler works."
- "No-op behavior undecided."
