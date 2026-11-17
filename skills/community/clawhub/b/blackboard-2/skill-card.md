## Description:

Typed multi-model workspace with kitchen-shift ownership, resource, hazard, protected-target, and next-action handovers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Blackboard to coordinate multi-model task handoffs by storing typed facts, inferences, decisions, actions, test results, hazards, protected targets, ownership, and next actions in local JSON board files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Board files persist coordination state and may contain task details, constraints, receipts, or handoff context.

Mitigation: Choose a board path inside the intended workspace and avoid storing secrets or unrelated sensitive data in board entries.

Risk: Timestamped backups may retain prior board contents after later edits.

Mitigation: Account for backup retention when handling sensitive tasks and prune or limit backups according to the deployment policy.

Risk: User approvals and user provenance cannot be authenticated by the JSON file alone.

Mitigation: Bind user/* writer identities and user provenance in the calling environment, and do not let models select those credentials.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/pinguy/Skills/tree/main/skills/blackboard)
- [ClawHub skill page](https://clawhub.ai/pinguy/skills/blackboard-2)
- [Blackboard schema](references/schema.md)
- [Three-model canary](references/canary.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON board records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and mutates local JSON board files; timestamped backups may retain prior board contents until pruned.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
