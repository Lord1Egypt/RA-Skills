## Description:

Auto Reflection automatically runs deep learning reflections every five rounds, updates capability assessments, adjusts learning plans, and optimizes a knowledge graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyblhl](https://clawhub.ai/user/wyblhl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain reflection reports, capability assessments, HEARTBEAT updates, and learning plans during iterative learning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically changes persistent workspace and agent-context files.

Mitigation: Review the skill before installation and use it only when writes under D:\OpenClaw\workspace are acceptable.

Risk: The script does not document an explicit confirmation or dry-run mode before writing reflection state.

Mitigation: Add or require a confirmation or dry-run workflow before deployment.

Risk: The shipped JavaScript is currently broken.

Mitigation: Fix the JavaScript syntax error before installing or running the skill.

Risk: HEARTBEAT.md updates may influence future agent behavior.

Mitigation: Validate generated content before writing HEARTBEAT.md and review the file after each automated update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wyblhl/skills/auto-reflection)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [JSON files, Markdown updates, and console or log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the script writes under D:\OpenClaw\workspace and does not document a dry-run mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
