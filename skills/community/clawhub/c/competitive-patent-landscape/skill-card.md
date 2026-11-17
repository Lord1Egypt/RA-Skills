## Description:

This skill helps an agent generate Chinese-language HTML competitive patent landscape reports by retrieving and analyzing recent global patent activity across competitors, technology routes, and geographic markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External business, product, and patent strategy teams use this skill to compare competitor patent activity and identify product strategy signals, geographic focus, technology trends, and opportunity windows. It is intended for competitive strategy reporting, not patent infringement or freedom-to-operate analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated patent conclusions may be mistaken for legal, infringement, or freedom-to-operate analysis.

Mitigation: Use the report as competitive strategy input and have qualified patent or legal reviewers check conclusions before external or high-stakes use.

Risk: Patent analysis depends on a user-authorized Zhihuiya/PatSnap MCP service and top-k patent samples, so missing authorization or limited samples can skew the report.

Mitigation: Confirm MCP access before use, disclose the sampling basis in reports, and review cited patents and search coverage before sharing findings.

## Reference(s):

- [ClawHub skill page: competitive-patent-landscape](https://clawhub.ai/yuanzhian-patsnap/skills/competitive-patent-landscape)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [Report Template Reference](artifact/references/REPORT_TEMPLATE.md)
- [Patent Search Strategy Reference](artifact/references/SEARCH_STRATEGY.md)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [HTML report with Chart.js visualizations and concise setup guidance when patent data tools are unavailable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the report to @session/output/<client_name>_patent_landscape.html when the required patent MCP service is configured.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
