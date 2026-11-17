## Description:

Claude Code+OMC orchestration: keep this session as decision maker/integrator; for non-trivial work prefer bounded available agents for search, reading, research, testing, review, and mutually exclusive writes. Preserve confirmation gates and the lowest-sufficient route.

This skill is ready for commercial/non-commercial use.

## Publisher:

[its-how](https://clawhub.ai/user/its-how)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route non-trivial Claude Code work through available OMC capabilities while keeping the primary session responsible for decisions, integration, permission gates, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using latest or unpinned installation commands can pull unexpected versions of OMC or the skill source.

Mitigation: Verify the OMC plugin and aha-orch source before installing or upgrading, and prefer pinned commits or versions.

Risk: Delegated agents may receive sensitive context or perform high-impact actions if the scope is too broad.

Mitigation: Avoid delegated agents for secrets, browser or session material, credentials, live account actions, destructive work, or other confirmation-gated work unless the scope is explicitly approved.

## Reference(s):

- [Capability Orchestration](references/capability-orchestration.md)
- [Skill repository](https://github.com/its-How/aha-orch)
- [OMC repository](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline commands and structured orchestration decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing routing guidance; it does not install OMC or persist state.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
