# Apple Minimal — Design Brief

## Visual Identity

Apple Minimal embodies the philosophy that great design is the elimination of the unnecessary. Every pixel, every spacing value, every color choice earns its place through intentional restraint. The result is an interface that feels inevitable — like it couldn't have been designed any other way.

## Core Design Language

**Colors**: The palette is surgically precise. Apple Blue (#007AFF) is used sparingly — only for primary actions and focus states. The background is never pure white; it uses iOS System Gray 6 (#F2F2F7) to create subtle depth. Text follows Apple's strict hierarchy: Label (black), Secondary Label (60% opacity feel), Tertiary Label (muted gray). No decorative colors — every hue serves a function.

**Shapes**: Generous, consistent rounded corners. Cards use 16px, buttons 12px, and containers 20px. The rounding is soft enough to feel premium but not so large that it looks playful. Consistency is key — all cards share the same radius.

**Shadows**: Extremely subtle. Apple uses layered, barely-there shadows. The deepest shadow is still gentle — used only for modals and sheets. The goal is depth cues without the user noticing them.

**Typography**: SF Pro is non-negotiable. This is the defining characteristic of Apple's design language. Headings in SF Pro Display (optimized for larger sizes), body in SF Pro Text (optimized for reading). The scale uses odd numbers (15px, 17px, 20px) — Apple's unconventional but carefully calibrated sizes.

**Motion**: Fluid, natural-feeling animations. Apple uses a distinctive ease-in-out curve. Springs are subtle — elements overshoot slightly and settle. Transitions feel "weighty" rather than snappy. Duration is slightly longer than other styles (250ms default) to create a sense of quality.

## Key Visual Signatures

1. **Generous white space**: Padding is never tight. Apple uses 24-32px as the default content padding. Group sections with 8-12px separators, but never crowd elements.

2. **SF Pro typography**: The distinct letterforms of San Francisco — slightly condensed, highly legible, with subtle optical sizing. System font stack must include `-apple-system` as fallback.

3. **Glass blur navigation**: Navigation bars and tab bars use subtle backdrop blur (saturation + blur) to hint at content beneath without full transparency.

4. **Thin stroke icons**: Apple's iconography uses a 1.5px stroke weight — delicate, precise, never heavy. Phosphor icons with 'thin' style match this perfectly.

5. **Haptic-grade interactions**: Every button press and toggle should feel physical. Scale transforms on press (0.97), spring-based transitions, and clear active states.

## When to Adapt

- **Content-heavy apps**: Maintain the spacing philosophy but compress when necessary — Apple's own Mail app is denser than Settings
- **Dark mode**: Invert to true black (#000000) backgrounds with pure white text. Keep the blue accent unchanged
- **Web vs native**: On web, use slightly larger touch targets (44px minimum) and account for cursor hover states that don't exist on iOS
- **Data visualization**: Use the system color palette (iOS has predefined chart colors) — keep it simple, 4-6 colors max

## Anti-Patterns (avoid these)

- Don't use pure white (#FFFFFF) as the main background — always iOS System Gray 6 or similar
- Don't use serif fonts — this is distinctly sans-serif
- Don't add decorative gradients — colors should be solid and purposeful
- Don't use heavy/bold shadows — Apple shadows whisper, they don't shout
- Don't crowd elements — when in doubt, add more whitespace
- Don't use stroke widths above 2px for icons
