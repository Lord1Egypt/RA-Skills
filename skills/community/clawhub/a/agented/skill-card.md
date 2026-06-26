## Description: <br>
A text editor for LLMs, not humans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frane](https://clawhub.ai/user/frane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Agented to guide LLM agents through durable, command-line text editing with state tokens, undo history, annotations, transactions, and conflict-aware file changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer commands can execute downloaded code when users choose the curl install path. <br>
Mitigation: Prefer the Homebrew installation path where available; if using curl, download and inspect the installer before running it. <br>
Risk: The ae tool can create and modify files and auto-save edits to disk. <br>
Mitigation: Use state tokens and review ae responses before continuing broad or multi-file edits. <br>
Risk: Agented stores workspace history and annotations in .agented/state.db. <br>
Mitigation: Treat the workspace database as project data and review it before sharing or archiving sensitive workspaces. <br>
Risk: Permission-management commands can change agent tool-permission settings. <br>
Mitigation: Review the intended target and scope before running commands that enable or disable internal tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frane/skills/agented) <br>
- [Project homepage](https://github.com/frane/agented) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing instructions for using the ae CLI; no binary output.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
