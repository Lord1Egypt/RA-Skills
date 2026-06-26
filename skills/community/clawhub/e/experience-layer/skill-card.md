## Description: <br>
Skill Experience Layer is a failure-driven learning mechanism for OpenClaw agents that accumulates lessons and best practices to help avoid repeated mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jilanfang](https://clawhub.ai/user/jilanfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain compact JSON experience files that record tool-use failures, successful practices, and prevention patterns for future OpenClaw agent runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent experience files can steer future agent behavior for shell commands, messaging, scheduling, skill management, and external-account actions. <br>
Mitigation: Review each JSON experience file before use and require explicit confirmation before applying stored lessons to sensitive or external actions. <br>
Risk: Example files include project-specific local paths and a Feishu/Lark open_id that may not apply to other users. <br>
Mitigation: Remove or replace local paths, account identifiers, and Feishu/Lark-specific values before installing the examples into an agent memory directory. <br>
Risk: Outdated or overly broad lessons can cause an agent to follow stale guidance. <br>
Mitigation: Keep experience entries project-specific where possible and periodically remove outdated or duplicate lessons. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jilanfang/experience-layer) <br>
- [Publisher Profile](https://clawhub.ai/user/jilanfang) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON, Shell commands] <br>
**Output Format:** [Markdown instructions with JSON experience templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent experience-file guidance and category templates for agent memory workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
