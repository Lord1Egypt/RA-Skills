## Description:

Provides real-time A-share market and financial news from Eastmoney for market-trend, stock-update, and finance-news queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[njbilly007-lab](https://clawhub.ai/user/njbilly007-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search A-share market and finance news, then present readable summaries with article title, content excerpt, date, and source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance search terms are sent to a third-party API.

Mitigation: Install only if sending finance queries to that service is acceptable for the intended use.

Risk: The package ships a reusable API key.

Mitigation: Rotate the exposed API key, remove it from the package and documentation, and manage credentials outside the skill.

Risk: The generic news trigger may activate for broad news requests.

Mitigation: Narrow the trigger wording before treating the skill as a routine install.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/njbilly007-lab/skills/eastmoney-news)
- [Publisher Profile](https://clawhub.ai/user/njbilly007-lab)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or JSON-derived text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries include title, content excerpt, date, and source when available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
