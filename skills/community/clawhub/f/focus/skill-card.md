## Description:

Focus — a fast productivity tool. Log anything, find it later, export when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use Focus to record plans, time-management notes, activity history, and reviews from a local command-line workflow, then search or export entries when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Productivity entries and exports may contain sensitive information because Focus stores local plaintext history under ~/.local/share/focus/.

Mitigation: Avoid saving passwords, tokens, or highly sensitive notes; treat exported JSON, CSV, and text files as sensitive and review them before sharing or backup.

Risk: Export formatting may need review before downstream use.

Mitigation: Inspect exported JSON, CSV, or text before importing it into other tools or sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/focus)
- [BytesAgain feedback](https://bytesagain.com/feedback/)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Shell commands]

**Output Format:** [Command-line text plus JSON, CSV, or plain text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/focus/ and can export saved history.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
