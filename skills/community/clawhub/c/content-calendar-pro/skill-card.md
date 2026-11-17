## Description:

Generate 7-day or 30-day social media content calendars for any niche, with post-level scoring, optional rewrites, past-performance adaptation, multi-platform output, A/B variants, CSV export, and an engagement tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, creators, and business operators use this skill to draft ready-to-schedule social media calendars tailored by niche, audience, platform, and tone. It can produce 7-day or 30-day calendars with hooks, body copy, CTAs, hashtags, quality scores, optional CSV export, and tracker templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send niche, audience, and generated-content prompts to Anthropic when the local backend is unavailable.

Mitigation: Provide an Anthropic API key only when hosted processing is acceptable, avoid sensitive prompt inputs, and prefer sandboxed execution with pinned dependencies for production use.

Risk: Local MLX and premium-feature claims may be overstated relative to the implementation.

Mitigation: Validate the required backend and selected options, such as 30-day generation, multi-platform output, CSV export, and tracker output, before relying on the skill in a production publishing workflow.

Risk: Generated marketing content for regulated or high-risk verticals may be inaccurate or unsuitable without review.

Mitigation: Review all generated posts before publication and run the included compliance check where applicable, especially for mortgage, real estate, crypto, healthcare, or financial content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/skills/content-calendar-pro)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, guidance]

**Output Format:** [Human-readable calendar text, structured JSON, and optional CSV scheduler export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include post scores, A/B hook variants, compliance-check results, and a blank engagement tracker template.]

## Skill Version(s):

1.2.1 (source: server release evidence; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
