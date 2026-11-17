## Description:

Provides cross-platform system health monitoring and optimization guidance for macOS, Windows, and Linux, including diagnostics, performance scoring, cleanup planning, memory review, and scheduled check recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT

## Use Case:

Developers and end users can use this skill to have an agent inspect system status, produce health reports, and propose cleanup or process-management steps across macOS, Windows, and Linux. Actions that affect the system should be reviewed and explicitly confirmed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup, process termination, or scheduled checks can affect the user's system if executed without clear review.

Mitigation: Require the agent to show exactly what it will change and obtain explicit user confirmation before any cleanup, process termination, or scheduled-check setup.

Risk: The skill instructions are primarily in Chinese, which can make review harder for users who do not read Chinese.

Mitigation: Before installation or use, review an accurate translation or have a Chinese-reading reviewer confirm the operational and safety instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/computer-efficiency-skill)
- [Skill source](artifact/SKILL.md)
- [MIT License](artifact/LICENSE)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell or PowerShell commands and JSON schedule examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only diagnostics, optimization recommendations, and confirmation-gated cleanup or process termination plans.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
