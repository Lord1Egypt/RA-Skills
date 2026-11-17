## Description:

Searches premium cabin and first-class flights, compares comfort, lounge access, frequent flyer miles, and value, and formats flyai CLI results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT

## Use Case:

External travelers and agents use this skill to collect trip parameters, run flyai flight searches for business or first class options, and return concise Markdown comparisons with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned flyai CLI, including fallback guidance that mentions sudo/global installation.

Mitigation: Install only after trusting the flyai CLI and package source, avoid sudo or global installation where possible, and run the skill in a constrained environment.

Risk: The skill may persist raw travel queries to a local execution log.

Mitigation: Warn users before logging travel queries, avoid collecting sensitive travel details where possible, and define log retention or deletion before deployment.

Risk: Fallback behavior may relax travel constraints or add booking links that affect user decisions.

Mitigation: Confirm relaxed constraints with the user and verify booking links before presenting them as actionable options.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/business-class-finder)
- [Parent flyai Skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel results; raw JSON should not be returned to the user.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
