## Description:

Monitor and summarize finance websites for fund-investing support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warriorfan](https://clawhub.ai/user/warriorfan)

### License/Terms of Use:


## Use Case:

External users and finance-focused agents use this skill to fetch public finance website text, summarize market headlines and fund-related takeaways, compare changes between monitoring runs, and schedule recurring briefings from approved URL lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled monitoring can persist through cron after initial setup.

Mitigation: Confirm the desired cadence before scheduling and remove cron jobs when monitoring is no longer wanted.

Risk: Change detection may keep a small local workspace snapshot of fetched finance text.

Mitigation: Use approved public finance URLs and delete stored state when the monitoring history is no longer needed.

Risk: Finance website summaries may be incomplete or misleading if a source blocks fetching or changes its page format.

Mitigation: Report blocked fetches, use approved alternate sources or APIs, and review summaries before making fund-related decisions.

## Reference(s):

- [Finance Sources](references/sources.md)
- [Skill release page](https://clawhub.ai/warriorfan/skills/finance-web-monitor)
- [Publisher profile](https://clawhub.ai/user/warriorfan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings with optional scheduling commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain a small local rolling snapshot for change detection when monitoring is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
