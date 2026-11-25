## Description:

Guide Codex through consequential multi-stage implementation work in small validated checkpoints. Use for production rollouts or mutations, external delivery, scheduled automation, secrets/permissions/billing/customer-data changes, destructive work, major dependency or rollback risk, or explicit step review. Avoid routine direct work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide consequential multi-stage implementation work through reviewable checkpoints, with validation and approval decisions at each stage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Consequential implementation steps may affect production systems or create external side effects.

Mitigation: Use read-only discovery and dry runs first, obtain approval before unauthorized live effects, and read back results after an approved batch.

Risk: Unresolved or weak validation can leave a change unsafe to continue.

Mitigation: Set acceptance criteria for each checkpoint and stop for review if validation remains missing, weak, or contradictory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniel-refahi-ikara/skills/dr-checkpoint-implementation)
- [APPLY.md](references/APPLY.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance and checkpoint records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
