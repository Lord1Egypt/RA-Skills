## Description:

Generates a Chinese-focused daily news brief by searching configured finance, technology, and international topics and saving summarized results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt6558609-cpu](https://clawhub.ai/user/zt6558609-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect Chinese-language news headlines, organize them by category, and produce scheduled Markdown news briefs for review or delivery through OpenClaw-managed channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run on a recurring schedule.

Mitigation: Review or remove the OpenClaw cron setup unless recurring news brief generation is intended.

Risk: The skill relies on a separate local SearXNG skill through subprocess execution.

Mitigation: Verify the local SearXNG skill and its configuration before installing or running this skill.

Risk: Generated briefs and raw search results are written under the skill's scripts/output directory.

Mitigation: Review retained output files and remove them if they contain unwanted or sensitive browsing-derived content.

Risk: The release overstates AI and push-channel behavior relative to the implementation evidence.

Mitigation: Confirm the actual summarization and delivery behavior in the local environment before relying on the generated brief.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zt6558609-cpu/skills/daily-news-brief-cn)
- [Publisher profile](https://clawhub.ai/user/zt6558609-cpu)
- [Skill definition](artifact/SKILL.md)
- [User documentation](artifact/README.md)
- [News source configuration](artifact/config/sources.json)
- [Schedule configuration](artifact/config/schedule.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown brief files, console text, and optional JSON raw-news data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefs are saved under artifact/scripts/output; optimized scripts can also save raw JSON search results.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
