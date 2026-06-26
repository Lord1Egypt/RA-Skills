## Description: <br>
Automator helps agents create and manage OpenClaw automation workflows for multi-step tasks, parallel processing, conditional logic, and scheduled operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fuczy](https://clawhub.ai/user/Fuczy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business users use this skill to design OpenClaw workflows for recurring reports, monitoring, data pipelines, approvals, backups, and notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated workflows can send messages, post publicly, back up data, or affect production systems. <br>
Mitigation: Test workflows in non-production environments first, limit credentials, verify destinations, and add human approval for high-impact steps. <br>
Risk: Scheduled workflows may continue running after conditions or recipients change. <br>
Mitigation: Confirm each workflow can be paused, stopped, and audited before enabling recurring execution. <br>


## Reference(s): <br>
- [Automator on ClawHub](https://clawhub.ai/Fuczy/clawd-automator) <br>
- [Automator homepage](https://clawhub.com/skills/automator) <br>
- [OpenClaw workflow documentation](https://docs.openclaw.ai/workflows) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with YAML workflow examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow design guidance and examples; it does not execute workflows by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
