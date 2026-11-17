## Description:

Access Artsonia (artsonia.com) student-art portfolios, comments, fans, teacher feedback, and downloads from a shell with curl instead of running the artsonia-mcp server — log in with a username/password form POST to get a session cookie, then curl the server-rendered member pages. Use when you want Artsonia data without the MCP, in a script, or on a machine where the MCP isn't installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and developers can use curl and scripts to retrieve Artsonia student portfolios, artwork details, comments, fan activity, teacher feedback, and downloads without running the Artsonia MCP server. The documented commands also include account and content updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write actions can change accounts or content beyond portfolio retrieval, while session cookies and student data may be stored locally.

Mitigation: Review each POST before running, re-fetch the affected page to confirm changes, and protect the cookie jar and any saved student data.

## Reference(s):

- [Artsonia endpoints and curl recipes](references/endpoints.md)
- [Artsonia member login](https://www.artsonia.com/members/login.asp)
- [ClawHub release page](https://clawhub.ai/chrischall/skills/artsonia-api)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown instructions with curl commands and JSON data parsed from Artsonia pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download artwork images as files.]

## Skill Version(s):

1.4.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
