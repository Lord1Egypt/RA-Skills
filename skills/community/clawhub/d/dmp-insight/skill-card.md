## Description:

Uses the Mingri DMP Open Platform API to create, query, and retrieve audience insight analyses across Minglue and partner insight dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing analysts, operators, and developers use this skill to inspect DMP audience traits, create insight tasks, check task status, and export insight results for downstream audience segmentation or campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses sensitive Mingri DMP access credentials.

Mitigation: Install and run it only in a trusted workspace, protect AK/SK values, and rotate or revoke credentials if exposure is suspected.

Risk: The skill discovers and executes supporting auth and logger skills.

Mitigation: Manually verify the publishers and versions of the auth and logger skills before allowing installation or execution.

Risk: Audience-task history, API result JSON, and Excel exports can contain sensitive business data.

Mitigation: Limit access to generated files and decline or remove the logger workflow when persistent task history is not required.

Risk: Scanning untrusted .skills directories can expose the workflow to unexpected local skill content.

Mitigation: Avoid running the skill in workspaces that contain untrusted skill directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingri26/skills/dmp-insight)
- [Mingdata DMP auth skill](https://clawhub.ai/mingri26/mingdata-dmp-auth)
- [Mingdata DMP API access application form](https://doc.weixin.qq.com/forms/ANEAJwfLAAoADMAHwbhAPICNUE0vDRd8f#/fill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files, JSON]

**Output Format:** [Markdown guidance, structured JSON responses, and generated JSON or Excel result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local credentials, task history, raw API JSON, and Excel exports that should be treated as sensitive business data.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
