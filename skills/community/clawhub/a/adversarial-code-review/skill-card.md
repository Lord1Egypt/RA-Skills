## Description: <br>
Use when reviewing pull requests or critiquing code changes and you want high-signal, low-noise feedback by running multiple adversarial agents that challenge each other's findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reikys](https://clawhub.ai/user/reikys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review pull requests or code changes with an adversarial multi-agent workflow that filters findings down to high-confidence, high-priority issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PR diffs may be sent to the configured model provider during standalone or CI review. <br>
Mitigation: Use only when repository policy allows that data flow, and avoid changes containing secrets, regulated data, or proprietary code unless approved. <br>
Risk: Automated CI comments may post incorrect or overconfident review output back to a pull request. <br>
Mitigation: Treat the output as review assistance, keep human review for security-critical or compliance-gated changes, and require actionable high-confidence findings before acting. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filtered review output is expected to include location, issue, impact, suggested fix, confidence, and priority.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
