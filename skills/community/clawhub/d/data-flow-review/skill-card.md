## Description:

Reviews code by tracing how data moves across state, branches, persistence, payloads, and downstream consumers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modeyapu](https://clawhub.ai/user/modeyapu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for data-flow-oriented code review, patch checks, and audits where correctness depends on field provenance, persistence timing, branch behavior, and downstream consumers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require the agent to inspect sensitive application code paths during review.

Mitigation: Use it only in workspaces where the agent is authorized to read the relevant code and keep findings within approved review channels.

Risk: Review findings can be incomplete if the flow is not traced through branch outcomes, persistence boundaries, and downstream consumers.

Mitigation: Require findings to cite the triggering path, branch scenario, affected data, and downstream consequence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modeyapu/skills/data-flow-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings, flow summaries, and audit guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings-first output with concrete file and line references when available.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
