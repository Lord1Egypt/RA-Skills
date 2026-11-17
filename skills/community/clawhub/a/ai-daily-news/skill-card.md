## Description:

Automated AI daily news collection and reporting system that collects AI papers from arXiv and Hugging Face, AI products from Product Hunt, YouTube videos from AI creators, and RSS feeds, then generates structured daily reports and pushes them to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephleohou-ui](https://clawhub.ai/user/josephleohou-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and run an automated daily AI news workflow that collects papers, products, videos, and RSS items, stores a structured local report, and optionally pushes the report to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe automation and dependency behavior may affect the host environment.

Mitigation: Review the code before installation, use an isolated low-privilege environment, and preinstall pinned dependencies through normal deployment controls.

Risk: The YouTube collection path can attempt automatic yt-dlp installation.

Mitigation: Avoid the automatic install path by preinstalling an approved yt-dlp version or disabling that collection path until reviewed.

Risk: Custom RSS feeds and browser fallback can fetch untrusted web content.

Mitigation: Restrict configured feeds to trusted HTTPS domains and review fallback behavior before enabling scheduled collection.

Risk: Feishu webhook and local config values are sensitive operational secrets.

Mitigation: Protect config.json as a secret, limit webhook scope, and rotate the webhook if it is exposed.

Risk: Scheduled execution can repeatedly run network collection and webhook posting.

Mitigation: Run the scheduler only under a low-privilege account and avoid privileged deployment until the shell-based browser helper is removed or tightly constrained.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/josephleohou-ui/skills/ai-daily-news)
- [Publisher profile](https://clawhub.ai/user/josephleohou-ui)
- [Development guide](references/DEVELOPMENT.md)
- [Configuration example](references/config.example.json)
- [Python requirements](references/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands; runtime scripts produce local JSON news data and Feishu interactive card payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable source limits, schedule settings, browser fallback behavior, and Feishu webhook settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
