## Description:

Generates meaningful conventional commit messages from staged Git changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vexify-build](https://clawhub.ai/user/vexify-build)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft specific conventional commit messages from staged Git changes, with a short subject and explanatory bullet points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad commit-related wording may activate the skill unexpectedly.

Mitigation: Confirm that a commit message is wanted before reading staged changes.

Risk: Staged changes may contain sensitive information that enters the agent's context.

Mitigation: Review staged changes and avoid staging sensitive content before using the skill.

Risk: A drafted message may misrepresent the changes or their purpose.

Mitigation: Review the message against the staged diff before committing.

## Reference(s):

- [commit-ai on ClawHub](https://clawhub.ai/vexify-build/skills/commit-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Conventional commit subject with Markdown bullet-point body]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subject limited to 72 characters; body explains why the changes were made.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
