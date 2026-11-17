# Refactoring Selection Guide

Choose by observed cause. The same smell can require different transformations.

## Long Function
- **Mixed named intentions** → `RF-EXTRACT-FUNCTION`; require a coherent slice and stable inputs/outputs.
- **Temporaries obstruct extraction** → `RF-REPLACE-TEMP-WITH-QUERY`; avoid when repeated computation is materially expensive or effectful.
- **Several inputs travel as one concept** → `RF-INTRODUCE-PARAMETER-OBJECT` or `RF-PRESERVE-WHOLE-OBJECT`.
- **Large conditional varies by type/variant** → first consider `RF-DECOMPOSE-CONDITIONAL`; use `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM` only when repeated variant behavior warrants dispatch.
- **One loop performs unrelated jobs** → `RF-SPLIT-LOOP` when separate passes preserve ordering/performance constraints.
- **Risk/verification:** preserve exceptions, side effects, event order, hook dependencies, state transitions, and async sequencing.

## Long Parameter List
- **A value can be derived from another parameter or stable receiver** → `RF-REPLACE-PARAMETER-WITH-QUERY`.
- **Callers unpack one existing object** → `RF-PRESERVE-WHOLE-OBJECT`.
- **Values repeatedly travel together as a concept** → `RF-INTRODUCE-PARAMETER-OBJECT`.
- **A boolean/enum selects behavior** → `RF-REMOVE-FLAG-ARGUMENT`; not for ordinary domain data.
- **Several functions share the same data context** → `RF-COMBINE-FUNCTIONS-INTO-CLASS`, interpreted as class/module/hook/composable/service according to the codebase.
- **Risk/verification:** public signatures and callback/component contracts raise compatibility risk.

## Mutable Data
- **Uncontrolled shared write access** → `RF-ENCAPSULATE-VARIABLE`.
- **One variable serves multiple meanings** → `RF-SPLIT-VARIABLE`.
- **A read operation also mutates** → `RF-SEPARATE-QUERY-FROM-MODIFIER`.
- **Stored derived data drifts** → `RF-REPLACE-DERIVED-VARIABLE-WITH-QUERY`; evaluate recomputation cost and memoization semantics.
- **Identity is unnecessary and mutation leaks** → consider `RF-CHANGE-REFERENCE-TO-VALUE`.
- **Risk/verification:** React/Vue identity, reactivity, memoization, subscriptions, and persistence are part of behavior.

## Divergent Change
- **One function has sequential concerns** → `RF-SPLIT-PHASE` or `RF-EXTRACT-FUNCTION`.
- **Behavior primarily belongs with another data owner** → `RF-MOVE-FUNCTION`.
- **A responsibility cluster has its own state and rules** → `RF-EXTRACT-CLASS`, including a frontend module/service/hook/composable equivalent.
- **Risk/verification:** do not split merely by technical layer if the business responsibility is cohesive.

## Shotgun Surgery
- **Behavior/data belonging together is scattered** → `RF-MOVE-FUNCTION` / `RF-MOVE-FIELD`.
- **Many functions share one context** → `RF-COMBINE-FUNCTIONS-INTO-CLASS` or `RF-COMBINE-FUNCTIONS-INTO-TRANSFORM`.
- **A pipeline has separable stages** → `RF-SPLIT-PHASE`.
- **Premature tiny abstractions caused scattering** → `RF-INLINE-FUNCTION` / `RF-INLINE-CLASS` may first regroup logic, followed by a better extraction.
- **Risk/verification:** keep each regrouping step independently behavior-preserving; temporary larger units are acceptable if verified.

## Primitive Obsession
- **A primitive carries invariants/formatting/domain behavior** → `RF-REPLACE-PRIMITIVE-WITH-OBJECT`; a TypeScript alias alone does not encapsulate runtime behavior.
- **A type code drives repeated variant behavior** → consider `RF-REPLACE-TYPE-CODE-WITH-SUBCLASSES` or a discriminated-union/strategy equivalent.
- **Repeated conditional variation is the real problem** → `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM` using the most idiomatic dispatch form.
- **Several primitives form one concept** → `RF-EXTRACT-CLASS` or `RF-INTRODUCE-PARAMETER-OBJECT`.
- **Risk/verification:** serialized DTOs, URL values, storage, validation, and API payload shape may be public contracts.
