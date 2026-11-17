## Description:

通过对话即可完成养老机构护理排班，简单快捷

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnspica](https://clawhub.ai/user/cnspica)

### License/Terms of Use:

MIT-0

## Use Case:

External care-facility staff and schedulers use this skill to collect staff names and shift parameters through conversation, then generate elder-care duty schedules. It returns a Markdown schedule table and can support CSV export when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Staff roster data may be sensitive and the security evidence reports under-disclosed external AI data transmission.

Mitigation: Use non-sensitive or pseudonymized staff identifiers unless disclosure and consent for DashScope AI use are clear.

Risk: Generated schedules may be incorrect or incomplete for care operations.

Mitigation: Manually review schedule coverage, rest periods, night-shift recovery, and weekly limits before operational use.

Risk: CSV export can persist staff schedule data locally and may create spreadsheet handling risk.

Mitigation: Export CSV only on explicit user request, store it according to facility data-handling policy, and review values before opening in spreadsheet tools.

Risk: Browser-side rendering issues involving staff roster data are reported in the security evidence.

Mitigation: Use the browser interface only with trusted inputs in a controlled environment until the publisher fixes the rendering issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnspica/skills/ai-care-scheduler)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Markdown table with optional CSV export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses default elder-care shifts for morning, afternoon, and night coverage unless the user provides different scheduling parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
