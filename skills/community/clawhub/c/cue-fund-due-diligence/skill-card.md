## Description:

Analyzes publicly disclosed data for A-share equity mutual funds, covering manager history, performance attribution, style consistency, risk, holdings, fees, and fund size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Individual fund investors, advisers, and researchers use the skill to review a public equity fund's reported history, manager, style, risks, holdings, fees, and scale before making their own decisions. It does not forecast future returns or recommend market timing.

### Deployment Geography for Use:

China (A-share public equity funds)

## Known Risks and Mitigations:

Risk: The security review reports a request to share an API key and promotional steps unrelated to fund analysis.

Mitigation: Do not paste an API key into chat. Review the setup and promotional instructions, and configure any key locally only if you choose to proceed.

Risk: The security review is incomplete: a referenced local path was missing and remote repository contents were not assessed.

Mitigation: Inspect the missing path and repository contents, then complete a security review before installing or running the skill.

Risk: The report depends on disclosed fund data and an external service, so coverage and timeliness may vary.

Mitigation: Check the report's data cutoff and source links, and treat its analysis as research support rather than a forecast or individualized investment recommendation.

## Reference(s):

- [Cue Skills runner repository (GitHub; referenced by the skill)](https://github.com/sensedeal/cue-skills)
- [Cue Skills runner repository (Gitee mirror; referenced by the skill)](https://gitee.com/sensedeal/cue-skills)
- [Cue service](https://cuecue.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown due diligence report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers fund and manager profiles, performance attribution, style consistency, risk metrics, holdings, fees, and scale; includes source links and a data cutoff when available.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
