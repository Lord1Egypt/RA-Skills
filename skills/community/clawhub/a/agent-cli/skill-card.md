## Description: <br>
Routes code editing, refactoring, review, debugging, and automation tasks to Cursor CLI or Qoder CLI with guidance for choosing and running each tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohei2022](https://clawhub.ai/user/xiaohei2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to decide when to delegate code edits, refactors, reviews, debugging, CI automation, and related repository tasks to Cursor CLI or Qoder CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegating coding work to Cursor or Qoder can modify repository files or run commands with elevated automation settings. <br>
Mitigation: Use the skill only in intended repositories, avoid force or yolo modes unless the repository is trusted and scoped, and review diffs before merging. <br>
Risk: Persistent CLI settings, MCP configuration, memory files, or tmux sessions can outlive the task and affect later work. <br>
Mitigation: Clean up tmux sessions and persistent AGENTS, MCP, or settings files after the delegated task is complete. <br>
Risk: Installer commands and API key setup can expose users to unverified binaries or credential handling mistakes. <br>
Mitigation: Verify official installers before running them and avoid committing or sharing API keys or local credential configuration. <br>


## Reference(s): <br>
- [Agent CLI reference index](references/README.md) <br>
- [Cursor CLI core operations](references/cursorcli.md) <br>
- [Qoder CLI core operations](references/qodercli.md) <br>
- [Cursor CLI installer](https://cursor.com/install) <br>
- [Qoder documentation index](https://docs.qoder.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and routing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tmux command sequences, CLI flags, output-format choices, and setup notes for Cursor or Qoder.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
