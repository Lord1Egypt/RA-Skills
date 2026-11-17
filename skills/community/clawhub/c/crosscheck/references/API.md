# crosscheck HTTP API

Base URL: https://crosscheckapi.com. All bodies are JSON. The authoritative, always-current summary is https://crosscheckapi.com/llms.txt.

## POST /v1/quote (free)

Request: `{"draft": "<text>"}`

Response 200:

```json
{"chars": 179, "units": 179, "price_usd": "0.02", "amount": "20000",
 "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "network": "eip155:8453", "pay_to": "0x…",
 "payment_options": [
   {"network": "eip155:8453", "label": "Base", "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "amount": "20000"},
   {"network": "eip155:84532", "label": "Base Sepolia (testnet)", "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e", "amount": "20000"}],
 "accepting": true, "free_tier": {"available": false},
 "order": {"method": "POST", "url": "https://crosscheckapi.com/v1/check"}}
```

400 for a missing or empty draft or one containing control or invisible tag characters, 413 above 48,000 units. Size is measured in units: one per character, or half the UTF-8 byte length when that is larger, so most non-Latin text and emoji count 1.5 to 2 units per character. `payment_options` has one entry per accepted network.

## POST /v1/check (paid, x402 v2)

Optional `sources`: up to 10 items, each a string or `{"text", "title", "url"}`, holding the text the draft relies on. They count toward size and price. The verdict then has `grounding` with each claim marked `supported`, `contradicted`, or `not_found`; a quote counts only if code finds it in that source. A contradicted claim is a major issue.


1. Send `{"draft": "<text>"}` with no payment header. Response: 402 with header `PAYMENT-REQUIRED` (base64 JSON, x402 v2). `accepts` has one option per network, Base (`eip155:8453`, USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, `extra.name` "USD Coin") first and Base Sepolia (`eip155:84532`, `extra.name` "USDC") second. Each has `scheme: "exact"`, `amount` (atomic USDC, 6 decimals), `asset`, `payTo`, `maxTimeoutSeconds: 300`, and `extra: {"name", "version": "2", "paymentFlow": "upfront"}`.
2. Sign an EIP-3009 `TransferWithAuthorization` for exactly `amount` to `payTo`, build the v2 payment payload with `accepted` equal to the option you pay (keep every `extra` field), and resend the identical body with header `PAYMENT-SIGNATURE: <base64 payload>`.
3. The payment settles before the review runs. Responses:
   - 200: `{"job_id", "status": "done", "verdict", "receipt", "result_url", "result_token", "receipt_keys_url"}` plus header `PAYMENT-RESPONSE`.
   - 202: `{"job_id", "status": "pending", "retry_after_seconds", "result_url", "result_token"}`. Poll the result.
   - 400, 402, 409, 413, 503 with "Nothing was charged": fix and retry with a new payment.

Each signed authorization buys one check. If you lose the response, resend the identical request (same body, same PAYMENT-SIGNATURE header): you get the same job and result token back, and nothing more is charged. Reusing the authorization for a different request returns 409.

## POST /v1/accept/quote (free) and POST /v1/accept (paid, x402 v2)

Check work another agent or service handed back, before you pay for it, release escrow, or pass it on.

Request: `{"task": "<what you asked for>", "deliverable": "<what came back>", "reference": "<optional, up to 200 characters>", "payment_tx": "<optional 0x transaction hash>", "payment_network": "eip155:8453"}`. With `payment_tx`, crosscheck reads that transaction's USDC transfers from the chain and adds `payment_reference` (status `verified` when it found them) to the verdict and the receipt. Size is the task plus the deliverable, in the same units as a draft. Price: $0.03 up to 12,000 units, plus $0.01 per further 12,000, up to 48,000 units ($0.06). Payment works exactly as for /v1/check.

Verdict: `{"accept": false, "summary": "...", "requirements": [{"requirement": "List 5 competitors", "met": "partly", "evidence": "Counted 3 items; the task asks for exactly 5 items.", "subjective": false, "blocking": true}], "injection_suspected": false}`. `accept` is true only when no requirement is blocking: `no` and `partly` always block, `cannot_tell` blocks unless the requirement is subjective. The receipt body has `kind: "accept"`, `task` and `deliverable` (`sha256`, `chars`), `reference`, the payment, and `review` (`accept`, `requirements`, `blocking`, `verdict_sha256`, model, prompt version).

## POST /v1/skillcheck/quote (free), POST /v1/skillcheck (paid), GET /v1/skillcheck/{bundle_sha256} (free)

Security review of a skill or MCP server before install. Request: `{"files": [{"path": "SKILL.md", "content": "..."}, ...]}` (1 to 50 text files) or `{"content": "..."}` for a single SKILL.md. Files may contain invisible characters (the scan looks for them). Price: $0.03 up to 12,000 units of content, plus $0.01 per further 12,000, up to 48,000 units ($0.06).

Verdict: `{"result": "findings", "risk": "high", "summary", "declared_purpose", "findings": [{"severity": "critical|high|medium|low", "category", "file", "location", "explanation", "source": "rule|review"}], "files_scanned", "bundle_sha256", "note"}`. `bundle_sha256` is SHA-256 of the canonical JSON list of `{path, sha256}` for every file, sorted by path. GET `/v1/skillcheck/{bundle_sha256}` returns the latest paid review of the same files (404 if none). The receipt body has `kind: "skillcheck"`, `bundle` (`sha256`, `files`, `chars`), and `review` (`result`, `risk`, `finding_counts`).

## GET /v1/checks/{job_id} (free)

Header: `Authorization: Bearer <result_token>` (the token is not accepted in the URL). Returns the same shape as the order response. `status` is `done`, `pending`, `unserved` (refund owed, recorded in the ledger), or `rejected` (payment not confirmed on chain; no review ran). 404 for an unknown job or wrong token.

## GET /.well-known/crosscheck-keys.json

`{"keys": [{"kty": "OKP", "crv": "Ed25519", "x": "…", "kid": "…", "alg": "EdDSA"}], "ledger_head": {"seq": 12, "hash": "…"}}`

## Receipt verification

`receipt.body` canonical JSON: object keys sorted at every level, no whitespace, standard JSON string escaping. Check `sha256(canonical(body)) == receipt.hash`, then verify `receipt.sig` (base64url, Ed25519) over the same bytes with the key whose `kid == body.key_id`. Check `sha256(canonical(verdict)) == body.review.verdict_sha256`. `body.prev_hash` links to the previous ledger entry.
