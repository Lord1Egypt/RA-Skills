## Description: <br>
Distill finished work into the right OpenClaw knowledge layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[traceme](https://clawhub.ai/user/traceme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after completing a task to decide whether the result belongs in a daily log, experience bank, playbook, reusable skill, multiple layers, or no long-term record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may write to memory, playbooks, or skills when explicitly asked, which can influence future agent behavior. <br>
Mitigation: Review the exact target files and proposed content before allowing writes, especially under playbooks or skills. <br>
Risk: Completed-task notes can contain sensitive details or low-value noise. <br>
Mitigation: Redact sensitive details and retain only dated evidence or reusable lessons appropriate to the selected knowledge layer. <br>


## Reference(s): <br>
- [Experience Distiller Decision Rules](references/decision-rules.md) <br>
- [Distill Invocation Template](references/template.md) <br>
- [Distill Invocation Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text, Files] <br>
**Output Format:** [Markdown recommendation block with optional file writes when explicitly requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes completed-work knowledge into daily-log, experience, playbook, skill, multi, or no-op categories.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
