## Description:

Analyzes, summarizes, and finds patterns across notes in a user's DeepVista knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search, retrieve, and synthesize notes in a DeepVista knowledge base into concise summaries, recurring themes, decisions, action items, and open questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve private notes that may contain personal, business, credential, or confidential information.

Mitigation: Use it only on notes the agent is allowed to inspect and prefer redacted or minimal excerpts for analysis.

Risk: The workflow suggests sending raw note contents to a chat service for synthesis.

Mitigation: Avoid sending raw note contents unless the user explicitly approves the payload and understands where it goes.

Risk: The installation metadata does not pin the DeepVista CLI version.

Mitigation: Pin the CLI version in deployment environments that require reproducible behavior.

## Reference(s):

- [DeepVista CLI homepage](https://cli.deepvista.ai)
- [ClawHub skill page](https://clawhub.ai/jingconan/skills/deepvista-recipe-analyze-notes)
- [ClawHub publisher profile](https://clawhub.ai/user/jingconan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured summaries, themes, decisions, action items, open questions, and optional note-creation guidance after user confirmation.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
