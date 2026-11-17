---
name: fec-svg-animation
description: Use when implementing or reviewing SVG animation, path drawing, icon motion, logo animation, illustration motion, micro-interactions, CSS/SMIL/Framer Motion/GSAP choices, motion accessibility, or fallback behavior; Chinese triggers include SVG animation, path stroke, animation.
---

# SVG animation implementation

## Purpose

Provide maintainable, accessible, and performance-controllable animation solutions for SVG icons, illustrations, and data visualizations.

## When to Use

- SVG icon, logo, illustration or path stroke animation needs to be implemented.
- Framer Motion, GSAP or CSS animation needs to be connected to React/Vue components.
- Need to provide motion reduction according to `prefers-reduced-motion`.
- Not used for complex 3D/WebGL scenes; for such scenes, Canvas / Three.js workflow is preferred.

## Procedure

### 1. Select animation mode

Choose based on complexity and runtime requirements:

| Scenario | Recommendation |
| --- | --- |
| hover/focus、opacity、transform | CSS animation/transition |
| Path stroke, simple repeating animation | CSS + `stroke-dasharray` |
| React component state-driven animation | Framer Motion |
| Timeline, complex arrangement, scrolling trigger | GSAP |
| Need to keep static SVG with zero dependencies | CSS or SMIL |

If the animation spans page transitions, scrolling narratives, or complex component arrangements, you should first judge the intensity, lazy loading, and reduced-motion strategies according to the interactive effects workflow; this skill is only responsible for the path, deformation, and icon motion of the SVG graphics themselves.

### 2. Use CSS to implement path strokes

```tsx
export function CheckmarkIcon() {
  return (
    <svg viewBox="0 0 24 24" className="checkmark" aria-hidden="true">
      <path
        className="checkmark-path"
        d="M5 12.5l4.5 4.5L19 7"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
```

```css
.checkmark-path {
  stroke-dasharray: 24;
  stroke-dashoffset: 24;
  animation: draw-checkmark 420ms ease-out forwards;
}

@keyframes draw-checkmark {
  to {
    stroke-dashoffset: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .checkmark-path {
    animation: none;
    stroke-dashoffset: 0;
  }
}
```

### 3. Using Framer Motion in React

```tsx
import { motion, useReducedMotion } from "framer-motion";

export function AnimatedSparkline({ path }: { path: string }) {
  const reduceMotion = useReducedMotion();

  return (
    <svg viewBox="0 0 120 40" role="img" aria-label="Trend Chart">
      <motion.path
        d={path}
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        initial={reduceMotion ? false : { pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 1 }}
        transition={{ duration: 0.7, ease: "easeOut" }}
      />
    </svg>
  );
}
```

### 4. Use GSAP to orchestrate complex timelines

```tsx
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";

export function LogoReveal() {
  const rootRef = useRef<SVGSVGElement>(null);

  useLayoutEffect(() => {
    if (!rootRef.current) return;
    const ctx = gsap.context(() => {
      gsap.timeline({ defaults: { ease: "power2.out" } })
        .from(".logo-mark", { scale: 0.9, opacity: 0, duration: 0.25 })
        .from(".logo-line", { strokeDashoffset: 80, duration: 0.55 }, "-=0.1");
    }, rootRef);

    return () => ctx.revert();
  }, []);

  return (
    <svg ref={rootRef} viewBox="0 0 120 32" aria-hidden="true">
      <circle className="logo-mark" cx="16" cy="16" r="10" />
      <path className="logo-line" d="M36 16h68" stroke="currentColor" />
    </svg>
  );
}
```

### 5. Control operating costs

- Split large SVG into static basemaps and a small number of animatable nodes. Do not let each path participate in the timeline.
- Icon libraries or Lottie alternatives must be loaded on demand, without going into the base package for all pages.
- The loop animation only runs in the visible area and stops when the page is hidden or the component is unloaded.
- The mobile version reduces filters, masks, clipPaths and a large number of gradient overlays.

## Constraints

- Prioritize animation `transform`, `opacity` and SVG path attributes; avoid frequent modification of layout-related attributes.
- Interactive controls must retain the visible focus state, and animation cannot replace state expression.
- All non-decorative SVGs must have accessible names; decorative SVGs use `aria-hidden="true"`.
- Default respects `prefers-reduced-motion`, complex animations must provide static or weak motion degradation.
- Don't inline large SVGs into frequently re-rendered components; extract as memoized components or external resources.
- Change clickable area, reading order or focus position without animation.
- Don't let SVG filters, blur, mask or clipPath become the main cause of frame drops on mobile devices; complex effects require device downgrading.

## Expected Output

Produce a reusable SVG animation component or style solution, including selection reasons, animation degradation and accessibility processing. During verification, check that the animation is smooth, there is no layout jitter, and keyboard and reduced-motion scenes are available.
