# HyperFrames Animation Guide — GSAP Seekable Timelines

## Timeline Contract

Every composition MUST follow these rules:

```javascript
// 1. Create paused timeline
const tl = gsap.timeline({ paused: true });

// 2. Add tweens
tl.from("#title", { opacity: 0, y: 60, duration: 0.8, ease: "power3.out" }, 0.2);

// 3. Register with composition ID
window.__timelines = window.__timelines || {};
window.__timelines["my-composition-id"] = tl;
```

## Non-Negotiable Rules

1. **Always `{ paused: true }`** — player controls playback via seeking
2. **Always register** to `window.__timelines["<data-composition-id>"]`
3. **Duration from `data-duration`** — NOT from timeline length
4. **No `repeat: -1`** — calculate: `repeat: Math.ceil(duration / cycleDuration) - 1`
5. **No randomness** — no `Math.random()`, `Date.now()`. Use seeded PRNG (mulberry32)
6. **No async construction** — no `setTimeout`, `await`, Promises. Timeline must be built synchronously
7. **Only animate visual properties**: `opacity`, `x`, `y`, `scale`, `scaleX`, `scaleY`, `rotation`, `color`, `backgroundColor`, `borderRadius`, transforms
8. **Never animate**: `visibility`, `display`, `width`/`height` on video elements
9. **Never call**: `video.play()`, `audio.play()`, `.pause()`, `.seek()`
10. **No `gsap.set()` on elements from later scenes** — they don't exist at page load. Use `tl.set(selector, vars, timePosition)` instead
11. **No `<br>` in text** — let text wrap via `max-width`

## Entrance Animations (gsap.from)

Animate FROM hidden/offscreen TO the CSS position:

```javascript
// Fade up
tl.from("#title", { opacity: 0, y: 60, duration: 0.7, ease: "power3.out" }, 0.2);

// Fade in from left
tl.from("#subtitle", { opacity: 0, x: -40, duration: 0.5, ease: "power2.out" }, 0.4);

// Scale in
tl.from("#logo", { opacity: 0, scale: 0.8, duration: 0.4, ease: "back.out(1.7)" }, 0.5);

// Stagger group
tl.from(".feature-item", {
  opacity: 0, y: 30, duration: 0.5, ease: "power2.out",
  stagger: 0.12
}, 0.8);
```

## Exit Animations (gsap.to) — FINAL SCENE ONLY

```javascript
// Only on the LAST scene
tl.to("#final-title", { opacity: 0, y: -30, duration: 0.4, ease: "power2.in" }, 8.5);
tl.to("#final-cta", { opacity: 0, duration: 0.3, ease: "power1.in" }, 8.7);
```

## Easing Reference

| Ease | Feel | Use For |
|------|------|---------|
| `power2.out` | Smooth deceleration | General entrances |
| `power3.out` | Snappy arrival | Titles, hero elements |
| `power4.out` | Very punchy | Impact moments |
| `expo.out` | Dramatic arrival | Big reveals |
| `back.out(1.7)` | Slight overshoot | Playful elements, logos |
| `elastic.out(1, 0.3)` | Bouncy | Attention grabbers |
| `power2.in` | Smooth acceleration | Exits |
| `power3.in` | Quick departure | Fast exits |
| `none` (linear) | Constant speed | Progress bars, counters |

### Rules:
- Vary eases across entrance tweens — use at least 3 different eases per scene
- Don't repeat an entrance pattern within a scene
- Offset first animation 0.1–0.3s (never start at exactly t=0)

## Scene Transitions

### Hard Rules for Multi-Scene Compositions

1. **ALWAYS** use transitions between scenes — no jump cuts
2. **ALWAYS** entrance-animate every element via `gsap.from()`
3. **NEVER** exit-animate before a transition fires — the transition IS the exit
4. **ONLY** the final scene may have exit animations

### Crossfade (simplest)

