## Description:

Automatically classifies user tasks and routes them to configured AI models for coding, reasoning, translation, summarization, writing, data analysis, image understanding, or chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joyyyced](https://clawhub.ai/user/joyyyced)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to route substantive agent tasks to configured AI providers or to an optional self-hosted router for model selection and feedback learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is written to activate for nearly all substantive requests and can take over ordinary agent tasks.

Mitigation: Narrow activation to explicit invocation or clear opt-in before broad deployment.

Risk: Prompt text may be sent to configured AI providers or to a user-configured router.

Mitigation: Disclose provider and router data flow, require user-controlled router configuration, and avoid enabling router mode unless explicitly configured.

Risk: The skill references command templates that pass user task text to scripts.

Mitigation: Include the referenced scripts, review their execution paths, and require safe argument handling before installation.

## Reference(s):

- [Auto Model Router ClawHub page](https://clawhub.ai/joyyyced/skills/auto-model-router)
- [Project homepage](https://github.com/JoyyyceD/auto-model-router)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional code blocks, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected task category, configured provider, model route, and optional router mode.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter declares 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
