## Description:

Monitor a Dataify Builder task through completion, recover safely after interruption, or guide cross-platform DATAIFY_API_TOKEN setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to monitor existing Dataify tasks, retrieve final results, recover safely after interrupted monitoring, and guide cross-platform Dataify API token setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Dataify services and uses a Dataify API token.

Mitigation: Use a limited, rotatable token and avoid exposing tokens, private results, or signed URLs in prompts, logs, and shared outputs.

Risk: Server security evidence reports broader undeclared scraping and business-intelligence scripts in the package.

Mitigation: Review the package scope before broad installation and run only the task-monitoring behavior needed for the current workflow.

Risk: Previewed or generated commands from untrusted parameter files may perform unexpected Dataify actions.

Mitigation: Inspect command targets, URLs, and task scope before execution, especially for high-volume, paid, or media-download workflows.

## Reference(s):

- [Dataify Token Setup](references/token-setup.md)
- [Dataify login and API token management](https://dashboard.dataify.com/login?utm_source=skill)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-task-operations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with task status summaries, final result summaries, and inline shell commands when setup or resume steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preserve access to raw task results while summarizing large outputs; bounded monitoring reports the task ID and resume command on timeout or interruption.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
