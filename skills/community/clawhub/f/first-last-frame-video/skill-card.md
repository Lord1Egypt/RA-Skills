## Description:

Generate one short directed transition from an approved first frame to an approved last frame, turning two images into one clip that begins and ends on those images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative developers use this skill to turn two approved endpoint images into one short transition clip for transformations, product reveals, before-and-after stories, or scene changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request voice-management permissions beyond what video creation needs.

Mitigation: Review the requested account scopes before authorizing, prefer narrower permissions where available, and revoke device access when no longer needed; check for other Beatra skills sharing that connection before revoking it.

Risk: Uninstalling or disconnecting may disrupt other Beatra skills that share the connection.

Mitigation: Follow the uninstall and disconnect guide, check which skills use the shared connection, and avoid removing shared credentials until their remaining consumers are understood.

Risk: Selected endpoint media is uploaded to Beatra for processing.

Mitigation: Confirm the user is comfortable sending both selected images to Beatra and avoid uploading media they are not authorized to share.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/first-last-frame-video)
- [Beatra skill information](https://beatra.ai/skills/first-last-frame-video)
- [Workflow guide](references/workflow.md)
- [Installation and authorization](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Video, Text]

**Output Format:** [One generated video artifact or link with a concise Markdown result and review summary]

**Output Parameters:** [One transition clip from one first frame to one last frame]

**Other Properties Related to Output:** [Includes a post-result check of endpoint fidelity, motion, direction, duration, and audio when accessible.]

## Skill Version(s):

0.2.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
