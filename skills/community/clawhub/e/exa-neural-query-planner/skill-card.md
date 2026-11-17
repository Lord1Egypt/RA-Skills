## Description:

Plan Exa neural web searches before calling any Exa wrapper; craft queries, pick categories, set domain and date filters, define fallbacks, and decide when Exa beats keyword search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruti3](https://clawhub.ai/user/ruti3)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and agents use this skill to prepare executor-ready Exa search plans before another tool performs the actual search. It helps select neural versus keyword search, category and freshness settings, domain filters, fallback queries, and stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could mistake the plan for live Exa or web results.

Mitigation: Treat the output as a planning artifact only; require a separate executor to run searches and cite actual results before presenting findings.

Risk: Users could paste API keys or other secrets into the planning prompt.

Mitigation: Do not ask for, echo, or store EXA_API_KEY or other credentials; keep credential handling outside this skill.

Risk: The plan could recommend unnecessarily expensive search settings or routes that violate access restrictions.

Mitigation: Use conservative defaults for deep search and result counts, justify filters, and avoid paywalls, login-only content, and site-terms violations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruti3/skills/exa-neural-query-planner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown search plan with a table, natural-language queries, YAML API hints, fallback queries, quality checks, and stop or escalation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only planning output; it does not execute searches, call Exa, access the network, store credentials, or handle API keys.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
