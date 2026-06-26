## Description: <br>
Interactive consultant that helps developers design agent systems by walking through structured intake questions about surfaces, tools, memory, deployment, and complexity, then synthesizing architecture recommendations grounded in curated external references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philitician](https://clawhub.ai/user/philitician) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan agent systems, AI assistants, chatbots, automation workflows, or personal agent setups. It gathers requirements across user surfaces, agent topology, memory, tools, deployment, knowledge bases, and complexity tolerance, then returns a grounded architecture recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture recommendations may lead users toward downstream systems that handle private data, such as memory stores, local sync, API integrations, or cloud storage. <br>
Mitigation: Review recommendations before implementation and apply project-specific privacy, access-control, and data-handling requirements to any downstream system. <br>
Risk: The skill provides planning guidance from curated references but does not execute code or validate the resulting implementation. <br>
Mitigation: Treat outputs as design guidance and verify implementation choices, security controls, and operational assumptions before deployment. <br>


## Reference(s): <br>
- [AgentSearch Manifesto](references/agentsearch-manifesto.md) <br>
- [Claude Code Memory & CLAUDE.md](references/claude-code-memory-docs.md) <br>
- [OpenAI Codex Customization](references/codex-customization-docs.md) <br>
- [Fly/Tigris Object Storage Documentation](references/fly-tigris-docs.md) <br>
- [Fumadocs](references/fumadocs-docs.md) <br>
- [Karpathy LLM Wiki](references/karpathy-llm-wiki.md) <br>
- [Nia Documentation](references/nia-docs.md) <br>
- [OpenClaw Documentation](references/openclaw-docs.md) <br>
- [Source Map](references/source-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Architecture overview, component recommendations, suggested reading order, and open questions grounded in bundled reference files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
