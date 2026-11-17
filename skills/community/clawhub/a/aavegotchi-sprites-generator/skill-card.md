## Description:

Generate official-style Aavegotchi game sprites and animated GIFs with the upstream gotchi-generator package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent operators use this skill to generate Aavegotchi-style sprite PNGs, animated GIFs, and manifests from gotchi JSON payloads or CLI trait flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed input can write outside the chosen output folder.

Mitigation: Run the skill in a constrained working directory and avoid untrusted JSON until the ID path traversal issue is fixed.

Risk: Extreme GIF settings can exhaust resources.

Mitigation: Keep GIF generation within bounded scale and canvas settings, and process only trusted inputs until GIF scale limits are fixed.

Risk: Dependency behavior can drift if installs ignore the lockfile.

Mitigation: Honor the bundled lockfile when installing dependencies.

## Reference(s):

- [Skill page on ClawHub](https://clawhub.ai/aaigotchi/skills/aavegotchi-sprites-generator)
- [Upstream gotchi-generator source](https://github.com/aavegotchi/aavegotchi-game-sprites)
- [Wearables Alignment Report](references/wearables-alignment-report.md)
- [Sprite Name Aliases](references/sprite-name-aliases.json)
- [Trait Types](references/trait-types.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, JSON manifests, PNG sprite sheets, and animated GIF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default outputs include a sprite PNG path, GIF path when generated, manifest JSON path, success status, and missing layer warnings.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