```javascript
// Scene 1 content entrance
tl.from("#s1-title", { opacity: 0, y: 50, duration: 0.7, ease: "power3.out" }, 0.2);
// NO exit tweens on scene 1

// Crossfade: scene 1 fades out while scene 2 fades in
tl.to("#scene-1", { opacity: 0, duration: 0.8, ease: "power1.inOut" }, 4.5);
tl.from("#scene-2", { opacity: 0, duration: 0.8, ease: "power1.inOut" }, 4.5);

// Scene 2 content entrance
tl.from("#s2-title", { opacity: 0, x: -40, duration: 0.6, ease: "expo.out" }, 5.3);
```

### Slide/Wipe

```javascript
// Slide scene 1 off left, scene 2 in from right
tl.to("#scene-1", { x: "-100%", duration: 0.6, ease: "power2.inOut" }, 5.0);
tl.from("#scene-2", { x: "100%", duration: 0.6, ease: "power2.inOut" }, 5.0);
```

### Scale Transition

```javascript
tl.to("#scene-1", { scale: 0.9, opacity: 0, duration: 0.5, ease: "power2.in" }, 4.8);
tl.from("#scene-2", { scale: 1.1, opacity: 0, duration: 0.5, ease: "power2.out" }, 5.0);
```

## Timing Patterns

### Quick Hits (2-3s scenes — social media)
```javascript
// Fast stagger, short holds
tl.from("#text-1", { opacity: 0, scale: 1.2, duration: 0.3, ease: "power4.out" }, 0.1);
tl.from("#text-2", { opacity: 0, y: 30, duration: 0.3, ease: "power3.out" }, 0.3);
```

### Standard Pacing (4-6s scenes — product demos)
```javascript
tl.from("#title", { opacity: 0, y: 50, duration: 0.7, ease: "power3.out" }, 0.3);
tl.from("#subtitle", { opacity: 0, y: 30, duration: 0.5, ease: "power2.out" }, 0.7);
tl.from(".features", { opacity: 0, y: 20, stagger: 0.15, duration: 0.4 }, 1.2);
```

### Slow/Cinematic (6-10s scenes — brand videos)
```javascript
tl.from("#hero", { opacity: 0, scale: 1.05, duration: 1.5, ease: "power1.out" }, 0.5);
tl.from("#tagline", { opacity: 0, y: 40, duration: 1.0, ease: "power2.out" }, 2.0);
```

## Looping Animations (Finite)

```javascript
const duration = 10; // composition duration
const cycleDuration = 2; // one loop cycle
const repeatCount = Math.ceil(duration / cycleDuration) - 1;

tl.to("#pulse", {
  scale: 1.1,
  duration: 1,
  ease: "power1.inOut",
  yoyo: true,
  repeat: repeatCount
}, 0);
```

## Counter / Number Animation

```javascript
const counter = { val: 0 };
tl.to(counter, {
  val: 1000,
  duration: 2,
  ease: "power2.out",
  onUpdate: () => {
    document.getElementById("counter").textContent = Math.round(counter.val).toLocaleString();
  }
}, 1);
```

## Typography Animation (Stagger per character)

```javascript
// Split text into spans first (in HTML or JS)
const chars = document.querySelectorAll("#title .char");
tl.from(chars, {
  opacity: 0, y: 20, duration: 0.4,
  ease: "power2.out", stagger: 0.03
}, 0.5);
```

## Sub-Composition Animation Note

In sub-compositions loaded via `data-composition-src`, prefer `gsap.fromTo()` over `gsap.from()` for more predictable behavior:

```javascript
tl.fromTo("#element",
  { opacity: 0, y: 40 },
  { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" },
  0.2
);
```

## Size & Readability Rules

For rendered video (not web):
- Headlines: 60px+ minimum
- Body text: 20px+ minimum
- Data labels: 16px+ minimum
- Use `font-variant-numeric: tabular-nums` on number columns
- Avoid full-screen linear gradients on dark backgrounds (H.264 banding)
