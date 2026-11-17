## Description:

Maintains a workspace memory log and runs daydream cycles that traverse accumulated memories and web searches to produce ideas, observations, recommendations, questions, warnings, analogies, or hypotheses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhuckobey](https://clawhub.ai/user/jhuckobey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve meaningful session memories and periodically synthesize connections across prior work. It can produce creative ideas, questions, observations, recommendations, or warnings from stored workspace memories and selected web search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Old session logs may be summarized into persistent workspace memory files.

Mitigation: Use manual setup or tightly limit memory seeding, and inspect proposed memories before writing them.

Risk: Private memory themes may be converted into external web searches during daydream cycles.

Mitigation: Avoid using the skill in workspaces containing secrets, customer data, regulated data, or confidential project names.

Risk: Generated memory logs and idea files can preserve sensitive context beyond the original session.

Mitigation: Review Daydreams.MD, Daydreamlog.MD, and ideas/*.md after sessions and remove sensitive entries before sharing or retaining the workspace.

## Reference(s):

- [Daydreamer on ClawHub](https://clawhub.ai/jhuckobey/skills/daydreamer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-backed workspace files with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Daydreams.MD, Daydreamlog.MD, daydreamer-config.json, ideas/*.md, and temporary .daydream-session JSON files in the configured workspace.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
