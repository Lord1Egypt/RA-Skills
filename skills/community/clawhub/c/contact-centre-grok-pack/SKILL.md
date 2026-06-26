---
name: contact-centre-grok-pack
description: Triage call-centre and voice support transcripts into summaries, sentiment, urgency, routing queues, and follow-up actions. Use for OpenClaw-ready Grok/voice contact centre workflows for councils, clinics, support desks, and SMEs.
---

# Contact Centre Grok Pack

Use this skill to convert raw call transcripts or voice-agent notes into operational routing output.

## Workflow

1. Export the transcript as plain text or JSON with a `transcript` field.
2. Run `scripts/contact_centre_grok_pack.py` with the relevant industry profile.
3. Review the JSON result before routing to live case systems.
4. Feed `summary`, `route`, and `actions` into downstream CRM/helpdesk workflows.

## Parameters

- `--input PATH`: Transcript text or JSON. If omitted, a demo complaint transcript is used.
- `--industry {council,clinic,support,sme}`: Tunes routing keywords.
- `--output PATH`: Optional JSON output path.
- `--sla-hours INT`: Target SLA used for urgency labelling.

## Outputs

- `summary`: One-line case summary.
- `sentiment`: positive, neutral, frustrated, or distressed.
- `urgency`: low, normal, high, or critical.
- `route`: Recommended queue/team.
- `actions`: Human-readable next steps.
- `evidence`: Keywords and reasons used.

This skill does not make calls, contact customers, or write to external systems.
