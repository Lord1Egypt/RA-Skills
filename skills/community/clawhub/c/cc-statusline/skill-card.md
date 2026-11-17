## Description:

Cc Statusline helps Claude Code users preview, install, switch, customize, troubleshoot, and remove statusline layouts across Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miluer-tcq](https://clawhub.ai/user/miluer-tcq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to configure preset or custom statuslines, choose themes, icons, and modules, and restore or troubleshoot statusLine settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or activated statusline scripts persist a Claude Code statusLine command that can run whenever the statusline refreshes.

Mitigation: Review the target script and settings change before activation, and uninstall by removing only the statusLine entry when the behavior is no longer wanted.

Risk: Automatic jq installation may download or install dependencies during setup.

Mitigation: Prefer a trusted system-installed jq and avoid automatic dependency installation paths when operating in controlled environments.

Risk: Untrusted custom layout, theme, icon, or target-path arguments can affect generated shell scripts or activation behavior.

Mitigation: Use known preset, theme, icon, and path values, and review generated scripts before enabling them.

## Reference(s):

- [Modules](references/modules.md)
- [Trigger phrases](references/trigger-phrases.md)
- [ClawHub skill page](https://clawhub.ai/miluer-tcq/skills/cc-statusline)
- [ClawHub publisher profile](https://clawhub.ai/user/miluer-tcq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or activate shell scripts that update Claude Code statusLine settings.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
