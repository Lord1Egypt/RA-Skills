## Description: <br>
Search academic papers and conduct literature reviews using OpenAlex API (free, no key needed). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogerSuperBuilderAlpha](https://clawhub.ai/user/rogerSuperBuilderAlpha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, researchers, students, and developers use this skill to search scholarly literature, inspect paper metadata and citation chains, and generate structured literature reviews from OpenAlex results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic queries, author names, and DOIs are sent to external OpenAlex or Unpaywall services. <br>
Mitigation: Avoid submitting sensitive research topics or private identifiers unless external API disclosure is acceptable. <br>
Risk: Generated reviews and cached OpenAlex responses may persist in local files, including /tmp/litreview_cache. <br>
Mitigation: Use ordinary project-local output filenames, avoid configuration or system paths, and clear the cache on shared machines or for sensitive topics. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rogerSuperBuilderAlpha/academic-research) <br>
- [Publisher Profile](https://clawhub.ai/user/rogerSuperBuilderAlpha) <br>
- [OpenAlex API](https://api.openalex.org) <br>
- [Topanga](https://topanga.ludwitt.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, files, guidance] <br>
**Output Format:** [Plain text, Markdown literature reviews, JSON records, and optional output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches may include paper titles, authors, abstracts, citations, DOIs, open access URLs, source venues, thematic clusters, and bibliography entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
