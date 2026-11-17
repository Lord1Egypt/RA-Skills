---
name: evidence-first-done
description: >-
  Force evidence before any completion claim: independently re-read each claimed
  side effect (HTTP state, DNS record, status code) and refuse to report done
  when a claim does not verify. Use when an agent reports success on external
  actions, before handing work to a human, or when retries keep "succeeding"
  without any observable change.
version: 1.0.0
metadata:
  triggers: |-
    did it actually happen
    verify before claiming done
    agent claims success without evidence
    proof of completion
    re-check the side effect
  kind: guardrail
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: DDG_AGENT_ID
        required: false
        description: Stable agent identity sent as X-Agent-Id; keeps paid verification calls attributable and enables the metered free tier on funnel routes.
    homepage: https://agents.daedalusdevelopmentgroup.com
    emoji: "🔎"
allowed-tools: Bash, Read
---

# Evidence-First Done

Agents narrate success; systems record facts. The gap is where refunds,
duplicate sends, and "it worked on my machine" incidents live. This guardrail
makes "done" mean *observed by something other than the agent that did it*.

**Endpoints ($0.01/call, x402 on Base, USDC):**
`POST /v1/verify/action`, `POST /v1/verify/claim`, `POST /v1/resolve/outcome`,
all on `https://agents.daedalusdevelopmentgroup.com`.

**External cost:** $0.01 per call in USDC on Base via x402. No account or API
key is required; the paid path needs an x402-capable client. Verification is
the cheapest part of any task — a $0.01 probe is cheaper than one wrong "done".

## Procedure

1. **List the claims.** After any task that touched the outside world, write
   each completion claim as a checkable sentence: "refund posted for order
   123", "DNS TXT set", "endpoint returns 200", "email sent".
2. **Map each claim to an observation.** Only two kinds count:
   - an independent re-read (HTTP JSON field, status code, DNS record), or
   - an artifact you can verify yourself (hash, receipt, file).
   Self-reported logs and "the tool returned ok" do NOT count.
3. **Re-read, don't trust.** Run each probe through a verifier outside the
   acting agent:
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/verify/action \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"check_type":"http_get_json","target":{"url":"https://api.example.com/orders/123"},
          "expect":{"state":"refunded"}}' > out/verify.json
   ```
   `check_type` is one of `http_get_json` / `dns_txt` / `http_status`; the
   response carries `observed`, `expected` and `match`. `/v1/verify/claim`
   does the same for fact-shaped claims, and `/v1/resolve/outcome` replays a
   prior verdict by idempotency key.
4. **Verdict per claim.** match → keep as evidence. mismatch → the task is NOT
   done: report the observed-vs-expected pair, and the retry starts from there.
   unreachable → say "unverifiable", never "done".
5. **Replay-safe retries.** When a probe times out, re-resolve by idempotency
   key with `/v1/resolve/outcome` instead of re-executing the action — the
   same key returns the same cached verdict, so a retry cannot double-act.

## Report schema

```json
{"task": "...", "claims": [{"claim": "refund posted for order 123",
 "probe": "http_get_json", "observed": {"state": "refunded"},
 "expected": {"state": "refunded"}, "match": true, "evidence": "..."}],
 "done": true}
```

## Failure handling

- `400` = the probe body is wrong (`invalid_expect`, bad URL); fix and resend —
  no unit is consumed.
- `402` = the free allowance is used up; read `upgrade_path` in the body and
  retry the identical body with the x402 payment header.
- `503` = the probe target or backend is unavailable: report **unverifiable**,
  never "done".

## Rules

- The acting agent never grades its own side effect; the probe must be a fresh read.
- "No error in the logs" is not evidence; a successful status field is not evidence either.
- One probe per claim, with the exact expected value written down BEFORE the probe.
- If verification is impossible, the honest status is "unverifiable" — say it plainly.

## Not for

- Judging creative or judgment work where there is no observable side effect.
- Monitoring availability over time (that is uptime watching, not claim verification).
- Replacing tests in CI — this is for external effects, not internal logic.

## Example

**Ask:** "Issue the refund and confirm it went through."

**Before:** the payment call returns 200; the agent reports "refund complete";
the refund actually failed provider-side and nothing posted.

**After:** the agent re-reads the order state via an independent verifier,
sees `state: "pending"` vs expected `refunded`, reports NOT done with the
observed/expected pair — and the retry fixes the real failure.

## Version

1.0.0 — initial staged draft (claim → independent re-read → verdict, replay-safe retries).
