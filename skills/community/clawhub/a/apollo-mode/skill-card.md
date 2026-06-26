## Description: <br>
Apollo Mode lets an agent enable or disable an engineering workflow for coding tasks, guiding it to clarify goals, draft specs, break work into small tasks, execute incrementally, and verify outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to switch an agent into a structured coding workflow for build, debug, and implementation tasks. It is intended for explicit enable, disable, and status commands, or for coding tasks while the mode is enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supported trigger phrases and naming use a mix of Apollo Mode and sysflow terms, which can make invocation expectations unclear. <br>
Mitigation: Review accepted trigger phrases and state-file naming before installation; invoke the mode explicitly and verify status after enabling or disabling. <br>


## Reference(s): <br>
- [Apollo Mode ClawHub listing](https://clawhub.ai/nic-yuan/apollo-mode) <br>
- [Plan template](artifact/references/plan-template.md) <br>
- [Spec template](artifact/references/spec-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local mode-state file and may produce specs, plans, risk checks, verification summaries, and next-step guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
