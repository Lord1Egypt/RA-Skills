# Platform Routing - Animate

Choose the highest-level abstraction that solves the job before dropping lower.

## Flutter
Start with:
- `AnimatedContainer`, `AnimatedOpacity`, `AnimatedAlign`
- `AnimatedSwitcher` for content swaps
- `TweenAnimationBuilder` for small custom ranges
- `Hero` for shared-element navigation
Drop lower only when needed:
- `AnimationController` for explicit choreography
- physics-based motion when user input or gesture momentum matters
Avoid:
- manual controllers for simple one-state transitions
- rebuilding large trees every tick

## React and Next.js
Start with:
- CSS transitions for simple state changes
- Motion presence and layout primitives for enter, exit, and shared layout
- router-safe page transitions that respect streaming and hydration boundaries
Drop lower only when needed:
- custom spring choreography across multiple surfaces
- gesture libraries or scroll-linked systems for interaction-heavy screens
Avoid:
- route transitions that fight Suspense, hydration, or async data
- mixing CSS, Motion, and GSAP on one surface without a clear owner

## SwiftUI
Start with:
- `withAnimation`
- implicit state-driven transitions
- `contentTransition`
- `matchedGeometryEffect`
Drop lower only when needed:
- custom springs and phase-based animation
- UIKit bridging for capabilities SwiftUI does not cover cleanly
Avoid:
- mixing unrelated animation styles inside one flow
- forcing identical motion when platform-native behavior reads better

## Jetpack Compose
Start with:
- `animate*AsState`
- `AnimatedVisibility`
- `AnimatedContent`
- `updateTransition`
Drop lower only when needed:
- `Animatable`
- low-level drawing or gesture-linked motion
Avoid:
- lower-level APIs when high-level transitions already model the state change
- non-lambda modifiers for frequently changing animated values

## React Native
Start with:
- `Animated` for common transitions
- layout-safe primitives for enter, exit, and presence
- worklet or native-thread paths for gesture-heavy motion
Drop lower only when needed:
- hand-written JS-thread choreography for non-critical or prototype-only effects
Avoid:
- critical motion that depends on busy JS thread timing
- mixing multiple motion engines on one surface without reason

## Web
Start with:
- CSS transitions on `transform` and `opacity`
- keyframes or View Transitions for short deterministic sequences
- framework-native transitions in Vue, Svelte, or router layers before GSAP
Avoid:
- `transition: all`
- animating layout properties when transform can express the same change
- scroll effects that ignore reduced-motion settings
