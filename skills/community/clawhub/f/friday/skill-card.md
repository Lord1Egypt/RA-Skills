## Description: <br>
专用编程代理 - 使用 opencode 进行代码编写、审查、重构和调试. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[easeclick](https://clawhub.ai/user/easeclick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding work to the opencode CLI, including code generation, review, refactoring, debugging, testing, and technical documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal or automatic opencode runs can modify project files. <br>
Mitigation: Use read-only or interactive mode for unfamiliar repositories and review generated changes before committing. <br>
Risk: Prompts may expose sensitive information to the coding agent workflow. <br>
Mitigation: Avoid including secrets, passwords, API keys, or other sensitive values in prompts. <br>
Risk: Generated code, reviews, or fixes may be incomplete or incorrect. <br>
Mitigation: Run the relevant tests and code checks, and manually review proposed changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/easeclick/friday) <br>
- [Skill homepage](https://clawdhub.com/skills/friday) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, file-change summaries, review findings, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the opencode CLI; supports Linux, macOS, and Windows according to ClawHub metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
