## Description:

This skill helps agents run Cue deep research for market capitalization management, including strategy planning, M&A target discovery, equity incentive design, market-cap monitoring, company overviews, health diagnosis, and private-company valuation monitoring using public data with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, finance teams, and capital markets practitioners use this skill to route a company or market-cap-management question to the relevant Cue research workflow and return a sourced research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can clone or update and execute mutable remote Cue runner code outside the reviewed package.

Mitigation: Use a pinned and reviewed cue-skills runner version, inspect updates before execution, and install only when the Sensedeal/Cue repository is trusted.

Risk: The runner uses a Cue API key and may spend Cue credits.

Mitigation: Require explicit user confirmation before each paid run, keep the API key in the Cue configuration, and monitor credit usage.

Risk: Generated reports rely on public data and may not be sufficient for due diligence, legal, underwriting, or investment decisions.

Mitigation: Review source links, validate material claims independently, and route high-stakes decisions through qualified professional review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-market-cap-mgmt)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key setup](https://cuecue.cn/hub/api-key)
- [Sensedeal Cue skills runner](https://github.com/sensedeal/cue-skills)
- [Sensedeal Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and sourced research report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Cue API key, live Cue playbook availability, and explicit user confirmation before spending Cue credits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
