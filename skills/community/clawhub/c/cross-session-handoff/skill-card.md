## Description:

Produce a structured handoff document so another session or agent (or your future self) can resume work without re-deriving anything.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and project maintainers use this skill to create self-contained handoff documents when work moves between sessions, agents, or future resumptions. The handoff captures state, decisions, blockers, next actions, dependencies, and an expiry for re-verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A handoff document may accidentally include secret values or sensitive private details.

Mitigation: Review the generated handoff before sharing it and include secret names only, not secret values.

Risk: A stale handoff may be treated as current project state.

Mitigation: Set an expiry date and re-verify the handoff after the expiry or before resuming work.

Risk: An incomplete handoff can lead the next session or agent to repeat work or take the wrong next step.

Mitigation: Record concrete file paths, commands, blockers, decisions, ordered next actions, and success criteria.

## Reference(s):

- [Cross-Session Handoff on ClawHub](https://clawhub.ai/tooled-app/skills/cross-session-handoff)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown file with a YAML machine-readable block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes state, blockers, decisions, next actions, dependencies, expiry, and secret references by name only.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
