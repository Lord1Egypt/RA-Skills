## Description:

Turns one Chinese tender or award notice into eight verbatim disclosure items with source anchors, marking missing details explicitly and keeping win odds and revenue judgments for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and procurement teams use this skill to extract and compare the wording of a single tender disclosure chain, including award amounts and source locations. It does not provide bidding advice or predict outcomes.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious: installation sources are unpinned, some external service checks do not match the tender-disclosure task, and attachment processing may send documents to a third party without clear disclosure.

Mitigation: The scanner recommends against installation. If considering use, review external-service and attachment-processing steps, do not submit sensitive documents or credentials, and verify the installer and source revision. The incomplete scan does not establish that the skill is safe.

## Reference(s):

- [Bid disclosure chain reference](references/bid-chain.md)
- [Cue data channel configuration](https://cuecue.cn/hub/mcp)
- [Cue attachment reader configuration](https://cuecue.cn/hub/omni-reader)
- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-bid-panorama-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown with five sections, verbatim quotes, source anchors, and explicit missing-data entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One disclosure card per tender; eight named items remain present even when evidence is missing.]

## Skill Version(s):

0.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
