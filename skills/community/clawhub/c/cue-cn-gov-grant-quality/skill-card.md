## Description:

Builds a source-linked ledger of a Chinese listed company's government grants, accounting treatment, deferred balances, and disclosed share of profit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

Financial analysts use it to organize a Chinese listed company's government-grant disclosures into a period ledger. It preserves quoted evidence and anchors, and leaves undisclosed totals and ratios uncomputed.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The documentation describes optional network retrieval, which conflicts with its offline-use promise.

Mitigation: Use supplied disclosure files for offline work; before enabling Cue retrieval, review the configured endpoint and provide CUE_API_KEY only to a trusted setup.

Risk: Running the scripts leaves a persistent daily usage marker under ~/.cue-usage.

Mitigation: Tell users when this marker is enabled and explain that they can remove the directory with rm -rf ~/.cue-usage.

Risk: A self-calculated profit ratio could be mistaken for a ratio stated in the disclosure.

Mitigation: Keep any computed ratio explicitly marked 〔自算〕 and cite its numerator and denominator separately; copy disclosed ratios verbatim.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-cn-gov-grant-quality)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Six-section Markdown ledger or an unfilled ledger skeleton, with quoted disclosure text and source anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Disclosure-based; ratios are copied as disclosed, totals are not self-summed, and the output does not assess earnings quality or grant compliance.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
