## Description: <br>
Evolution Watcher monitors installed ClawHub plugin versions, analyzes available updates and code changes, and generates upgrade reports with adapter-fix guidance. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw maintainers use this skill to check installed plugin versions, compare available updates, review compatibility risks, and prepare upgrade decisions. The artifact states this release is for development and testing rather than production deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose and apply adapter code changes when manually authorized. <br>
Mitigation: Use it only in a test or development OpenClaw environment, review each generated diff, and set authorized=True only after manual approval. <br>
Risk: Generated upgrade scripts or patch commands may modify files incorrectly. <br>
Mitigation: Inspect generated commands and patches before execution, keep backups, and run health checks or tests after applying any change. <br>
Risk: Email reporting can send update details through SMTP if configured. <br>
Mitigation: Avoid configuring SMTP credentials unless the recipient, sender, and report contents have been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/whoisme007/evolution-watcher) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>
- [Monitor Sources Configuration](artifact/config/monitor_sources.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, console text, JSON logs, unified diffs, and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include upgrade analysis, dependency conflict notes, sandbox validation results, and manual authorization prompts.] <br>

## Skill Version(s): <br>
0.6.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
