## Description:

Desearch Skill helps agents submit Zeelin Deep Research tasks asynchronously, monitor completion, and save the resulting research report as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angelandpeiqi](https://clawhub.ai/user/angelandpeiqi)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to run long-running Zeelin research jobs without keeping the agent session blocked, then retrieve saved Markdown reports and status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are sent to the Zeelin Deep Research API.

Mitigation: Submit only research topics and data that are appropriate for Zeelin processing, and review data handling expectations before use.

Risk: The skill can store the Zeelin API key plainly in a local OpenClaw configuration file.

Mitigation: Protect the local configuration file, remove keys when no longer needed, and rotate any key that may have been exposed.

Risk: The skill creates an OpenClaw cron notification targeting a hard-coded DingTalk recipient.

Mitigation: Change or remove the notification target before use and confirm task metadata is sent only to the intended recipient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/angelandpeiqi/skills/desearch-skill)
- [Zeelin API configuration guide](artifact/references/config.md)
- [Zeelin asynchronous task pattern](artifact/references/async-pattern.md)
- [Zeelin Deep Research service](https://desearch.zeelin.cn)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown research reports with JSON status metadata and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits asynchronous research tasks, writes status files, and saves completed reports under the skill reports directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
