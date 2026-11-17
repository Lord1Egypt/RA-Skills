## Description:

Financial Research helps agents use AnyGen to generate financial analysis, earnings research, and investment-related reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logictortoise](https://clawhub.ai/user/logictortoise)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to produce financial analysis, earnings research, valuation, due diligence, portfolio analysis, or other investment-related reports through AnyGen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install AnyGen tooling and a workflow into the agent environment.

Mitigation: Use a pinned or audited AnyGen CLI version and review the installed workflow before use.

Risk: Financial material provided to the skill may be routed to a third-party service.

Mitigation: Avoid sending confidential portfolio, company, or client data unless the user's AnyGen account and policies permit it.

## Reference(s):

- [Financial Research on ClawHub](https://clawhub.ai/logictortoise/skills/anygen-financial-research)
- [AnyGen](https://www.anygen.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces finance-report guidance through the AnyGen CLI and requires ANYGEN_API_KEY authentication.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
