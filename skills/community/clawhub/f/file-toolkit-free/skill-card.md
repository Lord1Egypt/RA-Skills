## Description: <br>
文件工具箱 helps agents guide local file organization with naming conventions, shallow directory structures, natural-language file search, cleanup workflows, and reusable configuration templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize personal or project files by generating naming rules, directory layouts, search approaches, cleanup plans, and command-oriented workflows. It is most useful when an agent has been granted local file read, write, and command execution authority for explicitly chosen folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to move, rename, or delete local files when granted write and command execution authority. <br>
Mitigation: Limit the agent to intended folders, run preview mode first, review generated operations before execution, and keep backups for important files. <br>
Risk: The artifact describes local-only operation, but privacy depends on the agent platform's handling of prompts and file metadata. <br>
Mitigation: Use platforms and settings that keep file names, paths, and prompts local when that privacy property is required. <br>
Risk: Sample cleanup configuration includes age-based deletion behavior that could remove files the user still needs. <br>
Mitigation: Review deletion thresholds and exclusions before applying cleanup settings, and prefer archive or quarantine actions before permanent deletion. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/thcjp/skills/file-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, tables, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill emphasizes preview-before-execute workflows for file moves, renames, organization, and cleanup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
