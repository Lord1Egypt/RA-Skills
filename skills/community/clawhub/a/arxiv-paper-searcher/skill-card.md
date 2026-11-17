## Description:

Searches arXiv for papers on a requested topic, analyzes titles and abstracts, and can optionally set up recurring monitoring through OpenClaw cron after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songxf1024](https://clawhub.ai/user/songxf1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical users use this skill to quickly survey recent arXiv papers for a topic, compare themes and novelty, and optionally monitor the topic on a schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring monitoring can persist user-provided search text as future agent instructions.

Mitigation: Create cron jobs only from trusted search keywords, inspect the generated cron payload when possible, and avoid instruction-like text in keywords.

Risk: The local config.json can influence future scheduled runs.

Mitigation: Treat config.json as reviewable state and verify that its job_id, search query, result count, sort order, and schedule snapshot match the intended OpenClaw cron job.

Risk: The arxiv Python dependency is not pinned by the artifact.

Mitigation: Pin the arxiv dependency for higher-assurance deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songxf1024/skills/arxiv-paper-searcher)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional JSON search data and cron or configuration payload snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to 20 papers, caps search results at 100, sorts by date unless specified, and uses Asia/Shanghai for scheduled monitoring.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
