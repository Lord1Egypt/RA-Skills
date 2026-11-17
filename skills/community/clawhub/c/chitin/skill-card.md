## Description:

Personality persistence for AI agents. Remember how you think, not just what happened. Structured insights that survive session restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morpheis](https://clawhub.ai/user/morpheis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Chitin to persist structured behavioral, personality, relational, principle, skill, and trigger insights across agent sessions. It helps agents retrieve compact personality context, reflect on sessions, and optionally share vetted insights through Carapace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent personality context can influence future agent behavior across sessions.

Mitigation: Install only when that persistence is desired, review stored insights periodically, and archive or update insights that no longer match intended behavior.

Risk: Embedding and search queries may send claim text or query text to a configured embedding provider.

Mitigation: Do not send secrets, credentials, private file contents, or sensitive operator context through embedding, retrieve, or similar-query workflows.

Risk: Promoting insights to Carapace can share local agent knowledge externally, and force overrides can bypass default promotion checks.

Mitigation: Review each insight before promotion, protect Carapace credentials, and avoid force overrides unless there is a deliberate and documented reason.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morpheis/skills/chitin)
- [npm package @clawdactual/chitin](https://www.npmjs.com/package/@clawdactual/chitin)
- [Project homepage](https://github.com/Morpheis/chitin)
- [Carapace shared knowledge base](https://carapaceai.com)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and documented text, Markdown, and JSON retrieval modes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval output can be budgeted for compact session context.]

## Skill Version(s):

1.4.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
