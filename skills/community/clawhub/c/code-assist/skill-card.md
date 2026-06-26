## Description: <br>
Generate, review, debug, and refactor production-ready code in Python, JavaScript/TypeScript, Go, Rust, Java, and C/C++ with syntax checks and targeted edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate new code, review existing code for security and performance issues, debug errors, and refactor code while preserving behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace code or analysis requests may be sent to api.evolink.ai. <br>
Mitigation: Use the skill only after confirming the selected repository has no secrets or confidential code, and prefer a sandbox or test repository for sensitive work. <br>
Risk: Verification may execute local syntax checks or tests against user code. <br>
Mitigation: Run the skill in a trusted, isolated environment and review commands before execution. <br>
Risk: File-scope and security claims are not clear enough in the security evidence. <br>
Mitigation: Confirm exactly which files will be read before use and keep secrets out of the workspace. <br>
Risk: Included authentication examples may require production hardening. <br>
Mitigation: Do not reuse sample secrets or debug-mode settings in production; replace secret handling and review generated authentication code before deployment. <br>


## Reference(s): <br>
- [ClawHub Code Assistant Listing](https://clawhub.ai/EvoLinkAI/code-assist) <br>
- [EvoLinkAI Publisher Profile](https://clawhub.ai/user/EvoLinkAI) <br>
- [Source Code Link from Artifact README](https://github.com/EvoLinkAI/code-assistant-skill-for-openclaw) <br>
- [Evolink API Reference](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=code-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, command examples, verification output, and explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated or modified source files, syntax-check commands, test commands, review findings, and debugging explanations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
