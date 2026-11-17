## Description:

Generates deterministic pixel-art avatar SVG files from seed strings by running the pinned @bitmappunks/avatar-generator@0.0.5 package via npx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tt-u](https://clawhub.ai/user/tt-u)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate reproducible pixel-art SVG avatars from names, IDs, or other seed strings and save them to explicit local paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a pinned npm package through npx.

Mitigation: Keep the @bitmappunks/avatar-generator@0.0.5 pin, install only in environments where npm package execution is acceptable, and review package behavior before deployment.

Risk: The skill writes an SVG file at the requested output path.

Mitigation: Use explicit output paths in trusted workspaces and avoid paths that could overwrite important files.

Risk: The optional terminal preview helper reads SVG files from a provided path.

Mitigation: Use the preview helper only on SVG files generated or otherwise trusted by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tt-u/skills/bmp-avatar-generator)
- [Project homepage](https://github.com/bitmappunks-com/avatar-generator-skill)
- [@bitmappunks/avatar-generator npm package](https://www.npmjs.com/package/@bitmappunks/avatar-generator)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [SVG file plus concise text confirmation and optional ANSI terminal preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one SVG per seed; output is deterministic for a given seed while @bitmappunks/avatar-generator remains pinned to version 0.0.5.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
