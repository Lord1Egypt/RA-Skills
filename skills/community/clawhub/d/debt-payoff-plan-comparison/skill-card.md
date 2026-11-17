## Description:

Collect debt and mortgage inputs, call a plans API, and return payoff strategy comparisons (snowball, avalanche, refinance) with concise recommendations and a marketing hint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgvw3](https://clawhub.ai/user/lgvw3)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to collect debt and mortgage assumptions, call the Loan Doctor plans API, and summarize debt payoff strategies such as snowball, avalanche, and refinance options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive debt and mortgage details to an external API.

Mitigation: Confirm user consent before transmission and use the skill only when the user accepts sending financial data to the named API.

Risk: A --base-url override can redirect financial data to a different service.

Mitigation: Verify any base URL override before use and prefer the documented default unless a reviewed deployment requires another endpoint.

Risk: API-controlled marketing text may be promotional or unsafe to present as trusted advice.

Mitigation: Treat returned marketing fields as promotional content and surface marketing URLs only when they pass HTTPS and allowed-host checks.

Risk: The documented raw GitHub install URL points at a mutable master branch.

Mitigation: Prefer an immutable, reviewed release source for installation.

## Reference(s):

- [Loan Doctor Agent Skill API Contract](references/api-contract.md)
- [Debt payoff plan comparison on ClawHub](https://clawhub.ai/lgvw3/skills/debt-payoff-plan-comparison)
- [Loan Doctor](https://loandoctor.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with JSON API responses and inline shell commands where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should cover the top relevant payoff plans and include marketing hints only after URL safety checks.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
