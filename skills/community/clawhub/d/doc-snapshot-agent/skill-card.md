## Description: <br>
Doc Snapshot Agent parses image markers in Markdown, captures website screenshots or generates conceptual images, and outputs an image-enriched Markdown file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, technical writers, and documentation teams use this skill to turn Markdown image markers into captured screenshots or generated illustrations and assemble an illustrated Markdown output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may access authenticated websites and local credentials to capture screenshots. <br>
Mitigation: Use test or least-privilege accounts, provide credentials through environment variables only, and stop for user confirmation at login, signup, invite, or verification gates. <br>
Risk: Screenshots, generated images, and persistent site knowledge may contain sensitive or user-specific information. <br>
Mitigation: Keep project roots and site-knowledge directories dedicated to the task, review outputs before sharing, avoid storing secrets in notes, and delete persistent site knowledge when it is no longer needed. <br>
Risk: Generated-image prompts are sent to an external image provider through OpenRouter. <br>
Mitigation: Avoid putting confidential document content or secrets in image prompts and supply OPENROUTER_API_KEY only through the environment. <br>


## Reference(s): <br>
- [Doc Snapshot Agent on ClawHub](https://clawhub.ai/wangzhiming1999/doc-snapshot-agent) <br>
- [Felo Skills homepage](https://github.com/Felo-Inc/felo-skills) <br>
- [Browser Automation Reference](references/browser-automation.md) <br>
- [Playwright MCP Reference](references/playwright-mcp.md) <br>
- [Site Explorer Reference](references/site-explorer.md) <br>
- [Image Generation Reference](references/image-generation.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated runs produce Markdown documents, PNG assets, and README inventories.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local project-root folders for cases, raw screenshots, final image assets, generated Markdown, and screenshot cache entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
