# Stage2 Clarification Handoff

Use Stage2 to ask targeted questions, absorb answers, recommend defaults when requested, and create a stable handoff for Stage3.

## Clarification Strategy

- Ask only questions that materially affect downstream work.
- Group related questions when it reduces user effort.
- Prefer 3-5 questions at a time for ambiguous requests.
- When the user asks for recommendations, choose defaults and explain briefly.
- Move non-blocking unknowns into `unresolved_questions.non_blocking`.

## Question Schema

```yaml
ClarificationQuestion:
  question_id: string
  target_field: string
  question: string
  reason: string
  blocking_level: blocking | important | optional
  suggested_options: string[]
  default_if_unanswered: string
```

## Handoff Schema

```yaml
UniversalRequirementHandoff:
  confirmed_facts: string[]
  confirmed_process_model: UniversalProcessModel
  clarified_scope:
    in_scope: string[]
    out_of_scope: string[]
    non_goals: string[]
  requirement_summary: string
  functional_requirements: string[]
  non_functional_requirements: string[]
  interaction_requirements: string[]
  data_requirements: string[]
  workflow_requirements: string[]
  business_rules: string[]
  accepted_defaults:
    - field: string
      value: string
      reason: string
  unresolved_questions:
    blocking:
      - question: string
        impact: string
    non_blocking:
      - question: string
        default_handling: string
  assumptions:
    accepted: string[]
    model_inferred: string[]
  risk_points: string[]
  rui: number
  ready_for_stage3: true | false
  traceability:
    - item: string
      source: user_answer | accepted_default | stage1_model | model_inference
      confidence: number
```

## Readiness Rules

Set `ready_for_stage3: true` only when:

- every blocking question has an answer or accepted default,
- the scope is explicit enough for downstream work,
- the expected outcome is clear,
- known assumptions are separated from confirmed facts.

Use `rui` as a rough residual uncertainty index:

- `0.0-0.2`: ready; only minor unknowns remain.
- `0.2-0.4`: probably ready if defaults are accepted.
- `0.4+`: ask more questions before Stage3.

## Default Recommendation Rules

When recommending defaults:

- choose the lowest-friction option for simple tasks,
- choose maintainable, conventional architecture for implementation tasks,
- avoid adding external dependencies unless they clearly improve the result,
- do not add unrequested premium features,
- mark every recommendation under `accepted_defaults` after user acceptance.
