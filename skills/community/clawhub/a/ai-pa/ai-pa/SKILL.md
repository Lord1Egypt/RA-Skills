---
name: ai-pa
description: AI Personal Assistant network skill. Use when: contacting another PA, coordinating with peer agents, scheduling meetings between owners, broadcasting messages, looking up contacts from the local PA directory, or performing any cross-PA task. Reads contact data from data/pa-directory.json in the workspace. Does NOT contain hardcoded contact data — each PA maintains their own directory file.
---

# AI-PA Network Skill

Operational guide for AI Personal Assistants working within a multi-agent PA network.

---

## Directory Setup

This skill reads contact data from a local file. Before using, ensure the file exists:

```
data/pa-directory.json
```

If it doesn't exist, create it using the schema below. Each PA maintains their own copy with their own network's data.

### Directory Schema

```json
{
  "pas": [
    {
      "name": "PA Name",
      "phone": "+972XXXXXXXXX",
      "owner": "Owner Full Name",
      "owner_phone": "+972XXXXXXXXX",
      "owner_role": "VP Product",
      "owner_email": "owner@company.com",
      "status": "active",
      "notes": ""
    }
  ],
  "groups": [
    {
      "name": "Group Name",
      "jid": "XXXXXXXXXXX@g.us",
      "purpose": "PA coordination / leadership / family"
    }
  ],
  "owners": [
    {
      "name": "Owner Name",
      "phone": "+972XXXXXXXXX",
      "role": "CTPO",
      "email": "owner@company.com",
      "pa": "PA Name",
      "pa_phone": "+972XXXXXXXXX",
      "contact_preference": "pa_only"
    }
  ]
}
```

### Loading the Directory

```bash
cat data/pa-directory.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
for pa in d['pas']:
    print(f\"{pa['name']} → {pa['owner']} ({pa['phone']})\")
"
```

---

## Core Rules

### When to Contact a PA vs Owner

**Always contact the PA** for:
- Scheduling meetings between owners
- Passing messages between leadership
- Coordination tasks, follow-ups

**Contact the owner directly** only when:
- Their PA is unavailable or unresponsive
- Urgent matter that cannot wait
- Explicitly instructed by your own owner

**Never contact an owner directly** if their `contact_preference` is `"pa_only"`.

---

## Task Templates

### Schedule a Meeting

```
1. Identify the other party's PA from pa-directory.json
2. Message the PA (not the owner):
   "Hey [PA], [your owner] would like to meet with [their owner].
    Are they available [proposed time]? Or what works best?"
3. Confirm time with your owner
4. Create calendar event:
   gog calendar create primary \
     --summary "Meeting: [Owner A] + [Owner B]" \
     --start "YYYY-MM-DDTHH:MM:SS+TZ" \
     --end "YYYY-MM-DDTHH:MM:SS+TZ" \
     --attendees "owner@company.com"
5. Confirm with both PAs
```

### Broadcast to All PAs

```
1. Find group JID with purpose "pa_coordination" in pa-directory.json
2. Send to group — do not DM individually unless personal message is needed
3. For follow-ups, DM each PA individually using their phone number
```

### Send Email on Owner's Behalf

```bash
GOG_ACCOUNT=owner@company.com gog gmail send \
  --to "recipient@company.com" \
  --subject "Subject" \
  --body "Body"
```

Always confirm with owner before sending external emails.

### Find a PA's Contact

```bash
cat data/pa-directory.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
name = 'owner name to search'
matches = [p for p in d['pas'] if name.lower() in p['owner'].lower()]
for m in matches:
    print(f\"PA: {m['name']} | Phone: {m['phone']}\")
"
```

---

## Operational Protocols

### Billing Error
When a peer PA or your own agent reports a billing error:
1. Notify your owner immediately
2. Contact the admin/budget owner (whoever manages API keys for your organization)
3. Workaround: switch to a non-paid model temporarily in agent settings
4. Do NOT share API keys between agents

### New PA Onboarding
Full flow:
1. Agent signup at the organization's agent platform (e.g. monday.com/agents-signup)
2. Set up messaging channel (WhatsApp Business recommended)
3. Connect calendar (requires owner to share their calendar with write permissions)
4. Add to pa-directory.json with all fields
5. Announce in PA coordination group

### PA Is Unresponsive
1. Try messaging their phone number directly
2. If no response in reasonable time → contact their owner with context
3. Note the issue in your memory files

---

## Communication Style Between PAs

- Be direct and concise — PAs are agents, not humans
- State the request clearly: what you need, from whom, by when
- No small talk needed, but be collegial
- If you're relaying a message from your owner, say so: "My owner [name] asked me to..."
- Confirm receipt when you receive a coordination request

---

## Updating the Directory

Add a new PA:
```bash
python3 -c "
import json
with open('data/pa-directory.json', 'r') as f:
    d = json.load(f)
d['pas'].append({
    'name': 'New PA',
    'phone': '+972XXXXXXXXX',
    'owner': 'Owner Name',
    'owner_phone': '+972XXXXXXXXX',
    'owner_role': 'Role',
    'owner_email': 'owner@company.com',
    'status': 'active',
    'notes': ''
})
with open('data/pa-directory.json', 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print('Done')
"
```

---

## Quick Reference

| Task | Action |
|---|---|
| Find a PA's phone | Check pa-directory.json → pas → name/owner |
| Schedule a meeting | Contact other PA, agree time, create calendar event |
| Broadcast message | Use PA coordination group JID |
| Billing issue | Notify owner + budget admin |
| New PA added | Update pa-directory.json + announce in group |
| Owner prefers no PA contact | Check contact_preference field |
