## Description: <br>
The operating system layer for AI agents that routes goals to the right skills and executes with checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contrario](https://clawhub.ai/user/contrario) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AGENT-OS as an instruction-only orchestration layer to route goals to appropriate skills, checkpoint multi-step work, and verify results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad workflow orchestration can influence multi-step agent behavior beyond the immediate prompt. <br>
Mitigation: Invoke it only when central routing, checkpoints, or multi-step coordination are needed, and keep final approval over high-impact actions. <br>
Risk: The artifact marks medical diagnosis, legal advice, and financial advice as not recommended domains. <br>
Mitigation: Avoid using the skill as the controlling workflow for those domains unless a qualified reviewer supplies the domain-specific process and approval gates. <br>


## Reference(s): <br>
- [AGENT-OS on ClawHub](https://clawhub.ai/contrario/agnt-os) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain-text agent instructions and checkpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only behavior; no file access, code execution, or external APIs are described.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
