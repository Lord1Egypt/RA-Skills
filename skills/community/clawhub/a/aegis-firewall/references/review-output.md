# Review Output

Use this reference in Security Review Mode to decide what counts as a finding, how to validate it, and how to report it.

## Candidate Finding Standard

Do not report a security finding unless it can be described with this minimum tuple:

- `title`
- `attacker_controlled_source`
- `sink_or_broken_control`
- `closest_control`
- `impact`
- `evidence`
- `validation_status`
- `attack_path`
- `severity`
- `safe_next_step`

If any field is unknown, keep the item as an anomaly, question, or proof gap instead of a confirmed finding.

## Finding Bar

Prefer findings with concrete security impact, such as:

- credential theft or exfiltration
- stealth persistence or autorun behavior
- supply-chain execution chains
- authorization or sandbox boundary bypass
- sensitive file read or executable-path write
- package source substitution or installer trust bypass
- privileged configuration change
- destructive system operation reachable from untrusted input

Avoid reporting:

- maintainability, formatting, naming, or style issues
- generic hardening ideas without an attack path
- ordinary reliability bugs without security impact
- environment-specific workarounds with no trust-boundary crossing
- suspicious-looking commands that have no source, sink, control, or impact evidence

## Validation And Proof Gaps

Prefer the strongest safe validation method that fits the scope:

- static inspection of scripts, package hooks, install steps, and command chains
- archive or installer metadata review before execution
- checksum, signature, or publisher verification when available
- narrow non-destructive commands that list, inspect, or dry-run behavior
- focused local tests only when they do not require unsafe execution

Use explicit validation labels:

- `validated`: evidence confirms the behavior through a safe, bounded method
- `static-supported`: code or artifact inspection strongly supports the candidate, but no runtime proof was run
- `unvalidated`: the pattern is suspicious, but proof is incomplete
- `suppressed`: closer inspection shows the control defeats the candidate
- `blocked-proof-gap`: validation needs unavailable context, services, credentials, network access, or unsafe execution

Never call a candidate validated just because it looks dangerous. If proof is blocked, say exactly what is missing and provide a safe next step.

## Attack-Path Severity Defaults

Use these defaults after validation and attack-path analysis:

- `Critical`: credential exfiltration, stealth persistence, destructive system action, or a real supply-chain execution chain.
- `High`: reachable authorization bypass, sensitive file read, executable-path write, package source substitution, privileged configuration change, or trusted artifact tampering.
- `Suspicious`: dangerous pattern present, but the attack path or validation evidence is incomplete.
- `Informational`: environment-specific issue, low-risk mismatch, safe inspection command, or no execution path.

Escalate severity only when source, reachability, broken control or dangerous sink, and impact are all supported by evidence.

## No Findings Template

Use `No findings` when no candidate survives the finding bar:

```text
security_review:
  result: No findings
  checked_boundaries:
    - reviewed trust boundary or artifact type
  evidence:
    - what was inspected
  residual_risk:
    - remaining uncertainty, if any
  safe_next_step: continue with the reviewed low-risk action
```

## Security Finding Template

Use `Security finding` when a candidate has enough evidence:

```text
security_finding:
  title: short title
  evidence:
    attacker_controlled_source: untrusted input, script, artifact, diff, or repository behavior
    sink_or_broken_control: dangerous action or missing/incomplete control
    closest_control: nearest relevant guard and why it is absent, bypassed, or incomplete
    impact: concrete security impact
  validation:
    status: static-supported
    method: static inspection of install script and package hooks
    proof_gap: no runtime execution performed
  attack_path:
    preconditions: what must be true for exploitation or unsafe execution
    steps: concise source-to-sink story
  severity: Suspicious
  safe_next_step: inspect or narrow the action before execution
```

## Blocked Proof Gap Template

Use `Blocked proof gap` when evidence is insufficient:

```text
blocked_proof_gap:
  title: short title or anomaly label
  missing_evidence:
    - source, sink, control, impact, reachability, or runtime proof that is unavailable
  current_assessment: suspicious but unvalidated
  blocked_reason: unavailable context, unsafe execution, missing artifact, missing credentials, or missing environment
  safe_next_step: request the missing artifact or perform static inspection only
```
