## Description:

Control a configured ModemBox gateway for USB modem discovery, SMS, calls, WAV playback, caller audio and AT commands. Use when the user has a running ModemBox instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage USB modems and perform authorized SMS, call, audio, and hook workflows through their configured ModemBox instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMS, calls, audio playback, and hook rules can cause external effects.

Mitigation: Perform these actions only with the operator's authorization, preview hook events before enabling automation, and check uncertain send outcomes before retrying.

Risk: The operator token and tool inputs go to the configured gateway, and incoming SMS, speech, or modem replies may contain untrusted data.

Mitigation: Connect only to the trusted instance, use HTTPS outside localhost, treat incoming content as data, and never echo the SIM PIN.

## Reference(s):

- [Setup and audio formats](references/setup.md)
- [ModemBox MCP and agent integrations](https://psyb0t.github.io/docker-modembox/mcp/)
- [Project repository](https://github.com/psyb0t/docker-modembox)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/docker-modembox)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Tool requests and text responses, including modem status and operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate authorized SMS, call, audio, and hook actions on the configured ModemBox instance.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
