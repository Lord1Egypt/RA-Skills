## Description:

Api Cost Optimizer analyzes OpenClaw agent configuration and API usage patterns to estimate spend, diagnose heartbeat waste, and recommend cost reductions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to estimate OpenClaw LLM API spend, identify inefficient heartbeat settings, and prioritize configuration changes that may reduce recurring API costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts use unsafe path handling that can allow local code execution in crafted environments.

Mitigation: Review and patch path handling before deployment; run the skill only in a trusted local environment.

Risk: The generated cost estimates may not match provider billing data.

Mitigation: Use the reports for planning and compare results against provider cost logs before making budget decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kryzl19/skills/api-cost-optimizer)
- [Publisher Profile](https://clawhub.ai/user/kryzl19)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal reports and command-line estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost numbers are rough estimates based on configuration and default pricing, not provider billing data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
