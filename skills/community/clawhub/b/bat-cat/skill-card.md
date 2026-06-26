## Description: <br>
A cat clone with syntax highlighting, line numbers, and Git integration - a modern replacement for cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arnarsson](https://clawhub.ai/user/Arnarsson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to preview files with bat, including syntax highlighting, line numbers, Git changes, themes, line ranges, and pager-style workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to display local file contents, which may expose sensitive data if used on confidential files. <br>
Mitigation: Only preview files the user has authorized the agent to read, and review command targets before execution. <br>
Risk: Optional aliases or pager environment variables can change shell behavior until removed. <br>
Mitigation: Apply shell aliases or pager settings deliberately and remove them from shell configuration when no longer needed. <br>


## Reference(s): <br>
- [Bat GitHub Repository](https://github.com/sharkdp/bat) <br>
- [Bat Customization Documentation](https://github.com/sharkdp/bat#customization) <br>
- [ClawHub Skill Page](https://clawhub.ai/Arnarsson/bat-cat) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the bat command-line tool; Debian and Ubuntu systems may expose it as batcat.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
