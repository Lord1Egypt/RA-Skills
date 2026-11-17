## Description:

Use when the user has a research problem but needs theoretical foundations, conceptual lineage, or research traditions that support the problem framing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snake-fan](https://clawhub.ai/user/snake-fan)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and research-writing agents use this skill to ground a checked research problem in appropriate theoretical traditions, select supported traditions, and produce a claim-centered Theoretical Grounding Report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local research files, including private or unpublished materials.

Mitigation: Review the workspace contents and exclude sensitive materials before running the workflow.

Risk: Theory selection can overstate a research problem if generated traditions, boundaries, or evidence needs are accepted without review.

Mitigation: Review selected traditions, support boundaries, and Theory Evidence Needs before relying on the final grounding.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/04-theoretical-grounding)
- [ClawHub skill page](https://clawhub.ai/snake-fan/skills/04-theoretical-grounding)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown workspace artifacts with concise interactive prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a structured theoretical-grounding workspace and preserves user edits when resuming.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
