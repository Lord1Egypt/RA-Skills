## Description:

Searches and summarizes arXiv papers for music-generation research, including recent research, topic-specific queries, and daily AI paper summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nomorecoding](https://clawhub.ai/user/nomorecoding)

### License/Terms of Use:


## Use Case:

Developers, researchers, and research assistants use this skill to search arXiv for music-generation papers, deduplicate results, capture paper metadata, and maintain an audit trail of search activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search logs and paper lists are saved locally and may retain sensitive query terms or research interests.

Mitigation: Use the skill in a project workspace and avoid sensitive or proprietary query terms when local persistence is a concern.

Risk: The curl helper accepts query and count inputs directly.

Mitigation: Prefer bounded, simple search counts and review the generated API command or script before execution until input handling is hardened.

Risk: Weak relevance keywords and broad arXiv queries can return papers that need human review before inclusion in a research summary.

Mitigation: Review matched keywords, deduplicated paper metadata, and the search log before relying on the resulting paper list.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nomorecoding/skills/arxiv-watcher-music)
- [arXiv API Query Endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands]

**Output Format:** [Markdown search logs and JSON paper lists, with optional shell/API command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local files under research/{domain}/search_results when used as documented.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
