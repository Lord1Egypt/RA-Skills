## Description:

Search and retrieve Japanese government statistics from e-Stat, Japan's official open data portal, including population, GDP, CPI, trade, and employment data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to search e-Stat and fetch official Japanese government statistics for analysis, reporting, or downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the estat-mcp package introduces ordinary third-party package dependency risk.

Mitigation: Confirm the package source is trusted and pin a reviewed version before installation.

Risk: The skill requires an e-Stat API key through ESTAT_APP_ID.

Mitigation: Use a dedicated e-Stat API key and avoid sharing it across unrelated systems.

Risk: Running command-line tooling with elevated privileges can increase impact if the dependency is compromised.

Mitigation: Run the tool with normal user privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajtgjmdjp/skills/estat-mcp)
- [Publisher profile](https://clawhub.ai/user/ajtgjmdjp)
- [e-Stat API usage information](https://www.e-stat.go.jp/api/api-info/use-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes package installation, ESTAT_APP_ID setup, search commands, data retrieval commands, and e-Stat filter parameters.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
