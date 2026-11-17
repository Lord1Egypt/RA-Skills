## Description:

Ai News Skills automates public AI-news collection, daily signal reports with morning guides, and weekly trend reports with deep dives across three collaborating agent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yy4fun](https://clawhub.ai/user/yy4fun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill bundle to collect public AI-news items into Feishu, produce daily signal reports and morning briefings, and synthesize weekly trend reports with deep dives and watch-list updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable installation steps and unpinned dependencies can change what is installed over time.

Mitigation: Review install.sh before use and pin Agent Reach to a trusted version.

Risk: Feishu credentials could grant broader access than the workflow requires.

Mitigation: Use a least-privilege Feishu app limited to the intended Bitable and wiki documents.

Risk: Scheduled or implicit runs may publish or modify records before the workflow is validated.

Mitigation: Disable cron and implicit invocation until the fetcher, reporter, and weekly reporter have been tested manually.

Risk: The skill updates watch_chains.md and analysis_framework.md as part of its reporting loop.

Mitigation: Require human approval before changes to watch chains or the analysis framework are applied.

Risk: The workflow sends article URLs to Jina Reader for public-page conversion.

Mitigation: Use it only with public URLs and avoid sending private, confidential, or access-controlled links.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/yy4fun/skills/ai-news-skills)
- [README](artifact/README.md)
- [Installation guide](artifact/docs/install.md)
- [Agent Reach](https://github.com/Panniantong/Agent-Reach)
- [Jina Reader](https://r.jina.ai)
- [Fetcher execution guide](artifact/skills/ai_news_fetcher/references/execution.md)
- [Fetcher data model](artifact/skills/ai_news_fetcher/references/data-model.md)
- [News source guide](artifact/skills/ai_news_fetcher/references/sources.md)
- [Daily report workflow](artifact/skills/ai_news_reporter/references/reporting.md)
- [Daily report output template](artifact/skills/ai_news_reporter/references/output-template.md)
- [Watch chains](artifact/skills/ai_news_reporter/references/watch_chains.md)
- [Weekly report workflow](artifact/skills/ai_weekly_reporter/references/reporting.md)
- [Deep-dive analysis framework](artifact/skills/ai_weekly_reporter/references/analysis_framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and guides, JSON news records, shell commands, configuration files, Feishu table/wiki updates, and process logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local daily and weekly Markdown copies, Feishu Bitable records, Feishu wiki documents, morning brief messages, watch-list updates, and concise run summaries.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter, README, and changelog show 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
