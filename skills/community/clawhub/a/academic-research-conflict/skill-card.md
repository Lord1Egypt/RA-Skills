## Description: <br>
Search academic papers and conduct literature reviews using OpenAlex API, including topic, author, DOI, citation-chain, metadata, open-access, and synthesis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Feiyang2007](https://clawhub.ai/user/Feiyang2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, students, and developer agents use this skill to find scholarly papers, inspect citation context, gather structured paper metadata, and produce literature-review summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, author names, and DOIs may be sent to external academic APIs. <br>
Mitigation: Avoid confidential or sensitive research queries unless the external API use is acceptable for the task. <br>
Risk: Literature-review runs can cache paper metadata locally in /tmp/litreview_cache. <br>
Mitigation: Clear /tmp/litreview_cache when cached paper metadata should not remain on the system. <br>
Risk: Server evidence reports unavailable provenance for this version. <br>
Mitigation: Review the publisher profile and release evidence before relying on the skill in higher-trust workflows. <br>


## Reference(s): <br>
- [OpenAlex API](https://api.openalex.org) <br>
- [ClawHub skill page](https://clawhub.ai/Feiyang2007/academic-research-conflict) <br>
- [Topanga](https://topanga.ludwitt.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, JSON records, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search outputs can include paper titles, authors, abstracts, citation counts, DOIs, open access URLs, source venues, thematic clusters, and synthesized literature reviews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
