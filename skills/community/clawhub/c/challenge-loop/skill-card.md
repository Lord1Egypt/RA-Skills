## Description:

Challenge Loop adds manual adversarial review for judgment-containing agent outputs through inline self-refutation or an independent challenger subagent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enzowyf](https://clawhub.ai/user/enzowyf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to challenge recommendations, plans, and other judgment-heavy outputs before relying on them. It supports a fast inline critique or a deeper subagent review loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Casual review phrases may activate challenge behavior when the user expected a direct answer.

Mitigation: Use the documented skip phrases when a direct answer is desired, and reserve challenge triggers for outputs that need adversarial review.

Risk: Subagent mode can share the current request and draft with an ephemeral challenger, adding cost and latency.

Mitigation: Use inline mode for quick checks and subagent mode only when deeper review is worth the additional cost and latency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enzowyf/skills/challenge-loop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with structured critique blocks and optional challenge summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subagent mode is bounded by documented round limits, a 2000-word challenger-output breaker, and a 120-second timeout fallback.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
