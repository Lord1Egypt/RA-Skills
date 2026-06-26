## Description: <br>
Provides AI agents with App Store research playbooks and live AppKittie data for app discovery, keyword research, metadata optimization, competitor analysis, growth, revenue, and ad intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tadasgedgaudas](https://clawhub.ai/user/tadasgedgaudas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, app marketers, and growth teams use this skill package to connect MCP-compatible agents to AppKittie data and produce App Store research, ASO plans, competitive analyses, growth and revenue benchmarks, ad intelligence reports, and shared app-marketing context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rely on AppKittie's hosted MCP/API and an API key. <br>
Mitigation: Use a dedicated API key, configure the Authorization header only in the MCP client, and verify the installation source before use. <br>
Risk: The app-marketing-context.md file can contain app strategy, budget, competitor, or performance details. <br>
Mitigation: Keep unrelated secrets, customer data, and confidential financial details out of the local context file. <br>
Risk: App Store downloads, revenue, growth, keyword, and ad intelligence are presented as estimates and signals. <br>
Mitigation: Label outputs as estimates, cite the data window used, and review recommendations before making spend, pricing, or positioning decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tadasgedgaudas/appkittie-mcp-skills) <br>
- [AppKittie documentation](https://www.appkittie.com/docs) <br>
- [AppKittie API](https://appkittie.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, tables, inline JSON configuration, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update app-marketing-context.md and may call AppKittie MCP/API endpoints when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
