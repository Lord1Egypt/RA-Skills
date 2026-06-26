# Migration checklist for stale scheduled jobs

## Goal

Convert a brittle scheduled job into a design where changes are effective on the next run.

## Checklist

### 1. Inspect the current job

Check:
- model field
- session mode
- prompt source
- policy source
- delivery route
- verification rules

### 2. Identify drift sources

Common causes:
- old pinned model
- isolated stale session behavior
- prompt rules only stored in chat history
- delivery target copied from misleading session metadata
- exact verification preventing intended inheritance
- cron registration embedding old prompt, model, or delivery values

### 3. Move behavior into files

Create or update:
- manifest
- prompt file
- policy file
- local registry or scheduler-id mapping if your tooling reconciles live jobs

### 4. Fix model policy

Choose one:
- inherit-default
- pin
- policy-file

Default: inherit-default.

### 5. Replace fat cron payloads with thin triggers

Make the cron payload a small stable instruction that tells the agent to load local files.

### 6. Make delivery explicit

Write the exact provider-valid outbound target in the manifest.

### 7. Relax harmful verification

Keep checks that validate assembly.
Remove checks that freeze old desired behavior.

### 8. Test one live run for content freshness

Confirm:
- current prompt is used
- current policy is used
- current model policy behaves as intended

### 9. Test final delivery separately

Confirm:
- the final outbound route works
- attachments work if relevant
- cron announce is not silently masking a delivery bug

### 10. Record discovered quirks

Document provider-specific routing or runtime behavior for future reuse.

### 11. Record ownership boundaries

Write down whether the design is:
- architecture-only guidance
- a manifest convention
- or a complete installable execution path

Do not imply a one-command rollout if local execution tooling is still required.
