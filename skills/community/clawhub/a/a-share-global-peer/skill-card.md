## Description:

Finds overseas listed peer companies for A-share companies by matching similar products or services and producing comparison reports with market-share context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agents use this skill to identify overseas listed companies comparable to A-share companies and produce Chinese peer-comparison reports with product overlap, market position, and sourced market-share data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted company names in documented shell commands could execute unintended commands.

Mitigation: Pass company names as argument-array values or apply proper shell escaping, and review commands before execution.

Risk: Peer rankings and market-share data can become stale or incomplete.

Mitigation: Verify market-share figures against current sources and clearly label uncertain or estimated data in the report.

## Reference(s):

- [Global Industry Leaders Reference Table](references/global_leaders_reference.md)
- [ClawHub skill page](https://clawhub.ai/laigen/skills/a-share-global-peer)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Chinese Markdown comparison report with source labels; helper script output may be JSON or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current source verification for market-share figures and can fall back to recommended web searches when optional APIs are unavailable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
