## Description: <br>
agent-daily-paper helps an agent subscribe to one or more research fields, retrieve recent arXiv papers, rank them by relevance, translate key metadata, generate Chinese paper digests, and deliver scheduled or on-demand Markdown summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ricardo-Ping](https://clawhub.ai/user/Ricardo-Ping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical teams use this skill to automate field-specific arXiv monitoring, receive bilingual paper cards, and archive daily Markdown digests with optional PDF-based Chinese analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs Python packages and local ML or translation models. <br>
Mitigation: Run the bootstrap and doctor scripts in a dedicated environment and review dependency/model installation before use. <br>
Risk: The digest flow queries arXiv, downloads PDFs, and writes local output, cache, and state files. <br>
Mitigation: Use trusted configuration files, review output/cache directories, and keep generated archives and state files scoped to the skill workspace. <br>
Risk: Optional OpenAI translation or profile generation can send paper titles, abstracts, field names, and translated summary text to an external API. <br>
Mitigation: Use the default local Argos provider when external API sharing is not acceptable; configure OpenAI only with explicit user approval. <br>
Risk: Scheduled delivery through cron, GitHub Actions, or Feishu can publish digests at recurring times. <br>
Mitigation: Confirm timezone, recipient, delivery channel, and generated schedule before enabling automated delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ricardo-Ping/agent-daily-paper) <br>
- [Publisher Profile](https://clawhub.ai/user/Ricardo-Ping) <br>
- [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy) <br>
- [arXiv API](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest text with configuration guidance and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily digest files under output/daily and may update local cache/state files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
