## Description:

Runs Cue-powered U.S. equity and macro research workflows that gather public disclosures, financials, risk factors, insider activity, institutional holdings, macro indicators, fiscal liquidity data, SEC filings, industry signals, and research funding trends into reviewable research drafts with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Investment researchers, analysts, and agents use this skill to run Cue scenarios for U.S. stock and macro research, including company due diligence, 13F tracking, COT positioning, inflation and labor monitoring, SEC filing monitoring, industry scans, and federal research funding analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download or update external runner code and execute it with access to the local Cue API key.

Mitigation: Use a preinstalled, pinned, verified runner when possible, and review the Cue/Sensedeal runner source before allowing installation, updates, or execution.

Risk: Running the workflow can spend Cue credits.

Mitigation: Require explicit user confirmation for the selected buddy, subject, and credit spend before execution.

Risk: Research drafts based on public data can be incomplete or unsuitable as final investment, legal, underwriting, or diligence advice.

Mitigation: Preserve source links, avoid unsupported claims, and require analyst review before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-us-research)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue runner source repository](https://github.com/sensedeal/cue-skills)
- [Cue runner source mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Cue API key, user confirmation before spending credits, and a Cue runner installed from a trusted source.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
