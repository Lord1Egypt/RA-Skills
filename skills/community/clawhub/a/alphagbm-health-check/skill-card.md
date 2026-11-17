## Description:

Weekly diagnostic report on a user's research knowledge base that flags stale profiles, thesis drift, and orphan pages, then returns a 0-100 health score with action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to audit an AlphaGBM research knowledge base, review stale or drifted investment research, and decide which profiles or theses need attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad requests such as 'generate a report' can be ambiguous when the skill has access to an AlphaGBM API key.

Mitigation: Confirm the user's intent before generating an on-demand report or taking follow-up actions.

Risk: Archive, delete, or refresh recommendations can affect ticker research records if acted on through related skills.

Mitigation: Require a separate confirmation for each ticker before refresh, archive, or delete actions.

Risk: Health reports may expose private research knowledge-base state through the configured AlphaGBM account.

Mitigation: Install and run the skill only with an authorized API key and share report details only in the intended user context.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/clementgu/skills/alphagbm-health-check)
- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API base URL](https://alphagbm.zeabur.app)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown health report summary with score, issue categories, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ticker-level stale profile, thesis drift, orphan page, and report freshness details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
