## Description:

Ctxkeeper records, searches, summarizes, and exports timestamped local context entries for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep local operational notes across categories, search previous entries, view recent activity, and export logs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local logging may capture sensitive notes, tokens, customer data, or private conversation context.

Mitigation: Use only for non-sensitive local notes and avoid recording secrets, tokens, customer data, or private transcripts.

Risk: Retention and deletion controls are not clearly documented for the stored context logs.

Mitigation: Review the data directory before use and add or require clear prune and delete procedures before handling sensitive workflows.

Risk: Local log and export files may be readable by other local users if file permissions are too broad.

Mitigation: Enforce private permissions on ~/.local/share/ctxkeeper and generated log or export files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/ctxkeeper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the bundled shell tool is executed, it can write local log and export files under ~/.local/share/ctxkeeper.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
