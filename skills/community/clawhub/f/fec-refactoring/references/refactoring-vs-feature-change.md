# Refactoring Boundaries

## Pure Refactoring

Use the behavior-preserving lane when the requested outcome is structural: clearer responsibilities, smaller functions, better names, safer encapsulation, moved behavior, simplified conditionals, cleaner API shape, or improved data organization without an intentional change to what callers or users observe.

Verification model: **GREEN -> REFACTOR -> GREEN**.

## Feature or Behavior-Changing Defect Work

A request is not pure refactoring when it adds a capability, changes a business rule, changes accepted input, changes visible output, changes an error outcome, or intentionally changes side effects. Establish the new desired behavior with a failing behavioral test before implementation.

## Debugging

When the failure cause is unknown, diagnose root cause before choosing structural changes. A refactoring may become part of a later fix, but it is not a substitute for evidence about the defect.

## Dead-Code Cleanup

Proven unused code, stale exports, unused dependencies, obsolete routes, and similar removal work require specialized reference discovery because dynamic imports, configuration, templates, routes, Storybook, CSS, and generated keys can create false positives. Keep cleanup separate from broad restructuring of live code.

## Migration

Framework, dependency, router, build-system, state-library, or architecture migrations intentionally alter compatibility boundaries and should be planned as migrations even when they also improve design.

## General Review

A merge-readiness review may identify structural findings, but review remains report-first. Diagnosis or a refactoring plan should be an explicit follow-up rather than silent source rewriting during review.
