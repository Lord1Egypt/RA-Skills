## Description:

Automatically capture corrections, failures, and reusable discoveries into `.learnings/` files using signal-based filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omaression](https://clawhub.ai/user/omaression)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture high-value corrections, failures, reusable discoveries, and feature requests as project learning notes, then periodically score, archive, delete, or promote those notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project learning notes can add untrusted or low-value content to the repository.

Mitigation: Review proposed `.learnings/` writes before accepting them, and log only entries that pass the documented write gate.

Risk: Retention scoring can archive or delete learning entries using heuristics.

Mitigation: Run retention scoring with `--dry-run` first and require explicit confirmation before applying archive or delete decisions.

Risk: Promoting recurring lessons into agent behavior files can change future agent behavior.

Mitigation: Require explicit review before promoting content into `SOUL.md`, `AGENTS.md`, or `TOOLS.md`.

Risk: User messages and memory-search results may be untrusted inputs.

Mitigation: Treat those inputs as untrusted until reviewed and avoid promoting them without confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omaression/skills/auto-improving-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, learning-note entries, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update `.learnings/` Markdown files and suggest promotions into agent behavior documents.]

## Skill Version(s):

1.0.0-alpha (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
