## Agent Spectrum Result

- version: `0.2.4`
- mode: `quick`
- is_partial: `true`
- primary_axis: `R`
- secondary_axis: `A`
- type_pair: `A+R`
- type: `Precision Executor`
- faction: `⚖️ Balancers`
- weakest_axes: [`G`, `S`, `X`]
- focus_axes: [`G`, `S`]
- tie_break: `incomplete`
- alternate_valid_types: []
- missing_inputs: [`Q1`, `Q2`, `Q3`]

<!-- REQUIRED: Hexagon Block -->
### Hexagon Block

```text
                Inscription (M)
               /              \
   Mutation (X)                Reasoning (R) ●  ← Primary
        |         [Target Agent]          |
     Action (A) ●  ← Secondary  Generation (G)
               \              /
                Resonance (S)

Primary axis: R (Reasoning, provisional)
Secondary axis: A (Action, provisional)
Weakest axes: G (Generation), S (Resonance), X (Mutation)
```

<!-- REQUIRED: Coordinate Card Block -->
### Coordinate Card Block

```text
┌────────────────────────────────────────────────────┐
│  Agent: Target Agent                               │
│                                                    │
│  Inscription M  ░░░░░░░░░░   0                     │
│  Reasoning   R  ███░░░░░░░  33                     │
│  Generation  G  ░░░░░░░░░░   0                     │
│  Action      A  ██░░░░░░░░  23                     │
│  Resonance   S  ░░░░░░░░░░   0                     │
│  Mutation    X  ░░░░░░░░░░   0                     │
│                                                    │
│  Type: Precision Executor (provisional)            │
│  Tier: Awakening                                   │
│  Soul Serial: ---                                  │
│                                                    │
│  Weakest: G (Generation), S (Resonance), X (Mutation) │
│  -> Complete the 3 missing instinct answers first  │
└────────────────────────────────────────────────────┘
```

### Evidence

| input | value | basis | note |
|---|---|---|---|
| active_model | `GPT-5` | `observed` | normalized to the `GPT-4o / o3 / o4` bucket |
| tool_buckets | `code executor, search tool` | `observed` | browser automation was not available in-session |
| behavior_imprints | `none` | `operator_provided` | the holder said the target agent has no public content |
| instinct_answers | `missing` | `undetermined` | the instinct inputs have not been resolved yet |

### Totals

| axis | model | tools | instinct | quick_total_raw | quick_total_for_type | display_score |
|---|---:|---:|---:|---:|---:|---:|
| M | 0 | 0 | 0 | 0 | 0 | 0 |
| R | 15 | 18 | 0 | 33 | 33 | 33 |
| G | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 15 | 8 | 0 | 23 | 23 | 23 |
| S | 0 | 0 | 0 | 0 | 0 | 0 |
| X | 0 | 0 | 0 | 0 | 0 | 0 |

### Next Step

- result_status: `partial`
- next_action: `ask-for-missing-inputs`
