## Description:

A file-backed agent workflow for generating, logging, and analyzing X and LinkedIn personal-brand content using audience context, brand voice, viral formulas, and performance feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dttnpole-commits](https://clawhub.ai/user/dttnpole-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, founders, and marketing operators use this skill to plan balanced batches of posts, record drafts and publishing status, feed performance data back into local logs, and turn winning patterns into reusable content formulas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes local brand, audience, draft post, and performance-tracking files.

Mitigation: Install it only in a workspace where that information is appropriate for agent access, and review draft records and memory updates before relying on them.

Risk: Optional helper scripts inspect and initialize content-tracking files relative to the current working directory.

Mitigation: Review the scripts and run them only from the intended project directory.

Risk: Generated social content and growth analysis may affect public brand perception or conversion claims.

Mitigation: Review posts, metrics interpretations, and formula promotions before publishing or reusing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dttnpole-commits/skills/ai-personal-brand-growth-engine)
- [README.md](README.md)
- [Post record template](assets/POST_TEMPLATE.md)
- [Viral formulas library](assets/VIRAL_FORMULAS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, markdown content records, growth reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local workspace files for brand context, content logs, feedback tracking, and optional script-generated reminders.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
