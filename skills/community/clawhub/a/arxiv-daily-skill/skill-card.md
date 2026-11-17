## Description:

Collects recent arXiv papers in LLM, RAG, Agent, and related AI topics, enriches them with author and affiliation context, and produces Chinese-friendly paper reports with optional Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seeu1688](https://clawhub.ai/user/seeu1688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical teams use this skill to monitor recent arXiv papers in LLM, RAG, Agent, Transformer, Harness, and Reasoning areas, then receive compact Markdown summaries or deeper single-paper analysis. It supports manual requests and scheduled weekday paper-report delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron setup and helper scripts can create persistent system behavior or overwrite existing scheduling if installed without review.

Mitigation: Review cron setup before installation, preserve existing crontab entries, run under an unprivileged account, and provide an uninstall path.

Risk: The skill handles network data from arXiv and includes an alternate shell fetcher with unsafe XML expansion behavior.

Mitigation: Use HTTPS for arXiv requests and remove the shell fetcher path that invokes xmllint with --noent.

Risk: Reports and previews may expose paper-report content through predictable temporary paths or an incorrectly configured Feishu webhook.

Mitigation: Store generated reports in a private directory and configure Feishu only for destinations where paper-report previews are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seeu1688/skills/arxiv-daily-skill)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [arXiv API Query Endpoint](http://export.arxiv.org/api/query)
- [Feishu Bot Webhook Endpoint](https://open.feishu.cn/open-apis/bot/v2/hook/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown reports, command-line status text, and optional Feishu interactive-card payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compact paper directories, detailed top-paper summaries, affiliation metadata, dated report files, and optional webhook previews.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
