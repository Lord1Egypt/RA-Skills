## Description: <br>
Advanced log analysis for Docker containers using signal extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkrdiop](https://clawhub.ai/user/mkrdiop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to extract high-signal Docker container log lines, analyze likely failure causes, and receive targeted troubleshooting guidance for code errors or resource issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted container name could cause the helper script to run unintended local shell commands. <br>
Mitigation: Use the skill only with container names you control until the helper invokes Docker with an argument list, disables shell execution, and validates container names. <br>
Risk: Selected Docker log lines may contain secrets or sensitive operational data. <br>
Mitigation: Avoid running the skill on logs that may contain secrets unless those selected log lines can be exposed to the agent. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes Docker logs and returns selected error context for agent analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
