# Optimization Patterns v1.0.0

Use this file when proposing architecture changes.

## High-value changes first

Prefer these before major redesign:

- clarify component ownership
- simplify routing logic
- add observability at handoff points
- narrow memory scope
- cache or batch expensive tool calls
- reduce unnecessary multi-agent hops

## When to restructure

Recommend deeper restructuring when:

- one component owns too many incompatible responsibilities
- routing quality is persistently poor
- memory contamination causes recurring errors
- coordination cost exceeds the value of specialization

## Recommendation values

Use one of:

- `stable`
- `iterate`
- `restructure`
