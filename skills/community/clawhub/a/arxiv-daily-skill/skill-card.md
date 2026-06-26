## Description: <br>
Arxiv Daily Skill collects recent arXiv papers in LLM, RAG, and agent topics, adds affiliation details, and prepares Markdown digests for Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seeu1688](https://clawhub.ai/user/seeu1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and developers use this skill to receive scheduled or manually triggered arXiv digests for LLM, RAG, agent, transformer, harness, and reasoning topics. The skill is intended to summarize selected papers, include affiliation context, and support follow-up deep analysis of individual arXiv IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu notifications depend on a user-configured webhook. <br>
Mitigation: Configure the webhook deliberately and keep the webhook value limited to the intended notification channel. <br>
Risk: Scheduled execution can affect existing cron behavior if added carelessly. <br>
Mitigation: Review the cron entry before enabling it and add it in a way that preserves existing scheduled jobs. <br>
Risk: The first generated digest may need review before recurring delivery. <br>
Mitigation: Review the first generated report before enabling scheduled Feishu notifications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seeu1688/arxiv-daily-skill) <br>
- [arXiv API Query Endpoint](http://export.arxiv.org/api/query) <br>
- [Skill README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and concise text guidance, with optional shell commands and configuration steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be saved locally under /tmp and optionally sent through a user-configured Feishu webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
