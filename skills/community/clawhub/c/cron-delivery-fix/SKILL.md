---
name: cron-delivery-fix
description: "Diagnose and fix OpenClaw cron job delivery failures. Script-based approach to prevent manual config errors. Fixes silent delivery failures, missing delivery params, and invalid session/payload combinations. Triggers: cron not delivering, scheduled task not sending, message not received."
---

# Cron Delivery Fix

Diagnose and fix OpenClaw cron job message delivery failures. Uses scripted operations to prevent manual configuration errors.

## Trigger Conditions

- User reports "didn't receive scheduled task message"
- Cron status shows `delivered` but user didn't receive it
- Cron status shows `not-delivered`
- Need to batch-check/fix all cron delivery configs

## Core Lessons (Historical Incident Log)

This issue recurred on multiple dates. Each manual fix introduced new problems:

1. **Session context**: Isolated session cron jobs lack contextToken, causing silent message failures
2. **Missing params**: Some tasks were missing `to`/`channel`/`accountId`, resulting in incomplete delivery
3. **Config wipe**: Manual `--no-deliver` accidentally cleared delivery configs; wrong `--session` caused invalid combinations

**Root cause**: Manually running `openclaw cron edit` one by one easily misses parameters or creates illegal configs.

**Solution**: Use scripts for unified management. Never manually edit cron session/delivery fields.

## Delivery Config Specification

### Valid Config Combinations

| sessionTarget | payload.kind | delivery.mode | Description |
|---|---|---|---|
| isolated | agentTurn | announce | AI executes + cron auto-delivers summary (requires complete to/channel/accountId) |
| isolated | agentTurn | none | AI self-delivers via message tool (must include send params in prompt) |
| main | systemEvent | none | Triggers in main session (no independent delivery) |

### Invalid Configurations

| Combination | Error Reason |
|---|---|
| main + agentTurn | Gateway rejects: `main cron jobs require payload.kind="systemEvent"` |
| announce + missing to | No delivery target, message cannot be sent |
| announce + missing accountId | Multi-account setups deliver to wrong account |
| none + agent in isolated session | AI's message tool lacks contextToken in isolated session |

### Standard Template for Delivery Tasks

All cron jobs that need to send messages to users must have:

```
sessionTarget: isolated
payload.kind: agentTurn
delivery.mode: announce
delivery.channel: <your-channel-id>
delivery.to: <your-user-id>
delivery.accountId: <your-account-id>
```

### Standard Template for Silent Tasks

Tasks that don't need to send messages:

```
sessionTarget: isolated
payload.kind: agentTurn
delivery.mode: none
```

## Operation Flow

### Step 1: Diagnose

```bash
bash skills/cron-delivery-fix/scripts/diagnose.sh
```

Outputs delivery status of all cron jobs, flagging problematic ones.

### Step 2: Fix

```bash
# Fix a single job
bash skills/cron-delivery-fix/scripts/fix-single.sh <job-id> [--announce|--silent]

# Fix all delivery-type jobs
bash skills/cron-delivery-fix/scripts/fix-all.sh

# Restore a broken job (with valid config)
bash skills/cron-delivery-fix/scripts/restore.sh <job-id>
```

### Step 3: Verify

```bash
# Run diagnosis again to confirm no issues
bash skills/cron-delivery-fix/scripts/diagnose.sh

# Manual trigger test
openclaw cron run <job-id>
```

## Prohibited Operations

1. **Never** manually use `openclaw cron edit --session main` on agentTurn-type tasks
2. **Never** use `--no-deliver` to clear delivery config then re-add params one by one (easy to miss params)
3. **Never** modify cron config without validating the combination is legal
4. **Never** fix cron without running `diagnose.sh` to verify afterwards
