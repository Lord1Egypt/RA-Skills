## Description:

Gemini CLI for one-shot Q&A, summaries, and generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask Gemini CLI one-shot questions, request summaries, generate content, choose models, request JSON output, and manage Gemini CLI extensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and files sent through Gemini CLI may be processed by Gemini.

Mitigation: Only pass prompts and files you are comfortable sending to Gemini, and follow your organization's data-handling requirements.

Risk: The interactive login flow may create local Gemini CLI authentication state.

Mitigation: Run interactive login only when you intend to authenticate Gemini CLI on the machine and can manage the resulting local auth state.

Risk: Using Gemini CLI's --yolo mode can reduce safety checks.

Mitigation: Avoid --yolo unless a reviewer has approved the workflow and its inputs.

## Reference(s):

- [Gemini developer documentation](https://ai.google.dev/)
- [ClawHub skill page](https://clawhub.ai/kenswj/skills/gemini-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/kenswj)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-formatted Gemini CLI output when the user requests --output-format json.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
