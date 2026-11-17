## Description: <br>
Auto File Organizer Free helps users organize local folders by file type or date, preview file moves before execution, generate organization summaries, and undo moves from an operation log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan and run local folder organization workflows for downloads, desktops, and project directories. It provides preview, execution, reporting, custom rule, and undo guidance for file moves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose file mutation and command execution for local folders. <br>
Mitigation: Use preview mode first, restrict runs to folders you intentionally choose, and keep backups before executing file moves. <br>
Risk: The security evidence notes broader routing, deletion, and callback/network language than expected for a local organizer. <br>
Mitigation: Avoid using callback_url, do not enable deletion or cleanup behavior unless the exact behavior is clear, and review proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/auto-file-organizer-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, YAML configuration examples, and JSON-style status output.] <br>
**Output Parameters:** [Folder path, organization mode, preview/undo/report flags, date granularity, and optional custom rules.] <br>
**Other Properties Related to Output:** [The skill can propose local file moves and command execution; users should preview and review changes before running commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
