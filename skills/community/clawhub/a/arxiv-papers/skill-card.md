## Description: <br>
Find and summarize arXiv.org preprints—keyword/category search, abstracts, PDF links. Use for literature scans, paper IDs, or quick orientation (not peer-review, not medical/legal advice). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research-oriented agents use this skill to search arXiv by keyword, identifier, or category and quickly summarize preprint abstracts with links for literature scanning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to arXiv through a local curl-based helper. <br>
Mitigation: Avoid sensitive private information in search queries. <br>
Risk: Returned papers are arXiv preprints and may not be peer reviewed or final. <br>
Mitigation: Treat summaries as orientation material and verify important claims against the full paper and other sources. <br>
Risk: Optional research logging can retain paper notes locally. <br>
Mitigation: Use the log only for notes intended to be retained in the agent environment. <br>


## Reference(s): <br>
- [arXiv API query endpoint](https://export.arxiv.org/api/query) <br>
- [ClawHub skill page](https://clawhub.ai/codenova58/arxiv-papers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with paper metadata, arXiv IDs, abstract and PDF links, and optional shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally append notable papers to a local research log when the agent environment supports it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
