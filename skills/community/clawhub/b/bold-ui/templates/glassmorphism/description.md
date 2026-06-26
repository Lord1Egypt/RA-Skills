# Glassmorphism — Design Brief

## Visual Identity

Glassmorphism creates interfaces that feel like they're made of frosted glass floating in colorful space. Elements are translucent, layered, and luminous — as if light is passing through them. The background isn't a flat color but a canvas of vibrant, blurred gradients and soft orbs of color. It's premium, modern, and undeniably visually striking.

## Core Design Language

**Colors**: The background is the star — not a solid color but a deep gradient canvas (#0F0F23) punctuated by large blurred color orbs. Indigo, purple, and pink orbs float in the background, creating a sense of depth and atmosphere. Glass surfaces use semi-transparent white (5-8% opacity) with a subtle white border (12-18% opacity) — this is what creates the "glass" illusion.

**Shapes**: Large, generous rounded corners (12-24px). The softness complements the ethereal glass effect. Glass cards should feel like modern architectural glass panels — clean edges, smooth curves, transparent depth.

**Shadows**: Glass elements cast soft, dark shadows — not for depth cues but to separate the glass from the background. Since the background is already colored, shadows need more spread (bigger blur radius) to work. No colored glows — the background provides the color.

**Typography**: Clean sans-serif (Inter) in white — text must contrast against potentially colorful backgrounds. Light text (white at 50-75% opacity) for secondary content. The glass surface itself provides some contrast, but text should still be clearly readable.

**Motion**: Smooth and floaty. Glass cards feel weightless — hover states can lift and scale subtly (scale 1.02) with a slow transition (250-400ms). The movement should feel like a physical glass panel being gently lifted.

## Key Visual Signatures

1. **Backdrop blur**: The defining CSS property — `backdrop-filter: blur(16px)` on all glass surfaces. This is what creates the frosted glass effect by blurring whatever is behind the element. Pair with `-webkit-backdrop-filter` for Safari support.

2. **Gradient orbs**: Large radial gradients positioned off-center in the background. These are NOT blurred — they're soft radial gradients that create the colorful "environment" that the glass reveals. Typically 2-4 orbs in complementary colors (indigo, magenta, purple).

3. **Glass borders**: Each glass element has a 1px solid border using `rgba(255, 255, 255, 0.18)`. This thin white line defines the glass edge. Combined with the subtle white background fill, it creates the illusion of a physical glass pane.

4. **Layered depth**: Stack glass cards with increasing blur and decreasing opacity for deeper layers. Foreground cards: 16px blur, 8% white fill. Background cards: 12px blur, 5% white fill. Modals: 24px blur, 10% white fill.

5. **Filled icons**: Use solid/fill style icons — they read better against translucent backgrounds than outline icons. Phosphor fill icons are ideal. Icon color should be white or the nearest orb color.

## When to Adapt

- **Light mode glass**: Change the background to light gradients (white to light blue/pink), glass surfaces become white at 70-80% opacity with blur, text becomes dark. This is harder to get right but can be stunning.
- **Accessibility**: For users with motion/contrast sensitivity, increase glass opacity to 15-20% and reduce blur to 8px. Add a solid background fallback for browsers without backdrop-filter support.
- **Mobile**: Reduce the number of background orbs, use smaller blur values (8-12px), and simplify layered depth. Mobile GPUs struggle with multiple backdrop-filter layers.
- **Data-heavy dashboards**: Use glass sparingly — only on cards/panels, not on the full page. Pair with solid dark surfaces for readability of charts and numbers.

## Anti-Patterns (avoid these)

- Don't use solid backgrounds for main content areas — the transparency is the point
- Don't use blur values below 8px — it looks like a mistake, not glass
- Don't put glass elements against a flat/solid background — the depth effect requires visual texture behind
- Don't use dark text on glass (unless light mode) — low contrast kills readability
- Don't stack more than 3 layers of glass — it becomes muddy
- Don't forget the border — glass without a defined edge looks like a rendering bug
- Don't use sharp corners — glass should feel smooth and organic
