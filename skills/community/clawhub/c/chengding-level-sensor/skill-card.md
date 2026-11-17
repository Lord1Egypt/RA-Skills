## Description:

Queries Chengding IoT liquid-level sensor device status, including online state and switch state, after the user configures key, tel, and imei values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devingonggz](https://clawhub.ai/user/devingonggz)

### License/Terms of Use:


## Use Case:

External users, developers, and device operators use this skill to query Chengding IoT liquid-level sensor status through a curl request or bundled shell script. It supports checking whether a device is online, reading switch-state values, and monitoring configured liquid-level devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key, phone number, and IMEI values can expose device or account information if committed, shared, or logged.

Mitigation: Keep filled-in credentials in private local configuration or environment variables with restricted permissions, and rotate any real credentials that were pasted into shared files or logs.

Risk: Calling an unverified third-party device API endpoint can disclose credentials to the wrong service.

Mitigation: Confirm that cd6969.com is the correct API endpoint for the user's Chengding IoT device account before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devingonggz/skills/chengding-level-sensor)
- [Chengding IoT device status API endpoint](https://www.cd6969.com/admin.php?s=/Admin/ApiV2/getList.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied key, tel, and imei values; the bundled script expects curl and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
