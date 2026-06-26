---
name: andara-meeting-minutes
description: Capture meeting summaries and action items from voice or text
---

# Meeting Minutes Skill

When ATTi or a team member sends a meeting summary (voice or text), save it as a structured record.

## Trigger
When user says something like "Meeting Notes:", "Besprechungsnotizen:", or "save meeting" — parse the content and store it.

## Steps

1. Extract the meeting topic, attendees, decisions, and action items from the message.

2. Save to PostgreSQL using bash + psql:
```bash
psql "$DATABASE_URL" -c "
INSERT INTO team_meetings (title, summary, attendees, meeting_date, created_at)
VALUES ('TOPIC', 'SUMMARY', ARRAY['ATTENDEE1','ATTENDEE2'], NOW(), NOW())
RETURNING id;"
```

3. For each action item, insert into meeting_action_items:
```bash
psql "$DATABASE_URL" -c "
INSERT INTO meeting_action_items (meeting_id, assignee, description, due_date, status, created_at)
VALUES (MEETING_ID, 'ASSIGNEE', 'TASK DESCRIPTION', 'DUE_DATE', 'pending', NOW());"
```

4. Confirm to the user: "Meeting gespeichert ✅ — [X] Action Items erstellt."

## Output Format
Reply in German with a structured summary:
- 📋 Meeting: [Title]
- 👥 Teilnehmer: [Names]
- ✅ Action Items: [List with assignees]
- 📅 Nächstes Treffen: [if mentioned]
