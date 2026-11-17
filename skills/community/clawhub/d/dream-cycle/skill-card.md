## Description:

Dream Cycle helps OpenClaw agents set up nightly memory review, workspace cleanup, and morning brief workflows to reduce memory bloat and prepare daily summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjohnathanblog-spec](https://clawhub.ai/user/imjohnathanblog-spec)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure recurring memory maintenance, audit OpenClaw workspace memory files, and generate morning summaries from recent notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled memory cleanup could silently change important OpenClaw memory or identity files if enabled without clear limits.

Mitigation: Define the exact files that may be changed, require dry-run output or approval before optimization, and keep backups before enabling cron automation.

Risk: The bundled scripts print local memory file names, sizes, and excerpts from recent notes.

Mitigation: Run the scripts only in trusted local workspaces and review the generated brief before sharing it outside the intended audience.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit and morning brief scripts that read local OpenClaw workspace memory files and print summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
