## Description:

Exact detection thresholds for identifying malicious network patterns including port scans, DoS attacks, and beaconing behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and developers use this skill to apply fixed threshold rules when assessing packet captures or network telemetry for port scans, DoS spikes, C2 beaconing, and benign traffic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fixed network detection thresholds may misclassify traffic if local baseline patterns differ from the examples.

Mitigation: Review the port scan, DoS, and beaconing thresholds against the target environment before relying on classifications.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wu-uk/skills/dapt-intrusion-detection-threat-detection)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides threshold-based network threat detection guidance; it does not execute code by itself.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
