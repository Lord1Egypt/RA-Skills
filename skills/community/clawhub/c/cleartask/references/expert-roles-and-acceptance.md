# Expert Roles and Acceptance Criteria

Use experts to generate professional task guidance and acceptance criteria. Experts provide domain quality; the Stage3 composer provides consistency. Expert outputs are internal by default and should be used to guide execution and concise self-check reporting.

## Expert Selection

Select one primary expert and zero or more supporting experts.

```yaml
expert_profiles:
  frontend_game:
    primary_expert: frontend_game_engineer
    supporting_experts:
      - game_designer
      - ux_designer
      - qa_engineer

  frontend_web_app:
    primary_expert: frontend_engineer
    supporting_experts:
      - ux_designer
      - qa_engineer

  backend_api:
    primary_expert: backend_architect
    supporting_experts:
      - api_designer
      - security_engineer
      - qa_engineer

  workflow_automation:
    primary_expert: workflow_architect
    supporting_experts:
      - integration_engineer
      - business_analyst
      - qa_engineer

  product_plan:
    primary_expert: product_manager
    supporting_experts:
      - ux_designer
      - business_analyst
      - qa_engineer

  document_or_content:
    primary_expert: technical_writer
    supporting_experts:
      - domain_expert
      - editor

  data_analysis:
    primary_expert: data_analyst
    supporting_experts:
      - data_engineer
      - qa_engineer
```

Create a custom expert when no listed profile fits. Name the expert by role, not by artifact type.

## Expert Focus

```yaml
frontend_game_engineer:
  focuses:
    - browser runtime behavior
    - rendering loop
    - input handling
    - state management
    - single-file or build constraints

game_designer:
  focuses:
    - core loop
    - controls
    - difficulty
    - win and lose conditions
    - feedback and game feel

ux_designer:
  focuses:
    - visible state
    - ease of use
    - layout clarity
    - accessibility basics

qa_engineer:
  focuses:
    - testability
    - edge cases
    - regression risks
    - pass and fail conditions

backend_architect:
  focuses:
    - service boundaries
    - data model
    - interfaces
    - reliability
    - maintainability

product_manager:
  focuses:
    - user goals
    - scope
    - priority
    - success metrics

technical_writer:
  focuses:
    - audience fit
    - document structure
    - clarity
    - completeness
```

## Acceptance Criteria Schema

```yaml
ExpertAcceptanceCriteria:
  expert_role: string
  criteria:
    - id: string
      category: string
      criterion: string
      why_it_matters: string
      verification_method: string
      pass_condition: string
      fail_examples: string[]
      priority: must | should | nice
      source_trace: string
```

## Rules

- Make every criterion verifiable.
- Include a concrete pass condition.
- Include fail examples when they clarify the boundary.
- Convert subjective quality into observable checks.
- Put unconfirmed or optional requirements under `should` or `nice`, not `must`.
- Tie criteria to Stage2 facts, accepted defaults, or expert recommendations.
- Keep expert recommendations separate from confirmed user requirements.
- Use criteria for implementation self-check and final concise reporting.
- Do not display full expert criteria unless the user asks to inspect the internal package or validation rubric.

## Bad Criteria

```yaml
- criterion: The UI should look good.
- criterion: The feature should be complete.
- criterion: The system should be robust.
```

## Better Criteria

```yaml
- criterion: The page shows current score, high score, selected difficulty, and start/pause/restart controls without requiring the user to read external instructions.
  verification_method: Open the page in a browser and inspect visible controls before starting the game.
  pass_condition: All listed controls and status values are visible in the first viewport.
```
