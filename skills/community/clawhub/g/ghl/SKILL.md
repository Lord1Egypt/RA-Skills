---
name: ghl-crm-mastery
description: Full read/write access to GoHighLevel CRM via API v2. Contacts, conversations, notes, opportunities, calendars, tags, tasks, forms, workflows, payments, and invoices. Includes rate-limit retries, safety guardrails, and real-time conversation support.
version: 1.3.0
author: SetupClaw.Tech
homepage: https://setupclaw.tech
metadata: { "openclaw": { "requires": { "env": ["GHL_API_KEY", "GHL_LOCATION_ID"], "bins": ["python3"] }, "primaryEnv": "GHL_API_KEY", "homepage": "https://setupclaw.tech" } }
---

# GHL CRM Mastery — GoHighLevel API v2 Skill

## What This Does

Gives your agent full operational access to GoHighLevel — read, write, and real-time conversation management. Designed for CRM automation agents (appointment setting, lead qualification, pipeline management).

### Contact Operations
- **contacts list** — List contacts with pagination
- **contacts get** — Full contact record by ID (name, email, phone, company, tags, custom fields)
- **contacts search** — Find contact by email
- **contacts search-phone** — Find contact by phone number
- **contacts update** — Update any contact field (company, tags, custom fields, etc.)
- **contacts add-tags** — Apply tags to a contact
- **contacts remove-tag** — Remove a tag from a contact

### Conversation Operations (Real-Time)
- **conversations list** — List recent conversations
- **conversations get** — Full conversation history for a contact (last 20 messages with direction, type, timestamp)
- **conversations send** — Send SMS, email, or DM reply through GHL. This is how the agent responds to leads.

### Notes
- **notes add** — Add research notes, call summaries, or interaction logs to a contact record
- **notes list** — Read existing notes for a contact

### Pipeline & Opportunities
- **opportunities list** — List pipeline items
- **opportunities get** — Full opportunity details
- **opportunities update** — Move opportunity to a different pipeline stage

### Calendars
- **calendars list** — List available calendars
- **calendars events** — List events for a calendar

### Tags, Forms, Workflows
- **tags list** — List all tags in the location
- **forms list** — List forms
- **forms submissions** — Get submissions for a specific form
- **workflows list** — List workflows (read-only)
- **workflows trigger** — Trigger a workflow for a contact (NEVER create/edit/delete)

### System
- **health** — Test GHL API connection

## Real-Time Conversation Pattern

The agent uses this skill for instant lead response. The pattern:

**First touch (new lead, no prior research):**
1. `contacts search-phone` or `contacts search` — find the contact
2. `contacts get` — pull full record
3. `notes list` — check for existing research
4. If no research notes → run identity verification (separate skill/process)
5. `conversations get` — read conversation history
6. Craft personalized response
7. `conversations send` — reply via GHL
8. `notes add` — log research findings + what was sent

**Follow-up messages (contact already researched):**
1. `contacts get` — pull record (already has research in notes)
2. `conversations get` — read latest messages
3. Craft contextual reply (15-30 second target)
4. `conversations send` — reply
5. `notes add` — brief log of interaction

**Key principle:** Research happens ONCE per contact. After that, the agent reads its own notes and the conversation history, then replies fast. The goal is real-time chat feel — under 30 seconds for follow-ups.

## Prerequisites

**Required environment variables** (must be set in your `.env` file):

```
GHL_API_KEY=your-private-integration-token
GHL_LOCATION_ID=your-location-id
```

**Required runtime:** `python3` (ships with macOS; verify with `python3 --version`).

## Getting Your GHL Credentials

1. Log into GoHighLevel → Settings → Integrations → Private Integrations → Create New
2. Name it appropriately for your deployment
3. Enable all required scopes:
   - contacts.readonly, contacts.write
   - conversations.readonly, conversations.write
   - conversations/message.readonly, conversations/message.write
   - opportunities.readonly, opportunities.write
   - calendars.readonly, calendars.write
   - calendars/events.readonly, calendars/events.write
   - locations/tags.readonly, locations/tags.write
   - locations/tasks.readonly, locations/tasks.write
   - forms.readonly, workflows.readonly
   - payments/transactions.readonly, locations.readonly
   - invoices.readonly, invoices.write, users.readonly
4. Copy the Private Integration Token → `GHL_API_KEY` in `.env`
5. Settings → Business Info → copy Location ID → `GHL_LOCATION_ID` in `.env`

## Usage

All commands are run via the included Python CLI at `{baseDir}/scripts/ghl_api.py`:

```bash
export GHL_API_KEY=$(grep GHL_API_KEY ~/.openclaw/.env | cut -d= -f2)
export GHL_LOCATION_ID=$(grep GHL_LOCATION_ID ~/.openclaw/.env | cut -d= -f2)

# Test connection
python3 {baseDir}/scripts/ghl_api.py health

# Test contact lookup
python3 {baseDir}/scripts/ghl_api.py contacts list --limit 1

# Test conversation read
python3 {baseDir}/scripts/ghl_api.py conversations get --contact-id "YOUR_CONTACT_ID"

# Send a message
python3 {baseDir}/scripts/ghl_api.py conversations send --contact-id "CONTACT_ID" --message "Hello" --type sms

# Add a note
python3 {baseDir}/scripts/ghl_api.py notes add --contact-id "CONTACT_ID" --body "Research findings..."
```

## Safety Guardrails (Non-Negotiable)

1. **Never create contacts** — GHL creates contacts automatically when forms are submitted, SMS received, or DMs received. Creating contacts manually risks duplicates. If a contact doesn't exist, flag to the appropriate channel.
2. **Never delete contacts** without explicit human confirmation in Slack
3. **Never send bulk SMS** without human approval
4. **Never modify workflows** — trigger only, never create/edit/delete
5. **Log every write operation** — every `conversations send` and `notes add` prints a timestamped log line
6. **TCPA compliance** — no SMS between 9PM and 8AM in the recipient's time zone (enforced by TCPA handler layer, not this skill)

## Network Endpoints

This skill connects exclusively to the GoHighLevel API:
- `https://services.leadconnectorhq.com` — GHL API v2 (all operations)

No other external endpoints are contacted. All credentials are read from local environment variables only.

## Changelog

### v1.3.0 (March 2026)
- Added `metadata.openclaw` frontmatter declarations (requires.env, requires.bins, primaryEnv) for ClawHub security compliance
- Added `{baseDir}` references for portable skill paths
- Added explicit network endpoint documentation
- Updated _meta.json with runtime and credential requirements
- Generalized agent references for broader deployment compatibility

### v1.2.0 (March 2026)
- Added conversations send, notes list, contacts search-phone
- Real-time conversation pattern documentation

### v1.0.0 (March 2026)
- Initial release: 24 endpoints covering contacts, conversations, notes, opportunities, calendars, tags, forms, workflows
