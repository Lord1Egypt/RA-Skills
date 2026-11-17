## Description:

Edits images by applying AI face and portrait beautification adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhi43](https://clawhub.ai/user/wangzhi43)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure and run portrait beautification on user-provided images, including preset or custom adjustments for skin, face shape, eyes, teeth, and makeup-like effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an external native program that was not included for review.

Mitigation: Review the publisher, obtain explicit user approval before initialization, and only run the downloaded executable in an isolated environment when the source and expected behavior are acceptable.

Risk: The download flow uses an insecure token-based HTTP request and may expose tokens through URLs or logs.

Mitigation: Avoid sharing token values, inspect logs for accidental token disclosure, and prefer a corrected release that uses HTTPS, avoids tokens in URLs, and verifies downloaded executables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhi43/skills/bitsoul-face-beauty-pro)
- [Publisher profile](https://clawhub.ai/user/wangzhi43)
- [AI Coding Yard token portal](https://www.aicodingyard.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown instructions with shell commands and JSON beauty parameter files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local output directories containing edited image files.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
