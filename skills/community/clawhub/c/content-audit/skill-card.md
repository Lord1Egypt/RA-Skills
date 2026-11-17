## Description:

Audits an existing social media account by reviewing provided native analytics and prior content, then producing a signal-based keep, kill, refresh triage with pillar, voice, profile, and roadmap recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brands, and social media teams use this skill to assess what is working in an existing account before replanning. It turns roughly 90 days of user-provided performance data and content history into an action-oriented audit roadmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit findings may be wrong if the user supplies incomplete, stale, or misread analytics.

Mitigation: Use native analytics and user-provided data as the input source, avoid fabricating metrics, and treat thin data as a structural audit with a later performance revisit.

Risk: Deleting or changing posts based only on vanity metrics can remove evergreen value, search value, or useful engagement history.

Mitigation: Score content on saves, shares, replies, and goal-mapped KPIs; refresh before killing content and require human approval for any deletion.

Risk: Profile or strategy recommendations may affect public brand presentation.

Mitigation: Review recommended deletions, profile edits, and voice changes before acting, especially where edits must be made directly in platform apps.

## Reference(s):

- [ClawHub Content Audit Skill](https://clawhub.ai/social-media-skills/skills/content-audit)
- [Content audit 2026 - verified](references/content-audit-2026-reality.md)
- [Scope, the bridge role + connections](references/scope-and-connections.md)
- [The AUDIT framework - find the signal under the busy-ness](references/the-audit-framework.md)
- [Triage rules, scorecard + two worked examples](references/triage-and-recipes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a retrospective audit roadmap; it recommends changes but does not execute account actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
