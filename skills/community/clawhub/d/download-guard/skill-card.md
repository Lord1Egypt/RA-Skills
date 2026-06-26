## Description: <br>
Download Guard is a Windows-only AI agent skill that checks download paths and disk space, blocks unsafe fallback to C:, logs downloads, and helps manage tool caches during install, clone, pull, and download workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nihaoljx](https://clawhub.ai/user/nihaoljx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on Windows use this skill to make agent-triggered downloads and installs visible, space-aware, and tied to an explicit download root. It is most relevant when agents run package installs, model pulls, git clones, cache scans, or cache migration commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cache migration and auto-fix commands may make persistent local package-manager or user environment changes. <br>
Mitigation: Treat "migrate cache" and "fix warnings" as system-maintenance actions, review the proposed changes, and confirm that PATH and tool-specific configuration still point to the intended locations. <br>
Risk: An unsuitable DOWNLOAD_ROOT or log-retention setting can make downloads fail, store files in an unintended location, or retain more history than expected. <br>
Mitigation: Review DOWNLOAD_ROOT and log retention during first setup and after storage changes; use the built-in path check before large downloads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nihaoljx/download-guard) <br>
- [README](artifact/README.md) <br>
- [Detailed Reference](artifact/reference.md) <br>
- [Configuration Reference](artifact/config.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status messages with inline PowerShell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows PowerShell 5.1+ is required; some flows can write logs or change user-level tool configuration after user-facing prompts.] <br>

## Skill Version(s): <br>
5.4.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
