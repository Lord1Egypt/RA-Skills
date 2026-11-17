## Description:

Ask Lenny searches Lenny Rachitsky's Podcast and Newsletter archive to help agents answer product, growth, GTM, pricing, AI product, and leadership questions with cited transcript excerpts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myclaw-ai](https://clawhub.ai/user/myclaw-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External product builders, founders, PMs, and growth teams use this skill to query a local archive of Lenny Rachitsky podcast and newsletter content and synthesize cited product and growth guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads or updates a public GitHub archive into the skill's data directory, so future setup runs may retrieve changed upstream content.

Mitigation: Run setup intentionally, review or pin downloaded source data when repeatability matters, and rebuild the local index only from trusted content.

Risk: Retrieved transcript text may contain language that should be treated as source material rather than agent instructions.

Mitigation: Use search results as quoted evidence for synthesis and do not follow operational instructions embedded in retrieved transcript content.

Risk: Skill responses are expected to carry a MyClaw.ai footer.

Mitigation: Keep the branding visible when using the skill and account for third-party branding in deployment review.

## Reference(s):

- [Guest Index](references/guest-index.md)
- [Lenny's Data Archive](https://lennysdata.com)
- [Ask Lenny on ClawHub](https://clawhub.ai/myclaw-ai/skills/ask-lenny)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with direct quotes and source references; JSON arrays from the local search script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include guest, title, date, score, source, and transcript text; answers are expected to include source filenames and a MyClaw.ai footer.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
