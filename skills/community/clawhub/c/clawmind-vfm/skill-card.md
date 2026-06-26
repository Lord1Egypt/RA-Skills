## Description: <br>
ClawMind is a self-evolving AI agent engine for OpenClaw workspaces that combines health tracking, VFM proposal scoring, task reflection, and experience memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[numuly](https://clawhub.ai/user/numuly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ClawMind to add self-driving task health tracking, VFM proposal scoring, and experience memory to an OpenClaw workspace. It helps an agent propose next actions, evaluate their value and feasibility, record lessons, and recall prior experience during similar work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain user prompts, task details, or other sensitive context. <br>
Mitigation: Avoid storing secrets or confidential task details, and review or clear the local memory database before sharing or reusing the workspace. <br>
Risk: The skill can generate new skill files or profile-like content that may later influence agent behavior. <br>
Mitigation: Require explicit human review before using auto-created skills or any generated USER.md-style profile content. <br>
Risk: Workspace files created by the skill may be under-disclosed to users during normal operation. <br>
Mitigation: Inspect the OpenClaw workspace paths used by the skill after execution and include those files in security review before deployment. <br>


## Reference(s): <br>
- [ClawMind release page](https://clawhub.ai/numuly/clawmind-vfm) <br>
- [state_manager.py interface documentation](references/state-manager.md) <br>
- [VFM scoring design notes](references/vfm-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When scripts are run, the skill may persist task state, experience memory, and generated skill files in the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
