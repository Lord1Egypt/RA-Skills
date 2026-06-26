---
name: slack-lead-scanner
description: Monitor a Slack channel for images/text of leads (badges, business cards), extract data, enrich with Apollo.io API, let Apollo auto-sync to HubSpot, search HubSpot for the new contact link, and reply in-thread with summary and link. Also monitors Slack DM replies to update HubSpot fields on existing leads. Use when setting up or managing Slack-based lead scanning, including polling configuration via cron.
---

# Slack Lead Scanner

Monitor #leadscanner for new images/text, process as leads via Apollo + HubSpot, reply in-thread. Also check Slack DM replies to update HubSpot contacts.

## Setup

- SLACK_TOKEN in ~/.openclaw/credentials/slack-bot-token (xoxb- token)
- Apollo key in ~/.openclaw/credentials/apollo-api-key
- HubSpot token in ~/.openclaw/credentials/hubspot-api-key
- State file: ~/clawd/memory/slack-lead-scanner-state.json
- Portal ID: 43856876
- Channel: #leadscanner (C0AQAJ8VD8A)

## State File Schema

```json
{
  "last_ts": 1234567890,
  "processed_ids": ["msg_ts_1", "msg_ts_2"],
  "channel_id": "C0AQAJ8VD8A",
  "pending_dm_replies": [
    {
      "dm_ts": "1234567890.123456",
      "hubspot_contact_id": "12345",
      "contact_name": "John Doe"
    }
  ]
}
```

## Polling Workflow

### Part 1: Process New #leadscanner Messages

1. Load state from ~/clawd/memory/slack-lead-scanner-state.json
2. Fetch messages: `curl -H "Authorization: Bearer $SLACK_TOKEN" "https://slack.com/api/conversations.history?channel=C0AQAJ8VD8A&oldest=[last_ts]&limit=50"`
3. Filter: ts > last_ts, not in processed_ids, has files or non-empty text
4. For each new message:
   a. Download image: `curl -H "Authorization: Bearer $SLACK_TOKEN" "[file.url_private_download]" -o /tmp/lead-[ts].jpg`
   b. Analyze with image tool: "Extract structured data from this badge or business card. Return JSON: {first_name, last_name, company, title, email, phone, notes}"
   c. Append message.text to notes
   d. Dedup: Search HubSpot first by firstname+lastname+company — if exists, skip enrich, go to step (g)
   e. Enrich via Apollo: `curl -X POST -H "Content-Type: application/json" -d '{"api_key":"[KEY]","first_name":"[f]","last_name":"[l]","organization_name":"[co]","title":"[t]","reveal_personal_emails":true,"reveal_phone_number":true}' https://api.apollo.io/api/v1/people/match`
   f. Sleep 10s, then search HubSpot for new contact (sort by createdate DESC, filter name+company)
   g. Get contact id, build link: `https://app.hubspot.com/contacts/43856876/contact/[id]`
   h. Send DM to Mark (user:U03H7C6HW5B) with formatted message (see Reply Format below)
   i. Track DM timestamp from response, add to pending_dm_replies in state
   j. React ✅ on original #leadscanner message
   k. Add msg ts to processed_ids, update last_ts
   l. Cleanup: `rm /tmp/lead-[ts].jpg`

### Part 2: Check DM Replies for HubSpot Updates

5. For each entry in pending_dm_replies:
   a. Fetch thread replies: `curl -H "Authorization: Bearer $SLACK_TOKEN" "https://slack.com/api/conversations.replies?channel=[DM_CHANNEL_ID]&ts=[dm_ts]"`
   b. Filter replies that are from the user (not the bot itself) and not yet processed
   c. Parse reply text as a natural-language HubSpot update instruction, e.g.:
      - "update title to VP of Sales" → jobtitle
      - "wrong email, it's john@acme.com" → email
      - "company is Acme Corp" → company
      - "phone is 415-555-1234" → phone
      - "add note: met at SaaStr" → note (create HubSpot note via /crm/v3/objects/notes)
   d. Apply update via HubSpot PATCH: `curl -X PATCH -H "Authorization: Bearer $HUBSPOT_TOKEN" -H "Content-Type: application/json" -d '{"properties":{"[field]":"[value]"}}' "https://api.hubapi.com/crm/v3/objects/contacts/[hubspot_contact_id]"`
   e. Reply in thread: "✅ Updated [field] to [value] for [contact_name]."
   f. If unrecognized instruction, reply: "❓ I didn't understand that. Try: 'update title to [value]' or 'email is [value]'"

6. Write updated state back to ~/clawd/memory/slack-lead-scanner-state.json
7. Log to memory/YYYY-MM-DD.md

## Reply Format (DM to Mark)

Use Slack line breaks (\n) between fields:

```
*[Full Name]*
[Title]
[Company]
📧 [Email]
📞 [Phone]
🔗 <https://app.hubspot.com/contacts/43856876/contact/[id]|View in HubSpot>

_Reply to this message to update any field in HubSpot._
```

## HubSpot Field Mappings

| Natural language | HubSpot property |
|-----------------|-----------------|
| name / first name / last name | firstname / lastname |
| title / job title / role | jobtitle |
| company / org | company |
| email | email |
| phone | phone |
| note / notes | create note object |

## Error Handling

- No Apollo match: send DM anyway with extracted data, note "No enrichment match"
- No HubSpot match after sleep: send DM with "Sync pending - check HubSpot later", omit link
- API errors: Log and DM "Error processing: [msg]" with ❌ react
- Unknown DM reply: Reply with ❓ and guidance

## Notes

- Use haiku model for cost efficiency
- Rate limits: Slack ~1 call/sec, Apollo per plan, HubSpot 100 req/10s
- Never log or output tokens
- Get DM channel ID for direct messages: it's a conversations.open response for user U03H7C6HW5B