## Description:

查询 Datayes/通联的宏观与行业指标数据，帮助 agents search, select, and retrieve macroeconomic or industry time series such as GDP, CPI, PPI, PMI, M2, credit, rates, employment, trade, output, and prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datayes](https://clawhub.ai/user/datayes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Datayes macroeconomic and industry indicators through the bundled Python CLI, inspect candidate indicators, and retrieve selected time series data. It is intended for questions about Chinese or broader macro and industry data where the agent should report indicator name, frequency, unit, source, latest value, and recent observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Datayes bearer token could leak across HTTP redirects.

Mitigation: Use a revocable, least-privileged token and avoid running the skill until redirect handling blocks cross-origin redirects or strips Authorization on origin changes.

Risk: The skill depends on a DATAYES_TOKEN secret in the environment.

Mitigation: Keep the token out of prompts, logs, and committed files, and rotate it if exposure is suspected.

## Reference(s):

- [Datayes API spec endpoint](https://gw.datayes.com/aladdin_llm_mgmt/web/mgr/api)
- [Datayes login](https://r.datayes.com/auth/login)
- [ClawHub skill page](https://clawhub.ai/datayes/skills/datayes-macro)
- [ClawHub publisher profile](https://clawhub.ai/user/datayes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a DATAYES_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
