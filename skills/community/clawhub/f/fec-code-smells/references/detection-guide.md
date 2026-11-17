# Code Smell Detection Guide

## Evidence First
Use code structure, dependency direction, ownership, repeated change patterns, and observable maintenance burden. Metrics can focus investigation but cannot prove a smell alone.

## Required False-Positive Guards
- LOC alone does not prove Long Function or Large Class.
- One switch does not prove Repeated Switches.
- A function/array pipeline is not automatically Message Chains.
- Comments are not defects by themselves.
- Immutable transfer data may legitimately remain data-only.
- React/Vue declarative composition is not automatically Middle Man.
- `filter().map().reduce()` pipelines are not Message Chains.

## Frontend Evidence Checklist
- Identify data ownership across props, stores, API DTOs, hooks/composables, and modules.
- Check lifecycle semantics before labeling effects/watchers as duplication or message chains.
- Check public component, route, event, and package contracts before recommending movement.
- Check dynamic references: lazy imports, route registries, Storybook, i18n keys, runtime templates, and generated CSS classes.
- Distinguish domain duplication from coincidentally similar rendering.

## Confidence
- **HIGH:** direct, repeated evidence and false positives ruled out.
- **MEDIUM:** evidence is meaningful but history, dynamic references, or ownership is incomplete.
- **LOW:** mostly metric/surface evidence or material uncertainty remains. Report only; do not auto-edit.
