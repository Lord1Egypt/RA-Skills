## Description:

CueCue Deep Research helps agents run financial research on market conditions, industry trends, company fundamentals, policy impacts, competitors, public sentiment, regional markets, and geopolitical risks, then produce structured, data-driven research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xfgong](https://clawhub.ai/user/xfgong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial professionals use this skill to ask an agent for market, company, industry, policy, competitor, public-sentiment, regional-market, or geopolitical research. The skill routes the request through the CueCue CLI and saves a Markdown research report for decision support, strategy planning, or market insight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial research prompts, company details, and related context may be sent to the CueCue service through an external CLI.

Mitigation: Install only if CueCue is trusted for the intended data, and avoid confidential prompts unless that use is approved.

Risk: The skill uses an API key and can run research jobs in the background.

Mitigation: Use a scoped CueCue API key that can be rotated, and prefer a local or isolated install.

Risk: The CLI writes persistent Markdown reports to the configured output path.

Mitigation: Review report destinations before execution and store generated reports according to the sensitivity of the research content.

## Reference(s):

- [CueCue homepage](https://cuecue.cn)
- [ClawHub skill page](https://clawhub.ai/xfgong/skills/cuecue-deep-research)
- [Publisher profile](https://clawhub.ai/user/xfgong)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report files with agent-facing command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the cue CLI, Node.js, and CUECUE_API_KEY; reports are written to a user-specified Markdown output path.]

## Skill Version(s):

1.1.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
