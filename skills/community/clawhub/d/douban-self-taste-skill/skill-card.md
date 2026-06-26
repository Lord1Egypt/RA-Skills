## Description: <br>
Collect, refresh, normalize, and analyze the user's own Douban history for taste analysis and recommendation reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XEric7](https://clawhub.ai/user/XEric7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to refresh, normalize, cache, and analyze their own Douban shelves, ratings, tags, comments, reviews, and recent activity. It supports category-specific taste analysis and recommendation reasoning from local cache, saved HTML, or authenticated personal crawls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Douban cookies and stores personal Douban ratings, comments, and history locally. <br>
Mitigation: Use it only with the user's own UID, keep .local/douban-self-taste/ private and out of version control, and delete cookie, cache, and analysis files when they should no longer be reused. <br>


## Reference(s): <br>
- [Analysis rubric for self taste](references/analysis-rubric.md) <br>
- [Data sources and refresh policy](references/data-sources.md) <br>
- [Output schema](references/output-schema.md) <br>
- [Storage layout](references/storage-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON cache or analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores refreshed crawl cache and optional analysis summaries under .local/douban-self-taste/.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
