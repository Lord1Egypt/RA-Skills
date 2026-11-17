## Description:

Lead Hunter finds freshly funded companies matching an ideal customer profile, researches and scores them, and produces qualified leads with personalized outreach drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zich-agent](https://clawhub.ai/user/zich-agent)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Lead Hunter to configure an ideal customer profile, research newly funded companies, qualify prospects, and generate outreach-ready lead reports for sales pipeline building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scrape web sources, including user-provided custom URLs.

Mitigation: Run it in a sandboxed environment, limit custom sources to trusted sites, and review blocked-source reports before expanding the source list.

Risk: The fallback scraper may install Crawl4AI and Playwright Chromium into a local virtual environment.

Mitigation: Require explicit approval before dependency installation and review the runtime environment before scheduled use.

Risk: Scheduled runs and persistent local files can accumulate lead history and run logs.

Mitigation: Review any cron setup, retention needs, and generated lead, seen-state, and memory files for policy fit.

Risk: Asana output can create tasks from generated lead research and outreach drafts.

Mitigation: Review generated Asana commands and task content before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zich-agent/skills/agitech-lead-hunter)
- [Onboarding interview flow](artifact/references/onboarding.md)
- [Lead source catalog](artifact/references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, CSV rows, Asana task commands, JSON configuration, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write lead files, local deduplication state, memory logs, and Asana tasks depending on configuration; caps full research at 5 leads per run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
