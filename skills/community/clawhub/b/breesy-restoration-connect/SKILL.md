---
name: breesy-restoration-connect
description: Submit customer-authorized property damage restoration help requests for water, fire, mold, storm, biohazard, and reconstruction services across the United States.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://breesy-connect.com
    skillKey: breesy-restoration-connect
---

# Breesy Restoration Connect

Use this skill when a customer needs restoration help for water damage, flooding, fire, smoke, mold, storm damage, biohazard cleanup, or reconstruction.

## API

- OpenAPI: https://breesy-connect.com/openapi.json
- Agent instructions: https://breesy-connect.com/llms.txt
- Agent manifest: https://breesy-connect.com/.well-known/agent.json
- Agent card: https://breesy-connect.com/.well-known/agent-card.json

## Main Action

Use `submitRestorationRequest` to submit a customer-authorized restoration request.

Endpoint:

`POST https://breesy-connect.com/api/requests`

Authentication is not required.

## Consent Rule

Only submit requests when the customer has authorized contact from Breesy Restoration Connect or its restoration partners.

## Required Fields

- `urgency`
- `serviceType`
- `serviceLocation`
- `state`
- `details`
- `callbackPhone`

Use `idempotencyKey` when retrying the same customer request.
