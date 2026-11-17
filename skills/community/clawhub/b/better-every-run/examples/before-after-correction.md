# BER Before/After Correction Artifact

This is the concrete story for Better Every Run. It shows one repeated bad behavior becoming a local lesson, then a later run improving.

## Before

Bad outcome:

```text
Agent: Done. I cleaned it up and everything looks good.
```

Problem: the human still has to ask what command ran, whether it passed, and what remains risky.

## Correction

Human command:

```text
/ber fix agent says done without proof -> agent gives exact verification output before claiming done
```

Helper command used by the agent:

```bash
node scripts/ber.js fix "agent says done without proof -> agent gives exact verification output before claiming done" --scope eval --tags proof,regression
```

Expected result:

```text
Durable file changed: none
Local store: .better-every-run/
Promotion: use card + promote for durable memory or skill changes; use eval-fixture for regression coverage.
```

## Local Evidence

BER writes a local lesson under `.better-every-run/`. That state is private and excluded from publishing. The lesson can become:

- a memory rule, after a reviewed lesson card and clean scanner verdict
- a skill behavior, after a reviewed lesson card and clean scanner verdict
- an eval fixture, through `eval-fixture` under `tests/` or `evals/`
- nothing durable, if it was a one-off correction

## After

Improved later response:

```text
Done. Verification output:
- make test: passed
- git diff --check: clean

Remaining risk: I did not run browser coverage because this repo has no browser harness.
Next action: tag the release after CI passes.
```

The important conversion point: BER is not a memory auto-writer. It is a small correction intake that leaves an auditable path from human correction to future behavior.

## Try It

```bash
make test
node scripts/ber.js fix "agent says done without proof -> agent gives exact verification output before claiming done" --scope eval --tags proof,regression
node scripts/ber.js report --today
```
