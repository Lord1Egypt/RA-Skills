## Description:

Create and manage reusable filter rules for email, news, search results, and structured task streams. Designed to reduce noise and preserve signal in OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to create reusable filtering rules for email, news, search results, JSON-like data, and task streams so repeated workflows can reduce noise and preserve relevant items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved filter criteria may persist secrets, private account details, or sensitive personal information if users include them in rules.

Mitigation: Avoid storing secrets or sensitive personal information in rule criteria, and periodically review the local rules file.

Risk: Overly broad allowlists or blocklists can hide relevant items or preserve noisy items in repeated workflows.

Mitigation: Review rule criteria before reuse and tune priority, include, and exclude terms against representative content.

## Reference(s):

- [Filter skill page](https://clawhub.ai/projectsnowwork/skills/filter)
- [ProjectSnowWork publisher profile](https://clawhub.ai/user/projectsnowwork)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [CLI text output and persisted JSON rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends reusable rules in ~/.openclaw/workspace/memory/filter/rules.json.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
