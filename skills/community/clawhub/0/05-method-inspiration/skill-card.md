## Description:

Use when the user has a rough problem and reads papers to collect transferable modeling ideas, architectures, training flows, optimization objectives, agent pipelines, or data construction methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snake-fan](https://clawhub.ai/user/snake-fan)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and developers use this skill to turn a rough research problem or Research Question Card into a structured library of auditable candidate methods inspired by papers. It supports method-need decomposition, targeted method search, pattern extraction, transfer mapping, and candidate-method documentation without selecting a final method design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated candidate methods are provisional inspiration and may be mistaken for a final method design.

Mitigation: Keep the output as a Method Candidate Library and require human review before committing to a method design.

Risk: The skill creates and updates Markdown research notes in the configured workspace.

Mitigation: Run it only in a project workspace where those artifacts are intended, and review file changes before relying on them.

Risk: Targeted paper search can surface weakly supported or poorly fitting method patterns.

Mitigation: Use the confirmation gates, evidence-status labels, and source URLs in the generated artifacts to review fit and support.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/05-method-inspiration)
- [ClawHub skill page](https://clawhub.ai/snake-fan/skills/05-method-inspiration)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown workspace artifacts and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates research notes under a method-inspirations workspace and preserves existing user edits when resuming.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
