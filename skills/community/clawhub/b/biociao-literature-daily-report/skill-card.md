## Description:

Generates and manages Chinese daily research literature reports by collecting recent PubMed, bioRxiv, and arXiv articles, filtering life-science and AI topics, summarizing articles, and preparing structured Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and research engineers use this skill to monitor recent literature across life sciences and AI, prioritize relevant papers, and produce a Chinese Markdown daily report with summaries, article metadata, links, and trend notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically write reports locally and sync content to ClawLib, Zotero, a knowledge graph, and Matrix.

Mitigation: Review and gate each sync target before routine use, especially Matrix sending and scheduled runs.

Risk: The skill loads broad shell credentials from ~/.zshrc.

Mitigation: Use a narrow secrets file or environment injection for only the required values instead of sourcing a full shell startup file.

Risk: Zotero integration can write to the configured library or group.

Mitigation: Use minimum-scope Zotero credentials and test with a low-privilege group or collection before enabling regular sync.

Risk: The arXiv API calls are documented and implemented with HTTP endpoints.

Mitigation: Switch arXiv requests to HTTPS before regular use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biociao/skills/biociao-literature-daily-report)
- [Publisher profile](https://clawhub.ai/user/biociao)
- [Category standards](artifact/references/categories.md)
- [Workflow guide](artifact/references/workflows.md)
- [bioRxiv API endpoint](https://api.biorxiv.org/details/biorxiv/{date_from}/{date_to}/0/json)
- [arXiv Export API endpoint](http://export.arxiv.org/api/query?search_query={query}&max_results={max_results})
- [Zotero API key settings](https://www.zotero.org/settings/keys/new)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown reports with structured summaries, article metadata, DOI or URL links, and optional configuration or code snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local report files and sync report content to ClawLib, Zotero, a knowledge graph, and Matrix when configured.]

## Skill Version(s):

1.1.0 (source: server release evidence; changelog notes v3.3 workflow updates)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
