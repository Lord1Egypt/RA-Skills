## Description:

Gemini CLI for one-shot Q&A, summaries, and generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to prompt Gemini CLI in one-shot mode for Q&A, summarization, JSON-formatted responses, text generation, and extension management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and source text sent through Gemini CLI may be processed by an external provider.

Mitigation: Avoid sending secrets, private data, or regulated material unless that use fits the user's Gemini account and data-handling expectations.

Risk: The skill references Gemini CLI command execution and warns against unsafe yolo behavior.

Mitigation: Use one-shot commands, review generated commands before execution, and avoid --yolo unless the execution environment is intentionally disposable.

Risk: The ClawHub quality signal quarantined this release for moderation review.

Mitigation: Review the skill text and intended Gemini CLI usage before listing or deployment.

## Reference(s):

- [Google AI for Developers](https://ai.google.dev/)
- [ClawHub skill page](https://clawhub.ai/andy27725/skills/gemini-andy27725)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to produce JSON when Gemini CLI is called with --output-format json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
