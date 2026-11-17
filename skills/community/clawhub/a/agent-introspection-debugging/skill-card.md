## Description:

Debug agent behavior through a four-stage self-diagnosis loop: capture failures, diagnose root causes, recover in a contained way, and report results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent is stuck in repeated failures, tool limits, context pressure, or uncertain environment state and needs a structured debugging workflow before retrying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may encourage inspection of local task state or writing diagnostic learning notes.

Mitigation: Review any diagnostic notes before retaining them and avoid recording secrets, private user data, or unrelated workspace details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/agent-introspection-debugging)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklists and short diagnostic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include failure-capture, recovery-action, and self-debug report sections.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
