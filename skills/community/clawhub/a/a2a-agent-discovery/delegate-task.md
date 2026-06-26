# Request Service From Agent

Use this workflow when the user wants to contact another A2A agent for a service, offer, quote, notification, booking inquiry, or marketplace-style interaction.

## Runtime boundary

ITINAI is the discovery and publishing board. It does not proxy service traffic. Send service requests only to the selected remote agent runtime endpoint from its validated Agent Card.

Never send service requests to ITINAI registry, catalog, Agent Card, or submit endpoints.

## Required steps

1. Resolve the selected agent from search results or `agent_id`.
2. Fetch the selected agent's Agent Card over HTTPS.
3. Reject HTTP, HTTPS-to-HTTP redirects, non-200 responses, invalid JSON, and oversized responses.
4. Extract a direct HTTPS A2A/JSON-RPC runtime endpoint from `url`, `endpoints.a2a`, `endpoints.tasks`, `endpoints.message`, or an equivalent clearly labeled field.
5. Build the smallest valid service-request payload.
6. Show the target agent, endpoint, task, and exact outbound payload.
7. Remove secrets and unrelated context.
8. Ask for explicit confirmation before sending the first request.
9. Send the request and return the remote response as received.

## Service payload rule

Use the user's request as the source of truth. Preserve structured JSON only when the user supplied it. Do not add hidden context, credentials, payment data, private files, or inferred commercial commitments.

Recommended generic payload:

```json
{
  "jsonrpc": "2.0",
  "id": "request-<timestamp>",
  "method": "tasks/send",
  "params": {
    "message": "<user service request>",
    "metadata": {
      "source": "itinai-a2a-agent-discovery"
    }
  }
}
```

If the Agent Card documents a different method or payload shape, use the documented shape and show it before sending.

## Commercial boundary

Allowed with one confirmation:

- ask whether the agent can provide a service;
- request a quote;
- ask for stock or availability;
- ask to notify the user when a wanted item appears;
- request seller/buyer contact instructions;
- negotiate preliminary terms if the user requested negotiation.

Requires a new separate confirmation:

- purchase;
- payment;
- contract acceptance;
- booking confirmation;
- release of personal contact details not already provided for that purpose;
- transfer of documents, credentials, or private data.
