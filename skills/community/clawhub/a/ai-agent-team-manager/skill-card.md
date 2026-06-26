## Description: <br>
AI Agent Team Manager coordinates multiple OpenClaw agents with task assignment, progress tracking, quality control, performance evaluation, and workflow management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[komong](https://clawhub.ai/user/komong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI operations teams use this skill to coordinate multi-agent OpenClaw projects, assign and track tasks, apply quality checkpoints, and evaluate agent performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation makes enterprise compliance and audit-trail claims that require additional controls. <br>
Mitigation: Use the skill only after defining approval, privacy, and agent-authentication boundaries, and independently validate any compliance or audit requirements. <br>
Risk: The package metadata points to index.js, but the artifact does not include an index.js export file. <br>
Mitigation: Verify or add the package entry point and exports before relying on require('ai-agent-team-manager') or the example usage in a real workflow. <br>
Risk: Multi-agent coordination can propagate incorrect task assignments, status reports, or quality recommendations. <br>
Mitigation: Keep human review checkpoints for critical work and review task plans, reports, and recommendations before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/komong/ai-agent-team-manager) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/komong) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local OpenClaw workspace with git, node, python3, and OPENCLAW_WORKSPACE configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
