## Description: <br>
Backup, sync, and version-track dotfiles across multiple machines. Use when syncing configs, backing up settings, restoring on new machines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to record local system configuration, monitoring, backup, restore, benchmark, and incident-response notes. Security evidence indicates it should be treated as an operational logging helper, not as a real dotfile backup or restore tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is presented as a dotfile backup and sync tool, but security evidence says the artifact behaves as a local sysops logging and export tool. <br>
Mitigation: Use it only for local operational notes, and do not rely on it to protect, synchronize, restore, or version configuration files. <br>
Risk: Operational entries may include secrets, host details, incident data, or sensitive configuration content that is stored locally and can be exported. <br>
Mitigation: Avoid entering sensitive values unless local storage and export of that text is acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub Dotfiles page](https://clawhub.ai/bytesagain1/dotfiles) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed script stores local logs under ~/.local/share/dotfiles and can export entries as JSON, CSV, or TXT.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence; artifact frontmatter and script report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
