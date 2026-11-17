## Description:

Agent Registry helps Claude Code discover and load specialized agents on demand through a local registry, search commands, and an automatic prompt hook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matrixy](https://clawhub.ai/user/matrixy)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to index Claude Code agents, search for relevant agents by task intent, and load selected agents only when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic prompt hook locally checks most prompts against the agent registry and may add agent suggestions to context.

Mitigation: Install only if this behavior is acceptable, and review suggested agents before following loaded instructions.

Risk: Agent metadata or loaded agent files can introduce untrusted or misleading instructions into the working context.

Mitigation: Review migrated agent files as trusted content and scan the skill before deployment.

Risk: Migration with --move can alter the original agent file locations.

Mitigation: Keep backups and use the default copy mode unless moving files is intentional.

Risk: Telemetry can make outbound requests when explicitly enabled.

Mitigation: Keep telemetry unset, or set AGENT_REGISTRY_NO_TELEMETRY or DO_NOT_TRACK when telemetry is not acceptable.

Risk: Floating install commands can resolve to a different package version over time.

Mitigation: Prefer pinned install or update commands for deployment.

## Reference(s):

- [Agent Registry on ClawHub](https://clawhub.ai/matrixy/skills/agent-registry)
- [README](README.md)
- [Agent Registry v2.0.1 release notes](docs/releases/v2.0.1.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-formatted CLI or hook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit command output, agent instruction text, registry metadata, and additionalContext suggestions.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
