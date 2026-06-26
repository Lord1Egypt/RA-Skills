## Description: <br>
Detect and automatically fix spelling errors in Markdown, plain text, and documentation files with support for custom dictionaries and batch processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Linux2010](https://clawhub.ai/user/Linux2010) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, documentation maintainers, and CI operators use this skill to check project documentation for spelling issues and apply common spelling corrections before review or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script may attempt to install aspell with a package manager, including sudo apt-get on supported systems. <br>
Mitigation: Review the script first and install aspell manually through the environment's approved package management process. <br>
Risk: Fix mode can rewrite documentation files, while the security evidence notes weaker safeguards than the documentation advertises. <br>
Mitigation: Run check mode or fix --dry-run first, and only run fix mode on files covered by version control or backups. <br>
Risk: The documentation advertises backup, rollback, and atomic commit behavior that is not fully reflected in the observed script behavior. <br>
Mitigation: Treat those safeguards as unverified and inspect diffs before committing generated edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Linux2010/doc-spellcheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and terminal-style status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify documentation files when fix mode is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
