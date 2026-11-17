## Description:

Analyze Japanese public company financial statements from EDINET by company name or stock code, compare periods and companies, and work across J-GAAP, IFRS, and US-GAAP data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp)

### License/Terms of Use:


## Use Case:

Developers, analysts, and finance-focused agents use this skill to search Japanese public companies, retrieve EDINET financial statements, compare periods, and screen companies by financial metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external, unpinned edinet-mcp package as the effective runtime component.

Mitigation: Install a reviewed package version in an isolated environment before using it with production workflows.

Risk: The skill requires an EDINET_API_KEY for data access.

Mitigation: Provide only an API key intended for this use and manage it through normal secret-handling controls.

## Reference(s):

- [EDINET disclosure system](https://disclosure2dl.edinet-fsa.go.jp/)
- [ClawHub skill page](https://clawhub.ai/ajtgjmdjp/skills/edinet-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the edinet-mcp command-line package and an EDINET_API_KEY; financial data retrieval is rate-limited by default.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
