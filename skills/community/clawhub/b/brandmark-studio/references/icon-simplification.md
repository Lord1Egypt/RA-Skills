# Icon Simplification Engine

## Purpose

When a logo or brandmark is created, automatically generate simplified icon versions that preserve the core identity while stripping away detail that fails at small sizes. The icon must remain recognizable at favicon scale (16×16).

## Simplification Workflow

1. **Analyze the master mark**: Identify the primary symbol, the silhouette, and the core visual metaphor.
2. **Determine reduction level**: How far must this mark be simplified to read at 16×16?
3. **Preserve critical elements**: Keep only what makes the mark identifiable.
4. **Remove non-critical elements**: Strip everything that doesn't contribute to recognition.
5. **Verify at 16×16**: Mentally or actually test the simplified mark at favicon size.
6. **Generate outputs**: Produce Icon, Favicon, Avatar, and App Icon variants.

## Preservation Rules

These elements must be retained in the simplified version:

- **Primary symbol**: The most recognizable and unique element of the mark. The thing that makes it "this brand and not another."
- **Silhouette**: The overall outer shape. If the silhouette changes, the mark becomes unrecognizable.
- **Negative space**: The defining cutouts and holes that shape the mark. These often carry as much identity as the positive form.
- **Core visual metaphor**: The abstract or concrete idea the mark communicates. If the mark is a bird, it must still read as a bird.

## Removal Rules

These elements must be removed or dramatically reduced:

- **Fine detail**: Hairlines, thin strokes, intricate patterns, small dots, thin gaps. Anything that closes up or disappears below 32×32.
- **Texture**: Grain, noise, stippling, halftone, distressed effects, pattern fills. These become visual noise at small sizes.
- **Decorative elements**: Flourishes, ornamental borders, non-essential stars, dots, or accents. Keep only if they define the silhouette.
- **Atmospheric effects**: Glows, shadows, gradients, dimensional shading. Convert to flat fills.
- **Tiny shapes**: Elements smaller than 2×2 pixels at 16×16. These either vanish or become distracting noise.
- **Text / letterforms**: Remove text unless the text IS the mark (e.g., a monogram). For symbol+wordmark logos, drop the wordmark entirely in the icon version.
- **Multiple overlapping colors**: Reduce to 2-3 colors maximum. Prefer single-color for favicon.
- **Gradients**: Convert to flat color. Gradients muddy at small sizes and add complexity.

## Size-Specific Optimization

### Favicon (16×16)
- **Color**: Single color or two-color maximum.
- **Detail**: Absolute minimum. The mark should be reducible to a simple geometric shape.
- **Negative space**: Holes and gaps must be large enough to survive; if a gap closes at 16×16, merge the shapes.
- **Approach**: Often requires re-drawing the mark as a simplified abstraction rather than just scaling down.
- **Test**: View at actual 16×16. If it takes more than 1 second to identify, simplify further.

### Icon (32×32)
- **Color**: 2-3 colors maximum.
- **Detail**: Minimal. Primary symbol only, no secondary elements.
- **Negative space**: Gaps must be clearly visible at 32×32.
- **Test**: View at 32×32. Should be instantly recognizable.

### Avatar (64×64)
- **Color**: 3-4 colors acceptable.
- **Detail**: Slightly more detail than icon but still stripped of texture and decoration.
- **Test**: View at 64×64. Should feel like the brand, not a generic placeholder.

### App Icon (64×64 to 512×512)
- **Color**: Full color acceptable, but still no gradients or complex effects.
- **Detail**: Simplified but slightly more complete than the icon version. The app icon version may be the same as the icon version for many brands.
- **Padding**: 10-15% padding within the square viewBox. The mark should not touch the edges.
- **Test**: View at 64×64 and 512×512. Should be clear at both sizes without feeling empty at large or crowded at small.

## Simplification Examples by Archetype

| Archetype | Master Mark | Icon Version | Favicon Version |
|-----------|-------------|--------------|-----------------|
| Hero (lion shield) | Detailed lion in shield | Lion silhouette only | Shield shape with lion head silhouette |
| Explorer (compass mountain) | Compass with mountain scene | Compass arrow + mountain peak | Mountain peak triangle |
| Sage (owl book) | Owl perched on open book | Owl head silhouette | Owl eyes in circular face |
| Creator (brush lightbulb) | Brushstroke forming lightbulb | Simplified lightbulb | Lightbulb silhouette |
| Ruler (crown laurel) | Crown with laurel wreath | Crown silhouette | Crown peak shape |

## Common Mistakes in Simplification

- **Over-simplifying**: Removing so much that the mark becomes generic and loses brand identity.
- **Under-simplifying**: Keeping too much detail so the mark becomes a muddy blob at 16×16.
- **Changing proportions**: Simplifying but stretching or compressing the silhouette, changing the mark's character.
- **Adding complexity**: "Simplifying" by replacing detail with gradients, shadows, or effects.
- **Ignoring negative space**: Filling in gaps that define the mark's identity.
- **Keeping text**: Trying to include wordmarks in a 16×16 favicon.

## Favicon-Specific Requirements

- Must be a simplified, abstracted version of the primary symbol.
- No text, no gradients, no complex multi-color scenes.
- Single-color or two-color maximum. Single-color preferred for maximum flexibility.
- Strong silhouette that reads instantly in a browser tab.
- Works on both light and dark backgrounds (test on both).
- Consider creating a small colored dot or geometric variant if the full mark simply cannot simplify enough.
