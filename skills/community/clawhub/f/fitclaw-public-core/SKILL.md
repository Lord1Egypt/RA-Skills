---
name: fitclaw-public-core
description: Public-safe FitClaw coaching workflow covering onboarding, hydration, nutrition, and training structure. Use when demonstrating a reusable AI fitness coaching method without exposing private user data or live production configuration.
---

# FitClaw Public Core

## Purpose

This is the public-safe packaging layer for FitClaw.

It is not the live production workspace.
Its purpose is to expose the reusable coaching workflow only.

---

## Release Gate

This package is review-first.

That means:
1. prepare the candidate package locally,
2. review it carefully,
3. publish only after explicit approval.

Without explicit approval, this package should remain in staging only.

---

## Included public workflow scope

This package currently focuses on four reusable workflow blocks:
1. onboarding
2. hydration support
3. nutrition guidance
4. training framework guidance

---

## Hard boundary

Never treat this package as a dump of the live FitClaw project.

Only include:
- reusable workflow logic
- public-safe templates
- generalized examples
- sanitized references

Never include:
- credential files
- private user media
- private user reports or history
- private runtime bindings
- private operational materials embedded in scripts or examples

---

## Packaging rule

If this package is prepared for ClawHub, it must pass privacy review first.
The public asset is the method, not the real operating state.

---

## Current candidate modules

- fitclaw-onboarding-public
- fitclaw-hydration-public
- fitclaw-nutrition-public
- fitclaw-training-public

These modules were rewritten into public-safe references before publish.

---

## Output goal

A publishable public-safe skill package that demonstrates the FitClaw coaching method without leaking private or operational data.
