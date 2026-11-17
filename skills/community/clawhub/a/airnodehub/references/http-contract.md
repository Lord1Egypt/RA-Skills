# Airnode Hub interfaces

## MCP discovery and calls
POST https://airnodehub.api3.org/mcp with Content-Type: application/json and Accept: application/json, text/event-stream. A connected MCP client handles transport; without one, parse JSON or SSE data lines according to Content-Type and reject JSON-RPC errors and tool isError.

Example request:
```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search-listings","arguments":{"query":"bitcoin","limit":3}}}
```

Current tools (inspect tools/list for changes):
- search-listings: query string, limit 1–10; empty query browses all. Keyword matching is not full-intent validation.
- get-listing-details: slugs array, 1–5. Inspect contract, price and signer.
- resolve-intent: intent string. Read candidates, unresolvedInputs and any outcome/provenance.
- call-operation: listing slug, operation, parameters object; optional responseProjection object mapping output names to RFC 6901 pointers.
- verify-attestation: full attestation, listing, operation and parameters together; include identical responseProjection when used. Require signature, signer and request binding to pass.

For example, call coingecko/simplePrice with {"ids":"ethereum","vs_currencies":"usd"}. An optional {"price":"/ethereum/usd"} projection is part of the signed request, not a post-verification edit.

## Direct HTTP
POST https://airnodehub.api3.org/resolve with {"intent":"current USD price of ETH"} for parameter-filled candidates. Treat candidates as proposals, not proof that missing inputs are resolved.

GET the selected catalogue Airnode URL for its live OpenAPI document. Read x-airnode.address and x-airnode.payment.prices and the POST request schema's operation variants. A live/cached signer mismatch requires investigation.

POST to the same URL with {"operation":"<live operation ID>","parameters":{}} and optional responseProjection. Success contains airnode, requestHash, timestamp, data, signature. Preserve the entire body.

Common failures: 400 invalid parameters; 404 unknown operation; 402 payment required; 429 rate limit; 502 upstream failure; 503 unavailable. Do not interpret failures as empty data or retry indefinitely. A signed provider error remains an error.

## Independent verification
The helper recomputes requestHash from JSON.stringify([operation, canonical(parameters)]) or, with projection, JSON.stringify([operation, canonical(parameters), canonical(responseProjection)]). Canonicalization recursively turns objects into key-sorted entry arrays while preserving array order.
It then checks the expected signer and EIP-191 signature over keccak256(encodePacked(bytes32 requestHash,uint256 timestamp,bytes dataBytes)); strings are UTF-8 directly and other data uses JSON.stringify.

Signing time is not observation time. Never reuse time-sensitive data merely because its operation is free. Apply a task-appropriate freshness policy using source timestamps or pinned chain blocks.

The helper accepts only URLs listed in the current official llms.txt catalogue, rejects credentials/query/fragment/nonstandard ports, redirects, private/reserved IPs and DNS answers, and caps response bodies at 4 MiB. DNS validation is applied in the connection lookup rather than as a separate preflight. It requires normal public DNS connectivity; proxy-only environments should use their supported MCP transport instead.

Sources:
- https://airnodehub-docs.api3.org/api-consumers/mcp
- https://airnodehub-docs.api3.org/airnode/attestation
