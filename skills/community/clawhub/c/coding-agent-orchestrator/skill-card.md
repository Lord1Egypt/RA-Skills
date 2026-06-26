## Description: <br>
Controls Varie Workstation sessions for Claude Code multi-session orchestration, including starting, resuming, dispatching to, stopping, and screenshotting local coding-agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masqueradeljb](https://clawhub.ai/user/masqueradeljb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage local Varie Workstation coding sessions from OpenClaw channels, route user requests to the right session, answer pending prompts, and share session screenshots when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad chat triggers and generic yes/no handling could accidentally approve, steer, interrupt, or expose active coding work. <br>
Mitigation: Use explicit project and session names, avoid casual yes/no replies while prompts are pending, and confirm ambiguous routing before dispatching commands. <br>
Risk: Full-screen screenshots can include unrelated windows or sensitive content. <br>
Mitigation: Prefer session-scoped screenshots and use full-screen capture only when the user explicitly requests it. <br>
Risk: The skill depends on local Varie Workstation and wctl control of coding sessions. <br>
Mitigation: Install wctl only from a trusted Varie Workstation source and use the skill only when local coding-session control is intended. <br>


## Reference(s): <br>
- [Varie Workstation](https://github.com/varie-ai/workstation) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [Coding Agent Orchestrator on ClawHub](https://clawhub.ai/masqueradeljb/coding-agent-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local session commands and screenshot delivery guidance for the requesting user's channel.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
