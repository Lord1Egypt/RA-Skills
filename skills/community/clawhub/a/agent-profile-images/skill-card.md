## Description:

Agent Profile Images for OpenClaw Control UI adds custom avatar upload, themed AI profile image generation, preview-before-save controls, and avatar persistence across refreshes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add agent profile image controls to the OpenClaw Control UI, including image upload, AI-generated avatar previews, save/remove actions, and persisted avatar display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes broad OpenClaw gateway and UI source snapshots beyond the avatar feature.

Mitigation: Review the referenced snapshots before installation and apply only the avatar-related diffs needed for the release.

Risk: Avatar upload writes user-supplied image data into agent workspaces.

Mitigation: Before shared or exposed use, harden upload validation and keep strict limits on accepted image type, size, and workspace path handling.

Risk: AI avatar generation sends prompt context and user-provided generation instructions to OpenAI.

Mitigation: Disclose OpenAI data sharing to users and enable generation only where external image-generation processing is acceptable.

## Reference(s):

- [Skill package overview](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/agent-profile-images)
- [Gateway avatar methods snapshot](artifact/references/src-gateway-server-methods-agents-ts.txt)
- [Avatar protocol schema snapshot](artifact/references/src-gateway-protocol-schema-agents-models-skills-ts.txt)
- [Control UI avatar action wiring snapshot](artifact/references/ui-src-ui-app-render-ts.txt)
- [Agents overview profile image UI snapshot](artifact/references/ui-src-ui-views-agents-panels-overview-ts.txt)
- [Avatar persistence and resolution snapshot](artifact/references/src-gateway-session-utils-ts.txt)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown skill instructions with TypeScript implementation snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The package describes source-level OpenClaw gateway and Control UI changes for avatar upload, generation, removal, preview, and persistence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
