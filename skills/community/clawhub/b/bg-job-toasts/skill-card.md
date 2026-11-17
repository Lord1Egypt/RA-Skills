## Description:

Background Job Toasts guides agents through adding or improving OpenClaw Control UI notifications for background processes, including cron jobs, memory compaction, knowledge extraction, and custom jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement bottom-right background job toasts in the OpenClaw Control UI and to troubleshoot cron job naming, compaction progress, and toast rendering behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Toast labels can expose sensitive details if cron job names or custom job names include secrets or private operational data.

Mitigation: Use human-readable but non-sensitive job names, and review notification payloads before showing them in the UI.

Risk: Compaction status UI may fail to update when mutable compact state is changed without requesting a render.

Mitigation: Call the app render update path after mutating compact state, and test running, complete, and error phases.

## Reference(s):

- [Source Snapshot](references/source-snapshot.md)
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/bg-job-toasts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript and CSS code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation notes, fallback ordering, state update guidance, and known gotchas for OpenClaw UI background job toasts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
