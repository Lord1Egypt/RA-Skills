## Description:

Find and evaluate the best affiliate programs to promote from openaffiliate.dev.

This skill is ready for commercial/non-commercial use.

## Publisher:

[affitor](https://clawhub.ai/user/affitor)

### License/Terms of Use:

MIT

## Use Case:

Affiliate marketers, content creators, and growth teams use this skill to discover, compare, score, and choose affiliate programs by niche, commission model, audience, and promotion platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use external web or API lookups when researching affiliate programs, which can expose private strategy details through search terms or requests.

Mitigation: Avoid providing confidential business strategy, unpublished campaign plans, or sensitive audience data unless those lookups are acceptable.

Risk: Affiliate program terms, commission rates, cookie windows, and product reputation can change after the directory data is fetched.

Mitigation: Verify commission, cookie, payout, and eligibility terms on the program's official site before making business decisions or publishing recommendations.

Risk: Broad activation wording may cause the skill to run on general promotion, niche, or product-selection questions.

Mitigation: Use explicit prompts when affiliate-program research is intended, and review recommendations before acting on them.

## Reference(s):

- [Affiliate Program Search on ClawHub](https://clawhub.ai/affitor/skills/affiliate-skills)
- [openaffiliate.dev](https://openaffiliate.dev)
- [openaffiliate.dev API](https://openaffiliate.dev/api)
- [openaffiliate.dev Data Access](references/openaffiliate-api.md)
- [Program Scoring Framework](references/scoring-criteria.md)
- [Platform-Specific Affiliate Rules](references/platform-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown recommendations with comparison tables, scorecards, next steps, and optional structured JSON fields for downstream agent use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores programs across earning potential, content potential, market demand, competition, and trust factor; recommendations may depend on live external search and API results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
