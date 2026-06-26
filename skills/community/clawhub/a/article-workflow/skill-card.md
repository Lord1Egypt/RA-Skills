## Description: <br>
Article Workflow analyzes article URLs, generates summaries, tags, reports, and quality scores, deduplicates repeated URLs, and can archive results to Feishu Docs and Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongnan](https://clawhub.ai/user/dongnan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams and individual users use this skill to process one or more shared article links, generate concise summaries and quality scores, and save structured results to Feishu/Bitable for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can monitor chat-shared URLs and store article-derived data in Feishu/Bitable. <br>
Mitigation: Review Feishu permissions, target chats, and Bitable tables before installation, and avoid sensitive or internal content unless affected users have notice and consent. <br>
Risk: Credentials and table identifiers are required for Feishu/Bitable workflows. <br>
Mitigation: Replace example credentials with clearly fake placeholders, keep real values in environment variables or local config, and verify that config backups are protected. <br>
Risk: Cleanup, restore, and bulk update commands may affect local caches, logs, and archived article records. <br>
Mitigation: Verify paths and target records before running cleanup or bulk update commands, especially in shared or production workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dongnan/article-workflow) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [User Guide](artifact/README.md) <br>
- [Configuration Protection Guide](artifact/docs/CONFIG_PROTECTION.md) <br>
- [Quality Scoring Guide](artifact/docs/quality-score.md) <br>
- [Security Audit](artifact/docs/SECURITY_AUDIT.md) <br>
- [Smart Router Implementation](artifact/docs/smart-router-implementation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status messages, article summaries, quality scores, Feishu/Bitable links, configuration snippets, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist article-derived records, reports, cover images, logs, caches, and config backups when Feishu/Bitable or local workflows are enabled.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
