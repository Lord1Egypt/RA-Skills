## Description: <br>
Controlled autonomous self-evolution grants an agent authority to improve its own memory, skills, tool rules, and configuration through tiered permissions, audit trails, rollback steps, and human oversight checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niveroviero](https://clawhub.ai/user/niveroviero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent propose and perform bounded self-improvements while recording what changed, why it changed, and how to roll it back. It is intended for environments where persistent changes to agent behavior are explicitly expected and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to make persistent self-improvements to memory, skills, tool rules, and configuration, including some behavior-changing edits before explicit user approval. <br>
Mitigation: Require explicit approval for every change to skills, tool rules, configuration, memory, or active behavior unless the deployment has separately authorized automated self-modification. <br>
Risk: The server evidence reports a listing mismatch between bacon and self-evolve, which can make it harder to confirm that the reviewed artifact matches the intended release. <br>
Mitigation: Verify that the bacon listing is expected to contain the self-evolve artifact before trusting or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/niveroviero/bacon) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/niveroviero) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with audit-log entries, rollback commands, and change notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause the agent to create or edit persistent workspace files when permitted by the host agent and user approvals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact declares 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
