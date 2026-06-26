## Description: <br>
Active Self-Improvement helps an agent read learning logs, errors, batch outputs, and memory, detect repeated patterns, and propose or apply updates to skills, protocols, and behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make an agent review prior errors and learnings, generate concrete improvement proposals, and update relevant guidance files when changes are low risk or explicitly approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to change its own skills, memory, or behavior guidance automatically. <br>
Mitigation: Use dry-run mode first, review diffs before writes, and restrict the files it may read or modify. <br>
Risk: Automatic or scheduled runs can compound incorrect guidance if repeated patterns are misread. <br>
Mitigation: Avoid unattended runs unless clear review gates, file allowlists, and high-risk approval rules are configured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dodge1218/active-self-improvement) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown proposals, reports, and guidance updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run reporting and risk-tiered application behavior when the invoking agent implements those modes.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
