## Description:

Ai Video Prompt helps agents build Chinese AI video prompts using a first-and-last keyframe workflow for multi-segment five-second video sequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atmosphere16happy](https://clawhub.ai/user/atmosphere16happy)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to plan long-form AI video prompts, keyframe image prompts, five-second segment prompts, and continuity checks for video-generation platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts may be unsuitable for a target video platform or project if used without review.

Mitigation: Review generated prompts, negative constraints, and continuity checks before submitting them to external video platforms.

Risk: The bundled helper script appears incomplete, so automated prompt generation may fail or produce partial output.

Mitigation: Use the Markdown workflow as the primary guidance and test the helper script before relying on it in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atmosphere16happy/skills/ai-video-prompt)
- [Keyframe workflow examples](examples/keyframe_examples.md)
- [Prompt examples](examples/prompt_examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text prompts with structured keyframe, segment, and review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are optimized for Chinese prompt-writing workflows and should be reviewed before use on external video platforms.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
