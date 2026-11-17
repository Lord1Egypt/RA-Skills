## Description:

Monitor blood glucose via Dexcom G7/G6 CGM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris-clem](https://clawhub.ai/user/chris-clem)

### License/Terms of Use:


## Use Case:

Developers and Dexcom users with Share access use this skill to retrieve current G6/G7 glucose readings and provide an agent with either a formatted glucose status report or raw JSON.

### Deployment Geography for Use:

Global, subject to Dexcom Share account and regional service availability.

## Known Risks and Mitigations:

Risk: The skill handles sensitive Dexcom account credentials and glucose readings.

Mitigation: Use a restricted environment, avoid checked-in or shared configuration files, and protect any local configuration that contains the password.

Risk: Runtime dependencies are installed and executed through uv.

Mitigation: Pin or lock dependencies before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris-clem/skills/dexcom)
- [Dexcom](https://www.dexcom.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Formatted plaintext report or pretty-printed JSON from a command-line script, with Markdown setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEXCOM_USER and DEXCOM_PASSWORD; DEXCOM_REGION is optional and defaults to ous.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
