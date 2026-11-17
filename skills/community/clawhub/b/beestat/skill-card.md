## Description:

Query ecobee thermostat data via Beestat API including temperature, humidity, air quality (CO2, VOC), sensors, and HVAC runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users and home automation operators use this skill to check ecobee thermostat status, sensor readings, air quality, HVAC runtime, and related Beestat analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses `BEESTAT_API_KEY`, which can grant access to thermostat and household analytics data if exposed.

Mitigation: Store the API key in a private environment, avoid logging or committing it, and rotate it if exposure is suspected.

Risk: Command output may reveal private household information such as occupancy, sensor history, temperature patterns, and HVAC runtime.

Mitigation: Treat command output as private data and avoid sharing it in public logs, screenshots, or transcripts.

Risk: The skill depends on the external `beestat-cli` binary.

Mitigation: Verify the installed package is the intended `beestat-cli` package and consider pinning a reviewed version before deployment.

## Reference(s):

- [Beestat homepage](https://beestat.io)
- [ClawHub skill page](https://clawhub.ai/mjrussell/skills/beestat)
- [Publisher profile](https://clawhub.ai/user/mjrussell)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may return text or JSON output from the Beestat CLI.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
