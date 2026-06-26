---
name: crm-snail-mail-postgrid
description: Send physical mail from CRM contacts using PostGrid. Use when pulling contacts from GoHighLevel (GHL) or Follow Up Boss (FUB), mapping contact/address fields, generating personalized mail payloads, and submitting letters or postcards through PostGrid API. Also use when another skill already produced GHL/FUB contact JSON and mail should be sent from that dataset.
---

# CRM Snail Mail via PostGrid

Use this skill to run targeted direct-mail outreach from CRM contacts.

## Workflow

1. Pick source: `ghl`, `fub`, or pre-exported contact JSON.
2. Pull and normalize contacts into a common schema.
3. Filter to records with mailable addresses.
4. Build personalized message content.
5. Submit jobs to PostGrid (`letters` or `postcards`) with dry-run available.
6. Return send summary with success/failure per contact.

## Script

- `scripts/crm_postgrid_mailer.py`
Purpose: Pull contacts from GHL/FUB (or load from JSON), normalize fields, render templates, and send to PostGrid.
- `scripts/postgrid_api.py`
Purpose: Full PostGrid API utility with broad endpoint catalog and `call-raw` fallback for any documented endpoint.

## Environment Variables

- `GHL_API_KEY`: GHL API key/token.
- `GHL_BASE_URL` (optional): defaults to `https://services.leadconnectorhq.com`.
- `FUB_API_KEY`: Follow Up Boss API key.
- `FUB_BASE_URL` (optional): defaults to `https://api.followupboss.com/v1`.
- `POSTGRID_API_KEY`: PostGrid API key.
- `POSTGRID_BASE_URL` (optional): defaults to `https://api.postgrid.com/print-mail/v1`.

## Typical Commands

List full PostGrid endpoint catalog included in this skill:

```bash
python3 scripts/postgrid_api.py list-endpoints
```

Call a cataloged PostGrid endpoint:

```bash
python3 scripts/postgrid_api.py call contacts.list
```

Call any PostGrid endpoint directly (full docs coverage fallback):

```bash
python3 scripts/postgrid_api.py call-raw GET /letters \
  --base-url https://api.postgrid.com/print-mail/v1
```

Normalize contacts from FUB to JSON:

```bash
python3 scripts/crm_postgrid_mailer.py fetch \
  --provider fub \
  --limit 200 \
  --output /tmp/fub_contacts_normalized.json
```

Normalize contacts from GHL to JSON:

```bash
python3 scripts/crm_postgrid_mailer.py fetch \
  --provider ghl \
  --location-id "$GHL_LOCATION_ID" \
  --limit 200 \
  --output /tmp/ghl_contacts_normalized.json
```

Dry-run PostGrid payload generation:

```bash
python3 scripts/crm_postgrid_mailer.py send \
  --contacts-file /tmp/ghl_contacts_normalized.json \
  --from-json-file references/example_sender_us.json \
  --html-template-file references/example_letter_template.html \
  --mail-route letters \
  --dry-run
```

Fetch + send in one command:

```bash
python3 scripts/crm_postgrid_mailer.py run \
  --provider fub \
  --limit 100 \
  --from-json-file references/example_sender_us.json \
  --html-template-file references/example_letter_template.html \
  --mail-route letters \
  --output /tmp/mail_send_summary.json
```

Send one ad-hoc mailer from raw address + content:

```bash
python3 scripts/crm_postgrid_mailer.py one-off \
  --to-name "Jane Seller" \
  --to-address1 "742 Evergreen Terrace" \
  --to-city "Springfield" \
  --to-state "IL" \
  --to-postal-code "62704" \
  --from-json-file references/example_sender_us.json \
  --content-text "Hi Jane,\n\nI'd love to send you a fresh home valuation this week.\n\nBest,\nDaniel" \
  --mail-route letters \
  --dry-run
```

Use JSON exported by another GHL/FUB skill:

```bash
python3 scripts/crm_postgrid_mailer.py run \
  --contacts-file /tmp/contacts_from_other_skill.json \
  --from-json-file references/example_sender_us.json \
  --html-template-file references/example_letter_template.html \
  --mail-route letters
```

## Data Contract

Normalized contact shape:

- `id`
- `first_name`
- `last_name`
- `full_name`
- `email`
- `phone`
- `address1`
- `address2`
- `city`
- `state`
- `postal_code`
- `country`
- `tags`
- `raw`

Contacts missing `address1`, `city`, `state`, or `postal_code` are skipped by default.

## Integration Notes

- If dedicated GHL/FUB skills exist and already return contact JSON, pass that file with `--contacts-file` and skip API pulling.
- If APIs change, adjust mapping candidates in `scripts/crm_postgrid_mailer.py` instead of rewriting workflow.
- Use `--postgrid-route` when account-specific PostGrid routes differ from defaults.

## PostGrid Safety

- Start with `--dry-run` to inspect generated payloads.
- Keep `--max-send` during first live run (for example `--max-send 10`).
- Include clear campaign metadata using `--description`.

See `references/postgrid-notes.md` for route/header assumptions and override strategy.
