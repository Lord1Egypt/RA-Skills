## Description: <br>
cc-sticky-notify installs and helps configure a macOS sticky-note notification system for Claude Code events using local shell hooks and a native Swift floating window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bucleliu](https://clawhub.ai/user/bucleliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code on macOS use this skill to install, configure, test, or troubleshoot sticky desktop notifications for completed tasks, permission prompts, idle prompts, and failed Bash commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Claude Code hooks can run the notifier automatically on task completion, permission prompts, idle prompts, and failed Bash commands. <br>
Mitigation: Review the hook commands in ~/.claude/settings.json before enabling them and remove the entries when the notifier is no longer needed. <br>
Risk: The notifier reads local application and window context to support source display and click-to-focus behavior. <br>
Mitigation: Grant macOS automation or accessibility permissions only after reviewing the prompts and use the skill only on trusted local Macs. <br>
Risk: The installer compiles and signs a local Swift app bundle for the floating sticky window. <br>
Mitigation: Run install.sh only from the reviewed release artifact and inspect the script before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bucleliu/cc-sticky-notify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
