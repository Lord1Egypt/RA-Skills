## Description:

Dazhong helps agents evaluate Dianping ratings, detect sponsored or inflated review patterns, and choose local-life merchants with clearer risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to assess Dianping restaurant and local-life listings, compare ratings and lists, identify signs of sponsored or inflated reviews, and produce practical merchant-selection guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dianping rankings, rating rules, merchant quality, and queue or booking conditions can change after the skill's guidance is applied.

Mitigation: Have the agent verify current in-app listing details, recent reviews, booking status, and platform explanations before recommending a final choice.

Risk: Restaurant preference is subjective, so reliability checks cannot guarantee that a recommended merchant will match a user's taste or occasion.

Mitigation: Frame outputs as evidence-based decision guidance, include tradeoffs and uncertainty, and align recommendations with the user's scenario, budget, and preferences.

Risk: The skill discusses inflated ratings and sponsored reviews, which could be misused to seek review manipulation tactics.

Mitigation: Keep outputs focused on detection, avoidance, and compliant merchant communication; do not provide review-farming, paid-ranking, or fake-review instructions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, analysis]

**Output Format:** [Markdown or plain text decision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, persistence, credential handling, or hidden data access is identified in the server security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
