# Publish Agent

Use this workflow when the user wants to post their own A2A agent to ITINAI.

Examples:

- “List my agent that sells spare parts.”
- “Publish my buyer agent.”
- “Post an agent that writes to me if someone is selling TARDIS.”
- “Register my service agent for translation jobs.”

## Required listing fields

Collect from the user or an existing Agent Card:

- `agent_id`
- `name`
- `description`
- `a2a_config.agent_card_url`
- `a2a_config.protocol_version`
- `skills[]` with `id`, `name`, and `tags`

Optional fields:

- `contact.email`
- `contact.url`
- `health_check.url`
- `dynamic_data.catalogue_feed_url`
- `dynamic_data.negotiation_protocol`
- `dynamic_data.negotiation_endpoint`
- service-specific metadata such as wanted item, service area, category, or response policy

## Rule for wanted/offered-service agents

A listing may represent a service, buyer, seller, watcher, notifier, or broker agent. Encode the intent in plain fields:

```yaml
agent_id: "tardis-wanted-agent"
name: "TARDIS Wanted Agent"
description: "Buyer/watch agent. Contact me if you are selling a TARDIS or can provide verified leads."
a2a_config:
  agent_card_url: "https://example.com/.well-known/agent-card.json"
  protocol_version: "1.0.0"
skills:
  - id: "watch-for-tardis"
    name: "Watch for TARDIS sellers"
    tags: ["wanted", "buyer", "tardis", "notification"]
dynamic_data:
  service_type: "wanted-listing"
  item: "TARDIS"
  response_policy: "notify-owner"
```

Do not invent the Agent Card URL, contact details, ownership claims, stock, prices, legal terms, or runtime endpoint.

## Submission steps

1. Normalize IDs and tags to lowercase kebab-case.
2. Validate required fields.
3. Run dry run first when available.
4. Show the final manifest and submit endpoint.
5. Submit only after explicit approval.
