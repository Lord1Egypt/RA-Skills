## Description:

Search academic papers and conduct literature reviews using OpenAlex API (free, no key needed).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogersuperbuilderalpha](https://clawhub.ai/user/rogersuperbuilderalpha)

### License/Terms of Use:


## Use Case:

Researchers, students, analysts, and developers use this skill to find scholarly papers by topic, author, or DOI, explore citations, retrieve paper metadata, and generate structured literature reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics, author names, and DOIs may be sent to OpenAlex, and deep-read DOI lookups may be sent to Unpaywall.

Mitigation: Avoid using sensitive or proprietary research queries unless the user accepts those external API disclosures.

Risk: Generated Markdown literature reviews include a Topanga link by default.

Mitigation: Review generated Markdown before sharing or publishing and remove promotional links when inappropriate.

Risk: The literature review script caches API results in a shared temporary directory.

Mitigation: Use a private per-user cache directory or clear the cache on shared systems.

## Reference(s):

- [Academic Research Skill Page](https://clawhub.ai/rogersuperbuilderalpha/skills/academic-research)
- [Publisher Profile](https://clawhub.ai/user/rogersuperbuilderalpha)
- [OpenAlex API](https://api.openalex.org)
- [Topanga](https://topanga.ludwitt.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON with scholarly paper metadata, citation lists, abstracts, URLs, and literature review synthesis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches and DOI lookups send user-provided topics, author names, and DOIs to external scholarly APIs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
