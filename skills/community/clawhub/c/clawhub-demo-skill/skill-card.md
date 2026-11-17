## Description:

Use this tiny demo skill to verify that a ClawHub skill can be published, installed, and invoked; it returns a short confirmation message and optionally echoes a user-provided phrase.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[colifire](https://clawhub.ai/user/colifire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to smoke test ClawHub publishing, installation, and invocation behavior by confirming the skill is active and optionally echoing a short phrase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation is enabled, so the skill may activate without an explicit skill mention in some agent contexts.

Mitigation: Keep the skill scope narrow, preserve the no-external-services and no-file-creation behavior, or disable implicit invocation in future versions if the behavior expands.

Risk: The release is quarantined for low quality and requires moderation review before listing.

Mitigation: Complete moderation review before public listing and confirm the skill remains limited to smoke-test confirmation behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colifire/skills/clawhub-demo-skill)
- [Publisher profile](https://clawhub.ai/user/colifire)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one concise confirmation sentence and may include one user-provided phrase.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
