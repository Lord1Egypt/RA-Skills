## Description: <br>
Guides an agent in installing, configuring, and using fzf for command-line fuzzy finding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and command-line users use this skill to install and configure fzf, learn fuzzy-search syntax, and build shell, Git, Docker, and content-search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose persistent shell profile changes for fzf integration. <br>
Mitigation: Show the exact lines before editing, back up the affected shell profile, and apply changes only after user approval. <br>
Risk: The skill includes process-kill, Git mutation, Docker stop, and Docker log workflows that can disrupt running work or expose sensitive output. <br>
Mitigation: Require deliberate confirmation before running those commands, and present the selected target and full command first. <br>
Risk: Installation guidance may download or install packages and binaries. <br>
Mitigation: Prefer trusted package managers or the referenced fzf release source, verify the platform choice, and avoid elevated privileges unless required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/fzf) <br>
- [fzf project homepage](https://github.com/junegunn/fzf) <br>
- [fzf wiki](https://github.com/junegunn/fzf/wiki) <br>
- [fzf examples](https://github.com/junegunn/fzf/wiki/examples) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent shell profile edits and operational commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
