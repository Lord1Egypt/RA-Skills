## Description:

Company Search Tool Pro helps Chinese-speaking agents produce enterprise due diligence reports, risk screening, batch company lookups, monitoring alerts, relationship analysis, history checks, intellectual property lookups, and bidding record lookups with structured outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, enterprise teams, developers, and automation workflow owners use this skill to research companies, prepare due diligence summaries, assess supplier or investment risk, query multiple companies, and monitor company status changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags broad local file access and shell execution authority.

Mitigation: Install and run the skill only in an environment where those permissions are acceptable, and review commands or file operations before execution.

Risk: The security guidance calls out monitoring and webhook behavior that can transmit company-risk data.

Mitigation: Enable callbacks or monitoring only for trusted webhook destinations, and avoid sending sensitive company-risk data unless the destination and data handling are approved.

Risk: The security verdict is suspicious.

Mitigation: Review the skill before installation, configure API keys through environment variables, and limit enabled capabilities to the workflows required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/company-search-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and structured JSON-style results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include company-risk summaries, execution logs, API usage guidance, and optional webhook notification guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
