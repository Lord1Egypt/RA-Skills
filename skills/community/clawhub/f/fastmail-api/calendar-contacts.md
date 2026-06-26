# Contacts and Calendar — Fastmail API

## Contacts Operations

For contact updates:
- Read with narrow filters first
- Upsert in small batches
- Preserve existing fields unless explicitly replacing
- Record unresolved conflicts for follow-up

## Calendar Event Operations

For event writes:
- Confirm timezone assumptions before create/update
- Preserve attendee and organizer data when patching events
- Verify recurring event changes on both parent and instances

## Cross-Domain Safety

When one workflow touches mail plus contacts or calendar:
1. Confirm account IDs per capability.
2. Run independent read validation for each capability.
3. Report partial success separately instead of collapsing results.
