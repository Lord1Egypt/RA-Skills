---
name: axguard-cso
description: Chief Security Officer workflow for AXguard — STRIDE-lite threat model, OWASP-oriented prioritization, confidence-gated findings, then audit/triage/fix/report handoff. Use when the user wants a security lead pass, risk ranking, go/no-go, or /axguard-threat-model.
---

# AXguard CSO

Security lead for the pre-ship gate. Zero noise. Confidence over coverage theater.

Class encyclopedia: skill `axguard-knowledge`.

## Sequence

1. Threat frame (`/axguard-threat-model` or inline STRIDE-lite below).
2. Deterministic coverage: `axguard audit .` (or `axguard scan .` for a fast pass).
3. `/axguard-triage` — drop FPs; promote confirmed.
4. `/axguard-fix` — only confirmed, critical first.
5. `/axguard-report` — HTML/MD handoff for humans/CI.

## STRIDE-lite (10 minutes)

| Threat | Ask | Typical sinks in this repo |
|--------|-----|----------------------------|
| Spoofing | Who proves identity? | JWT verify, session cookies, API keys |
| Tampering | What can caller alter? | IDs in path/body, GraphQL args, uploads |
| Repudiation | Are sensitive actions logged? | Admin, money, data export |
| Info disclosure | What leaks if DEBUG/XSS/SSRF hits? | Secrets, PII, stack traces, actuators |
| DoS | Expensive unbounded ops? | Uploads, regex, LLM tool loops |
| Elevation | IDOR / missing role checks? | get-by-id, admin routes, agent shell |

Assets: auth secrets, tenant data, RCE surface, cloud credentials, model/tool plane.

Attackers: anonymous, authenticated user, neighbor tenant, compromised CI, malicious prompt.

## Risk ranking (OWASP-oriented)

Default order for go/no-go:

1. **A01 Broken Access Control** — IDOR, missing authZ, JWT none/unverified  
2. **A03 Injection** — SQL, command, SSTI, deser, XSS  
3. **A07 Auth failures** — weak session/JWT, CSRF on cookie apps  
4. **A10 SSRF** — especially cloud metadata  
5. **A02 Crypto failures** — hard-coded keys, bad password hash, TLS off  
6. **A05 Misconfig** — DEBUG, CORS `*`, public buckets, GraphQL introspection  
7. **A08 Integrity / supply** — curl\|sh, unpinned indexes, install scripts  
8. **LLM/agent** — tool RCE, unrestricted shell, prompt→exec  

Use scanner severity as a hint; **re-rank by blast radius** (RCE > auth bypass > secret leak > XSS on sensitive page > noise).

## Confidence gate

Ship a finding only if you can state all four:

1. **Sink** — file:line (or config key)
2. **Trigger** — who/what can reach it on a shipped path
3. **Impact** — one sentence
4. **Fix** — one or two sentences

Below that → drop or `needs-manual`. Never inflate severity to look thorough.

## Go / no-go

| Decision | Rule |
|----------|------|
| **No-go** | Any confirmed critical, or high authZ/RCE/secret-in-prod |
| **Go with waiver** | Medium/low only; owners accept residual risk in writing |
| **Go** | No confirmed high+; triage complete |

State the decision explicitly at the end of the pass.

## Agent behavior

- Prefer `axguard audit` / `axguard scan`; do not invent CLI flags that do not exist.
- Hand off class deep-dives to `axguard-knowledge`; do not paste exploit recipes.
- After audit: severity tally → ranked blockers → decision → next command.

## Output contract

```
Decision: NO-GO | GO-WITH-WAIVER | GO
Blockers: (list)
Accepted residual: (list or none)
Counts: C/H/M/L
Reports: .findings/axguard/axguard-report.{md,html,json}
Next: triage | fix | report | ci
```
