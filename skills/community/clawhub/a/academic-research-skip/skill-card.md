## Description: <br>
Searches academic papers and conducts literature reviews with OpenAlex, including paper lookup, citation exploration, metadata extraction, and structured synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmyg11](https://clawhub.ai/user/mmyg11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, analysts, and agents use this skill to find scholarly works by topic, author, or DOI and to assemble structured literature reviews with paper metadata, citation context, and thematic synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic queries, author names, and DOIs are sent to external services such as OpenAlex or Unpaywall. <br>
Mitigation: Avoid confidential research topics or sensitive identifiers when running searches. <br>
Risk: The literature-review workflow can write output files and may overwrite a chosen output path. <br>
Mitigation: Choose output paths deliberately and review generated files before relying on them. <br>
Risk: Fetched paper metadata may remain in the local cache under /tmp/litreview_cache. <br>
Mitigation: Clear the cache when retained academic metadata should not remain on the machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mmyg11/academic-research-skip) <br>
- [OpenAlex API](https://api.openalex.org) <br>
- [Topanga](https://topanga.ludwitt.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, and terminal text from academic search and literature-review commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write user-selected review files and cache fetched paper metadata in /tmp/litreview_cache.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
