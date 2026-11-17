## Description:

Visualize and diagnose OpenClaw context window usage with reports on workspace bootstrap files, installed skills, and token budget allocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzocb](https://clawhub.ai/user/jzocb)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to inspect OpenClaw context window health, diagnose bootstrap overhead, identify missing or truncated workspace files, and produce shareable context usage summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostic reads local OpenClaw bootstrap files and installed skill metadata.

Mitigation: Use it only in workspaces where local context diagnostics are acceptable.

Risk: Terminal, JSON, summary, or PNG outputs may reveal workspace paths, file status, file sizes, token estimates, and installed skill names.

Mitigation: Review generated output before sharing it outside the workspace.

Risk: PNG export depends on optional rendering packages or system converters.

Mitigation: Use isolated environments or pinned package versions when enabling optional PNG dependencies.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, image, shell commands, guidance]

**Output Format:** [Terminal report, concise text summary, JSON, or PNG image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG output requires optional rendering dependencies; JSON and summary modes are available for agent workflows.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
