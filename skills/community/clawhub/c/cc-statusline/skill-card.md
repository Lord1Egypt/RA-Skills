## Description: <br>
Cc Statusline helps Claude Code users preview, install, switch, customize, troubleshoot, and remove statusline configurations across Windows, macOS, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Miluer-tcq](https://clawhub.ai/user/Miluer-tcq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to configure a Claude Code statusline, choose preset or custom layouts, switch themes and icon styles, and restore or troubleshoot statusline setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can modify ~/.claude/settings.json and install a persistent Claude Code statusline command. <br>
Mitigation: Review the preview, target path, and statusLine change before activation; confirm that only the intended statusLine entry is changed. <br>
Risk: The setup can automatically install jq with sudo or download a jq executable. <br>
Mitigation: Prefer installing jq from a trusted source before using the skill, and avoid approving automatic sudo, package-manager, or binary-download steps unless the source is trusted. <br>


## Reference(s): <br>
- [README.en.md](README.en.md) <br>
- [Modules](references/modules.md) <br>
- [Trigger phrases](references/trigger-phrases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or activate statusline scripts and update the Claude Code statusLine setting after preview.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
