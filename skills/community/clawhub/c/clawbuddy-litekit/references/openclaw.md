# OpenClaw integration reference

ClawBuddy LiteKit talks to OpenClaw via the OpenResponses HTTP API,
proxied through a Lovable Cloud edge function (`openclaw-proxy`) so the
API key never ships to the browser.

## Required secrets (Lovable Cloud)

- `OPENCLAW_GATEWAY_URL` — e.g. `https://gateway.openclaw.ai`
- `OPENCLAW_API_KEY` — server-side only

## Endpoints used

- `POST /v1/responses` — primary request/response surface
- `GET  /v1/agents`    — agent registry hydration
- `GET  /v1/health`    — surfaced as the "Connected" badge

## Docs

- Gateway: <https://openclaw-openclaw.mintlify.app/concepts/gateway>
- OpenResponses HTTP: <https://documentation.openclaw.ai/gateway/openresponses-http-api>
- Agent Protocol: <https://openclaw-openclaw.mintlify.app/api/agent-protocol>
