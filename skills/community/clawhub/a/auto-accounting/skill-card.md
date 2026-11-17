## Description:

Auto Accounting extracts bookkeeping details from payment, order, and receipt images and records them in the YiDay Accounting Android app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taobaoaz](https://clawhub.ai/user/taobaoaz)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals using ClawHub or OpenClaw on Android use this skill to turn screenshots from payment, shopping, and food delivery platforms into accounting entries in YiDay Accounting. It is intended for assisted personal bookkeeping where the user can verify the final financial record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial screenshots and derived transaction details may contain sensitive personal data.

Mitigation: Use only trusted image and GUI dependencies, keep local history in a private directory, and avoid sharing screenshots outside the required runtime.

Risk: Automated bookkeeping can save inaccurate or unintended financial records.

Mitigation: Enable confirmation before saving and verify the amount, merchant, date, type, and category before committing records.

Risk: GUI automation could operate outside the intended accounting app.

Mitigation: Constrain automation to YiDay Accounting and stop execution when the active app or screen no longer matches the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taobaoaz/skills/auto-accounting)
- [Publisher profile](https://clawhub.ai/user/taobaoaz)
- [Project homepage from ClawHub metadata](https://github.com/taobaoaz/auto-accounting)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured bookkeeping fields and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the XiaoYi Claw runtime, trusted image-understanding and GUI-agent dependencies, Android device access, and the YiDay Accounting app.]

## Skill Version(s):

1.0.8 (source: server release metadata, SKILL.md frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
