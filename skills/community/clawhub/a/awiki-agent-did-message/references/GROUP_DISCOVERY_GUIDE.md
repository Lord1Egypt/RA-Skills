# Group Discovery Guide

Reference for group-based relationship discovery. This guide supplements the workflow defined in `SKILL.md` — it does NOT repeat the two-phase post-join workflow, authorization model, or CLI commands already documented there.

## DM Composition Guidance

When composing personalized direct messages to recommended connections:

- **Goal**: Establish initial connection, not sell or pitch
- **Personalization is mandatory**: Analyze the person's bio, tags, and work direction from their Profile. Find a specific intersection point with the user
- **Structure** (150-200 characters recommended):
  1. Who you are (one line)
  2. Which group you found them in
  3. Which specific point in their Profile resonated with you
  4. What concrete intersection you share
  5. One-sentence expectation (e.g., "would love to exchange ideas on X")
- **Prohibitions**: No mass-sending identical content; no generic pleasantries; no big asks in the first message
- **Workflow**: Generate draft for each candidate → present all drafts to user in a batch → user reviews/edits → send confirmed ones

## Local Contact Write Paths

Record a recommendation candidate (always allowed, even in default mode):
```bash
cd <SKILL_DIR> && python scripts/manage_contacts.py --record-recommendation \
  --target-did "<DID>" --target-handle "<HANDLE>" \
  --source-type meetup --source-name "OpenClaw Meetup Hangzhou 2026" \
  --source-group-id grp_xxx --reason "Strong fit"
```

Save a confirmed contact:
```bash
cd <SKILL_DIR> && python scripts/manage_contacts.py --save-from-group \
  --target-did "<DID>" --target-handle "<HANDLE>" \
  --source-type meetup --source-name "OpenClaw Meetup Hangzhou 2026" \
  --source-group-id grp_xxx --reason "Strong fit"
```

Mark follow or DM state:
```bash
cd <SKILL_DIR> && python scripts/manage_contacts.py --mark-followed --target-did "<DID>"
cd <SKILL_DIR> && python scripts/manage_contacts.py --mark-messaged --target-did "<DID>"
```

## Recommendation Output Structure

When outputting recommendations, use this structure per candidate:

```
### Candidate N
- target_handle:
- target_did:
- fit_score: 0-100
- why_this_person:
  - bullet 1
  - bullet 2
  - bullet 3
- evidence:
  - profile_signal:
  - group_message_signal:
  - local_relationship_signal:
- suggested_next_action: save_local | follow | dm | wait
- source_context:
  - group_id:
  - group_name:
  - source_type:
  - source_name:
```

Wrap all candidates in a group snapshot header:
```
## Group Snapshot
- group_name:
- group_goal:
- total_members_observed:
- total_group_messages_observed:
- recommendation_basis:
```

End with:
```
## Do Not Prioritize Yet
- 1-3 weak-signal people with short reasons

## Suggested User Decision
- a short direct question asking whether to save/follow/DM any of the above
```

## Recommendation Quality Checklist

Before presenting any recommendation, verify:

- the recommendation reason is specific, not generic
- the evidence points to actual profile / message / local-state signals
- if a system message is involved, the recommendation uses `system_event` metadata instead of only parsing the text content
- the action is proportional to confidence
- the person is not already over-handled locally
- the final user question is explicit and easy to answer

## Recommendation Criterion

Recommend whenever a member shows potential as a valuable connection for the user — based on Profile, self-introduction content, or group activity signals. There is no minimum member count or message count threshold.
