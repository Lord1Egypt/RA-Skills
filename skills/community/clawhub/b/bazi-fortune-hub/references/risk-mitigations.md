# Risk Mitigations — Reference

> **For protocol-level summary**, see [`../SKILL.md`](../SKILL.md) §1 (Synchronous semantics) and §6 (Rate Limits).
>
> This document describes the **client-side risks** an agent should be aware of when integrating with fortune-hub.

## R1 — Description drift between hub and upstream

**Risk**: The upstream BaZi service may change a t1–t4 description; the hub proxies these descriptions live on every `tools/list` call. There is no server-side cache. If your agent caches `tools/list` responses across sessions, you may serve stale descriptions to the user.

**Mitigation**:
- Call m1 `get_skill_info` at the **start of every session** — never rely on session-start discovery alone.
- Do not cache `tools/list` responses across sessions.
- If a tool description in the live response differs from what you remember, trust the live one.

## R2 — Meta-tool flooding (m2 / m3)

**Risk**: An agent key hits m2 / m3 at high frequency (e.g. polling balance every 30s). m2/m3 are rate-limited at 60/min for agent keys.

**Mitigation**:
- Cache m2 result per conversation (the balance only decreases).
- Use m3 `get_usage_history` for audit; only call when the user asks or after a paid chain.
- For high-frequency monitoring, use a personal key (exempt from rate limits).

## R3 — `agent_metadata` size abuse

**Risk**: An agent passes a multi-megabyte JSON object as `agent_metadata` in f3 / f4.

**Mitigation**:
- Server enforces strict schema validation + size < 4 KB (4096 bytes UTF-8).
- Use the 3-field schema: `agent_name` (1–64), `agent_version` (1–32), `platform` (enum).
- See [`../usage/agent-metadata.md`](../usage/agent-metadata.md) for the recommended payload.

## R4 — Skipping m2 credit check before the paid chain

**Risk**: An agent starts the t1→t2→t3→t4 chain without first calling m2 `get_user_credits`. Mid-chain, t2 or t4 returns `INSUFFICIENT_CREDITS` (HTTP 402), the chain stops at step 2 or 4, the user has already been charged for t1 (if no free quota), and the agent has no `pattern_result` / `year_analysis_result` to return. The agent has to refund in chat and restart — a poor user experience and a partial credit burn.

**Mitigation**:
- Always call m2 `get_user_credits` **before** t1 (the documentation's recommended pattern: m1 → m2 → t1 → t2 → t3 → t4).
- If `balance < sum(fortune_pricing)`, **stop before t1** and prompt the user to top up at the hub's `/billing` page.
- Treat `INSUFFICIENT_CREDITS` mid-chain as a **stop signal**, not a retry signal — never silently re-charge by re-running t1 with a different `agent_metadata` payload.
- t1 itself may be free (it depends on the user's free quota); m2 is the only reliable way to know whether t1 will deduct 0 or 1 credit.

## R5 — t4 client-side timeout (the most important risk)

**Risk**: `bigluck_year_fortune_eval` contains 1 internal LLM step that takes ~30–90s (worst case ~90s). Some MCP clients default to ~60s tool timeout, which will cut off the call mid-execution.

**Three concrete failure modes** observed in production:

1. **Cursor / Cline IDE-side MCP client** defaults vary by version. Older builds cap at ~60s; newer builds expose a setting. **Configure to ≥120s.**
2. **HTTP intermediaries** (corporate proxies, CDN edge timeouts) may sever the connection before the LLM returns, even if the client timeout is generous. Symptom: HTTP 502/504 with partial body.
3. **SSE consumers** reading `Content-Type: text/event-stream` may interpret an idle connection (>60s with no event) as a hang and close. Hub streams the final JSON-RPC response as a single event; the connection will be idle during the LLM call.

**Mitigation**:
- Configure your client's tool-call timeout to **≥120s**.
- Hub has `maxDuration=300` server-side, so the server will hold the connection; the limit you feel is your client's read timeout.
- If a client genuinely cannot tolerate >60s, call t1, t2, t3, and **stop before t4** — the user gets the structured data and can request a re-try on a different client.

## What the agent should do on partial failure

If a fortune step fails with a 5xx (`UPSTREAM_ERROR` / `REST_ERROR` / `UPSTREAM_TIMEOUT`), **re-run that step from scratch**, re-using the outputs of the earlier steps you already hold:

- Re-run t4 with the same `year_analysis_result` + `pattern_result` (do not restart from t1).
- Re-run t3 with the same `base_context` + `pattern_result`.
- Re-run t2 if the upstream LLM is genuinely unavailable (you will be charged again).
- There is **no `get_job_result` async tool** — calls return synchronously (OneShot).

## See also

- [`../SKILL.md`](../SKILL.md) §1 (Synchronous semantics)
- [`../SKILL.md`](../SKILL.md) §3 (12 Tools) — t4 row client timeout warning
- [`../usage/chain-patterns.md`](../usage/chain-patterns.md) — failure inside the chain
- [`../usage/error-handling.md`](../usage/error-handling.md) — retry rules
