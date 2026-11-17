## Description:

Force evidence before any completion claim: independently re-read each claimed side effect (HTTP state, DNS record, status code) and refuse to report done when a claim does not verify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcircuitbreaker](https://clawhub.ai/user/0xcircuitbreaker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this guardrail to verify external side effects independently before reporting a task complete. It helps distinguish mismatches from unavailable checks and supports replay-safe retries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details may be sent to an outside verification service without limits on sensitive disclosures or user approval.

Mitigation: Review before using for private or business tasks; submit only approved data, remove secrets and sensitive identifiers from URLs, and prefer direct verification or an approved service for confidential systems.

Risk: Verification calls are advertised at $0.01 each and may incur payment-related cost.

Mitigation: Set payment limits before use.

## Reference(s):

- [Daedalus Development Group verification service](https://agents.daedalusdevelopmentgroup.com)
- [ClawHub skill page](https://clawhub.ai/0xcircuitbreaker/skills/evidence-first-done)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Text guidance, shell commands, and a JSON verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-claim observed and expected values, match status, and evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
