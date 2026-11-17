## Description:

Content repurposer: turn one blog post, video, or podcast into social posts, email newsletters, and threads on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, founders, and content teams use this skill to convert long-form content into platform-ready social posts, email snippets, quote pull-outs, and summary bullets. It supports review and refinement before optional scheduling or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private drafts, local file paths, or authenticated URLs may expose sensitive source content to the agent environment.

Mitigation: Provide only content approved for processing, and avoid private or logged-in URLs unless the agent environment is trusted.

Risk: Generated marketing copy may be inaccurate, off-brand, or misleading if published without review.

Mitigation: Review and approve generated posts, threads, captions, and email snippets before scheduling or publication.

Risk: Connected posting or calendar tools could schedule or publish content after approval.

Mitigation: Limit integration permissions and require explicit user approval before posting or scheduling any generated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-content-repurposer)
- [DoctorClaw website](https://www.doctorclaw.ceo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with platform-specific content sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces multiple reviewed marketing assets from one source input.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
