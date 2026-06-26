## Description: <br>
Read DeepSeek chat share links and continue development from extracted code and docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fhekg](https://clawhub.ai/user/fhekg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn DeepSeek chat share links into local project files, README notes, fragment tracking, and next-step implementation guidance. It is aimed at continuing work from code and design decisions already produced in DeepSeek conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may open DeepSeek links in a headless browser and install Puppeteer to render external pages. <br>
Mitigation: Use it only with chats you own or trust, and prefer running it from a fresh or sandboxed project directory. <br>
Risk: The skill can create or modify project files and persist extracted context across sessions. <br>
Mitigation: Review planned file writes before allowing overwrites and inspect generated README, TODO, and extracted files. <br>
Risk: Code extracted from chat output can be incomplete, stale, or unsafe to run as-is. <br>
Mitigation: Review, test, and security-scan extracted code before executing, deploying, or relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fhekg/deepseek-dev-assistant) <br>
- [DeepSeek share page structure](references/deepseek-page-structure.md) <br>
- [Example extraction workflow](references/example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with extracted files, TODO notes, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write project files, README.md, FRAGMENTS_TODO.md, and session memory based on the DeepSeek chat content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
