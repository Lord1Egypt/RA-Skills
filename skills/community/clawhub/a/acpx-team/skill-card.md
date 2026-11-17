## Description:

Multi-agent collaboration and task delegation via the Agent Client Protocol (ACP) using acpx for teams formed from Claude Code, Codex, OpenCode, Gemini, Cursor, Copilot, and other ACP-compatible agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[csuwl](https://clawhub.ai/user/csuwl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate ACP-compatible coding agents for parallel reviews, security audits, architecture discussions, implementation delegation, and consensus-building workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates coding work to multiple agents and may encourage high-impact execution modes.

Mitigation: Use default, plan, deny-all, or narrowly scoped read approval unless running in a disposable branch, sandbox, or CI runner with minimal credentials.

Risk: The artifact recommends mutable global package installation with latest versions.

Mitigation: Verify package names and publishers, pin versions where possible, and install only when multi-agent coding delegation is intended.

Risk: Persistent sessions and temporary files can retain sensitive project context.

Mitigation: Use private temporary directories and clean up or close sessions after collaboration workflows complete.

## Reference(s):

- [Role Definitions & Team Presets](references/roles.md)
- [Collaboration Protocols](references/protocols.md)
- [ClawHub skill page](https://clawhub.ai/csuwl/skills/acpx-team)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include multi-agent role assignments, protocol steps, session commands, and permission posture recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
