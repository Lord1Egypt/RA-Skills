## Description:

Runs Cue deep-research workflows for short-term market monitoring, including 24-hour catalysts, Dragon Tiger List analysis, pre-market strategy notes, intraday tape reading, sector fund-flow logic, watchlists, trading calendars, commodities, and gold-market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market researchers use this skill to select and run Cue short-term market research agents for public-data analysis, then return sourced market reports for trading-oriented review. It is intended to support analysis workflows, not to replace independent due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can clone or update mutable external Cue runner code outside the reviewed package and run it locally.

Mitigation: Install only after reviewing the Cue runner source you will execute, pin or audit the runner revision where possible, and rerun security review when the runner changes.

Risk: The external runner can use a local Cue API key and consume Cue credits.

Mitigation: Keep the Cue API key scoped to acceptable exposure, confirm credit use before each run, and monitor credit consumption after execution.

Risk: Market-research output may be incomplete, stale, or unsuitable as trading advice.

Mitigation: Treat reports as analysis drafts, preserve source links, and require independent review before using results for financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-short-term-market)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue runner repository](https://github.com/sensedeal/cue-skills)
- [Cue runner mirror](https://gitee.com/sensedeal/cue-skills)
- [Cue API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with source links and inline shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a long-running Cue research runner and should preserve returned source links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
