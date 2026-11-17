## Description:

Geo Poison Detector helps agents flag potentially manipulated product recommendations, product names, or recommendation articles by scanning pseudo-technical claims, soft-ad patterns, source quality, and verification links for Chinese and global markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[graysonzeng](https://clawhub.ai/user/graysonzeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistants use this skill to evaluate product recommendations, product names, and recommendation articles for signs of GEO poisoning before purchase decisions. It provides advisory risk labels, supporting indicators, verification links, and next-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's green, yellow, and red labels may be mistaken for authoritative proof of product authenticity.

Mitigation: Treat the labels as advisory and confirm important purchases through official retailers, company records, patents, standards, and independent reviews.

Risk: URL analysis can expose the host agent to untrusted web content if pages are fetched automatically.

Mitigation: Configure the host to fetch URLs only after an explicit user request and ask for pasted text when fetching fails or is blocked.

## Reference(s):

- [Pseudo-Tech Term Library](references/pseudo-tech-terms.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown risk badge or report with indicators, verification links, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and may include green, yellow, or red risk labels plus generated retailer, company-record, patent, standards, and review-site search links.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
