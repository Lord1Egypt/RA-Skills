## Description:

Comprehensive editorial review for Chinese content before publication, covering proofreading, grammar, punctuation, fact-checking, political compliance, and advertising law review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liqiongyu](https://clawhub.ai/user/liqiongyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, editors, marketers, and publishing teams use this skill to review public-facing Chinese text before release. It produces layered findings for text quality, factual accuracy, mainland-China publication norms, and advertising-law compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies mainland China publication and compliance norms by default, which may be unsuitable for Taiwan, Hong Kong, Macau, or non-PRC audiences.

Mitigation: State the target publication region before review and have a qualified human reviewer assess political and legal suggestions for that audience.

Risk: Fact-checking and compliance findings are advisory and may depend on web access or the agent environment's available tools.

Mitigation: Verify important claims, legal conclusions, and sensitive compliance findings against authoritative sources before publication.

Risk: Optional file writes and web checks may expose draft documents or claims to the active agent environment.

Mitigation: Only permit file or web access for documents and claims that are appropriate to share in that environment.

## Reference(s):

- [Advertising Law Compliance Reference](references/advertising-law.md)
- [Fact-Checking Reference](references/fact-checking.md)
- [Grammar and Logic Reference](references/grammar-and-logic.md)
- [Political and Territorial Compliance Reference](references/political-compliance.md)
- [Typography and Punctuation Reference](references/typography-and-punctuation.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown structured review report with issue tables and optional corrected text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include review mode, severity counts, layer-by-layer issues, suggested fixes, and reviewer notes.]

## Skill Version(s):

0.1.0 (source: artifact/skill.json and changelog, released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
