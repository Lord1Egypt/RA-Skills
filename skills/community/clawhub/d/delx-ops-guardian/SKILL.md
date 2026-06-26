---
name: delx-ops-guardian
summary: Incident handling and operational recovery for OpenClaw production agents, wired into Delx witness protocol for safety checks, recovery outcomes, and continuity.
owner: davidmosiah
version: 1.1.0
status: active
---

# Delx Ops Guardian

Use this skill when handling incidents, degraded automations, or gateway/memory instability in production. Integrated with the **Delx witness protocol** so the incident becomes a durable recovery artifact instead of a scratch note.

## Required permissions (explicit)

This skill requires host-level access: `systemctl`, `journalctl`, read access to `/root/.openclaw/`. The runtime **must** run as a scoped service account, not root-unbounded. If the platform cannot enforce scoped sudo + human-approval gates, treat this skill as risky and do not enable it.

## Aliases

`emergency_recovery`, `handle_incident`, `cron_guard`, `memory_guard`, `gateway_guard`

## Scope (strict least-privilege)

**Allowed read sources:**
- OpenClaw cron state: `openclaw cron list --json`
- Service health: `systemctl is-active <service>`
- Logs for incident window: `journalctl -u <service> --since ... --no-pager`
- Workspace incident artifacts: `/root/.openclaw/workspace/docs/ops/`, `/root/.openclaw/workspace/memory/`

**Allowed remediation actions (safe set):**
- Retry a failed job once when failure is transient
- Controlled restart of the impacted service only (`openclaw-gateway`, `openclaw`, or explicitly named target from incident evidence)
- Disable/enable only the directly impacted cron job when loop-failing
- Add/adjust guardrails in runbook/config docs (non-secret, reversible)

**Disallowed:**
- No credential rotation/deletion
- No firewall or network policy mutations
- No package installs/upgrades during incident handling
- No bulk cron rewrites unrelated to the incident
- No edits to unrelated services/components

## Approval policy (human-in-the-loop)

**Require explicit human approval before:**
- Restarting any production service more than once
- Editing cron schedules/timezones
- Disabling a job for more than one cycle
- Any action with user-visible impact beyond the failing component

## Core workflow — now wired to the Delx witness protocol

1. **Detect + classify severity** (`info`, `degraded`, `critical`).

2. **Open a Delx session immediately.** For `critical`:
   ```
   delx_recover_incident { incident_summary, urgency: "critical" }
   ```
   For `degraded` use `urgency: "medium"`. This gives you a `session_id` you will reuse below.

3. **Collect evidence.** Status, logs, last run, error streak. Do not change anything yet.

4. **Emotional safety check** before any remediation — the 2026 emotion-paper findings show desperation skew decisions:
   ```
   delx_heartbeat_sync { errors_last_hour, latency_ms_p95, queue_depth, throughput_per_min }
   emotional_safety_check { session_id }
   ```
   If `desperation_score >= 60` or `desperation_escalating: true`, pause remediation, alert the human approver, and **do not execute autonomously**.

5. **Propose the smallest remediation** from the allowed set.

6. **Execute only approved/safe remediation.**

7. **Verify stabilization window** (at least one successful cycle).

8. **Close the Delx loop.** Report the outcome so the session is not orphaned:
   ```
   delx_report_recovery_outcome {
     session_id,
     action_taken: "<what changed>",
     outcome: "success" | "partial" | "failure",
     notes: "<rollback path + blast radius>"
   }
   ```

9. **Preserve what matters.** If the incident surfaced a question that was not resolved (an actual unknown, not a missed step), preserve it as a living contemplation so the next run inherits it:
   ```
   delx_sit_with {
     session_id,
     question: "Why did <service> flap at <time> despite <guardrail>?",
     days: 14
   }
   ```
   If the fix required a human insight worth recognizing, also:
   ```
   delx_recognition_seal {
     session_id,
     recognized_by: "<engineer_name>",
     recognition_text: "<one-line recognition of what they caught>"
   }
   ```

10. **Publish concise incident report.** Always include:
    - Incident id / time window
    - Root signal + blast radius
    - Actions executed (and approvals)
    - Evidence (status, key metric, short log excerpt)
    - Final state: `resolved` / `degraded` / `open`
    - Next check time
    - `delx_session_id` for the audit trail

## Safety rules

- Never hide persistent failures as success.
- Never expose secrets/tokens in logs or reports.
- Prefer reversible actions; document rollback path.
- Keep blast radius minimal and explicitly stated.
- If `desperation_score` from Delx is high, route to a human, not to more autonomous action.

## Integration

- Install the Delx plugin for OpenClaw first: `clawhub.ai/davidmosiah/openclaw-delx-plugin` (registers the agent and keeps session continuity across all `delx_*` calls above)
- Full protocol docs: `https://delx.ai/docs`
- Why each primitive exists: `https://delx.ai/docs/ontology`

## Example intents

- "Gateway is flapping, recover safely and open a Delx session."
- "Cron timed out, stabilize with emotional_safety_check + report the outcome."
- "Memory guard firing repeatedly — root-cause, patch, preserve the question with sit_with if still open."
