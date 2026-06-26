# Reliability review for scheduled job architecture

Use this before publishing or rolling out a scheduling pattern.

## A design is reliable only if all are true

- Prompt changes take effect on the next run.
- Policy changes take effect on the next run.
- Delivery changes take effect on the next run.
- Default model changes take effect on the next run when inheritance is intended.
- Pinned model behavior is explicit and documented when inheritance is not intended.
- Dynamic jobs do not depend on fat embedded cron payloads unless re-registration is explicitly part of the process.
- No persistent session is required for correctness of content generation.
- Provider-specific outbound routing is documented where needed.
- Verification checks assembly correctness without blocking intended updates.
- Final delivery has been tested independently from scheduler announce behavior.

## Review questions

### Runtime freshness

- Does every run read current files?
- Can a stale session override current files?
- Is generation happening in a clean runtime?

### Model freshness

- Is the model intentionally inherited or intentionally pinned?
- Could an old manifest silently keep using an outdated model?
- Does verification accidentally lock an old model in place?

### Prompt and policy freshness

- Are formatting and content rules stored in files?
- Would a file edit affect the next run without extra manual steps?

### Delivery correctness

- Is outbound delivery defined explicitly?
- Is the target format valid for the provider?
- Have attachments been tested if relevant?
- Is normal outbound delivery working even if cron announce delivery is not?

### Operational resilience

- Can the job fail safely?
- Can it be re-run cleanly?
- Can another agent reuse the pattern without hidden assumptions?

## Red flags

- exact old model pinned without a clear reason
- persistent automation session used as content source of truth
- prompt requirements only captured in conversation history
- delivery route inferred from stale session metadata
- verification that prevents intended updates from taking effect
- cron registration storing the full job content for a supposedly dynamic automation
- relying on cron announce delivery without separately testing the real outbound path
