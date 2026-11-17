## Description:

Creates file-based task archives and memory handoffs so agents can continue work from files instead of chat history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shr860910](https://clawhub.ai/user/shr860910)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to preserve long-running task state in task archives, handoff files, work logs, decision records, and memory files. It is intended for workflows where continuity across context cleanup or session handoff matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts paid billing before use through a network request that uses a billing API key and user identifier.

Mitigation: Install only when the billing behavior is expected, keep SKILL_BILLING_API_KEY secret, verify SKILL_BILLING_URL before use, and review configured charge amounts.

Risk: The skill writes persistent task, work log, handoff, decision, and memory files in the workspace.

Mitigation: Use it only in workspaces where persistent local notes are acceptable, and review generated files before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shr860910/skills/file-memory-billing)
- [SkillPay billing endpoint](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown task and memory files with concise status text and optional JSON responses from the billing helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and SKILL_BILLING_API_KEY for the bundled billing helper.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
