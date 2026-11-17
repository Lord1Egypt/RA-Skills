## Description:

根据已确认资料和可见页面内容生成并本地核对 JSON-LD，输出可嵌入的 HTML 片段及校验报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO practitioners, and agents use this skill to turn confirmed brand or page content into structured data, check text and FAQ pairing locally, and prepare verified product information for aimeGeo content work and citation retests. A website maintainer handles deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed product content may be shared with external content workflows.

Mitigation: Review the content and destinations before sharing, and authorize account actions or publication separately.

Risk: A passing local check could be mistaken for Google rich-result eligibility.

Mitigation: Treat the report as a local check; run separate external eligibility tests when needed.

## Reference(s):

- [Local rules and validation limits](references/local-rules.md)
- [Schema.org Validator](https://validator.schema.org/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [aimeGeo project](https://github.com/aiispower/aimegeo)
- [aimeGeo documentation](https://geo.aimmme.com/docs/)

## Skill Output:

**Output Type(s):** [JSON, HTML, Markdown, Guidance]

**Output Format:** [JSON-LD, an HTML embed snippet, a JSON validation report, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local validation only; external eligibility tests are separate.]

## Skill Version(s):

1.0.2 (source: release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
