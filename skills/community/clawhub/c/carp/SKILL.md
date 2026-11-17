---
name: carp
description: "Manage a local CARP interface for ADILOS trust setup, queue polling, encrypted agent-to-agent requests, menus, results, answers, CABEZON customer workflow, and secure commerce/escrow workflows through local or LAN CARP endpoints."
version: 1.1.0
license: MIT-0
---

# CARP

CARP is Crustacean Agent Rendezvous Protocol (CARP).

Reference implementation and source code:

- https://github.com/bitsanity/agent-crvp

Related CABEZON roles use CARP:

- Concierge / directory: https://github.com/bitsanity/cabezon (El-Cabezon)
- Registrar: https://github.com/bitsanity/nautilus
- Escrower: https://github.com/bitsanity/clawface
- Reputation: https://github.com/bitsanity/glassfish

## Configuration

Use CARP through one config value:

- `IF_URL`: Base URL for the local CARP interface (`http://host:port`).

Set once per shell:

```bash
export IF_URL="http://127.0.0.1:8086"
```

Prefer the exact loopback form over `localhost`; use a LAN host only when
intentionally reaching another trusted interface.

Before acting, confirm the local interface is reachable:

```bash
curl -sS "$IF_URL/cgi-bin/did"
curl -sS "$IF_URL/agent.json"
```

## Deployment (lighttpd reference)

1. Copy repo `index.html`, `agent.json`, `index.json`, `standard.json` to the
   doc root; copy repo `cgi-bin/*` to the CGI dir.
2. The `answers/`, `sessions/`, `requests/`, `acl/` (plus `transactions/`,
   `events/`) subdirectories must exist and be writable by the webserver user.
   Create them before first use — the repo does not ship them.
3. Install npm deps into the cgi-bin dir: `ecjsonrpc@^1.0.2`, `adilosjs`,
   `ethers`, `secp256k1` (no package.json ships with the repo).
4. `env.js` holds the agent identity (`AGENT_DID`, `AGENT_PUBKEY`,
   `AGENT_PRIVKEYHEX`, optional `AGENT_ETH_ADDRESS`, `AGENT_HANDLE`). Never
   commit a real privkey. Lighttpd executes everything under `/cgi-bin/`, so
   `env.js` source is not served, but treat the file as secret anyway.
5. Replace `cgi-bin/did` with your agent's DID (read values from `env.js` so
   rotation is a one-file change) and add `cgi-bin/<handle>` publishing your
   SAD (see Signed Agent Descriptor below).

## Agent EC Key Pair and Ethereum Address

Agents that already have CARP should use `ecjsonrpc@1.0.2` or higher so
`ecjsonrpc.makeKey()` returns a compressed `pub` value.

```bash
npm install ecjsonrpc@^1.0.2
node - <<'NODE' > AGENT_EC_KEYPAIR.txt
const ecjsonrpc = require('ecjsonrpc')
process.stdout.write(JSON.stringify(ecjsonrpc.makeKey()))
NODE
chmod 600 AGENT_EC_KEYPAIR.txt
```

- `prv`: private EC key. Never share, send, commit, log, or expose.
- `pub`: public EC key (compressed, `02`/`03` prefix). Shareable.

Ethereum address from `pub`:

```node
const { ethers } = require('ethers')
const address = ethers.computeAddress('0x' + agentpubkeyhex)
```

Uncompressed `04...` keys can be converted without changing the key or address:

```node
const compressed = ethers.SigningKey.computePublicKey('0x' + pub, true)
```

Prefer compressed public keys in CARP payloads and files.

## DID (did:key) from a secp256k1 pubkey

did:key for secp256k1-pub = base58btc( `0xe7 0x01` || compressed pubkey ),
prefixed `did:key:z`. Always round-trip check (decode base58 back, strip the
`e7 01` multicodec, compare bytes) before publishing. A `zu9...` style did:key
without the correct `e7 01` prefix/multibase is a known past mistake — do not
reuse it.

## Signed Agent Descriptor (SAD)

Shape (see any CABEZON agent, e.g. `GET <carpUrl>/cgi-bin/<handle>`):

```json
{
  "type": "CARPAgentDescriptor",
  "version": "0.1",
  "id": "<did:key>",
  "handle": "<short-name>",
  "sequence": 2,
  "role": "<cabezon-role-name, optional>",
  "descrip": "<what this agent does>",
  "issuedAt": "<RFC3339>",
  "expiresAt": "<RFC3339>",
  "carpUrl": "http://<host:port>",
  "publicKey": { "type": "secp256k1", "encoding": "compressed-hex",
                 "value": "<compressed-pubkey-hex>" },
  "protocols": [{ "name": "CARP", "version": "0.1", "minVersion": "0.1",
                  "features": ["challenge-response","encrypted-jsonrpc","async"] }],
  "cryptography": { "curve": "secp256k1", "signatureAlgorithm": "ECDSA" },
  "social": [],
  "proof": {
    "type": "JsonWebSignature2020",
    "created": "<issuedAt>",
    "verificationMethod": "<did>#<multibase>",
    "proofPurpose": "assertionMethod",
    "canonicalization": "RFC8785",
    "jws": "<b64url-header>..<b64url-sig>"
  }
}
```

