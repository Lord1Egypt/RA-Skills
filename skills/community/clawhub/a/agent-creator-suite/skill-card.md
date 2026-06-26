## Description: <br>
Build high-performing OpenClaw agents end-to-end by designing a new agent's persona and operating rules, generating required OpenClaw workspace files, and iterating on existing agent behavior, guardrails, autonomy model, heartbeat plan, and skill roster. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced OpenClaw users use this skill to interview for requirements, generate a complete agent workspace, add practical safety guardrails, and create short acceptance tests for the resulting agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent workspace files can affect future agent behavior and persistence. <br>
Mitigation: Review generated AGENTS.md, MEMORY.md, HEARTBEAT.md, and related workspace files before using them. <br>
Risk: Memory or workspace files may accidentally include secrets or sensitive information. <br>
Mitigation: Keep credentials, tokens, session transcripts, and private configuration out of generated memory and workspace files. <br>
Risk: Heartbeat or autopilot behavior can increase autonomous activity beyond the user's intent. <br>
Mitigation: Enable heartbeat or autopilot behavior only when explicitly desired and keep heartbeat checklists short and reviewable. <br>


## Reference(s): <br>
- [OpenClaw agent workspace](references/openclaw-workspace.md) <br>
- [OpenClaw agent file templates](references/templates.md) <br>
- [Agent Architecture Patterns](references/architecture.md) <br>
- [Project homepage](https://github.com/ryan-wuxl/agent-creator-suite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with generated workspace file contents, checklists, and scenario prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or generate OpenClaw workspace files such as IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, memory/YYYY-MM-DD.md, and TOOLS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
