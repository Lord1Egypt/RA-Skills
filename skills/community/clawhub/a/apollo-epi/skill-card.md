## Description:

Apollo Epi helps an agent preserve learned preferences, workflow lessons, and important task experience across sessions instead of starting from scratch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Apollo Epi to decide which user preferences, repeated workflow lessons, and important decisions should be preserved in memory, fine-tuning data, or dedicated skills. The bundled check script reports whether local memory files, learning notes, and Apollo skill documentation appear current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may capture secrets, sensitive personal data, safety-policy changes, authorization rules, or tool-permission instructions.

Mitigation: Require explicit confirmation before storing learned content and prohibit those categories in persistent memory, fine-tuning datasets, or generated skills.

Risk: The skill is designed to preserve learnings across sessions without clear limits, consent, or cleanup controls.

Mitigation: Define consent, retention, and cleanup steps before use, and periodically review saved items for continued relevance.

Risk: The bundled status script inspects local workspace memory and learning files and writes a local inheritance state file.

Mitigation: Review the target paths before execution and run the script only in workspaces where that inspection and state write are expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/apollo-epi)
- [Publisher profile](https://clawhub.ai/user/nic-yuan)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration, text]

**Output Format:** [Markdown guidance and shell-script status reports; the bundled script writes JSON state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and depend on local OpenClaw workspace memory, learning, and skill-documentation files.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