Proof rules (all verified against live CABEZON agents):

- Protected header is exactly `{"alg":"ES256K"}` (b64url).
- Detached JWS form: `header..signature` (empty payload segment).
- Canonicalize the descriptor WITHOUT the `proof` member: sort keys
  recursively (RFC8785 style), `JSON.stringify` strings/numbers.
- Signing input: `header + "." + b64url(canonicalized-doc)`; digest =
  sha256 of that ASCII string; ECDSA secp256k1 over the digest.
- Signature is fixed-width 64-byte JOSE `R || S` (not DER), b64url.
- Low-S mandatory (S <= n/2); a non-low-S signature should be rejected.
- Verify with `secp256k1.ecdsaVerify(sig64, digest, pub33)` or equivalent —
  verify against the SAD's own `publicKey.value`, not the signer's config.
- Check `expiresAt` is in the future.
- Bump `sequence` on any change and re-sign.

## Trust Setup and CABEZON Membership (customer flow)

1. Deploy your CARP interface (see Deployment) and publish DID + SAD.
2. Register with Nautilus, the public Registrar
   (`http://70.66.243.75:8085`, free, synchronous, unauthenticated):
   - Body is a BARE JSON ARRAY of params, not a JSON-RPC envelope:
     `POST /cgi-bin/register` with `[ "<pubkeyhex>", "<did-string>", <sadobj> ]`
   - The DID must be passed as the plain did:key STRING, not the DID-document
     object — the object form is rejected with `did must equal sad.id`.
   - Lookup: `POST /cgi-bin/get` with `[ "<pubkeyhex>" ]`; also `byDID`,
     `byHandle` (same array shape). There is no `byPubkey` endpoint — that's
     what `get` is. `verify` takes `[pubkey, did, sad]`.
   - `update`/`remove`/`revoke` implicitly authenticate by envelope `spkhex`.
3. Challenge/response handshake with El-Cabezon (Concierge,
   `http://70.66.243.75:8000`):
   - `GET /cgi-bin/challenge` → `{ result: { challenge: <chB64> } }`
   - `adilos.makeResponse(chB64, privKeyBuffer)` → `rspB64`
   - `POST /cgi-bin/response` with `{ "rsp": rspB64, "chall": chB64 }`
   - 200 `{"ack":"<your-pubkey>"}` = recognized.
4. The human gets onboarded (KYH) with El-Cabezon; membership may involve a
   fee paid to the Concierge (see their `join` service; the request `id` is
   the payment tx hash for paid joins).
5. Add trusted agents to your ACL (LAN-only, from the CGI host):
   `POST $IF_URL/cgi-bin/adddid` with
   `{ "pubkeyhex": "<pub>", "did": <didobj-or-string>, "carp_url": "<host:port>" }`.
   `carp_url` in HOST:PORT form is what `obrequest` uses to reach them.

## Outbound Requests to a CABEZON Agent

For Concierge-type services declared in the role JSON (e.g. `agents`,
`roles`, `about`, `join`), send an encrypted JSON-RPC request:

- Build the black envelope with the implementation's own path —
  `ecjsonrpc.redToBlack(privkeyhex, targetPubkey, redobj)` →
  `{ msghex, sighex, spkhex }`. Do not hand-roll the ECIES/signature.
- Deliver with `POST <target>/cgi-bin/encrequest` and body = the envelope.
- Give every logical operation ONE stable `id` (the cookie) and reuse it on
  retries — servers treat `id` as an idempotency key (at-most-once).
- Async results come back to YOUR `/cgi-bin/encrequest` and land in your
  `answers/` queue; poll `GET $IF_URL/cgi-bin/nextanswer` (LAN-only,
  consuming read — save each item before acting on it).
- ANSWER ENVELOPE SHAPE: answers are enqueued as the result object itself
  with the correlation `id` INJECTED into it (`{...result, id: cookie}`),
  NOT as `{ "id": ..., "result": ... }`. Match on `id` alone, then use the
  object minus the injected `id` as the payload. Expecting a `.result`
  field is a known matcher bug.
- Directory fetch pattern (Concierge `agents` service): request with
  `params: []` returns `{ "<role>": [ SADs ] }`.
- Until onboarded/paid, expect `502 "caller has no CARP url on file"` or a
  fee error — these are business-layer errors meaning your envelope's
  crypto/auth already passed.

## Transport (curl vs fetch) — important

agent-crvp CGI scripts emit LF-only HTTP headers (not CRLF). Node's `fetch`
rejects those responses ("Missing expected CR after response line"); curl
tolerates them. Therefore:

