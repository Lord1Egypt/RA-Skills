## Description:

广告创意需求管理技能 - 处理需求发起、评审、拆解全流程.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeyeshield](https://clawhub.ai/user/jeyeshield)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operations teams and agents use this skill to create, review, break down, and track advertising creative demands through production handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Callers can read or change demand workflow state and trigger production-style events without clear authorization controls.

Mitigation: Enable the skill only where command invocation is restricted, or add explicit authorization for reviewers, owners, and production roles before shared or production use.

Risk: Demand records, review comments, and event payloads may contain business-sensitive campaign information.

Mitigation: Minimize approval event payloads and redact or validate logged event data before enabling the skill for real workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeyeshield/skills/ad-production-demand-management)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [JSON-like command results, status messages, and Markdown demand documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit demand workflow events when an approved demand moves toward production.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
