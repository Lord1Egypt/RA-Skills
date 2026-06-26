## Description: <br>
Exact detection thresholds for identifying malicious network patterns including port scans, DoS attacks, and beaconing behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and agent operators use this skill to apply documented network-traffic thresholds for port scan, DoS pattern, C2 beaconing, and benign traffic assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Threat labels may be misleading if the thresholds are applied without the required packet context and combined conditions. <br>
Mitigation: Apply the documented detection requirements exactly and review resulting classifications before relying on them operationally. <br>
Risk: Example imports refer to a local packet-analysis helper library. <br>
Mitigation: Verify the referenced helper library is trusted before running it on packet captures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/dapt-intrusion-detection-threat-detection) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Markdown] <br>
**Output Format:** [Markdown with Python code blocks and threshold tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides threshold guidance and example detection functions; it does not install software or take actions on the user's system.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
