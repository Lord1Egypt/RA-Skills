# Security Model — Bobiverse Replicate Skill

## Objective

Maintain the Bobiverse replication concept while ensuring replication is an explicit, purposeful, operator-approved event.

## Security Principles

1. **Explicit trigger only**
   - Replication is never inferred from context.
   - Requires direct operator invocation in-session.

2. **Purpose required**
   - Every replication request must include a concrete purpose and task boundary.

3. **Dry-run first**
   - Planning output is shown before any write/registration action.
   - Dry-run creates a pending approval record under
     `~/.openclaw/replication-pending/`.
   - Pending approvals expire after 15 minutes.

4. **Confirmation token required for execution**
   - Execution requires exact token: `REPLICATE <clone-id> <nonce>`.
   - The token must match the dry-run-issued pending approval record.

5. **Path boundary enforcement**
   - Filesystem operations are constrained to `~/.openclaw`.
   - Parent paths must be direct-child validated workspace directories
     (`workspace` or `workspace-<agent-id>`), never `~/.openclaw` itself or
     an arbitrary descendant under it.
   - The runner rejects symlinks anywhere in the source tree.

6. **No shell interpolation**
   - External commands are invoked with argument arrays (`shell=False`).

7. **Rate/resource guardrails**
   - Warn/block when workspace count is high unless explicitly acknowledged.
   - Enforce a default 24-hour cooldown between execute-mode replications unless
     operator provides explicit override reason.

8. **Auditability**
   - Replication actions are recorded in `~/.openclaw/replication-audit.log`.
   - Audit events include `dry-run-created`, `execute-started`,
     `execute-failed`, and `execute-succeeded`.
   - Cooldown override reason is captured in the audit entry when used.
   - Failed execute attempts are logged and still count toward the cooldown.

9. **Transactional execution**
   - Clone copies are staged in `~/.openclaw/.replication-staging-<agent-id>`.
   - Failed executions roll back the staged or final clone workspace.

## Implementation Requirement

All clone workspace duplication and `openclaw agents add` registration must be done through:

- `skills/replicate/scripts/replicate_safe.py`

Ad-hoc shell copy/register command assembly is not permitted for replication flow.
