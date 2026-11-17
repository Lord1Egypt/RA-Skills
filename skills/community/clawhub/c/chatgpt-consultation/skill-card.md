## Description:

Automatically or manually consults ChatGPT through a browser workflow to answer complex, current, or specialized user questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahaoxiong](https://clawhub.ai/user/mahaoxiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to route complex, current, or specialist questions to ChatGPT when local model knowledge is insufficient or when the user explicitly asks for ChatGPT consultation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Matched questions may be sent to ChatGPT through an existing browser session, which can expose sensitive prompts.

Mitigation: Use only with non-sensitive prompts and add explicit consent or redaction controls before broader deployment.

Risk: The security evidence reports an unsafe shell command path that could execute unintended local commands.

Mitigation: Fix the shell invocation and review the command path before running this skill in a privileged workspace.

Risk: The artifact references missing runtime dependencies and browser configuration files.

Mitigation: Supply and review the required scripts, configuration, and browser access before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mahaoxiong/skills/chatgpt-consultation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text response with possible command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ChatGPT consultation results, status notices, and error messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
