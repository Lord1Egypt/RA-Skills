## Description: <br>
Helps users organize download folders and categorize local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neutronstar238](https://clawhub.ai/user/neutronstar238) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to organize download folders and categorize local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad local file permissions for organizing files. <br>
Mitigation: Name the exact folder to organize, request a preview or dry run first, and require explicit confirmation before any move, rename, edit, overwrite, or delete action. <br>
Risk: The artifact describes planned work and does not include executable implementation or tests. <br>
Mitigation: Review proposed behavior and test on non-critical files before relying on it for routine file organization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neutronstar238/auto-file-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file-organization guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file reads, moves, renames, edits, or shell commands; users should require a preview and explicit confirmation before changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
