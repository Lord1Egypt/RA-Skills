## Description:

Generates structured Chinese-language Markdown cheatsheets from built-in templates or a generic fallback, with guidance for saving the result as a Markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanwan2qq](https://clawhub.ai/user/wanwan2qq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create quick-reference Markdown documents for technical and general topics, including npm publishing, OpenClaw skill development, and common Git commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Git recovery advice may include destructive commands such as hard resets or force pushes.

Mitigation: Review the generated command sequence before copying it, especially for shared branches or work that has not been backed up.

Risk: Broad trigger phrases may activate the skill for generic manual, quick-reference, or configuration-guide requests.

Mitigation: Confirm the requested topic and intended scope before relying on the generated cheatsheet.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanwan2qq/skills/cheatsheet-generator)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks and checklist sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for user review before saving or copying commands.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact package.json and README list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
