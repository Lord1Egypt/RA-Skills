## Description:

Academic citation lookup and formatter. Given a fuzzy paper title (Chinese or English), searches CrossRef, Semantic Scholar, Baidu Scholar, and CNKI, then returns GB/T 7714, APA 7th, and MLA 9th formatted citations with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and agents use this skill to find likely academic paper matches from fuzzy Chinese or English titles and produce standard citation formats with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to third-party academic search services.

Mitigation: Avoid entering confidential paper titles or private research details unless sharing them with CrossRef, Semantic Scholar, Baidu Scholar, and CNKI is acceptable.

Risk: Citation metadata can be incomplete or incorrectly matched, especially for fuzzy titles or scraped sources.

Mitigation: Manually verify final citations and source links before submitting or publishing references.

Risk: Runtime dependencies and web-scraped sources may change over time.

Mitigation: Install in a virtual environment, consider pinning dependency versions, and recheck behavior after dependency or source-site changes.

## Reference(s):

- [Citation Finder ClawHub Skill](https://clawhub.ai/antonia-sz/skills/citation-finder)
- [CrossRef Works API](https://api.crossref.org/works)
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search)
- [Baidu Scholar](https://xueshu.baidu.com)
- [CNKI](https://kns.cnki.net)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted citation text with source links and candidate lists when confidence is low]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns GB/T 7714, APA 7th, and MLA 9th citations; may ask the user to confirm among candidate matches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
