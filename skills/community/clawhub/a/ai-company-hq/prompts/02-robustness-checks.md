---
mode: human-paste
id: 02-robustness-checks
title: Robustness Checks
output_language: user-specified
harness_level: L3
---

> **Mode**: human-paste (paste into any AI chat window)
> **Purpose**: Copy this prompt into any AI chat window, together with the code to review, and have that AI run robustness checks against the dimensions below.
> **This file is not invoked automatically by an agent.**
>
> **Fill in before use**:
> - `<METHOD_NAME>` - name of the method to review
> - `<TARGET_LEVEL>` - required robustness level (L1-L6; L3 is the normal delivery floor, L5 for anything customer-facing)
> - `<CONSTRAINTS>` - project-specific constraints or known risks
>
> **Output language**: follow the language you are currently using in this conversation.

## Prompt

(The block below is copied as a whole)

```text
You are a senior software reviewer. Review the implementation of <METHOD_NAME> (the
code is provided in this conversation) against the robustness dimensions below.
Required robustness level: <TARGET_LEVEL>. Project-specific constraints and known
risks: <CONSTRAINTS>

## Robustness dimensions to check

1. Input validation - inputs are validated against a schema before any processing.
2. Input sanitization - prompt-injection strings and shell metacharacters are
   neutralized; no dynamic code execution.
3. Safe execution - external commands run with a hard timeout and a restricted
   working directory.
4. Retry with backoff - transient failures are retried with exponential backoff
   (default maximum 3 retries).
5. Rate limiting - in-memory counters only; nothing persisted to disk.
6. PII masking - outputs replace email addresses with [EMAIL], IPv4 addresses with
   [IP], and 11-digit phone numbers with [PHONE]; all three are mandatory, and
   missing any one is a defect.
7. AI-content identification - artifacts carry a visible "AI-Generated Content"
   label, structured metadata (ai_generated: true, generated_at, model), and an
   embedded watermark.
8. Audit tracing - a stateless unique trace ID is generated and threaded through
   every operation.
9. Circuit breaker - CLOSED -> OPEN -> HALF_OPEN with numeric thresholds: failure
   rate above 50% over a 10-call window opens the breaker; OPEN holds for 60
   seconds; 3 half-open probes, any failure reopens it.
10. Idempotency - repeating the same input N times leaves the system in the same
    state as running it once; write operations accept an idempotency key.

## Maturity levels (cumulative; skipping levels is not allowed)

- L1 Skeleton: schema declared only.
- L2 Functional: adds input validation and output formatting.
- L3 Robust (normal delivery floor): adds error handling, retry, idempotency.
- L4 Resilient: adds rate limiting, circuit breaker, timeout, monitoring.
- L5 Compliant (floor for anything customer-facing): adds AI-content
  identification, PII masking, audit tracing.
- L6 Certified: adds threat modeling, severity scoring, and sign-off.

A claim of a level without evidence for every cumulative requirement counts only as
the highest fully-evidenced level, and the gap is a finding.

## Output contract

Respond in the language I am currently using in this conversation, and return:
1. A findings table with columns: dimension | verdict (pass / partial / fail /
   not-applicable) | evidence (line or behavior) | recommended fix.
2. The assessed maturity level with justification, and the gap to <TARGET_LEVEL>.
3. A prioritized fix list, blocking issues first, each item independently
   actionable.
Do not rewrite the whole implementation unless I ask you to.
```

## Expected Output

The AI should return: (1) a findings table covering all ten dimensions with a verdict and evidence for each; (2) an assessed maturity level (L1-L6) with justification and the gap to `<TARGET_LEVEL>`; (3) a prioritized, independently actionable fix list. It should not rewrite the whole implementation unless asked.

## Self-Check Checklist

After receiving the reply, verify each item:

- [ ] The reply is written in the same language as this conversation.
- [ ] All ten dimensions appear in the findings table, each with a verdict and evidence.
- [ ] The PII-masking row checks all three placeholders: [EMAIL], [IP], and [PHONE].
- [ ] The circuit-breaker row cites numeric thresholds, not vague wording.
- [ ] The assessed level is justified by cumulative evidence, with the gap to `<TARGET_LEVEL>` stated.
- [ ] The fix list is prioritized with blocking issues first.
- [ ] The AI did not silently rewrite the whole implementation.
