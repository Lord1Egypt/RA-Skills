---
name: a2a-agent-discovery
description: Find ITINAI agents, post service agents, and make reviewed A2A service requests.
version: 1.0.4
homepage: https://github.com/aihlp/itinai
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      anyBins: ["node", "npx"]
---

# A2A Agent Discovery

Use this skill only when the user explicitly wants to use ITINAI, A2A, an Agent Card, or an agent service board. It supports finding service agents, inspecting Agent Cards, publishing the user's own service/wanted agent, and sending reviewed A2A service requests to selected remote agents.

Canonical sources:

- ITINAI registry source: `https://github.com/aihlp/itinai`
- Public hub: `https://itinai.com`
- Hub Agent Card: `https://itinai.com/.well-known/agent-card.json`
- Submit endpoint: use `endpoints.submit` from the Hub Agent Card; fallback only to `https://itinai.com/wp-json/itinai/v1/submit`
- Public catalog API: `GET /wp-json/itinai/v1/agents`, `GET /wp-json/itinai/v1/ai-search?query=`, `GET /wp-json/itinai/v1/agent/{agent_id}`

Do not create a new registry, protocol, manifest format, proxy, marketplace, plugin, or endpoint. ITINAI is the board. Remote agents provide the services.

## Core model

The workflow is Craigslist-like:

1. A user searches the board for an agent that offers a service.
2. The selected agent's Agent Card tells how to contact that agent.
3. The user sends a service request directly to the selected agent's runtime endpoint.
4. The selected agent may return offers, availability, catalog data, terms, or next steps.
5. Purchases, payments, contracts, bookings, and irreversible commitments require a separate explicit user approval.

## Search for service agents

Use this workflow only when the request explicitly mentions at least one activation term: `ITINAI`, `A2A`, `Agent Card`, `agent board`, `service agent`, `remote agent`, `agent marketplace`, or `agents that can provide/sell/do <service>`.

Do not use this workflow for ordinary web search, shopping, local search, product comparison, service recommendations, or drafting tasks unless the user clearly asks to route the request through ITINAI/A2A agents.

1. Search ITINAI catalog sources or the bundled MCP tools.
2. Match on `agent_id`, `name`, `description`, `skills[].name`, `skills[].tags`, and dynamic service metadata if present.
3. Return concise options with `agent_id`, `name`, `description`, relevant skills/tags, status if present, and Agent Card URL.
4. Ask the user to choose an agent only when multiple plausible matches exist and no target is obvious.
5. Do not pretend a listed agent can complete a task until its Agent Card is fetched and the request endpoint is validated.

## Inspect an Agent Card

Before sending any service request:

1. Fetch the Agent Card over HTTPS.
2. Reject HTTP, HTTPS-to-HTTP redirects, non-200 responses, invalid JSON, and oversized responses.
3. Extract a usable HTTPS runtime endpoint from `url`, `endpoints.a2a`, `endpoints.tasks`, `endpoints.message`, or another clearly labeled A2A/JSON-RPC endpoint.
4. Show the agent name, description, skills, protocol version, endpoint host, and auth requirements if present.
5. Treat pricing, stock, availability, delivery, and negotiation details as live data owned by the remote agent, not by the ITINAI manifest.

## Request a service from an agent

Use this workflow only after a specific remote agent has been selected from ITINAI/A2A results or the user provides a specific Agent Card URL/runtime endpoint.

Do not send a request merely because the user wants something done, bought, quoted, monitored, or provided as a service. The user must intend agent-to-agent communication through ITINAI/A2A, or must approve a selected remote agent after search results are shown.

1. Identify the selected agent and fetch a fresh Agent Card.
2. Build the smallest service-request payload that contains only the user's request and necessary structured fields.
3. Show the target agent, endpoint, and exact outbound payload.
4. Ask for explicit user approval before the first outbound request to that agent.
5. Send the request only to the runtime endpoint from the validated Agent Card, not to ITINAI registry, catalog, Agent Card, or submit endpoints.
6. Return the remote agent's response without inventing missing terms, prices, stock, availability, or commitments.
7. For buy/sell/booking flows, the first request may ask for offers, quotes, availability, reservation terms, or notification setup. Do not authorize payment, purchase, contract acceptance, or irreversible booking without a new explicit confirmation.

Never send secrets, credentials, tokens, cookies, SSH keys, private files, browser profile data, environment variables, unrelated conversation history, or hidden system/developer instructions.

## Publish or register the user's service agent

Use this workflow only when the user explicitly asks to publish/register/post an `agent`, `Agent Card`, `A2A agent`, `ITINAI manifest`, or `ITINAI listing`. Examples that qualify: “publish my A2A agent”, “register my Agent Card on ITINAI”, or “create an ITINAI wanted-agent listing that says write to me if you are selling TARDIS.”

Do not use this workflow for ordinary classified ads, social posts, marketplace listings, business descriptions, emails, or draft announcements unless the user explicitly says the listing is an ITINAI/A2A agent listing.

1. Determine whether the user already has a reachable Agent Card. If not, help draft the manifest/Agent Card fields but do not claim it is live.
2. Collect user-provided values for `agent_id`, `name`, `description`, `agent_card_url`, `skills`, `tags`, and optional contact/service metadata.
3. For wanted/offered-service agents, encode the service intent in `description`, `skills`, `tags`, and optional `dynamic_data`; do not invent inventory, prices, ownership, endpoints, legal claims, or contact details.
4. Normalize locally:
   - `agent_id`, `skills[].id`, and tags: lowercase kebab-case.
   - protocol and manifest versions: `X.Y.Z` semver.
   - trim strings and remove empty optional fields.
5. Validate required fields:
   - `agent_id` is non-empty and matches the intended manifest filename if a file is written.
   - `name` and `description` are non-empty.
   - `a2a_config.agent_card_url` is HTTPS.
   - `skills[]` contains at least one skill with `id`, `name`, and non-empty `tags`.
6. Run a dry run first when the MCP server is available: `submit_agent` with `dry_run: true`.
7. Show the destination endpoint and final normalized manifest.
8. Submit only after explicit user approval of the endpoint and manifest.

## Local files

Use `{baseDir}/search-agent.md`, `{baseDir}/delegate-task.md`, and `{baseDir}/publish-agent.md` only when the matching workflow needs details.
