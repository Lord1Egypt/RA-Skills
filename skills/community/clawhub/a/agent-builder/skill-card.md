## Description: <br>
Builds high-performing OpenClaw agents end-to-end by guiding persona, operating rules, guardrails, autonomy, memory, and workspace file generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and advanced users use this skill to design new OpenClaw agent workspaces or improve existing agents. It helps generate tailored workspace files, guardrails, heartbeat guidance, memory posture, and acceptance test scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent instructions may grant broader autonomy than intended or omit needed safety boundaries. <br>
Mitigation: Review AGENTS.md and SOUL.md before use, retain ask-before-destructive and ask-before-outbound-message rules, and choose conservative autonomy unless broader autonomy is intentional. <br>
Risk: Generated memory and heartbeat files may capture sensitive information or trigger unnecessary recurring work. <br>
Mitigation: Keep memory free of secrets, review MEMORY.md and daily memory entries before use, and leave HEARTBEAT.md empty until heartbeat behavior is explicitly needed. <br>


## Reference(s): <br>
- [Agent Builder ClawHub page](https://clawhub.ai/plgonzalezrx8/agent-builder) <br>
- [OpenClaw agent workspace](references/openclaw-workspace.md) <br>
- [OpenClaw agent file templates](references/templates.md) <br>
- [Agent Architecture Patterns](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with generated workspace file content, checklists, and scenario prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file contents for IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, memory entries, and TOOLS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
