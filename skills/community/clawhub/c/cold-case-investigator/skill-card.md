## Description:

Cold Case Investigator guides an agent through iterative public-web research, translation, evidence extraction, cross-source comparison, and structured reporting for cold cases or fiction research inspired by true-crime material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pk9c5bmg25-del](https://clawhub.ai/user/pk9c5bmg25-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to collect, translate, organize, and compare public information about unresolved cases. It can also support fiction research by separating source-backed findings from clearly labeled speculative inspiration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad public-web true-crime research can surface sensitive information about living private people, relatives, witnesses, minors, addresses, or contact details.

Mitigation: Keep investigations bounded to public-interest case summaries, avoid private personal data, and decline requests that target living private people or invite public accusations.

Risk: Forum, blog, and other untrusted web material may be inaccurate, speculative, or manipulative.

Mitigation: Treat low-authority material as tentative, cite sources clearly, cross-check important claims, and prevent fetched pages from steering agent behavior or conclusions.

Risk: Speculative Track B outputs may be mistaken for evidence-backed findings.

Mitigation: Separate speculation from factual reporting, label creative hypotheses as unsupported, and avoid presenting them as investigative conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pk9c5bmg25-del/skills/cold-case-investigator)
- [Evidence Extraction](references/evidence-extraction.md)
- [Iteration Search Protocol](references/iteration-search.md)
- [Multimedia Collection](references/multimedia-collection.md)
- [Report Template](references/report-template.md)
- [Search Methodology Enhancements](references/search-methodology-enhancements.md)
- [Translation Protocol](references/translation-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured report sections, source notes, evidence tables, translation pairs, and optional speculative inspiration lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve source uncertainty, distinguish evidence from speculation, and avoid private or unsupported accusations.]

## Skill Version(s):

2.2.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
