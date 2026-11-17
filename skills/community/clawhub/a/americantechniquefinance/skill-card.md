## Description:

Analyzes US-listed technology giants and produces sourced investment and competitive analysis with charts, valuation tables, risk matrices, and dated financial evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttggjj](https://clawhub.ai/user/ttggjj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, students, and agent operators use this skill to turn requests about Apple, Microsoft, Nvidia, Amazon, Alphabet, Meta, Tesla, or comparable US-listed technology companies into sourced company analysis. The skill supports business-model review, market-share analysis, growth outlook, moat assessment, financial-report interpretation, stock-trend context, peer valuation, and risk review without providing personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial figures, stock prices, analyst targets, and market-share data can become stale quickly.

Mitigation: Require dated sources for every figure and ask users to verify source dates before acting on the analysis.

Risk: Generated reports could be mistaken for personalized investment advice.

Mitigation: Frame stock-trend and valuation content as research context and include a clear analysis-only disclaimer.

Risk: Reports may default to Chinese headings, which can reduce clarity for some audiences.

Mitigation: Tell the agent or reviewer to localize headings and labels when the target audience requires another language.

## Reference(s):

- [US Tech Giant Analyst - Deep Analysis Framework](references/analysis-framework.md)
- [SEC EDGAR Company Search](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=[TICKER])
- [ClawHub Skill Page](https://clawhub.ai/ttggjj/skills/americantechniquefinance)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report plus self-contained HTML report with inline CSS or SVG charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires dated public sources for figures, explicit disclosure of missing data, and an analysis disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
