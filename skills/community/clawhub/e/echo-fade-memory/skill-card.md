## Description:

Runs a thin long-term memory workflow on top of the echo-fade-memory service for recalling, storing, and forgetting durable text and image context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiparker](https://clawhub.ai/user/hiparker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add a durable memory layer that can recall prior context, store preferences, project decisions, screenshots, OCR text, and forget obsolete entries through a local or configured echo-fade-memory service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad automatic recall and durable storage of personal, project, screenshot, and OCR data.

Mitigation: Use the always-on hook only when needed, narrow hook matchers, review memory contents before storing, and avoid storing secrets, precise personal data, regulated data, screenshots, or OCR text unless the user clearly opts in.

Risk: Memory data is sent to the configured echo-fade-memory service endpoint.

Mitigation: Use a trusted local endpoint or authenticated HTTPS endpoint and verify EFM_BASE_URL before running store, recall, or forget commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hiparker/skills/echo-fade-memory)
- [Examples](references/examples.md)
- [Hooks Setup](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [OpenClaw Natural Trigger](references/openclaw-natural-trigger.md)
- [Memory Templates](assets/memory-templates.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an echo-fade-memory service endpoint and an embedding backend such as Ollama, OpenAI, or Gemini.]

## Skill Version(s):

2.0.0 (source: server release evidence; artifact frontmatter lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
