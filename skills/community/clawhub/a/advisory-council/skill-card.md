## Description:

Runs a real-time multi-advisor market analysis using live prices to deliver a consensus trading report with actionable insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryandeangraves](https://clawhub.ai/user/ryandeangraves)

### License/Terms of Use:


## Use Case:

Developers and market-analysis users use this skill to run a five-advisor crypto market council that fetches live prices, compares bullish, bearish, technical, risk, and contrarian views, and summarizes consensus, dissent, verdict, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires running an unreviewed local Python script outside the reviewed package.

Mitigation: Install only when the local script is controlled and trusted; prefer a release that bundles the script, pins its integrity, and requests confirmation before execution.

Risk: The script may make live network and model calls while running under the agent's local permissions.

Mitigation: Run it only in an environment where those calls and permissions are acceptable, and report actual execution errors instead of fabricating output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryandeangraves/skills/advisory-council)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown report with shell commands and action-oriented market-analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live market data, advisor bullet points, consensus, dissent, verdict, confidence level, and action items.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
