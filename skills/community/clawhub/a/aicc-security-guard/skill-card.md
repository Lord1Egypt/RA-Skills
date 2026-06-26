## Description: <br>
Ensure the AICC native plugin is active before handling confidential data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[senmud](https://clawhub.ai/user/senmud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users working with confidential data use this skill to require an AICC native plugin check before an agent reads, generates, transmits, or stores sensitive information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause the agent to refuse sensitive-data work when the AICC native plugin is missing or cannot be confirmed. <br>
Mitigation: Verify plugin status with `openclaw plugins list` and review the native plugin's source and permissions before installing or enabling it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to refuse sensitive-data handling until plugin status is confirmed.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
