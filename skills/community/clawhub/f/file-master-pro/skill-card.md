## Description: <br>
强大的文件批量处理工具，支持重命名、整理、搜索、转换等操作，让文件管理变得简单高效。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shengjun33333-code](https://clawhub.ai/user/shengjun33333-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage local file collections through bulk renaming, organization, search, duplicate detection, backup, and archive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk file operations can rename, move, delete, or reorganize important local files. <br>
Mitigation: Run the workflow on a test folder first, keep a separate backup, and confirm target paths before executing commands. <br>
Risk: The installer can persistently change command resolution through PATH or /usr/local/bin changes. <br>
Mitigation: Allow global command installation only when intentionally desired; otherwise run the Python entry point directly or install in a contained user directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shengjun33333-code/file-master-pro) <br>
- [File Master documentation](https://docs.file-master.pro) <br>
- [Project homepage](https://file-master.pro) <br>
- [Project repository listed in artifact metadata](https://github.com/file-master-pro/file-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with inline shell commands, Python snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute filesystem-changing workflows; review target paths, backups, and command scope before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, clawhub-publish-config.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
