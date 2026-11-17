---
name: fec-motion-interaction
description: Use when designing, implementing, or reviewing frontend interaction motion, page transitions, scroll animation, Framer Motion, GSAP, Lottie, CSS animation, motion intensity, animation performance, reduced-motion behavior, or cinematic but accessible UI motion. Do not use for SVG-only path drawing, Canvas/WebGL rendering, or ordinary hover states; Chinese triggers include motion design, interactive effects, page transitions, scroll animation, Framer Motion, GSAP.
---

# Interactive effects

It is suitable for front-end animation tasks that need to design page transitions, scrolling narratives, component introductions, micro-interactions and feedback rhythms into maintainable, degradable and verifiable forms. Load [motion-patterns.md](references/motion-patterns.md) when a specific implementation pattern is required.

## Purpose

Choose the right animation tools, intensity, and quality gates for your front-end interface.

## Procedure

1. Determine animation responsibilities
   - First write down the user intention of the dynamic effect service: positioning, feedback, level changes, status confirmation, narrative guidance or brand memory.
   - The tool-based interface is restrained by default, and priority is given to ensuring scanning efficiency; the marketing page and work page can increase the rhythm, but cannot block the main information.
   - If animation is merely decorative and does not improve understanding, feedback or brand recognition, it should be deleted or replaced with a static visual treatment.
   - Loading, skeleton, toast, error prompts and success feedback belong to status communication; animations can only enhance the feedback rhythm and cannot replace text, semantics or visible status.

2. Choose a technical route
   - CSS transitions/keyframes: hover, focus, toast, simple entry and small status feedback.
   - Framer Motion: React state-driven, layout transitions, list orchestration, and interruptible component-level animations.
   - GSAP: timelines, scroll triggers, complex sequences and precise orchestration across elements.
   - Lottie: The icon or empty state animation output by the design tool is lazy loaded on demand.
   - CSS scroll-driven animation: Use when progressive enhancement is acceptable and legacy browser consistency is not required.

3. Define intensity levels
   - Level 1-2: Only uses 150-250ms opacity/transform, suitable for background, forms and high-frequency tools.
   - Level 3-4: Add short stagger, partial spring and lightweight reveal, suitable for dashboards, settings pages and management consoles.
   - Level 5-6: Add parallax, layout morph, and pointer response, suitable for product display and interactive homepage.
- Level 7+: To use scrolling narrative, fixed paragraphs or 3D/WebGL cooperation, the mobile version and reduced-motion downgrade must be done separately.
   - Scenario default values: public services, medical, financial and highly accessible products start from Level 1-2; SaaS tools and data backends start from Level 2-3; marketing pages, brand pages and portfolios can start from Level 4-6; only experimental activity pages or immersive narratives can consider Level 7+.
   - If the UI design process already has a motion intensity dial set up, use that dial; don’t automatically increase the intensity just because a certain motion library is introduced.

4. Establish performance boundaries
   - Only high-frequency animations `transform`, `opacity`, use `filter` and `clip-path` with caution.
   - GSAP, Lottie, Three.js, heavy animation components must be dynamically imported or isolated in leaf components.
- Sustained animations require pause conditions: invisible, tab hidden, user closed, low battery, or reduced motion.
   - Do not read and write layout synchronously on scroll events; use IntersectionObserver, ScrollTimeline, or throttled rAF.
   - Scroll narrative, stagger, spring, magnetic pointer and parallax effects must have clear responsibilities respectively; do not stack multiple high-intensity motion languages on the same screen at the same time.
   - The rhythm of repeated reveal animations on long pages must be controlled to avoid each block entering with the same delay, direction, and easing, causing a template feel and scrolling fatigue.

5. Design for accessible degradation
   - All non-essential motion effects read `prefers-reduced-motion` and downgrade to static, fade-in or instant state.
   - If the automatic playback or looping animation exceeds 5 seconds, a pause method should be provided or it should only run in local non-critical areas.
   - Do not flash more than 3 times per second; do not use animation as the only status reminder.
   - The focus ring, error prompt, and success feedback must be equally clear when there is no animation.
   - Gesture animations must be replaced by clicks, keyboards, or explicit controls; dragging, sliding, and long-pressing cannot be the only operation paths.

6. Verify delivery
   - Check whether the animation blocks the copy, button or table content at 375px, 768px, and 1440px.
   - Check whether the first loaded bundle is significantly bloated by the animation library.
   - Turn on reduced motion manually and confirm that the animation is disabled or weakened.
   - Confirm scrolling and key interactions without noticeable frame drops using the performance panel or actual device.
   - Check that the animation intensity matches the page type: the workbench should not have a marketing-style scrolling theater, and the portfolio should not only have a default hover fade-in.
   - Verify that scroll trigger sequences allow users to reach content quickly without losing context due to pinned blocks, long timelines, or uninterruptible transitions.

## Constraints

- Do not mix Framer Motion and GSAP controls for the same element within the same component.
- Don’t use animations to cover up missing statuses such as loading, empty, error, disabled, etc.
- Do not add large parallax or scroll hijacking by default for ordinary background tables, configuration pages and high-frequency workbench.
- Do not use the same reveal template for all blocks; the rhythm of the animation should vary with the information level and user tasks.
- Do not animate `width`, `height`, `top`, `left`, `margin`, `padding` and other properties that frequently trigger layout.
- Do not put large Lottie JSON, GSAP plug-ins or 3D scenes into the above-the-fold sync package.
- Don't let animations change reading order, focus order, or keyboard accessibility.
- Do not use skeleton for a long time to cover up the actual loading failure; when it exceeds expectations, it should be transferred to an understandable loading, retry or error state.

## Expected Output

The output should include animation purpose, technology selection, intensity level, degradation strategy, performance boundaries and verification results. Post-completion interactions help users understand state and hierarchy, remain available on reduced-motion and low-end devices, and do not significantly slow down the above-the-fold or scrolling experience.
