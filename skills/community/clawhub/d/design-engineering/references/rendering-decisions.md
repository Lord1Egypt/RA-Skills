# Rendering Technology Decisions

Production-tested guidance for choosing between CSS, SVG, and Canvas for visual effects.

## Decision Matrix

| Criteria | CSS background-image | Inline SVG | Canvas 2D | WebGL/Three.js |
|----------|---------------------|------------|-----------|----------------|
| Static patterns | ✅ Best | ✅ Good | Overkill | Overkill |
| <50 animated elements | ❌ Jittery | ✅ Best | Good | Overkill |
| 50-200 animated elements | ❌ | ⚠️ DOM overhead | ✅ Best | Good |
| >200 animated elements | ❌ | ❌ Jank | ✅ Best | ✅ Best |
| Procedural generation | ❌ | ❌ Impractical | ✅ Best | ✅ Good |
| Parallax scroll | ❌ Broken on iOS | ⚠️ Complex | ✅ Native | ✅ Native |
| Glow/blur effects | Limited | ✅ SVG filters | ✅ shadowBlur | ✅ Post-processing |
| No-JS fallback | ✅ Built in | ✅ Built in | ❌ Needs JS | ❌ Needs JS |
| HiDPI | ✅ Auto | ✅ Auto | Manual (dpr) | Manual |
| Bundle size | 0KB | 0KB | 0KB (native) | 500KB+ (Three.js) |

## Critical Lesson: SVG in background-image Cannot Animate

**This is the #1 trap.** SVG embedded as `background-image: url("data:image/svg+xml,...")` is sandboxed:
- Browser treats it as a static image (security restriction)
- SMIL animations may run but execute on main thread, outside compositor → jitter
- CSS animations on SVG elements inside background-image are NOT GPU-composited
- `animateMotion`, `animate`, CSS `@keyframes` — all unreliable in this context

**Rule**: Animated SVG must be inline `<svg>`. Static-only SVG can be background-image.

## SVG `preserveAspectRatio` Pitfall

When an SVG viewBox doesn't match its container:
- `preserveAspectRatio="none"` → stretches content. Circles become ovals. Paths warp.
- Default (`xMidYMid meet`) → maintains ratio, letterboxes
- `xMinYMin slice` → maintains ratio, crops excess

Always verify when SVG dimensions differ from container dimensions.

## Canvas Parallax Architecture

The proven pattern for full-page animated backgrounds:

```
position: fixed canvas → reads window.scrollY → draws layers at different offsets
```

- Canvas stays fixed, covers viewport
- Each depth layer offsets by `scrollY × layerSpeed`
- Deep: 10% scroll speed, Mid: 25%, Near: 5%
- Wrap with modulo for seamless tiling: `offset = -(scrollY * speed % virtualHeight)`
- Draw everything twice (at offset and offset + virtualHeight) for seamless wrap

## Canvas Resize Trap

`buildScene()` on resize randomizes all procedurally-generated elements → visual jump.

Fix:
```js
function setupCanvas(regenerateScene) {
  // Always resize the canvas dimensions
  // Only regenerate scene geometry if regenerateScene is true
}
// On resize: only regenerate on width change, not height change
// Mobile address bars cause height changes constantly
```

## CSS Scroll Parallax (`animation-timeline: scroll()`)

Modern alternative to JS parallax. Runs on compositor thread — zero jank.

Browser support (March 2026): Chrome ✅, Edge ✅, Samsung ✅, Safari 26+ ✅, Firefox ❌ (flag only).

Pattern:
```css
@supports (animation-timeline: scroll()) {
  .bg-layer { animation: drift linear both; animation-timeline: scroll(root block); }
}
```
Always provide JS fallback for Firefox (~25% of users).

## Performance Rules of Thumb

- Canvas: 50-100 paths + 25-40 pulses = imperceptible on modern devices
- SVG: performance degrades noticeably above 100-200 animated elements
- `shadowBlur`: batch all glow draws, set once, reset once. Per-element toggle is expensive.
- `navigator.hardwareConcurrency < 4` → halve element counts
- `contain: layout paint style` on canvas wrapper for browser optimization hints
