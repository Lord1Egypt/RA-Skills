## Description: <br>
Academic citation lookup and formatter. Given a fuzzy paper title (Chinese or English), searches CrossRef, Semantic Scholar, Baidu Scholar, and CNKI, then returns GB/T 7714, APA 7th, and MLA 9th formatted citations with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, students, and external users can use this skill to look up academic papers from fuzzy Chinese or English titles and produce standard formatted citations with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper titles and search terms are sent to external academic services. <br>
Mitigation: Avoid confidential or unpublished research titles unless sharing those queries with the listed services is acceptable. <br>
Risk: Dependency provenance may matter in controlled environments. <br>
Mitigation: Install requests, beautifulsoup4, and rapidfuzz in a controlled environment using the organization's normal dependency review process. <br>
Risk: Citation details may be incomplete or mismatched because the skill uses fuzzy matching and source metadata. <br>
Mitigation: Review the selected paper and citation details before using the citation in formal work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/antonia-sz/citation-finder) <br>
- [CrossRef Works API](https://api.crossref.org/works) <br>
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [Baidu Scholar](https://xueshu.baidu.com) <br>
- [CNKI](https://kns.cnki.net) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style citation response with source links and optional candidate list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns GB/T 7714, APA 7th, and MLA 9th citation strings when a confident match is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
