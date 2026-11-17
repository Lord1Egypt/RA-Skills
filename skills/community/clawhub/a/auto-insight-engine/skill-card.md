## Description:

Auto Insight Engine collects public-source signals from Hacker News, GitHub, Wikipedia, RSS, ArXiv, and extended search, then uses NVIDIA NIM analysis and trend tracking to report insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run or inspect a local public-source insight collection engine, view engine status, and review tracked trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper imports and executes engine code from an external local directory that is not included in the package.

Mitigation: Use it only where that directory is administrator-controlled, reviewed, and least-privileged before running the skill.

Risk: Insight collection and analysis may send collected data to NVIDIA NIM or write it into a knowledge base.

Mitigation: Confirm data handling, retention, and knowledge-base write permissions before enabling collection cycles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/auto-insight-engine)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON-compatible status, trend, or run result data returned to the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reviewed local engine directory before running collection cycles.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
