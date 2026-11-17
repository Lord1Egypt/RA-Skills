## Description:

把财报收入确认五步法整理成逐条附原文引句、锚点和来源编号的登记表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

面向财报分析人员，将年报或中报中的收入确认披露整理为可回查原文的结构化登记表，覆盖合同、履约义务、交易价格、分摊及确认时点。

### Deployment Geography for Use:

China (Chinese-language financial filings)

## Known Risks and Mitigations:

Risk: ClawScan reports privacy concerns when financial documents are sent to an external parsing service.

Mitigation: Only submit documents you are authorized to share; use a local, user-supplied copy for sensitive material and review the parsing service's data handling before connecting it.

Risk: ClawScan flags network activity and local usage tracking; the package describes optional CUE service access and a first-run marker under ~/.cue-usage.

Mitigation: Review the configured service endpoint before enabling CUE_API_KEY, and inspect or remove the usage marker if local tracking is not wanted.

Risk: ClawScan reports a possible mismatch between the stated scope and calculations the instructions may allow.

Mitigation: Keep the result to a source-linked disclosure register, and check every computed ratio or progress figure against its stated method and cited numerator and denominator.

Risk: The security scan is partial because a referenced path was missing, so its evidence is incomplete; the reported verdict is suspicious, not malicious.

Mitigation: Review the complete package, including the missing referenced path, before installation or before supplying credentials.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/huhoo/skills/cue-cn-revenue-recognition-cn)
- [CUE MCP Catalog](https://cuecue.cn/api/mcp-catalog)
- [CUE MCP Guide](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader Guide](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown register with quoted filing text, anchors, source IDs, gaps, and basis notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps conclusions tied to cited disclosure; authenticity, fraud, forecasting, ratings, and investment decisions remain for human review.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
