## Description:

Use when you need to parse or audit a FigJam User Story Map (Jeff Patton methodology) into LLM-readable Markdown or JSON after a Story Mapping workshop, before publishing a Story Map template, or when feeding a Story Map to a coding agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monikazapisek](https://clawhub.ai/user/monikazapisek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and design teams use this skill to audit FigJam story maps for LLM readiness and parse trusted FigJam board data into structured backlog outputs. It is intended for post-workshop transcription, template review, and preparing story map context for coding or product-management agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editable FigJam board text may be copied into Markdown that is later provided to a coding agent, including embedded `[00_SECTION_AI_Readme]` instructions.

Mitigation: Treat board content as untrusted input, review generated Markdown before reuse, and keep higher-priority agent instructions from being overridden by board text.

Risk: The parser can use a Figma personal access token to fetch board data.

Mitigation: Provide the token through an environment variable or other safe secret mechanism, avoid pasting it into chat or files, and prefer a least-privilege token.

Risk: Generated backlog data may preserve incorrect story map structure or workshop assumptions if the source board is poorly formed.

Mitigation: Run the audit checklist first and review node-level findings before relying on parsed Markdown or JSON for implementation planning.

Risk: Runtime dependencies and API calls are executed locally when using the parser.

Mitigation: Install dependencies in an isolated environment with pinned versions when practical and use saved Figma JSON for offline parsing when live API access is unnecessary.

## Reference(s):

- [LLM-Ready FigJam Guidelines](artifact/references/llm-ready-figjam-guidelines.md)
- [System Prompt - FigJam Story Map Parser](artifact/references/system-prompt.md)
- [FigJam Story Map Template Spec](artifact/references/figjam-template-spec.md)
- [FigJam Story Map Executive Summary](artifact/references/figjam-executive-summary.md)
- [Published FigJam Community Template](https://www.figma.com/community/file/1661156551667594442)
- [Figma REST API Documentation](https://www.figma.com/developers/api)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports, Markdown backlog files, JSON backlog data, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parser output may include story hierarchy, release slices, acceptance criteria, owners, priorities, connector relationships, and node IDs for review.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
