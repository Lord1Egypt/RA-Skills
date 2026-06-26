## Description: <br>
Automate web browser interactions using natural language via CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peytoncasper](https://clawhub.ai/user/peytoncasper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to browse websites, navigate pages, extract page data, capture screenshots, fill forms, click controls, and interact with web applications through a CLI-driven browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad browser-control authority, including page navigation, form interaction, screenshots, and downloads. <br>
Mitigation: Use isolated Chrome profiles, avoid saved passwords, and confirm before form submissions, purchases, account changes, downloads, or remote Browserbase sessions. <br>
Risk: Persistent sessions and retained browser artifacts can preserve sensitive account state or downloaded data. <br>
Mitigation: Clear .chrome-profile and ./agent/downloads/ when retained session data or downloads are no longer needed. <br>
Risk: The global browser command install target was not reviewable from the provided evidence. <br>
Mitigation: Review the actual CLI package and source behind the browser command before installing or linking it globally. <br>


## Reference(s): <br>
- [Browser Automation CLI Reference](REFERENCE.md) <br>
- [Browser Automation Examples](EXAMPLES.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/peytoncasper/agent-browser-stagehand) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser commands may create screenshots and downloads under agent-managed output directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
