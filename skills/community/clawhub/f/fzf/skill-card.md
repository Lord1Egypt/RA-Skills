## Description:

Fzf helps agents guide users through installing, configuring, troubleshooting, and using the fzf command-line fuzzy finder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users use this skill to learn fzf workflows, configure shell integration, build reusable search commands, and troubleshoot common installation or usage issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to install software or edit persistent shell startup files.

Mitigation: Review package sources and inspect exact shell configuration diffs before applying changes.

Risk: Examples include process, container, stash, checkout, and file operations that may be destructive.

Mitigation: Require explicit user confirmation before running commands that kill processes, stop containers, alter Git state, or delete files.

Risk: Download commands that use latest release URLs may retrieve unverified binaries.

Mitigation: Prefer trusted package managers or verify release artifacts before installation.

## Reference(s):

- [fzf GitHub Project](https://github.com/junegunn/fzf)
- [fzf Wiki](https://github.com/junegunn/fzf/wiki)
- [fzf Wiki Examples](https://github.com/junegunn/fzf/wiki/examples)
- [ClawHub Fzf Skill](https://clawhub.ai/cn-big-cabbage/skills/fzf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that install tools, edit shell startup files, or perform destructive command-line operations.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
