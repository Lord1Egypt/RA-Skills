## Description:

Group related tickers into named investment themes with AI-generated summaries and news keyword monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to create, update, delete, and inspect AlphaGBM investment themes made from ticker baskets and news keywords. It supports theme-level summaries, aggregated movers, and matched news views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Theme names, tickers, descriptions, and news keywords are sent to AlphaGBM through a remote API.

Mitigation: Use the skill only with data you are comfortable sharing with AlphaGBM, and configure the API key only in trusted agent environments.

Risk: Update and delete actions can affect the wrong theme when a request uses generic terms such as theme or basket.

Mitigation: Resolve the intended theme by name or ID and confirm it before performing updates or hard deletes.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API Base URL](https://alphagbm.zeabur.app)
- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/alphagbm-theme-research)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries, tabular text, JSON request and response examples, and API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALPHAGBM_API_KEY and may use ALPHAGBM_BASE_URL; tier limits may cap theme creation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
