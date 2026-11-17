#Interactive effect implementation mode

## CSS Microinteractions

```css
.action {
  transition:
    transform 180ms ease,
    opacity 180ms ease,
    background-color 180ms ease;
}

.action:hover {
  transform: translateY(-1px);
}

.action:active {
  transform: translateY(0) scale(0.98);
}

@media (prefers-reduced-motion: reduce) {
  .action {
    transition-duration: 1ms;
  }

  .action:hover,
  .action:active {
    transform: none;
  }
}
```

## Framer Motion component entry

```tsx
import { motion, useReducedMotion } from "framer-motion";

export function MotionPanel({ children }: { children: React.ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.section
      initial={reduceMotion ? false : { opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.24, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.section>
  );
}
```

## GSAP Timeline Cleanup

```tsx
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";

export function RevealTimeline() {
  const rootRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!rootRef.current) return;

    const context = gsap.context(() => {
      gsap
        .timeline({ defaults: { ease: "power2.out" } })
        .from("[data-title]", { opacity: 0, y: 16, duration: 0.28 })
        .from(
          "[data-item]",
          { opacity: 0, y: 10, stagger: 0.04, duration: 0.2 },
          "-=0.08",
        );
    }, rootRef);

    return () => context.revert();
  }, []);

  return (
    <div ref={rootRef}>
      <h2 data-title>Release health</h2>
      <div data-item>Build</div>
      <div data-item>Tests</div>
      <div data-item>Deploy</div>
    </div>
  );
}
```

## Heavy animation lazy loading

```tsx
import { lazy, Suspense } from "react";

const InteractiveShowcase = lazy(() => import("./InteractiveShowcase"));

export function ShowcaseSlot() {
  return (
    <Suspense fallback={<div aria-busy="true" />}>
      <InteractiveShowcase />
    </Suspense>
  );
}
```

## Review Checklist

- Animation goals can be described in one sentence and serve information level or status feedback.
- High throughput interface does not use scroll hijacking or long entry occlusion.
- The information is still complete under reduced-motion, and the focus and reading order do not change.
- The animation library is loaded on demand, and continuous animation can be paused or uninstalled for cleaning.
- Check for frame drops, text occlusion and above-the-fold bundle changes on key devices.
