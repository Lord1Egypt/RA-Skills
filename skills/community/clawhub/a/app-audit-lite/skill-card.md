## Description:

Audits one App Store or Google Play app with live AppGoat data and returns a prioritized list of improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafalzawadzki](https://clawhub.ai/user/rafalzawadzki)

### License/Terms of Use:

MIT

## Use Case:

App owners and developers use this skill to review an app's store listing, ratings, reviews, search visibility, competitors, and localization, then prioritize improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged a concern about API key exposure in a command's arguments.

Mitigation: Keep API keys out of command-line arguments and logs; pass them through a protected configuration or environment mechanism.

Risk: The scheduled workflow can write to and push repository changes beyond producing an app audit.

Mitigation: Enable repository write and push access only when needed, constrain the workflow token, and review generated changes before they are pushed.

Risk: The security scan was partial, and some obfuscated text and references were not fully evaluated.

Mitigation: Review the unevaluated skill content and referenced material before deployment.

## Reference(s):

- [AppGoat REST fallback](reference/api.md)
- [AppGoat API](https://api.appgoat.ai/v1)
- [AppGoat MCP server](https://api.appgoat.ai/mcp)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with evidence tables and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes app and competitor findings, keyword opportunities, review themes, and a prioritized list of up to seven fixes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
