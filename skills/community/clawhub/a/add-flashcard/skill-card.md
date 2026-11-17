## Description:

Spaced repetition flashcard system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add or trigger spaced-repetition flashcards through the add flashcard command and related English or Chinese trigger phrases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unprovided local Python executor, so its real behavior cannot be verified from the package alone.

Mitigation: Install only after reviewing and trusting the exact local capability_executor.py, or bundle and pin the executor before normal use.

Risk: The skill references failure reporting and confidence tracking integrations whose data handling is not documented in the package.

Mitigation: Document telemetry and data-change behavior, then disable or constrain reporting integrations unless they are approved for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/add-flashcard)
- [Bilibili study link: geography flashcard app tutorial](https://www.bilibili.com/video/BV12ScqzqERN)
- [Bilibili study link: geography flashcard app with images](https://www.bilibili.com/video/BV12ScqzqESC)
- [Bilibili study link: flashcard app with images](https://www.bilibili.com/video/BV16hF5ztExA)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on a local capability executor that is not bundled with the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
