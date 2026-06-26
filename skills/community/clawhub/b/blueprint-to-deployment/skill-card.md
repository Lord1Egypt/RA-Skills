## Description: <br>
将 Agent 规划结果补全为可交付、可部署的落地闭环，适用于把蓝图、架构、next actions 写入目标 Agent workspace，并主动推进到平台部署与接入引导。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BeAChanger](https://clawhub.ai/user/BeAChanger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill after planning an agent or MVP to turn blueprints into workspace documents, handoff notes, next actions, and deployment-channel onboarding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent workspace documents under memory or skills directories. <br>
Mitigation: Confirm the target workspace and review planned file paths and generated content before preserving them. <br>
Risk: Saved handoff documents may carry private context into future agent sessions. <br>
Mitigation: Avoid including secrets or private data unless future sessions are explicitly intended to use them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BeAChanger/blueprint-to-deployment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and workspace file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent handoff documents and platform onboarding guidance for a target agent workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
