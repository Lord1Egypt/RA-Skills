## Description:

Extracts lessons, decisions, patterns, and dead ends from AI conversation exports using local Ollama or an OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can analyze exported AI conversations to capture actionable insights in persistent semantic memory. Use a dry run and review the generated learnings before relying on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When remote mode is enabled, private conversation exports and the API key are sent to the configured endpoint.

Mitigation: For local processing, unset OPENAI_API_KEY and keep Ollama on loopback. For remote processing, verify the provider and privacy terms and use a trusted HTTPS endpoint.

Risk: Generated learnings are unreviewed text written into persistent memory and may be inaccurate or misleading.

Mitigation: Start with --dry-run, limit the selected exports, and review the generated learnings before relying on them in memory.

Risk: A dry run still contacts the configured model and may create directories.

Mitigation: Check the selected model endpoint and workspace location before running, and use a narrow input scope.

## Reference(s):

- [Chat Learnings Extractor on ClawHub](https://clawhub.ai/djc00p/skills/chat-learnings-extractor)
- [Related chat-history-importer skill](https://clawhub.ai/djc00p/chat-history-importer)
- [Model Modes and Extraction Categories](references/model-modes-and-categories.md)
- [Extraction Prompt Template](references/prompt-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown organized into lessons learned, decisions made, patterns noticed, and dead ends]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model-generated learnings can be previewed with --dry-run before they are written to persistent memory.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
