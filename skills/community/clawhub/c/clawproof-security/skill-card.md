## Description:

Enterprise-grade security for OpenClaw - blocks malicious skills, detects hallucinated packages, and prevents prompt injection attacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinewaveai](https://clawhub.ai/user/sinewaveai)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, skill authors, and security teams use this skill to scan OpenClaw skills, prompts, packages, commands, and generated code before installation or execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable npm code with broad local authority.

Mitigation: Install only when the npm publisher is trusted; prefer pinning the declared version and using a project-local locked install.

Risk: The scanner may read files and prompts supplied for analysis.

Mitigation: Scan only content you are comfortable sharing with the local scanner process and review any generated findings before acting on them.

Risk: Initialization, git hook, and auto-fix commands can modify local project behavior or files.

Mitigation: Review changes from init, init-hooks, and auto-fix workflows before enabling or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinewaveai/skills/clawproof-security)
- [agent-security-scanner-mcp GitHub repository](https://github.com/sinewaveai/agent-security-scanner-mcp)
- [agent-security-scanner-mcp npm package](https://www.npmjs.com/package/agent-security-scanner-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return scan verdicts, A-F grades, warnings, findings, and remediation guidance depending on the invoked scanner command.]

## Skill Version(s):

3.10.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
