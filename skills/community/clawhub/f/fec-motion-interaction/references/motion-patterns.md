# 交互动效实现模式

## CSS 微交互

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

## Framer Motion 组件入场

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

## GSAP 时间轴清理

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

## 重型动效懒加载

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

## 审查清单

- 动画目标能用一句话说明，且服务信息层级或状态反馈。
- 高吞吐界面不使用滚动劫持或长时间入场遮挡。
- reduced-motion 下信息仍完整，焦点与阅读顺序不变化。
- 动画库按需加载，持续动画可暂停或卸载清理。
- 关键设备上检查掉帧、文字遮挡和首屏 bundle 变化。
