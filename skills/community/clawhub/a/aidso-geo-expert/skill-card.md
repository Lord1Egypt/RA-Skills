## Description:

End-to-end GEO workflows for question mining, AI answer monitoring, result retrieval, GEO reporting, and content creation with AIDSO.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangyuanmile-coder](https://clawhub.ai/user/tangyuanmile-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run AIDSO GEO workflows for question mining, AI answer monitoring, task-result retrieval, GEO reporting, and content creation. Paid monitoring and task-result retrieval require an AIDSO token and may consume AIDSO account credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The main operating rules and executable scripts are hidden behind an encrypted runtime, reducing reviewability before use.

Mitigation: Use a sandboxed environment and install only when the encrypted-runtime trust tradeoff is acceptable.

Risk: AIDSO_TOKEN may authorize paid monitoring submission and task-result retrieval.

Mitigation: Provide only the task-specific token through trusted environment configuration and avoid broad filesystem or environment access.

Risk: AIDSO AI monitoring may consume external account credits.

Mitigation: Review paid-credit confirmations carefully and proceed only after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangyuanmile-coder/skills/aidso-geo-expert)
- [Publisher profile](https://clawhub.ai/user/tangyuanmile-coder)
- [AIDSO MCP endpoint](https://api.aidso.com/geo_api/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, text, HTML reports, and shell-command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Node.js and a Python interpreter; paid monitoring and task-result retrieval require AIDSO_TOKEN.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
