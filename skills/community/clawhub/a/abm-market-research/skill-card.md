## Description:

Conducts market and industry research by gathering source-backed data on market size, growth, trends, key players, opportunities, and risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, analysts, and go-to-market teams use this skill to research markets, assess market size and trends, compare key players, and identify opportunities and risks for a defined industry or segment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command examples may interpolate user-supplied industry names or report URLs if followed literally.

Mitigation: Pass market names and URLs as literal arguments through structured tool calls or argument arrays with shell processing disabled, and avoid untrusted inputs unless the agent enforces that handling.

Risk: Market sizing and forecast sources can be stale, sparse, or conflicting.

Mitigation: Use recent authoritative sources where available, cross-reference important estimates, and state confidence levels or ranges instead of presenting unsupported precision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mariokarras/skills/abm-market-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with structured sections and optional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured market research report with source-quality and confidence notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
