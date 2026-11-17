## Description:

将 A 股招股说明书整理为八项逐字速览卡，保留原句和页码锚，并标注发行人自述与未检索到的内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

分析人员可用它从 A 股招股说明书中提取可回原文核对的八项信息，涵盖发行安排、业务、募资、集中度、研发、风险、控制权和财务口径。它保留发行人自述及前瞻措辞，并将估值和申购判断留给人工。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Cue services may receive confidential prospectus drafts or annotations for external processing.

Mitigation: Use supplied text without Cue integrations when external processing is unnecessary; before enabling Cue, verify legitimate HTTPS endpoints and review retention terms. Keep API keys out of chat.

Risk: A concise extract could omit or misstate prospectus details, or be mistaken for investment guidance.

Mitigation: Check quotations and page anchors against the original, name unretrieved items, preserve forward-looking qualifiers, and leave valuation, subscription, price-direction, and risk-ranking judgments to a human.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-prospectus-digest-cn)
- [self-claimed.md](artifact/references/self-claimed.md)
- [Cue data configuration](https://cuecue.cn/hub/mcp)
- [Cue long-document reader configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown prospectus card with a header, eight verbatim items, comparison, missing-items list, and pending human review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight fixed items; source quotations with page anchors; missing facts named; periods and units retained; no valuation or subscription recommendations.]

## Skill Version(s):

0.1.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
