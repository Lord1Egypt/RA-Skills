## Description:

Use when planning conference schedules, optimizing session selection at scientific meetings, managing time between presentations, or maximizing networking at academic conferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan scientific or medical conference attendance by ranking sessions against interests, selecting a non-conflicting schedule, and preserving must-attend items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation describes features such as PDF program input, calendar export, real-time updates, and networking target export that are not implemented in the bundled script.

Mitigation: Test the installed artifact against the actual JSON-based CLI before relying on advertised workflow features.

Risk: Schedule selection is a lightweight heuristic based on keyword matching, same-start conflict handling, and must-attend flags.

Mitigation: Manually review the generated schedule against the official conference program, room changes, travel time, breaks, and personal priorities.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aipoch-ai/skills/conference-schedule-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; bundled CLI prints text and can write JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script operates locally on schedule JSON input and optional JSON output.]

## Skill Version(s):

0.1.0 (source: server release metadata and tile.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
