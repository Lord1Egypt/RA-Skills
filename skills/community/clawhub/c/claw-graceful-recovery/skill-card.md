## Description: <br>
Claw Graceful Recovery guides an agent through aborting permission-denied or stalled WeChat command execution, sending brief user feedback, and returning to standby. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandon114](https://clawhub.ai/user/brandon114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using Claw through WeChat can use this skill to recover cleanly when permission failures, repeated command failures, or unavailable interaction channels would otherwise leave the agent stuck. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad recovery triggers can stop and reset active work before the user intended to abort it. <br>
Mitigation: Narrow triggers to explicit permission-denial signals and require confirmation for generic stuck or unresponsive cases. <br>
Risk: Fallback recovery logging can silently write task metadata to a local file. <br>
Mitigation: Disable fallback logging or define redaction, retention, and deletion rules for recovery metadata written to disk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brandon114/claw-graceful-recovery) <br>
- [Permission error signals reference](references/error-signals.md) <br>
- [User feedback templates reference](references/feedback-templates.md) <br>
- [English permission error signals reference](i18n-en-references/error-signals.md) <br>
- [English user feedback templates reference](i18n-en-references/feedback-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Shell commands] <br>
**Output Format:** [Markdown instructions with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes short user-facing recovery messages and optional local recovery logging guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
