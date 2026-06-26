## Description: <br>
Generates, patches, reads, and compresses HTML pages for reports, dashboards, documents, invoices, and similar agent-facing outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xdnaimino](https://clawhub.ai/user/xdnaimino) <br>

### License/Terms of Use: <br>
GPL-3.0-only <br>


## Use Case: <br>
Developers and AI-agent users can use this MCP server to create, inspect, and update structured HTML outputs instead of relying on long Markdown responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server can create and modify local HTML files, so mistaken paths or prompts could affect files outside the intended workspace. <br>
Mitigation: Run it in a dedicated workspace or temporary output folder, review target paths before approving edits, and avoid sensitive directories. <br>
Risk: Email-oriented tools can turn generated HTML into content intended for sharing or delivery. <br>
Mitigation: Review generated email content and confirm the intended use before using it with confidential or externally shared material. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/xdnaimino/fast-html-mcp) <br>
- [README](references/README.md) <br>
- [MCP server manifest](references/server.json) <br>
- [Package metadata](references/package.json) <br>
- [License](references/LICENSE) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML files and compressed text responses, with Markdown examples and JSON MCP configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write or patch local HTML files and return token-efficient reads for inspection.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
