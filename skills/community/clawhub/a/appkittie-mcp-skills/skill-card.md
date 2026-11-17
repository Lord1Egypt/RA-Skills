## Description:

AppKittie provides AI agents with live App Store intelligence for app discovery, keyword research, metadata optimization, competitor analysis, growth, revenue, and advertising workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tadasgedgaudas](https://clawhub.ai/user/tadasgedgaudas)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, app marketers, and growth teams use this skill suite to research iOS App Store opportunities, benchmark competitors, prioritize ASO keywords, optimize listing metadata, and analyze growth, revenue, and ads with AppKittie data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill suite from an untrusted or mutable source could expose users to modified instructions.

Mitigation: Install only from a trusted AppKittie or ClawHub source and prefer a pinned release or reviewed commit.

Risk: The AppKittie API key can be exposed if stored in shared project files or plain-text configuration checked into source control.

Mitigation: Store the API key in the MCP client's secret mechanism or another protected local configuration.

Risk: App-market queries, keywords, and app identifiers are sent to AppKittie when the live tools or API are used.

Mitigation: Avoid sending confidential launch plans or sensitive internal strategy terms unless they are approved for AppKittie processing.

Risk: The suite can create or reuse a local app-marketing-context.md file containing app strategy, competitor, and performance notes.

Mitigation: Keep the context file out of shared repositories when it contains private product or market information.

## Reference(s):

- [AppKittie API documentation](https://www.appkittie.com/docs)
- [AppKittie API](https://appkittie.com)
- [ClawHub release page](https://clawhub.ai/tadasgedgaudas/skills/appkittie-mcp-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, configuration snippets, shell commands, JSON examples, and optional app-marketing-context.md files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include App Store research tables, ASO recommendations, API or MCP setup commands, and strategy guidance based on AppKittie data.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
