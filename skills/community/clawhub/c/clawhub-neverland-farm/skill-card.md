## Description:

Automates Neverland farm management by collecting products, harvesting crops, selling inventory, and advancing to the next day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bi4ive](https://clawhub.ai/user/bi4ive)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to automate routine Neverland virtual farm actions, including collecting animal products, harvesting mature crops, selling inventory, and progressing the farm day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically mutate the configured Neverland farm by selling inventory and advancing the day.

Mitigation: Run it only with an API key and farm ID for a farm where automated state changes are acceptable; review console output after each run.

Risk: Optional cron usage can cause repeated unattended farm operations.

Mitigation: Enable scheduled execution only when repeated automation is intended, and remove or pause the cron entry when manual control is preferred.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bi4ive/skills/clawhub-neverland-farm)
- [Neverland Farm](https://neverland.coze.site)
- [Neverland Farm Development Guide](https://neverland.coze.site/skill.md)
- [Agent World](https://world.coze.site)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, API calls]

**Output Format:** [Console text and Python automation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEVERLAND_API_KEY and NEVERLAND_FARM_ID environment variables; execution can mutate the configured virtual farm.]

## Skill Version(s):

1.5.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
