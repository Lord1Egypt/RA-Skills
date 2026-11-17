## Description:

Guides AI coding tools through designing, implementing, and optimizing production-grade agent systems with phased architecture, tooling, permissions, context management, multi-agent coordination, MCP integration, and deployment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sofild](https://clawhub.ai/user/sofild)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide AI coding assistants through requirements confirmation, scaffold selection, and phased construction of production-ready agent systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scaffold templates may encourage broad file, network, hook, credential, or logging behavior.

Mitigation: Review generated scaffolds before use and add workspace path enforcement, network allowlists, approval gates for writes or mutating requests, secret redaction, and safe credential storage.

Risk: Users may copy older scaffold implementations directly instead of adapting the v3 abstract guidance to their environment.

Mitigation: Use the v3 phase guidance and safer professional or enterprise skeletons as design inputs, then generate environment-specific implementations with explicit security checks.

## Reference(s):

- [Agent Harness Engineer README](README.md)
- [Agent Harness Engineer Skill Definition](SKILL.md)
- [Phase 1: Project Initialization](references/01-phase-init.md)
- [Phase 2: LLM Abstraction](references/02-phase-llm.md)
- [Phase 3: Tool System](references/03-phase-tools.md)
- [Phase 4: Agent Core Loop](references/04-phase-agent-loop.md)
- [Phase 5: Context Management](references/05-phase-context.md)
- [Phase 6: Permissions and Security](references/06-phase-permissions.md)
- [Phase 7: Productionization](references/07-phase-production.md)
- [Technology Stack Selection](references/11-technology-stack.md)
- [Sandbox Design](references/12-sandbox-advanced.md)
- [Session Design](references/13-session-design.md)
- [Observability](references/14-observability.md)
- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code, shell command, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tailored agent-system plans and project scaffolding guidance rather than a fixed runtime artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
