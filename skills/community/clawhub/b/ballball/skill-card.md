## Description:

BallBall is a football match betting prediction skill that collects Nowscore match data, applies a five-step quantitative analysis framework, and outputs betting recommendations with predicted scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[owaio](https://clawhub.ai/user/owaio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use BallBall to gather football match odds and team context, run quantitative betting analysis, and produce pre-match picks, predicted scores, and post-match review notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save football betting requests, match IDs, predictions, recommendations, and learned model changes across sessions.

Mitigation: Review the skill before installation and disable or manually control memory writes where the runtime allows it.

Risk: The skill uses external Nowscore lookups for match analysis.

Mitigation: Use the skill only when external match lookups are acceptable for the environment and avoid submitting sensitive context with match requests.

Risk: Betting predictions and recommendations may be wrong or misleading.

Mitigation: Treat outputs as decision-support analysis, verify odds and match data independently, and follow applicable betting rules and restrictions.

## Reference(s):

- [Data Collection Guide](references/data-collection.md)
- [Prediction Framework](references/prediction-framework.md)
- [Post-Match Review & Learning Framework](references/review-framework.md)
- [BallBall ClawHub Page](https://clawhub.ai/owaio/skills/ballball)
- [Nowscore Match Analysis](https://m.nowscore.com/Analy/Analysis/{match_id}.htm)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Concise text or detailed Markdown/HTML report with odds tables, probability calculations, betting recommendations, predicted scores, and review summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist match history and optimized prediction weights to local memory files after predictions or post-match reviews.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
