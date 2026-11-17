## Description:

Builds playable 2D Canvas or 3D Three.js browser games from natural-language requests and checks screenshots before delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game creators use this skill to create or refine browser games, verify their appearance with screenshots, and optionally publish them when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game projects are written persistently under ~/games and local verification commands run against them.

Mitigation: Use a workspace you trust and review generated files and verification results before sharing.

Risk: Publishing can make game files and included personal images, copyrighted assets, or secrets publicly accessible on a permanent URL.

Mitigation: Publish only after an explicit request, and review all game files and assets for sensitive or unlicensed content first.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/paradoxfuzzle/skills/build-game-plus)
- [Canvas2D patterns](reference/canvas2d-patterns.md)
- [3D engine patterns](reference/engine-patterns.md)
- [Graphics quality patterns](reference/graphics-quality.md)
- [Procedural asset patterns](reference/procedural-assets.md)
- [GUI patterns](reference/gui-patterns.md)
- [Audio patterns](reference/audio-patterns.md)
- [Game systems patterns](reference/game-systems.md)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, JSON, Guidance]

**Output Format:** [HTML/JavaScript game, Markdown progress notes, JSON verification report, and screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent local game files; optional public game URL only when requested.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
