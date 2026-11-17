## Description:

Automates article URL fetching, analysis, summarization, tagging, quality scoring, deduplication, and archiving to Feishu Docs and Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongnan](https://clawhub.ai/user/dongnan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to process single articles or batches of article URLs from chat or CLI workflows. It produces summaries, tags, analysis reports, quality scores, deduplication checks, and Feishu/Bitable archival records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential backups and local configuration files may expose Feishu or Bitable tokens if they are stored or synced carelessly.

Mitigation: Use a least-privilege Feishu/Bitable token, keep the skill in a private directory, and ignore .env, .env.*, .config.backup.json, config.backup.json, and config.local.json.

Risk: Analyzing private or internal URLs can expose content through fetching, summarization, logs, or external storage.

Mitigation: Avoid private/internal URLs unless the fetch tool blocks local and private network destinations and the storage destination is approved for that content.

Risk: Heartbeat automation can forward or process group-chat links without enough operator awareness.

Mitigation: Confirm whether Heartbeat automation is enabled before connecting the skill to group chats.

Risk: Analysis outputs and article metadata are archived to Feishu Docs and Bitable.

Mitigation: Review workspace permissions and destination tables before enabling archival workflows.

## Reference(s):

- [Article Workflow on ClawHub](https://clawhub.ai/dongnan/skills/article-workflow)
- [Skill Instructions](SKILL.md)
- [README](README.md)
- [Configuration Protection Guide](docs/CONFIG_PROTECTION.md)
- [Security Audit](docs/SECURITY_AUDIT.md)
- [Quality Scoring](docs/quality-score.md)
- [Smart Router Implementation](docs/smart-router-implementation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and reports, chat status text, Feishu document links, Bitable records, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-URL analysis and batch analysis with a documented maximum of 5 concurrent subagents.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
