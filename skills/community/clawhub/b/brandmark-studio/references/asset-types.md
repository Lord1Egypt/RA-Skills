# Asset Types

## Logo (Master)

- **Primary deliverable**: The canonical version of the brandmark.
- **Contents**: Full symbol + wordmark (if applicable). All detail, all elements.
- **ViewBox**: Tight framing with minimal padding (2-5%).
- **Color**: Full color.
- **Use cases**: Brand presentations, website headers, large format, primary brand usage.
- **SVG requirements**: All grouping, all IDs, all detail. Production-ready master file.
- **Scalability check**: Must work at 512×512 and above. Detail should not feel excessive even at large sizes.

## Horizontal Logo

- **Layout**: Symbol left, wordmark right (or reversed for RTL contexts).
- **ViewBox**: Wide rectangle to accommodate full width.
- **Spacing**: Clear space between symbol and wordmark equal to 0.5×–1× symbol height.
- **Alignment**: Symbol and wordmark should optically align (not mathematically; adjust by eye).
- **Use cases**: Website headers, letterheads, business cards, narrow spaces.
- **Variations**: Compact version with tighter spacing may be needed for very narrow spaces.

## Stacked Logo

- **Layout**: Symbol top, wordmark below. Centered.
- **ViewBox**: Tall rectangle.
- **Spacing**: Generous vertical spacing between symbol and wordmark (1×–1.5× symbol height).
- **Alignment**: Centered. Both elements should be centered on the same vertical axis.
- **Use cases**: Square spaces, app splash screens, social media profiles, vertical signage.

## Icon

- **Simplified version**: Load `references/icon-simplification.md`.
- **Contents**: Symbol only. No text.
- **ViewBox**: Square, centered, minimal padding (5-10%).
- **Color**: Full color or brand color simplified.
- **Use cases**: UI icons, browser bookmarks, toolbars, small UI elements.
- **Scalability**: Must be clear at 32×32. Icon readability is critical.
- **Construction**: Often redrawn, not just scaled down from the master logo.

## Favicon

- **Further simplified**: Simplified from icon.
- **Contents**: Absolute minimal symbol. Often a single geometric shape or the most distinctive silhouette element.
- **ViewBox**: Square, centered, tight padding (2-5%).
- **Color**: Single-color or two-color maximum. Single-color preferred for maximum flexibility.
- **Use cases**: Browser tab, bookmark icon, browser history, search results.
- **Scalability**: Must read at 16×16. No gradients, no text, no fine lines.
- **Test**: View at actual 16×16. If not instantly recognizable, simplify further.

## App Icon

- **Simplified from icon**: Slightly more detail than favicon but still stripped.
- **Contents**: Symbol only. No text.
- **ViewBox**: Square, centered, generous padding (10-15%). The mark should not touch the edges because platform layers may add rounded corners.
- **Color**: Full color acceptable but no gradients, no complex effects.
- **Use cases**: Mobile app store, home screen, task switcher, app drawer.
- **Scalability**: Must read at 64×64 (app store listing) and 512×512 (app store featured).
- **Platform note**: The SVG itself should be square with no rounded corners. Platform-specific rounding (iOS squircle, Android adaptive icons, etc.) is applied by the platform layer, not the SVG.

## Avatar

- **Simplified from icon**: Similar to icon but may retain slightly more personality.
- **Contents**: Symbol only or stylized initial. No text phrases.
- **ViewBox**: Square, centered, generous padding (10-15%).
- **Color**: Full color or brand color.
- **Use cases**: Social media profiles, user accounts, chat apps, forum avatars.
- **Scalability**: Must read at 64×64 and 128×128. Should feel like the brand, not a generic placeholder.
- **Platform note**: Platforms often crop avatars to circles. Ensure the mark works when cropped to a circle; nothing critical should be near the edges.

## Badge

- **Contained mark**: Circular, crest, or shield form. Self-contained.
- **Contents**: Symbol + text (often curved around frame or inside). Frame is part of the mark.
- **ViewBox**: Sized to contain the full badge shape.
- **Color**: Often full color with metallic or textured effects (but keep SVG flat for scalability; effects can be added in raster exports).
- **Use cases**: Certifications, achievements, awards, team logos, stickers, patches.
- **Construction**: Frame and internal elements should be separate groups for flexibility. The badge should work without the frame (as a standalone symbol) and the frame should work without the content (as a blank template).

## Emblem

- **Institutional mark**: Similar to badge but more formal, heraldic, or institutional.
- **Contents**: Symbol + text (often ribbon or banner). Crest, shield, or circular frame.
- **ViewBox**: Sized to contain the full emblem.
- **Color**: Often limited palette (2-4 colors) for gravitas. Monochrome versions are common.
- **Use cases**: Government, universities, sports teams, military, traditional organizations, automotive.
- **Construction**: Highly structured. Frame, symbol, and text should be in separate groups. The emblem must work at medium sizes (64×64+) but is rarely needed at favicon size.

## Monogram

- **Letter-based mark**: Interwoven, overlapping, or stylized initials.
- **Contents**: 1-3 letters (typically brand initials). No separate symbol unless the letters form one.
- **ViewBox**: Tight framing around the letterforms. Usually square or slightly rectangular.
- **Color**: Often single-color or two-color. Luxury monograms may use gold/silver tones.
- **Use cases**: Fashion, luxury goods, personal brands, editorial, hospitality, premium services.
- **Construction**: Letterforms must be custom, not off-the-shelf font. Interweaving, ligatures, and negative space between letters are critical. Must work at small sizes (favicon is possible for simple monograms).
- **Readability**: The letters must be legible at medium sizes but can become abstract at very small sizes. Balance artistry with legibility.

## Icon Pack

- **System of icons**: Multiple icons sharing a unified visual language.
- **Contents**: Set of related icons (10-50+ depending on request).
- **ViewBox**: Each icon square, centered, consistent padding (10-15%).
- **Color**: Consistent palette across all icons. Usually single-color or two-color system.
- **Use cases**: UI/UX design, app design, website design, design systems.
- **Shared requirements**: Every icon in the pack must share:
  - **Geometry**: Same grid system, same proportions, same base shape language.
  - **Visual language**: Stroke vs fill, flat vs dimensional, outlined vs solid. Pick one and apply to all.
  - **Stroke weight**: If stroke-based, all strokes must be the same weight (or follow a consistent 1x/2x ratio).
  - **Spacing**: Consistent padding ratios. No icon should feel larger or smaller than others in the set.
  - **Corner treatment**: All sharp, all rounded, or a consistent system (e.g., outer corners rounded, inner sharp).
- **Construction**: Build on a grid (e.g., 24×24, 32×32). Use consistent construction methods. Do not mix stroke-based and fill-based icons in the same pack.
- **Scalability**: Each icon must be clear at 16×16 and 24×24 (standard UI sizes). Test the smallest and largest icons in the set at these sizes.
- **Variation**: Icons should feel related but not identical. Variety within the system is important. Avoid making every icon a variation of the same base shape.
