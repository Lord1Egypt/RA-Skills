# H5 Interaction Design

Read this when the chosen format is H5 and the concept involves user interaction (tap, swipe, reveal, unlock, etc.). Skip for static or auto-play H5 gifts.

## Core Principle

In an interactive H5 gift, animation IS the emotion. The user's tap is a commitment — the response must reward that commitment with proportional delight. A tap that only changes a CSS class feels like clicking a broken button. A tap that triggers a cascade of motion, light, and surprise feels like magic.

## Emotion Escalation

Interactive gifts with sequential steps (unlock achievements, open envelopes, reveal cards) must build emotional intensity through escalating animation:

### Level 1: Early steps (1-3)
- subtle, satisfying micro-animations
- gentle transitions: fade-in, slight scale bounce, color shift
- small particle burst (4-8 particles)
- brief haptic-like visual pulse
- sound: soft click or chime if audio is present

### Level 2: Middle steps (4-6)
- more pronounced animations
- larger scale bounce, slight overshoot
- more particles (12-20), varied sizes
- glow or shimmer effects on unlocked elements
- maybe a brief screen shake or ripple
- previous unlocked items can react slightly (sympathetic animation)

### Level 3: Climax / Hidden reveal (final)
- MAXIMUM celebration
- full-screen effect: confetti rain, fireworks burst, or radial light explosion
- card/element should dramatically enter: bounce, shake, grow from center, or slam down
- screen flash or pulse
- all previous elements react (glow brighter, bounce once)
- text reveal with typewriter or fade-word-by-word effect
- hold the peak for 1-2 seconds before settling
- if there is a final message, delay it 0.5-1s after the climax so the user has a beat to absorb

## State Transition Design

Every interactive state change needs three phases:

1. **Exit old state** (0.1-0.2s): the locked/hidden element visually breaks, dissolves, or releases — the lock icon could shatter, fade with a puff, or fly away
2. **Transition** (0.2-0.4s): the moment of transformation — scale bounce, color bloom, glow ignition
3. **Enter new state** (0.3-0.5s): the unlocked element settles into its final form with a gentle overshoot

Do NOT skip the exit phase. A lock that simply disappears feels like a rendering glitch. A lock that shatters, dissolves, or pops feels like something happened.

## Specific Patterns

### Unlock / Reveal
- lock icon: shatter into 4-6 fragments that fly outward and fade
- card border: flash bright then settle to unlock color
- icon: scale 0→1.3→1 with slight rotation wobble
- badge: slide in from right with bounce

### Progress Bar
- fill should animate with momentum (ease-out, slight overshoot)
- color should intensify as progress increases
- at 100%: pulse glow effect, then settle

### Hidden / Secret Reveal
- initial reveal: dramatic entrance (grow from 0, bounce, shake 2-3 times)
- background: flash or dim-then-brighten
- confetti / fireworks: 40-80 particles, multiple colors, varied sizes, staggered timing
- the element itself should feel heavier/more important than the others (bigger card, thicker border, different background)
- text content should reveal progressively, not all at once

### Final Message / Emotional Landing
- delay 0.5-1s after the last interaction
- fade in word-by-word or line-by-line (not all at once)
- highlighted words should have their own entrance (scale pulse, color bloom)
- the final message area should feel like a separate emotional space (background shift, increased padding, visual separation)

## Anti-Patterns

- Tap does nothing visible for >0.1s → feels broken
- All steps have identical animation → feels robotic
- Climax has same energy as step 1 → anticlimactic
- Text appears all at once → no pacing, no build
- No transition between states → feels like a slideshow, not an experience
- Particles without variety (same size, same speed, same direction) → feels cheap
- Animation duration >1s per step → feels slow and tedious

## Visual Fidelity Rule

When the concept uses a real-world metaphor (tree, ocean, building, garden, sky), the H5 must make that metaphor visually convincing — not just symbolically present.

A single CSS vertical line does NOT look like a tree. A circle with an emoji does NOT look like a fruit. A gradient background does NOT look like an ocean.

If CSS alone cannot make the metaphor visually convincing, you must either:
1. Generate a background image that establishes the visual metaphor (see stage3-visual-strategy.md Background Asset Strategy)
2. Use detailed SVG illustrations inline
3. Simplify the concept to one that CSS CAN render convincingly (e.g. a data dashboard, a terminal screen, a document)

Do not ship an H5 where the concept promises a "tree" but the user sees a vertical line with circles attached.

### Layout Must Match Metaphor Physics

If the metaphor has physical direction (trees grow up, water flows down, timelines go left-to-right), the H5 layout must respect that direction:
- Trees: roots at BOTTOM, crown at TOP, growth animates upward
- Water: flows downward
- Growth: bottom to top
- Timeline: left to right or top to bottom
- Stack or pile: bottom-up accumulation

Getting the direction wrong breaks the metaphor immediately.

## Related References

- `{baseDir}/references/h5-design-philosophy.md` for anti-AI-slop design standards around typography, color, motion, and background quality
- `{baseDir}/references/h5-mobile-patterns.md` for mobile-first rendering patterns, safe areas, touch targets, and performance constraints

## Template Reference Map

Before writing H5 code, find the closest template in `{baseDir}/assets/templates/` and READ its full index.html:

All templates must be available locally at `{baseDir}/assets/templates/<name>/index.html`. They are text/code assets and should be installed with the skill rather than fetched remotely at runtime.

| Emotional register | Template | Key technique to study |
|---|---|---|
| Growth / blooming | tap-to-bloom | p5.js Plant class, trigger radius, per-character state |
| Dispersal / release | wind-scatter | Character physics, ring formation, fly-away velocity |
| Flow / continuity | text-river | Particle stream, canvas text rendering, flow direction |
| Melancholy / rain | rainy-night | Rain particle system, fog layers, ambient motion |
| Destruction / reveal | burn-reveal | Burn edge simulation, reveal mask, ember particles |
| Vulnerability | tear-stained-paper | Paper texture, water stain spread, ink bleed |
| Wistfulness | wet-letter | Water droplet physics, ink dissolution |
| Lightness / joy | o-balloons | Floating physics, string simulation |
| Ceremony / drag | drag-straighten | Drag interaction, crumple/smooth physics |

Adapt the technical approach (not content) to your concept. If no template matches the emotional register, pick the one with the closest technical requirements (e.g. particle systems, physics, growth animation) and study that.

Templates are craft references, not creative constraints. Use their techniques to build things they never imagined.
