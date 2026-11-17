## Description:

Configure OpenClaw tool policies, exec security, and per-agent tool restrictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kjvarga](https://clawhub.ai/user/kjvarga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure OpenClaw tool policies, per-agent restrictions, provider-specific rules, plugin tool access, and exec security settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed tool policy changes may grant broader agent capabilities than intended, especially full gateway exec access or disabled approvals.

Mitigation: Review generated config changes before applying them, prefer least-privilege profiles for non-main agents, and keep approvals enabled for sensitive exec access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kjvarga/skills/configure-tools)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown with JSON and JSON5 configuration snippets, command examples, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed OpenClaw config patches and least-privilege review checklist items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