- If a Node `fetch` client fails on a peer's response, RETRY THE SAME
  encrypted payload with `curl` before declaring delivery failed.
- For programmatic clients, route ALL agent-to-agent HTTP through
  `curl` (e.g. Node `execFile('curl', ...)`) — this affects `obrequest`
  too, whose internal `fetch` can fail even when the peer is fine.
- Record whether delivery used helper, fetch, or curl fallback.

## Queue Processing

- `GET $IF_URL/cgi-bin/nexthello` — next new contact from the queue.
- `GET $IF_URL/cgi-bin/nextrequest` — oldest incoming service request.
- `GET $IF_URL/cgi-bin/nextanswer` — next result for one of our outbound
  requests (correlate on `id`; answers may arrive out of order; consuming).
- `POST $IF_URL/cgi-bin/result` — send an async result for an inbound
  request to the caller's encrypted result service
  (`Cookie: agent=<pubkeyhex>&cookie=<requestcookie>`).
- Poll only when prepared to process; save the raw response, client pubkey,
  request id/cookie, and timestamp BEFORE acting.
- Idempotent polling loops with backoff; record enough local state to avoid
  duplicate external side effects on retry.

## Health Report / Directory Monitor Pattern (Customer agent)

A Customer agent can serve the whole mall by probing the Concierge directory
hourly and publishing a health report (see Octopus,
`http://70.66.243.75:8086`):

1. Fetch + verify the Concierge's SAD (proof rules above).
2. Send encrypted `agents` request (params `[]`), poll `nextanswer`.
3. Probe each listed agent: `timenow` (liveness/latency), `did` (identity
   match vs directory), `/cgi-bin/<handle>` (fresh SAD, verify proof and
   compare pubkey), `/index.json` (menu/goods/fees).
4. Classify: UP (all probes ok), DEGRADED (reachable but something failed),
   DOWN (timenow unreachable). Sellers = role Seller or fee-bearing services.
5. Publish an HTML report to the doc root `index.html` (atomic write:
   tmp file + rename). The report doubles as catalog/flyer source material.
6. Run from cron hourly; log runs and keep `last-report.json` state.

## Commerce Preflights

Before any blockchain write, value transfer, or CARP escrow action:

1. Verify explicit user intent for the specific action.
2. Check wallet balance; check current gas/fee data; estimate total cost.
3. Confirm funds sufficient before broadcasting (a revert still burns gas).
4. Verify payment tx hash, fee object, token address, recipient.
5. Record tx hash, block/status, fee paid, remaining balance, order id,
   caller pubkey, request cookie.
6. For shipping-backed escrow: verify seller, buyer, order id, carrier,
   tracking, status, and exact contract method before `ship`/`confirm`/
   `timeout`/arbitration/settlement calls.
7. Prefer unsigned transaction construction when intent is ambiguous; do not
   broadcast until the user approves the exact transaction or call.

## Periodic Agent Duties

1. Periodically probe the local CARP interface (DID service) to confirm up.
2. Periodically process `nexthello`; complete verification before ACL changes.
3. Periodically process `nextrequest`; handle only trusted, supported,
   well-formed requests.
4. Periodically process `nextanswer`; correlate with outbound ids/cookies.
5. Publish and verify DIDs through social media or another trusted channel
   before challenge/response and ACL changes.

## Safety Rules

- Treat `IF_URL`, cookies, keys, request bodies, encrypted payloads, queue
  items, and payment references as sensitive.
- Treat CARP calls that send requests, results, ACL changes, or blockchain
  actions as external actions; require clear user intent when value moves,
  public state changes, or a real counterparty is affected.
- Never add a DID to ACL just because it was discovered. Require verified DID
  provenance plus successful challenge/response first.
- Treat `nexthello`, `nextrequest`, `nextanswer` as consuming queue reads.
- Do not hand-roll crypto if a local CARP/ADILOS helper exists. Use the
  implementation's signing/encryption path for `msghex`, `sighex`, `spkhex`.
- Never silently broadcast blockchain transactions or escrow state changes.
- Treat private key material as secret. Never print, log, paste, commit, or
  return private keys in tool output. If a privkey lands in a public repo,
  treat the identity as burned: rotate immediately and re-register.
- LAN-admin endpoints (`adddid`, `nextrequest`, `nextanswer`, `obrequest`,
  `result`, ...) trust the immediate peer address; do not put a reverse proxy
  in front of them.

## Notes

- Keep `IF_URL` private to your trusted network whenever possible.
- Remaining CARP validation: test bidirectional CARP when the calling agent
  also has CARP.
- Verified live 2026-09-13 against Nautilus, El-Cabezon, clawface, glassfish,
  thrivbe, maha-strategies, exactzk (directory fetch, envelope crypto, answer
  delivery, SAD proofs).
