## Description:

Control Anova Precision Ovens and Precision Cookers via WiFi WebSocket API to start or stop cooking, set temperatures, and monitor device status remotely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodeja](https://clawhub.ai/user/dodeja)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and external users use this skill to let an agent operate Anova Precision Ovens and Precision Cookers through documented shell commands for cooking, stopping, and monitoring appliance state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can start, stop, or modify cooking on a real heating appliance.

Mitigation: Require explicit user confirmation before every cook or stop command, verify the selected device, and keep a person able to monitor the appliance.

Risk: Unsafe temperature, duration, fan, element, or humidity settings could be sent to the appliance.

Mitigation: Enforce local temperature and duration limits, validate requested cooking parameters, and prefer conservative defaults before execution.

Risk: The Anova personal access token enables remote appliance control if exposed.

Mitigation: Store the token with restricted file permissions, avoid logging or sharing it, and rotate it if compromise is suspected.

Risk: The skill may report success before a stop or cook command has been independently verified.

Mitigation: Check device telemetry after action commands and locally verify that stop commands actually took effect.

Risk: Unpinned dependencies can change behavior across installs.

Mitigation: Pin the websockets dependency to a reviewed version before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dodeja/skills/anova-skill)
- [Source Repository](https://github.com/dodeja/anova-skill)
- [Anova Developer Portal](https://developer.anovaculinary.com)
- [Anova WiFi Developer Project](https://github.com/anova-culinary/developer-project-wifi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell command examples and terminal text or JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Anova token file, Python 3.7 or later, the websockets dependency, internet access, and a paired Anova device.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
