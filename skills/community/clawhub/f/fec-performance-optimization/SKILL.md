---
name: fec-performance-optimization
description: Use when diagnosing or improving frontend performance, Core Web Vitals, bundle size, runtime rendering cost, network waterfalls, memory leaks, long tasks, Lighthouse findings, or performance budgets; Chinese triggers include performance optimization, page freeze, slow first screen, bundle volume, Web Vitals.
---

# Front-end performance optimization

## Purpose

Use measurable methods to locate front-end performance bottlenecks, and converge optimization suggestions to the user's main path, build products, and runtime evidence.

## Procedure

1. Lock in experience goals
   - Clarify whether the problem is first screen loading, interaction delay, scrolling lag, memory increase, network waterfall, packet size, or visual stability.
   - Document routes, devices, network conditions, browsers, replication steps, and currently available metrics.
   - When there are no indicators, establish a baseline first and do not directly give generalized suggestions of "optimizing everything".

2. Establish a measurement baseline
   - Read project scripts, build configurations, dependencies and existing performance reports.
   - Prioritize the use of Lighthouse, Performance trace, React Profiler, Vue Devtools, Memory snapshot or RUM data for page experience.
   - Prioritize build products, source maps, dependency duplication, first-screen chunks and dynamic import boundaries for package bodies.
   - Prioritize long tasks, repeated renderings, expensive calculations, synchronized loops, layout jitters and large lists for runtime lags.
   - If there are online monitoring, platform indicators or CI products, first use them to confirm the affected routes, devices, time windows and user main paths, and then decide which source code to read.

3. Hierarchical positioning
   - Loading layers: critical CSS, fonts, images, script blocking, preloading and caching.
   - Rendering layer: unstable keys, too wide Context, meaningless effects, repeated calculations, and component trees that are too large.
   - Data layer: serial requests, repeated requests, too large payload, lack of paging or caching strategy.
   - Main thread: JSON/CSV parsing, image processing, complex sorting and filtering, synchronous compression and large object deep copy.
   - Resource layer: event listeners, timers, subscriptions, WebGL/Canvas resources and object URLs are not released.

4. Form an optimization plan
   - Each suggestion must be bound to location, impact, modification and verification method.
   - Prioritize the high-frequency main path and P95 experience; low-frequency background tasks do not occupy the first screen budget.
   - Make low-risk, high-yield changes first, such as lazy loading, deduplication, caching, size reservation, virtual lists, stable references and releasing resources.
   - For techniques that sacrifice maintainability, evidence of benefits and alternatives must be stated.
   - It is recommended to go through the candidate access control before entering the implementation: whether there is indicator support, whether the route/component/chunk/request can be located, whether it can be verified by the front end, and whether there are smaller changes.

5. Verify regression
   - Rerun affected build, test, and performance collection commands.
   - Compare indicators or product volumes before and after optimization.
   - Confirm that loading, empty, error, offline, reduced-motion and mobile state are not destroyed by optimization.

## Budgets

| Area | Default Target | Notes |
| ---- | -------------- | ----- |
| LCP | Within about 2.5s | Subject to core page, target area network and real device |
| CLS | Less than 0.1 | Media, advertising, and asynchronous content require reserved space |
| INP | Within about 200ms | Prioritize splitting long tasks and reduce interaction path re-rendering |
| Initial JS | Follow project budget | Report current gzip / brotli size first if there is no budget |
| Main thread | Avoid continuous long tasks | Consider sharding, caching or Worker for large calculations |

## Checks

- Whether the above-the-fold resources include non-above-the-fold components, charts, editors, maps, or full icon libraries.
- Whether the image has clear size, appropriate format, lazy loading and first screen priority.
- Whether lists, tables, and timelines require virtualization or paging.
- Whether searching, filtering, and sorting repeat O(n*m) scans on the hot path.
- Whether the request can be parallelized, cached, cancelled, and reusable.
- Whether listening, subscription, timer, AbortController, Object URL, Canvas/WebGL resources are cleaned symmetrically.

## Constraints

- Don’t do premature optimization without goals and evidence.
- Don’t trade off features, remove status feedback, or reduce accessibility in exchange for performance points.
- Do not sacrifice real user home paths for a single Lighthouse score.
- Solve small problems without introducing large new dependencies; first use the existing tools and browser capabilities of the project.
- Do not confuse back-end, network and browser-side issues; the parts that can be verified on the front-end should be separately documented.
- Do not jump directly from repo-wide grep to the optimization conclusion; first use indicators or recurrence paths to narrow down candidates, and then read the relevant source code.

## Detailed reference

When writing a performance analysis report, load [references/report-template.md](references/report-template.md).
When you need to locate framework-specific performance risks classified by React, Vue, Next.js or Nuxt, load [references/framework-performance-patterns.md](references/framework-performance-patterns.md).

## Expected Output

Output a performance analysis report with an evidence chain, describing the baseline, candidate access control, bottlenecks, optimization suggestions, verification methods and remaining risks. The report is saved as `reports/performance-review-YYYY-MM-DD-HHmmss.md`.
