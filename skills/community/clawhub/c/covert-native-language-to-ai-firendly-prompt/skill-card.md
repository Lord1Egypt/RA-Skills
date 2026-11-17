## Description:

Transforms casual or voice-transcribed user requests into precise, AI-optimized prompts for mixed-language, vague, or ambiguous tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesxu81](https://clawhub.ai/user/jamesxu81)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI users use this skill to turn informal, voice-transcribed, mixed-language, or ambiguous requests into structured prompts with clear task, context, requirements, and output criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refined prompts may be used for sensitive workflows such as account access, external posting, deletion, deployment, or service restarts.

Mitigation: Review generated prompts and require explicit user confirmation before an agent performs sensitive, destructive, or external-facing actions.

Risk: Artifact examples contain real-looking personal identifiers and local paths that could be copied into generated prompts.

Mitigation: Replace example email addresses, account names, service names, and local paths with placeholders or user-provided values before use.

## Reference(s):

- [Prompt Refiner worked examples](references/examples.md)
- [Prompt engineering techniques reference](references/techniques.md)
- [ClawHub skill page](https://clawhub.ai/jamesxu81/skills/covert-native-language-to-ai-firendly-prompt)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Structured prompt text with optional JSON analysis from the CLI helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend one clarifying question before producing a final refined prompt.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
