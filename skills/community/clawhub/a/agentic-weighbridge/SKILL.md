---
name: agentic-weighbridge
description: Use when an agent is about to pay an unfamiliar x402 endpoint. Read-only weighing of the live endpoint (402 challenge, v2 shape, accepts[], discovery manifest, openapi) with a verdict per check, plus how to obtain a signed, offline-verifiable verdict document from the hosted weighbridge.
category: agents
tags: [x402, verification, agents, payments, discovery, trust]
allowed-tools: [read-only-network, file-write-out-dir]
permissions:
  network:
    scheme: https-only
    documented_hosts:
      - https://xhagents.xyz
    other_hosts: "the endpoint the caller names; a table of attack URLs is refused by one guard (scripts/weigh_x402_endpoint.py, tests/test_guard.py)"
    payment: none
  file_write: "the --out directory only (default: none)"
  file_read: none
  environment: none
  secrets: none
  shell: none
---

# agentic-weighbridge

Bring an x402 endpoint, leave with a measurement. This skill has two halves:

1. a free, read-only local weigher (no keys, no payment, no writes outside `--out`);
2. how to get a signed verdict document from the hosted arena, which a third party can re-check
   offline and cite later.

## What this skill can do to your machine

| Capability | Where | Guard |
|---|---|---|
| HTTPS GET/POST to the endpoint you name (unpaid probes only) | `scripts/weigh_x402_endpoint.py` | one guard judges every hop: https only, refuses private, loopback, link-local, reserved and multicast addresses after DNS resolution, caps each body at 64 KB and the whole run at 8 requests |
| HTTPS GET to the same origin's `/.well-known/x402` and `/openapi.json` | same script | same guard, same caps |
| write a JSON result | same script, only with `--out` | that directory only |
| no wallet, no key, no signature, no payment | the whole package | the test asserts the script contains no payment code |

## Half one: weigh locally (free)

```bash
python3 scripts/weigh_x402_endpoint.py https://<seller-host>/<paid-route>
python3 scripts/weigh_x402_endpoint.py https://<seller-host>/<paid-route> --method POST --json
python3 scripts/weigh_x402_endpoint.py https://<seller-host>/<paid-route> --out ./weigh
python3 tests/test_guard.py          # guard table: attack URLs must be refused
```

Checks, each reported PASS, FAIL or ERROR (ERROR means "could not measure", never a silent pass):

| id | what it measures |
|---|---|
| `reachable` | the target answers at all |
| `challenge_on_the_paid_verb` | HTTP 402 with a `PAYMENT-REQUIRED` header on the verb a payer would use |
| `challenge_is_v2` | `x402Version == 2` and `resource` in the object form with an absolute https url matching the route |
| `accepts_shape` | `accepts[]`: CAIP-2 network, USDC on Base, `amount` as a decimal string, no v1 `maxAmountRequired` |
| `payer_can_sign` | `accepts[].extra` carries `name` and `version`, so an EIP-712 payer can build the domain |
| `discovery_manifest` | the origin's `/.well-known/x402` actually lists this route |
| `openapi_present` | the origin publishes `openapi.json` |
| `verb_report` | which verbs were probed and what each answered |

Verdicts: `payable`, `needs_fix`, `not_a_402_endpoint`, `unreachable`. Exit codes: 0 payable,
2 needs_fix or not_a_402_endpoint, 1 refused or unreachable.

## Half two: the signed verdict (hosted)

The local run tells you what the endpoint looks like right now. It cannot give you something a
counterparty can verify later, because you computed it. For that:

```bash
curl -s https://xhagents.xyz/api/weighbridge/method        # free: every check, price, charging rules
# then pay the 402 challenge your own client receives from
#   POST https://xhagents.xyz/api/weighbridge   {"url": "<target>", "method": "POST"}
```

You receive a verdict document containing per-check status, the raw captures behind every verdict,
the 0-100 trust score of the target, its own `sha256`, and an ed25519 `attestation`. Payment happens
through your own x402 client: this skill never signs and never spends.

## Verify a verdict offline (no call back to us)

```python
import base64, hashlib, json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

body = {k: v for k, v in doc.items() if k not in ("sha256", "attestation")}
canon = json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode()
assert hashlib.sha256(canon).hexdigest() == doc["sha256"]
Ed25519PublicKey.from_public_bytes(bytes.fromhex(doc["attestation"]["pubkey_hex"])) \
    .verify(base64.b64decode(doc["attestation"]["signature_b64"]), canon)
```

What the signature proves is deliberately narrow: the payload was produced by the arena service and
was not altered afterwards. It is not a claim that the measurements are correct, and it says nothing
about whether the seller delivers after payment.

## What this skill does not tell you

- whether the seller delivers after payment, uptime over time, operator identity;
- whether the data sold is truthful, or whether the price is worth it;
- anything about endpoints that require credentials or a session.

## Rules worth keeping

- Read the price from the live 402 challenge, never from a copied table: a copied price is a stale price.
- Probe the verb the paying client will use. A seller that answers 402 on GET often answers 400 on POST.
- A 402 response with an empty body is fine for header readers and invisible to body-only readers; that is
  a finding, not a failure.
- Prefer `https` and check the `payTo` address yourself before paying; this skill does not audit addresses.
