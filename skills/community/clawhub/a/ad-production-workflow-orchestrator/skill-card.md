## Description: <br>
Coordinates ad-production workflows by creating, starting, pausing, resuming, canceling, and monitoring dependent task steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JEyeshield](https://clawhub.ai/user/JEyeshield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to define and run multi-step ad-production workflows, coordinate other OpenClaw skills, manage dependencies, and inspect workflow state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically launch multi-step workflows from OpenClaw events and workflow definitions without clear scoping or confirmation. <br>
Mitigation: Review workflow definitions before use, restrict connected event sources, and avoid production publishing or distribution accounts until approvals or allowlists are configured. <br>
Risk: Automatic demand.approved workflow starts may create costly or unintended downstream automation. <br>
Mitigation: Monitor or disable automatic demand.approved starts unless the event source and downstream skills are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JEyeshield/ad-production-workflow-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/JEyeshield) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [JSON command responses and workflow status objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates in-memory workflow records and can invoke configured OpenClaw skill commands during workflow execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
