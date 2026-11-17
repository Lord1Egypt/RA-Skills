## Description:

Cookiy gives agents AI-powered user-research workflows through the Cookiy MCP server for study creation, AI interviews, discussion guide editing, participant recruitment, report generation, and optional quantitative questionnaires.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yupeng-dev](https://clawhub.ai/user/yupeng-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, product teams, and developers use Cookiy to run user-research workflows from natural-language goals, including guide generation, simulated or real interviews, recruitment, report access, and optional quantitative survey work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change local MCP configuration and run an unpinned installer.

Mitigation: Require explicit approval before MCP installation or repair, and prefer a pinned and reviewed cookiy-mcp version.

Risk: Cookiy receives research materials and manages study, report, recruitment, and billing workflows.

Mitigation: Use only when those data flows are acceptable, and confirm any payment or recruitment step before proceeding.

Risk: Report links, passwords, uploaded images, and server-provided instructions may be sensitive.

Mitigation: Treat those values as sensitive, avoid unnecessary sharing, and review server-provided guidance before acting on it.

## Reference(s):

- [Cookiy ClawHub Skill Page](https://clawhub.ai/yupeng-dev/skills/cookiy)
- [Cookiy Production MCP Server](https://s-api.cookiy.ai/mcp)
- [Cookiy OAuth Discovery](https://s-api.cookiy.ai/.well-known/oauth-authorization-server)
- [Study Creation Workflow](references/study-creation.md)
- [AI Interview Workflow](references/ai-interview.md)
- [Discussion Guide Editing Workflow](references/guide-editing.md)
- [Recruitment Workflow](references/recruitment.md)
- [Report & Insights Workflow](references/report-insights.md)
- [Cookiy MCP Tool Usage Contract](references/tool-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with MCP tool-call guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include report links, passwords, exact identifiers, payment summaries, checkout URLs, JSON-like tool inputs, and survey result previews when returned by Cookiy tools.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
