## Description: <br>
智能文件夹颜色标注与命名规范技能。通过 emoji 色块对文件/文件夹进行颜色分类，配合序号补零排序规则，实现直观的视觉化文件管理。适用于个人知识库、项目分类、资源归档等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyrilcao](https://clawhub.ai/user/cyrilcao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to inspect, rename, and organize local folders with emoji-based categories, zero-padded ordering, and generated workspace structure suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file operations can rename, move, create, or reorganize files when execution mode is enabled. <br>
Mitigation: Run dry-run previews first, inspect the planned operations, test on a small folder, and keep backups enabled before applying changes. <br>
Risk: Optional config loading can execute local Python code. <br>
Mitigation: Use only inspected bundled configuration files and avoid --config with untrusted or path-like values. <br>
Risk: Automatic confirmation and no-backup flags reduce operator review and recovery options. <br>
Mitigation: Avoid --yes and --no-backup for real work unless the target directory is already backed up and the dry-run output has been reviewed. <br>


## Reference(s): <br>
- [Color-Filer API Reference](references/api_reference.md) <br>
- [Color-Filer Naming Rules](references/naming_rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cyrilcao/color-filer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output with file-operation previews and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run operation lists, rename mappings, directory analysis summaries, and backup guidance.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
