# Content Pipeline and Asset Strategy

Use this file when content scale starts to dominate delivery speed.

## Asset Lifecycle

1. Intake: define source and licensing status
2. Normalize: enforce naming, units, and orientation
3. Optimize: compression and LOD generation
4. Integrate: register with content manifest
5. Validate: load-time and in-game checks

## Browser Asset Budgets

- Texture atlas strategy before importing many unique materials
- Audio split by purpose: short SFX in memory, music streamed
- Mesh simplification for mobile fallback variants

## Naming and Versioning Rules

- Stable IDs for gameplay-critical assets
- Human-readable names for production workflow
- Version tag for assets with gameplay impact

## Content Manifest Pattern

A manifest should define:
- asset id
- category
- quality tier
- preload priority
- fallback asset

This allows deterministic loading and graceful degradation.

## Collaboration Guardrails

- Lock core interaction assets before polish batch
- Treat particle and post-processing assets as optional quality layers
- Reject unbounded asset additions without budget updates
