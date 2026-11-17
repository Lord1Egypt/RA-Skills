## Description:

Records the structure of conversations where ideas evolve, branch, get rejected, pivot, or combine, saving structural shifts as local JSON trees that users can browse on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joncik91](https://clawhub.ai/user/joncik91)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to preserve the branching structure of brainstorming, problem-solving, and option analysis so they can revisit proposals, rejected paths, pivots, merges, and recurring concepts later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically persist short conversation-derived topics, summaries, rejection reasons, and concepts to local JSON and Markdown files.

Mitigation: Use a private trees directory, disable always-on mode for explicit invocation, and periodically review or delete stored trees for sensitive conversations.

Risk: Local tree files may expose decision structure to other users or processes if stored in a shared or broadly writable directory.

Mitigation: Store trees in a user-controlled private directory and avoid directories writable by other users.

## Reference(s):

- [Decision Topology Schema v2](references/schema.md)
- [Decision Topology ClawHub Page](https://clawhub.ai/joncik91/skills/decision-topology)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime commands emit JSON, ASCII tree text, Mermaid Markdown, and local JSON or Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; persisted text fields are length-limited and stored in a user-controlled local trees directory.]

## Skill Version(s):

1.0.6 (source: server release metadata, target metadata, and changelog, released 2026-03-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
