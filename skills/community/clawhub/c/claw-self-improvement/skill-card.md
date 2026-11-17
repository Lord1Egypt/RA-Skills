## Description:

Capture errors, corrections, knowledge gaps, better practices, and feature requests in `.learnings/`, then distill proven recurring patterns into `.learnings/PROMOTED.md`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-tian](https://clawhub.ai/user/paul-tian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve local learning notes about errors, corrections, knowledge gaps, better practices, and feature requests, then promote durable patterns into reusable Markdown guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent `.learnings/` files may capture sensitive operational details if users record them directly.

Mitigation: Redact tokens, passwords, private keys, customer data, request bodies, and sensitive environment details before writing entries.

Risk: Promoted entries can become durable behavior guidance even when the underlying lesson is incomplete or too specific.

Mitigation: Review `.learnings/PROMOTED.md` before relying on entries as rules, and promote only mature recurring patterns.

Risk: The bootstrap reminder changes future agent context and may be unwanted in some sessions.

Mitigation: Disable the hook and keep or delete the learning files according to retention needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paul-tian/skills/claw-self-improvement)
- [Format Reference](artifact/references/FORMAT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local `.learnings/` Markdown files when the agent follows the workflow.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
