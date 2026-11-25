## Description:

Applies eight stylized video effects to existing footage using tested FFmpeg presets and HyperFrames or Remotion equivalents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT

## Use Case:

Video editors and developers can choose a look for footage they own or are licensed to use, then get matching preset values, FFmpeg commands, or composition guidance for effects such as glow, glitch, CRT, halftone, and distortion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment identifies a conditional supply-chain risk from invoking an unpinned `npx hyperframes` package.

Mitigation: Review the package invocation, trust the package source, and consider whether an unpinned release running with the agent's permissions is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vargai/skills/footage-effects)
- [FFmpeg Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html)
- [HyperFrames Media Treatment Recipes](https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/media-use/references/media-treatment-recipes.md)
- [Remotion Zoom Blur](https://www.remotion.dev/docs/effects/zoom-blur)
- [GPU Gems 3: Volumetric Light Scattering as a Post-Process](https://developer.nvidia.com/gpugems/gpugems3/part-ii-light-and-shadows/chapter-13-volumetric-light-scattering-post-process)
- [Source index](artifact/references/sources.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with FFmpeg commands and preset configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preset settings are scaled for frame size; render durations should be capped to the source clip.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
