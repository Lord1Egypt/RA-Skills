## Description: <br>
Create a new OpenClaw agent with a workspace directory and SOUL.md configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create a named agent workspace, set its identity, customize SOUL.md, and initialize local memory structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested commands create or modify a persistent local OpenClaw agent workspace. <br>
Mitigation: Confirm the agent name and workspace path before running commands, and check whether the target workspace already exists. <br>
Risk: Generated SOUL.md and memory files can affect the agent's identity, boundaries, and future behavior. <br>
Mitigation: Review the generated SOUL.md and memory file content before relying on the agent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/agent-creation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and SOUL.md template content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace setup guidance and editable agent identity files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
