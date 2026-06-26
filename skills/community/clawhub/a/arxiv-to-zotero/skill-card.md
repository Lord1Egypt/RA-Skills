## Description: <br>
Find recent arXiv papers, skip what is already in Zotero, and save new imports with parent-item tagging and PDF attachments into a dedicated collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnicpyx](https://clawhub.ai/user/cnicpyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External research users use this skill to search recent arXiv papers by topic and time range, deduplicate them against Zotero, and import only new papers into an organized Zotero collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zotero API key and can create Zotero items, attachments, and a target collection. <br>
Mitigation: Use a minimally scoped Zotero API key, keep it in ~/.openclaw/.env or the process environment, and install only where the agent is allowed to write new Zotero content. <br>
Risk: Optional run summaries may reveal research topics and Zotero import details. <br>
Mitigation: Avoid configuring run.export_summary_path to a shared location and review any exported summaries before sharing them. <br>
Risk: The skill downloads PDFs from arXiv and uploads or links them in Zotero. <br>
Mitigation: Review imported papers and attachments according to the user's research and data-handling expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnicpyx/arxiv-to-zotero) <br>
- [Publisher profile](https://clawhub.ai/user/cnicpyx) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>
- [Zotero Web API endpoint](https://api.zotero.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Plain text or Markdown final summaries, with a single Python command invocation and optional JSON run summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZOTERO_API_KEY plus local python3 and curl; creates Zotero parent items, attachments, and the configured target collection when needed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
