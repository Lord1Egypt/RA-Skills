## Description:

Reads and reports hardware temperature sensor values from the DGX Spark system via SNMP for hardware health monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seitzbg](https://clawhub.ai/user/seitzbg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check DGX Spark hardware temperatures via SNMP and summarize sensor readings for hardware health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a plaintext SNMPv2c community string for a named DGX Spark host.

Mitigation: Move the community string to protected configuration, prefer SNMPv3, and rotate the exposed community before broad use.

Risk: The skill includes host and system details for a specific DGX Spark environment.

Mitigation: Use it only on systems you own or are authorized to monitor, and avoid distributing internal host, location, or system details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seitzbg/skills/dgx-spark-temperature)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown and terminal text with inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports sensor temperatures in Celsius and summarizes average, maximum, and minimum readings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
