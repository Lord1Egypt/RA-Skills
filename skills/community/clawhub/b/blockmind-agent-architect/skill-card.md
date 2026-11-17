## Description:

Interactive consultant that helps developers design agent systems by walking through structured intake questions about surfaces, tools, memory, deployment, and complexity, then synthesizing architecture recommendations grounded in curated external references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philitician](https://clawhub.ai/user/philitician)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan agent systems, AI assistants, chatbots, automation workflows, and personal agent setups. It gathers requirements and returns architecture recommendations, component guidance, reading order, and open implementation questions grounded in the bundled references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Architecture recommendations may be incomplete or mismatched if the user's requirements extend beyond the bundled references.

Mitigation: Review recommendations before implementation and independently verify gaps the skill identifies as outside its curated sources.

Risk: Third-party setup commands referenced by source material may install unreviewed packages if executed directly.

Mitigation: Verify the package and publisher, and pin a reviewed version before allowing an agent to run `npx nia-wizard@latest` or similar setup commands.

## Reference(s):

- [AgentSearch Manifesto](references/agentsearch-manifesto.md)
- [Claude Code Memory & CLAUDE.md](references/claude-code-memory-docs.md)
- [OpenAI Codex Customization](references/codex-customization-docs.md)
- [Fly/Tigris Object Storage Documentation](references/fly-tigris-docs.md)
- [Fumadocs](references/fumadocs-docs.md)
- [Karpathy LLM Wiki](references/karpathy-llm-wiki.md)
- [Nia Documentation](references/nia-docs.md)
- [OpenClaw Documentation](references/openclaw-docs.md)
- [Source Map](references/source-map.md)
- [ClawHub skill page](https://clawhub.ai/philitician/skills/blockmind-agent-architect)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Analysis, Configuration]

**Output Format:** [Markdown prose with headings, bullet lists, inline file references, and optional code or command snippets when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory recommendations should cite bundled reference files and flag gaps when the curated sources do not cover a requirement.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
