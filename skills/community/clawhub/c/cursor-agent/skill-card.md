## Description: <br>
A comprehensive skill for using the Cursor CLI agent for various software engineering tasks, including model selection, session management, automation, and tmux-based execution guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swiftlysingh](https://clawhub.ai/user/swiftlysingh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to install, authenticate, configure, and operate the Cursor CLI agent for code review, refactoring, debugging, session management, and CI-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that install remote code and run Cursor CLI with broad repository access. <br>
Mitigation: Use a verifiable installer or package-manager install, run commands only in repositories where Cursor CLI access is acceptable, and review generated changes before keeping them. <br>
Risk: The documented force mode can auto-apply edits without confirmation. <br>
Mitigation: Avoid force mode unless the target repository is reviewed, version controlled, and changes can be reverted. <br>
Risk: The automation workflow includes trusting a workspace from tmux. <br>
Mitigation: Do not automate workspace trust for untrusted, newly downloaded, or unfamiliar projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swiftlysingh/cursor-agent) <br>
- [Cursor CLI installer](https://cursor.com/install) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes interactive and non-interactive Cursor CLI workflows; some referenced commands can install software or modify repository files when executed.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
