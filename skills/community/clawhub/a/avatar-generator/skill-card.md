## Description:

Generate customizable social media and profile avatars in multiple styles with local Pillow rendering and multi-platform export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create profile avatars for WeChat, QQ, Xiaohongshu, Twitter/X, Discord, and other social platforms. It supports letter, geometric, gradient, abstract, pattern, and badge-style avatars with platform-specific PNG exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gradient avatar generation depends on NumPy, but the documented dependency only lists Pillow.

Mitigation: Pin Pillow and add or remove NumPy before relying on gradient avatar output.

Risk: The skill writes avatar files to an output directory and can export multiple platform-specific files.

Mitigation: Specify the intended output directory and target platforms before generation so only expected avatar files are written.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/avatar-generator)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Python code and generated PNG avatar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local generation with Pillow; gradient avatars require NumPy even though the documented dependency only lists Pillow.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
