## Description:

Author durable Lethe memory through Charon as a proposer principal using owned refs, CAS changesets, semantic operations, and merge proposals for independent review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mentholmike](https://clawhub.ai/user/mentholmike)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to author durable Charon/Lethe memory changes as propose-only principals. It supports reading context, branching owned refs, committing validated changesets, and submitting merge proposals for independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory proposals can affect future agent work if they contain incorrect, stale, sensitive, or unnecessary information.

Mitigation: Review proposed memory before merge, re-verify changing facts against source systems, and avoid credentials, authorization values, private chain-of-thought, or unnecessary personal data.

Risk: A proposer could attempt to move protected refs, touch another principal's refs, or broaden its effective authority.

Mitigation: Use exact project grants, owned refs only, and independent review and merge through a separate reviewer principal.

Risk: Conflicts or retried writes could create unintended memory changes.

Mitigation: Use CAS with the current expected head, stable idempotency keys for identical retries, and reread the ref head before reconciling conflicts.

## Reference(s):

- [Charon Proposer on ClawHub](https://clawhub.ai/mentholmike/skills/charon-proposer)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown with memory operation summaries, Charon tool call guidance, changeset identifiers, ref heads, and proposal status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid credentials, authorization values, private chain-of-thought, and unnecessary personal data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
