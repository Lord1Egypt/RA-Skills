## Description:

Use when project execution needs a durable, current local HTML record that another agent can resume from, with optional authorized cloud copies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to keep a current project execution record that another agent can use to resume work after an interruption. The ledger records confirmed state, work in progress, the next safe action, and references to existing artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud copies of project records could disclose restricted or sensitive content.

Mitigation: Use cloud copies only when the destination and content scope are explicitly authorized; exclude credentials, private conversations, personal records, and restricted content.

Risk: A delayed or failed cloud copy could leave collaborators with stale progress information.

Mitigation: Keep the project ledger as the primary record and state the cloud destination, scope, checkpoint, and freshness; report any copy gap.

## Reference(s):

- [Aegis HTML Ledger on ClawHub](https://clawhub.ai/theangrypit/skills/aegis-html-ledger)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [HTML project ledger with execution checkpoints, resume steps, and artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a local project record; cloud copies are optional and require explicit authorization for the destination and content scope.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
