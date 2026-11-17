## Description:

将财报和重组公告中的债务重组披露整理成逐条可追溯到原句与来源的登记表，并明确标出缺失项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财报分析人员可用它从年报、半年报或重组公告中登记重组方式、相关金额和条款，并为每项保留原句与出处。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The retrieval and parsing workflow may send financial documents to an external parsing service.

Mitigation: Before sending a document, confirm that your organization's data rules and the service's handling terms allow it; do not submit confidential material when they do not.

Risk: ClawScan flags undisclosed usage tracking; the artifact documents a first-run local marker under ~/.cue-usage.

Mitigation: Tell users about the marker before installation, inspect it if needed, and remove ~/.cue-usage if it should not be retained.

Risk: ClawScan flags external tool-discovery behavior that contacts a tool catalog and lists available tools.

Mitigation: Review the catalog destination and whether discovery is needed before enabling that workflow; skip discovery when it is not needed.

Risk: Security analysis was partial and does not establish that all artifact behavior is safe.

Mitigation: Review the artifact and complete a security scan before installation.

## Reference(s):

- [CUE MCP catalog](https://cuecue.cn/api/mcp-catalog)
- [CUE MCP setup](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown note with quoted source text, location anchors, and source IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One structured debt restructuring record; missing disclosures are explicitly marked, and amounts and classifications are transcribed from the cited disclosure.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
