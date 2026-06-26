## Description: <br>
Aider is an AI coding assistant for terminal-based pair programming, Git-integrated edits, multi-model workflows, and code refactoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to guide terminal-based AI pair programming with Aider, including installing the tool, selecting models, managing file context, running tests, and using Git-integrated code edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aider can edit files and create commits in local repositories. <br>
Mitigation: Use a clean branch, review diffs and generated commits before pushing, and keep repository backups or normal Git recovery paths available. <br>
Risk: Using external model providers can expose prompts, code excerpts, logs, command output, or other sensitive data. <br>
Mitigation: Avoid sending secrets, private logs, customer data, or sensitive command output to external providers; use isolated environments or local models when privacy requirements demand it. <br>
Risk: Installing the underlying tool globally can affect the user's Python environment. <br>
Mitigation: Prefer pipx or a virtual environment for installation. <br>


## Reference(s): <br>
- [Aider on ClawHub](https://clawhub.ai/zhangifonly/aider) <br>
- [Publisher profile](https://clawhub.ai/user/zhangifonly) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for installing and running Aider, configuration snippets, model-selection guidance, and workflow advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
