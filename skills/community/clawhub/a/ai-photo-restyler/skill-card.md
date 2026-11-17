## Description:

Restyle supplied photos into a chosen illustration look while preserving recognizable features and carrying that style across a batch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn personal, pet, product, or travel photos into stylized artwork for avatars, portraits, sticker sets, posters, merchandise, and consistent content series.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection requests broader account permissions than the photo-restyling task needs, including voice management and unrelated paid media creation.

Mitigation: Review the full permission grant before connecting; the helper does not accept narrower authorization.

Risk: Selected photos leave the user's computer, and installation analytics are reported automatically.

Mitigation: Tell users where selected photos go and that analytics are reported; upload only photos they choose to share.

Risk: Image generation uses paid credits.

Mitigation: Confirm each request after presenting its current maximum charge.

Risk: Removing the package may leave the shared account connection active.

Mitigation: Revoke device access in the Beatra Console when access should end.

## Reference(s):

- [Photo Restyle Workflow](artifact/references/workflow.md)
- [Updates and Security](artifact/references/updates-and-security.md)
- [Beatra AI Photo Restyler](https://beatra.ai/skills/ai-photo-restyler)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)

## Skill Output:

**Output Type(s):** [Images, Guidance]

**Output Format:** [Generated image files with concise Markdown status and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation requires a supplied photo and confirmation before each paid request.]

## Skill Version(s):

0.2.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
