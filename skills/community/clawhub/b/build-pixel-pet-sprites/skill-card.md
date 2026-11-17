## Description:

Create aligned, production-ready chibi pixel-art virtual desktop pet sprite packages from character references or repair existing sprite packages whose subject drifts between frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmgongzhu](https://clawhub.ai/user/mmgongzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agent users use this skill to turn a character reference into aligned transparent pixel-art animation assets, package them for web delivery, or repair frame drift in an existing sprite package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts may trust manifest or configuration paths in ways that can read images or write generated files outside the intended package directories.

Mitigation: Use only trusted sprite configs and packages, run the workflow in a project-limited or disposable workspace, and review third-party sprite-manifest.json and package-config.json files before execution.

Risk: Generated sprite packages may have clipping, edge contamination, empty frames, incorrect dimensions, or persistent anchor jitter.

Mitigation: Run alignment and validation before delivery, inspect validation reports, and regenerate or add transparent padding when complete content cannot move without clipping.

## Reference(s):

- [Pixel-pet prompt patterns](artifact/references/prompting.md)
- [Package configuration](artifact/references/package-config.md)
- [ClawHub skill page](https://clawhub.ai/mmgongzhu/skills/build-pixel-pet-sprites)
- [Publisher profile](https://clawhub.ai/user/mmgongzhu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with commands, JSON configuration, generated asset paths, QA summaries, and packaging instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or describes aligned atlas files, transparent RGBA frames, action strips, sprite-manifest.json, GIF previews, ZIP packages, and validation reports.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
