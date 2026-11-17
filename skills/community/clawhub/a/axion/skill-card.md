## Description:

Forecast the probability of a future event with the Axion API. Use when asked the odds, likelihood, or a prediction for an uncertain or future event.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternis](https://clawhub.ai/user/eternis)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and analysts use Axion to request research-backed probabilistic forecasts for uncertain future events, deals, scenarios, markets, geopolitics, product launches, and similar questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecast questions and related context are sent to Axion using the user's API key.

Mitigation: Use the skill only when the user is comfortable sharing that information with Axion, and never print or hard-code the API key.

Risk: The API reference includes account actions such as public sharing, deletion, stopping forecasts, listing account history, and purchasing credits.

Mitigation: Require separate explicit confirmation before performing those actions.

Risk: Forecast API usage consumes prepaid credits and can fail when the account has no balance.

Mitigation: Check for sufficient credits before starting a forecast and explain that API usage is prepaid.

## Reference(s):

- [Axion API reference](references/axion-api.md)
- [Axion documentation](https://axion.eternis.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, API Calls]

**Output Format:** [Markdown with inline bash commands and summarized forecast probabilities, confidence intervals, resolution dates, and reasoning.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AXION_API_KEY and curl; forecast requests run asynchronously and should be polled with backoff until completed or failed.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
