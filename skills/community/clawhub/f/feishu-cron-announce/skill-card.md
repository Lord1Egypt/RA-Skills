## Description:

Creates scheduled OpenClaw cron announce tasks that push generated monitoring results to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbj375767338-arch](https://clawhub.ai/user/bbj375767338-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure recurring OpenClaw monitoring tasks, such as release, weather, or stock checks, and deliver concise results to a Feishu user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps create persistent scheduled agent jobs that can repeatedly send generated results to Feishu.

Mitigation: Review the exact prompt, cron schedule, recipient open_id, and delivery channel before creating the job, and document how to list and delete the cron job afterward.

Risk: Monitored output could include secrets or private data that would be sent to Feishu.

Mitigation: Avoid including secrets or private data in monitored output and verify that the generated message content is appropriate for the Feishu recipient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbj375767338-arch/skills/feishu-cron-announce)
- [ClawHub publisher profile](https://clawhub.ai/user/bbj375767338-arch)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command templates and parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cron timing, Feishu channel, recipient open_id, session isolation, delivery verification, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
