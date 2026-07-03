## Description: <br>
Agent Harness Engineer guides AI coding tools through designing, scaffolding, and hardening production-grade AI agent systems across minimal, professional, and enterprise scales. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sofild](https://clawhub.ai/user/sofild) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent engineers use this skill to plan and generate AI agent harnesses with scale-appropriate architecture, LLM abstraction, tools, permissions, context management, observability, and deployment scaffolds. It is intended for building customized agent systems rather than copying fixed example code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward powerful file, shell, browser, network, hook, and logging behavior. <br>
Mitigation: Require explicit approval for file writes, shell, browser, and network actions, and restrict filesystem access to the active workspace. <br>
Risk: Generated network tooling or integrations may make unintended outbound requests. <br>
Mitigation: Use outbound network allowlists and SSRF protections before enabling network-capable scaffolds. <br>
Risk: Generated projects may handle OAuth tokens or other sensitive credentials. <br>
Mitigation: Keep credentials outside generated code, avoid hardcoded API keys, and use secret redaction or scanning before commits and logs. <br>
Risk: Prompt, tool input, and session logs can expose sensitive data when stored or transferred. <br>
Mitigation: Redact or minimize prompts, tool inputs, and session logs before persistence, export, or third-party transfer. <br>
Risk: A deprecated JavaScript sandbox package may be used as a security boundary. <br>
Mitigation: Do not rely on deprecated vm2 for isolation; use supported sandboxing such as workspace restrictions, containers, or stronger isolation where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sofild/agent-harness-engineer) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Phase 1: Project initialization](artifact/references/01-phase-init.md) <br>
- [Phase 2: LLM abstraction](artifact/references/02-phase-llm.md) <br>
- [Phase 3: Tool system](artifact/references/03-phase-tools.md) <br>
- [Phase 4: Agent core loop](artifact/references/04-phase-agent-loop.md) <br>
- [Phase 5: Context management](artifact/references/05-phase-context.md) <br>
- [Phase 6: Permissions and safety](artifact/references/06-phase-permissions.md) <br>
- [Phase 7: Production readiness](artifact/references/07-phase-production.md) <br>
- [Technology stack guidance](artifact/references/11-technology-stack.md) <br>
- [Advanced sandbox design](artifact/references/12-sandbox-advanced.md) <br>
- [Session design](artifact/references/13-session-design.md) <br>
- [Observability design](artifact/references/14-observability.md) <br>
- [Claude Code skills documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are tailored to the user's selected language, LLM provider, scale, sandbox posture, and observability needs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
