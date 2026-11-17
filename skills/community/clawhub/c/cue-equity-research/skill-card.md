## Description:

Uses Cue to run investment research workflows for equity valuation, financial statement analysis, fundamentals and risk checks, index comparison, and convertible bond risk alerts, producing source-linked research reports from public data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment research analysts use this skill to ask an agent to select a live Cue investment-research workflow, confirm credit use, run the Cue research runner, and return a source-linked research report. It is suited for public-data equity, index, financial statement, and convertible bond analysis, not as a substitute for formal due diligence or regulated advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches or updates mutable remote runner code before local execution.

Mitigation: Review the Cue runner and publisher before installation, and prefer a pinned, audited checkout for repeatable use.

Risk: The runner can read the Cue API key from ~/.cue/config.json and use paid credits.

Mitigation: Protect the Cue API key, confirm the selected workflow and credit use before running, and monitor credit consumption.

Risk: Investment research outputs may be incomplete, stale, or unsuitable for regulated decisions.

Mitigation: Keep source links in the report, verify important claims independently, and treat outputs as public-data research support rather than due diligence or financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-equity-research)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key page](https://cuecue.cn/hub/api-key)
- [Cue runner repository referenced by the skill](https://github.com/sensedeal/cue-skills)
- [Cue runner mirror referenced by the skill](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require network access, a Cue API key, local runner setup, user confirmation before consuming credits, and replay retrieval for final long-running reports.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
