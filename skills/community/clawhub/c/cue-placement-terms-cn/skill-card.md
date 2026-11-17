## Description:

将一份 A 股定增方案整理为附逐字引文与来源锚的十项条款卡，并明确标出缺失条款和需要人工判断的事项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users reviewing one A-share private placement proposal use this skill to extract its disclosed terms with verbatim quotations and source anchors, identify missing information, and flag investment or approval judgments for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Cue services can process source documents externally, with charges and retention terms set by the service.

Mitigation: Prefer user-supplied public text when practical; verify the HTTPS endpoints, charges, and retention terms, and authorize confidential uploads before enabling Cue.

Risk: The terms checker can miss omissions; a reproduced missing-row bypass means PASS does not establish that a card is complete or accurate.

Mitigation: Manually compare quotations and recommendations with the original disclosure, even when the checker reports PASS.

Risk: Optional downloads may contain unsafe or misleading content.

Mitigation: Review optional downloads before opening or using them.

Risk: Separate Cue implementations are outside the supplied security review.

Mitigation: Verify the specific endpoints and service terms before sending documents through those implementations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-placement-terms-cn)
- [Cue data MCP configuration](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown terms card with source quotations and anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ten disclosed-term entries; missing items are identified, and investment judgments are marked for human review.]

## Skill Version(s):

0.1.0 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
