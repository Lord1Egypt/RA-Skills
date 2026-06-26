# Delivery Modes

## boss-primary (default)
Send only one management summary to the primary channel.

Default:
- `boss_channel = primary`

If the configured preferred destination is unavailable, fallback to the first verified available destination and state that clearly.

## broadcast
Send the same summary to multiple channels.
Use only when the user explicitly wants multi-channel delivery.

## generate-only
Generate files only. Do not push to external channels.
Useful for review, testing, and approval flows.
