## Description:

Local-first chart generation engine for trends, comparisons, distributions, and quick visual explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panchenbo](https://clawhub.ai/user/panchenbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn inline data, CSV, or JSON into local bar, line, pie, and scatter chart images, suggest an appropriate chart type, and review previously generated chart history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart titles, labels, numeric values, and output paths are saved in local chart history.

Mitigation: Avoid highly sensitive datasets unless local history storage is acceptable, and clear or protect ~/.openclaw/workspace/memory/chart when needed.

Risk: Temporary-file based local saves may need additional hardening for shared or multi-user deployments.

Mitigation: Review and harden the temporary-file save behavior before deploying in shared environments.

## Reference(s):

- [Chart Philosophy](references/philosophy.md)
- [ClawHub skill page](https://clawhub.ai/panchenbo/skills/chart-data-viz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local chart image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PNG charts and chart history are stored locally under ~/.openclaw/workspace/memory/chart.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
