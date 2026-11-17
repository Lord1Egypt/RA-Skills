## Description:

Review OpenClaw agent workspace files (AGENTS, SOUL, USER, MEMORY, IDENTITY, daily notes): size limits, load status, contradictions, misplaced rules, stale facts. Proposes edits; applies only owner-approved ones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holgergruenhagen](https://clawhub.ai/user/holgergruenhagen)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw workspace owners and developers use this skill to review agent startup files for size, load status, consistency, stale information, and misplaced content. It produces proposed edits and applies only changes the owner approves exactly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review findings may be incomplete when context data or referenced paths are unavailable.

Mitigation: Provide `/context list` output and verify referenced paths before relying on the review.

Risk: A proposed workspace edit could introduce incorrect or misleading guidance.

Mitigation: Review and scan each exact proposed change; apply it only after owner approval.

## Reference(s):

- [OpenClaw issue 153426: untrusted workspace files](https://github.com/openclaw/openclaw/issues/153426)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report with findings and proposed edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review is read-only; edits require exact owner approval. Changes to other agents' files are provided as an apply sheet.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
