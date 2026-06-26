## Description: <br>
Query CNKI by journal name or research topic, and create journal or topic subscriptions that periodically push new CNKI paper metadata into the main OpenClaw chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YJLi-new](https://clawhub.ai/user/YJLi-new) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use CNKI Watch to run one-off CNKI journal or topic lookups and configure recurring subscriptions that push new paper metadata into OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports hidden CAPTCHA or slider verification automation that conflicts with the documented human-check behavior. <br>
Mitigation: Use a version that stops for manual verification and asks for a fresh CNKI cookie or manually refreshed session when CNKI presents CAPTCHA, slider verification, or another human check. <br>
Risk: The skill automates CNKI web access with CNKI cookies or credentials. <br>
Mitigation: Install only in environments where this access is authorized, keep CNKI credentials in the configured environment fields, and rotate or remove them when the skill is no longer needed. <br>
Risk: Subscriptions store state, create scheduled OpenClaw jobs, and can post new findings into the main chat. <br>
Mitigation: Review subscription schedules and limits before enabling recurring watches, and use the list and unsubscribe commands to audit or remove active jobs. <br>


## Reference(s): <br>
- [CNKI Watch ClawHub Release](https://clawhub.ai/YJLi-new/cnki-watch) <br>
- [Command Contract](references/commands.md) <br>
- [Runtime Config](references/config.md) <br>
- [Schedule Format](references/schedule.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns CNKI paper metadata and links only; subscription runs may create scheduled OpenClaw jobs and push new items into the main chat.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
