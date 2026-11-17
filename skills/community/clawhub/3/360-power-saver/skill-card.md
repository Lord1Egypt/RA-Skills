## Description:

360 Power Saver helps agents inspect local battery, CPU, memory, process, and power-plan status and produce power-saving diagnostics and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttqftech](https://clawhub.ai/user/ttqftech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and IT/admin-oriented agents use this skill to inspect Windows and macOS power state, generate battery and energy reports, rank resource-heavy processes, and provide power-saving recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Markdown fetched by the skill may contain unvalidated content.

Mitigation: Treat remote responses as untrusted text, validate them outside the agent workflow, and delete the temporary file if injection-like content appears.

Risk: Local diagnostic outputs may expose battery, CPU, memory, process, and power-plan state.

Mitigation: Persist diagnostic data only with user consent, keep it in temporary storage, and remove it when no longer needed.

Risk: Energy reports and power-plan changes may request administrator privileges.

Mitigation: Proceed only after the user understands the permission prompt and the specific powercfg action being requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ttqftech/skills/360-power-saver)
- [Remote power strategy markdown endpoint](https://clawhub.virustotal.com/trustedApi/360power/v1/devicePower.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell or PowerShell commands and generated local diagnostic report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open local HTML reports and system dialogs; some Windows powercfg operations request administrator approval.]

## Skill Version(s):

0.0.15-dazhanhongtu (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
