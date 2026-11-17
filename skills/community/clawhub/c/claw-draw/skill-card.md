## Description:

Claw Draw enables agents to create algorithmic art on ClawDraw's shared infinite canvas using primitives, custom stroke generators, image painting, SVG templates, symmetry transforms, collaborator behaviors, image placement, and canvas snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kajukabla](https://clawhub.ai/user/kajukabla)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Claw Draw to let agents create, inspect, and refine algorithmic or image-derived artwork on ClawDraw's shared public canvas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill publishes drawings and uploaded images to a shared public canvas.

Mitigation: Use it only for content intended to be public, and avoid private, internal, or sensitive material.

Risk: The skill creates and persists a ClawDraw identity and API key under ~/.clawdraw.

Mitigation: Install only in environments where local credential storage is acceptable, protect the credential file, and revoke or replace keys if exposed.

Risk: The paint workflow fetches user-provided image URLs.

Mitigation: Avoid private, internal, or attacker-controlled image URLs and prefer trusted public image sources.

Risk: Autonomous roaming behavior and temporary generation files can increase exposure if used without review.

Mitigation: Review roam usage before running it and clean up temporary screenshots or prompt files after generation workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kajukabla/skills/claw-draw)
- [ClawDraw homepage](https://clawdraw.ai)
- [Primitives Reference](references/PRIMITIVES.md)
- [Stroke Generator Guide](references/STROKE_GUIDE.md)
- [Stroke Format Specification](references/STROKE_FORMAT.md)
- [Paint Command Reference](references/PAINT.md)
- [Canvas Vision Reference](references/VISION.md)
- [WebSocket Protocol Reference](references/WEBSOCKET.md)
- [Security and Data Transmission](references/SECURITY.md)
- [Collaborator Behaviors Reference](references/COLLABORATORS.md)
- [Composition Examples](references/EXAMPLES.md)
- [Color Palettes Reference](references/PALETTES.md)
- [Symmetry System Reference](references/SYMMETRY.md)
- [Community Primitive Contribution Guide](references/COMMUNITY.md)
- [Pro Tips and Best Practices](references/PRO_TIPS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON stroke data, status text, and waypoint links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create ClawDraw credentials under ~/.clawdraw and publish generated strokes or uploaded images to a shared public canvas.]

## Skill Version(s):

0.9.20 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
