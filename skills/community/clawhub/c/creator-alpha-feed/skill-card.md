## Description: <br>
Collect and rank daily AI content for creator-focused publishing workflows. Use when users ask for AI topic scouting, KOL tracking (especially X/Twitter), practical tutorial picks, industry updates, or automated Feishu/Obsidian briefing pushes with configurable templates and time windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rotbit](https://clawhub.ai/user/rotbit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, content operators, and agents use this skill to collect AI-related items from configured sources, rank them for publishing workflows, and produce concise group briefings plus full Obsidian reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefings may be posted to an unintended Feishu destination if the chat ID is misconfigured. <br>
Mitigation: Verify the Feishu chat ID before enabling group posting. <br>
Risk: Browser-based X/Twitter collection could expose private pages or notifications during collection. <br>
Mitigation: Use a dedicated browser session and avoid collecting private pages or notification views. <br>
Risk: Cron or automated runs can publish generated reports without a human review step. <br>
Mitigation: Review generated reports and automation settings before enabling scheduled group posting. <br>


## Reference(s): <br>
- [Cron prompt template](references/cron-prompt-template.md) <br>
- [Data collection rules](references/data-collection-rules.md) <br>
- [Push format](references/push-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, concise group-message summaries, shell command guidance, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ranked TOP lists, source fallback notes, must-track account status, and final report paths.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
