## Description:

Provides portfolio risk metrics, stress testing, and position management advice using VaR, CVaR, volatility, Beta, Sharpe ratio, and Kelly-style position sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbabyzs](https://clawhub.ai/user/gbabyzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to calculate investment risk indicators, run stress-test style analyses, and produce position-sizing guidance for portfolio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risk metrics and position-sizing output may be mistaken for personalized financial advice.

Mitigation: Present outputs as analytical aids and require human review before trading, investment, or portfolio decisions.

Risk: Runtime behavior can change if Python dependencies are installed without version pinning.

Mitigation: Install the skill in an isolated Python environment and pin akshare, pandas, numpy, and scipy versions for reviewed deployments.

Risk: Chinese-language user-facing text may be misunderstood by users who do not read Chinese.

Mitigation: Route outputs to users or reviewers who can read Chinese, or translate and validate the guidance before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbabyzs/skills/aigc-risk-assessment)
- [Publisher profile](https://clawhub.ai/user/gbabyzs)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell command snippets; callable functions return Python dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language risk metrics and position-sizing guidance; depends on akshare market data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
