## Description:

Creates an eight-part, source-linked summary of an A-share equity incentive plan draft, marks missing terms, and leaves calculations and participation judgments for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users reviewing A-share incentive plan disclosures can use this skill to extract eight quoted terms, compare related filings, and track missing evidence. Financial calculations, eligibility checks, and participation advice remain for human review.

### Deployment Geography for Use:

China (A-share disclosure documents)

## Known Risks and Mitigations:

Risk: ClawScan recommends against installation pending review and reports an undeclared MCP discovery workflow that sends CUE_API_KEY to a catalog-provided endpoint.

Mitigation: Review discovery and credential routing before considering installation; verify the endpoint and its handling before providing the key.

Risk: ClawScan reports unpinned installation commands and skill source, so the installed version may differ from the reviewed release.

Mitigation: Pin the installer and skill source to versions that have been reviewed.

Risk: The security evidence identifies privacy gaps and does not establish whether document parsing sends content externally or how it is handled.

Mitigation: Confirm document routing and content handling before sending plan documents through the parsing path.

## Reference(s):

- [Equity incentive plan terms reference](references/eip-terms.md)
- [Live MCP catalog](https://cuecue.cn/api/mcp-catalog)
- [MCP data leg setup](https://cuecue.cn/hub/mcp)
- [Attachment parsing setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with eight quoted clause entries, source anchors, wording comparison, missing-data list, and human-review items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quotes and figures are retained verbatim; missing items are named, and calculations or advice are left for human review.]

## Skill Version(s):

0.1.3 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
