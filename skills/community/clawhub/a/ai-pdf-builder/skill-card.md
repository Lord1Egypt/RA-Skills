## Description: <br>
AI PDF Builder helps agents generate professional PDFs for legal documents, pitch decks, reports, and startup documents from Markdown or prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NextFrontierBuilds](https://clawhub.ai/user/NextFrontierBuilds) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to create professional PDF whitepapers, memos, agreements, SAFEs, NDAs, term sheets, reports, and proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run npm CLI commands and local Pandoc or LaTeX setup commands on the user's machine. <br>
Mitigation: Review the commands before execution and install only in environments where those tools are approved. <br>
Risk: Optional AI features may process sensitive document content with Anthropic or Claude. <br>
Mitigation: Use AI features only with documents approved for external AI processing and protect the Anthropic API key. <br>


## Reference(s): <br>
- [AI PDF Builder npm package](https://www.npmjs.com/package/ai-pdf-builder) <br>
- [AI PDF Builder GitHub repository](https://github.com/NextFrontierBuilds/ai-pdf-builder) <br>
- [ClawHub skill page](https://clawhub.ai/NextFrontierBuilds/ai-pdf-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of local Pandoc and LaTeX tooling, npm CLI commands, and optional Anthropic API key configuration.] <br>

## Skill Version(s): <br>
1.2.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
