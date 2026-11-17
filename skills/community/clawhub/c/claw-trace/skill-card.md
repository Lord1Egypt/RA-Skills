## Description:

Track and visualize the OpenClaw agent's work process by recording tool call inputs, outputs, duration, and status in easy-to-read trace views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdchi](https://clawhub.ai/user/jdchi)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to inspect an agent's tool-call process, including call sequence, status, durations, optional statistics, filters, and exportable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace output can expose tool-call inputs, outputs, private file content, or secrets when detailed logging is enabled.

Mitigation: Keep simple mode for normal work, avoid detailed logging around secrets or private files, and review traces for accidental sensitive content.

Risk: Saved trace reports can retain sensitive process details in the workspace.

Mitigation: Enable workspace report saving only when a retained trace file is intentional.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration]

**Output Format:** [Markdown trace summaries with optional JSON or HTML exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default mode is simple and off by default; detailed logging and workspace report saving are optional.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
