# Pattern Card Template

Use this file as the shared skeleton for new or refactored pattern cards.

This template is intentionally lightweight. It should help OpenClaw understand the pattern quickly without pretending every pattern already has a finished implementation.

## Status

Choose one:

- `Scaffold only`
- `V0 reference-only`
- `V1 reference pattern with a reusable template`

## Template Status

Choose one:

- `reference-only`
- `template-backed`
- `hybrid`

## Reference Assets

- template: `../assets/templates/<template-id>/` or `none yet`
- reference_images: `../assets/examples/<pattern-id>/` or `none yet`
  Fetch first if missing: `bash {baseDir}/scripts/fetch-asset-bundle.sh "examples/<pattern-id>"`
- reference_videos: `../assets/examples/<pattern-id>/` or `none yet`
  Fetch first if missing: `bash {baseDir}/scripts/fetch-asset-bundle.sh "examples/<pattern-id>"`

If using reference images, prefer path-and-note references rather than embedded markdown images by default.

If using short reference videos, store them alongside the images and cite them by relative path plus a short note about what motion, timing, or alignment should be borrowed.

## Fit Scope

Primary:

- the pattern's most natural use cases

Stretch:

- nearby use cases it may still support if the deeper emotional logic fits

## Reference Use

State clearly that the card is a high-quality reference, not a fixed script.

OpenClaw should be free to:

- widen the apparent use case
- borrow only one mechanic or pacing idea
- remix it with other patterns
- change copy, composition, assets, and tone

OpenClaw should not:

- copy the demo text literally
- assume the first obvious mood is the only correct fit
- treat one implementation as the entire pattern

## Intended Use

Use for:

- ...

Short note on what this pattern is especially good at.

## Emotional Fit

Best for:

- ...

Can also work for:

- ...

Usually not ideal for:

- ...

## Narrative Role Fit

Strongest roles:

- ...

Sometimes works for:

- ...

Usually not ideal for:

- ...

## Interaction Grammar

Core mechanic:

- ...

Supporting mechanic:

- ...

Short note on the emotional logic of the interaction.

## Visual Logic

- ...
- ...
- ...

## Content Strategy

OpenClaw should adapt:

- ...

Good source structures:

- ...

Avoid:

- ...

## Tone Guidance

Good tones:

- ...

Can also support:

- ...

Avoid:

- ...

## Reference Images

Use this section when screenshots or visual fragments are important.

Preferred format:

- `../assets/examples/<pattern-id>/ref-01.png`
  Bundle: `See references/asset-manifest.json for the matching OSS bundle key`
  - what to borrow: ...
  - do not copy literally: ...

- `../assets/examples/<pattern-id>/ref-02.png`
  Bundle: `See references/asset-manifest.json for the matching OSS bundle key`
  - what to borrow: ...
  - do not copy literally: ...

If no reference images exist yet, say:

- `none yet`

## Reference Videos

Use this section when short videos communicate motion, timing, layering, or alignment better than still images.

Preferred format:

- `../assets/examples/<pattern-id>/ref-03.mp4`
  - what to borrow: ...
  - do not copy literally: ...

- `../assets/examples/<pattern-id>/ref-04.mp4`
  - what to borrow: ...
  - do not copy literally: ...

If no reference videos exist yet, say:

- `none yet`

## Customization Knobs

- ...

## Implementation Notes

- ...

## Good Use Cases

- ...

## Risks

- ...

## Related References

- `./gift-mechanics.md`
- `./h5-visualizer-workflow.md`
- `../assets/templates/<template-id>/` or `none yet`
