## Description:

Gives agents persistent, structured local memory for recalling and updating client, project, trade, and knowledge records across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to persist useful context across sessions, including client interactions, project decisions, trade outcomes, follow-up dates, and accumulated knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores client, project, trade, and knowledge records that may contain sensitive personal or business data.

Mitigation: Define retention and deletion procedures before use, and avoid storing credentials, payment data, raw sensitive messages, or other unnecessary confidential data.

Risk: Memory is broadly reloaded across sessions and may be stale, incomplete, or unsuitable as an authoritative source.

Mitigation: Treat recalled memory as reference material and verify important facts before acting on them.

Risk: The security review notes that removal requests are handled as archiving rather than deletion.

Mitigation: Use a separate deletion workflow for forget or removal requests, and do not treat archived records as proof that data was deleted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/agent-memory-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/georges91560)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text with JSON and Markdown memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and retrieves local workspace memory records; evidence declares no network requests.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
