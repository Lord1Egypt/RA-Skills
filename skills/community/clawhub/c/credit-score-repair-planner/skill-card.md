## Description:

Use when repairing or building credit: decodes the 5 FICO factors for a specific profile, plans statement-date utilization timing (AZEO), writes validation/623/goodwill dispute letters, and models the score impact of payoffs, new accounts, and derogatory age-off dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users planning credit repair or building credit can use the skill to understand profile-specific score factors, plan utilization timing and derogatory-item timelines, and draft dispute or goodwill letters. It provides directional estimates rather than exact score predictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credit-profile and letter files may contain sensitive personal or financial information.

Mitigation: Protect profile and letter files and write drafts to a dedicated output directory.

Risk: Calculated payment dates may not account for weekends or holidays, and statement days above 28 are clamped.

Mitigation: Independently confirm payment dates with the issuer before acting.

Risk: Draft letters may contain legal citations or default factual statements that do not fit a user's circumstances.

Mitigation: Review every letter, including its citations and factual statements, before mailing.

## Reference(s):

- [FICO Mechanics](references/fico-mechanics.md)
- [ClawHub Skill Release](https://clawhub.ai/voronindenis5/skills/credit-score-repair-planner)

## Skill Output:

**Output Type(s):** [Analysis, Text, Files, Guidance]

**Output Format:** [Console text report and plain-text letter drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized to a supplied JSON credit profile; score changes are directional estimates, not predictions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
