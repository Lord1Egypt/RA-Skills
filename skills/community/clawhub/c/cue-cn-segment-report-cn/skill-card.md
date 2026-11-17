## Description:

Reads annual-report segment disclosures into a source-linked register covering segment identification, financial figures, inter-segment transactions, and reconciliation to consolidated statements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and finance teams use this Chinese-language skill to turn annual-report segment disclosures into a seven-section Markdown ledger with quoted evidence, page or table anchors, and explicit gaps. It keeps disclosed figures distinct and leaves business valuation and investment judgments to a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External document processing may share supplied annual reports or other files.

Mitigation: Review the processing service's data handling terms and avoid sending sensitive documents unless that use is approved.

Risk: MCP discovery may send CUE_API_KEY to the endpoint selected for the connection.

Mitigation: Check the live catalog and endpoint before connecting, and provide the key only to the intended service.

Risk: Running the skill writes a local usage marker under ~/.cue-usage/.

Mitigation: Account for this marker in local privacy and cleanup practices.

## Reference(s):

- [CUE MCP configuration](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Seven-section Markdown ledger with source quotes, anchors, and references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing items are listed explicitly; computed values are marked and show their source figures.]

## Skill Version(s):

0.1.0 (source: release evidence, frontmatter, changelog, released 2026-11-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
