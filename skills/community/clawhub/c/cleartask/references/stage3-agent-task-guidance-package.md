# Stage3 Agent Task Guidance Package

Stage3 turns the Stage2 handoff into an internal package for downstream execution. Do not display the full package by default. Use it to continue the user's task immediately unless the user asks to inspect, export, save, or review the package.

## Internal Flow

```text
Stage3A TaskClassifier
Stage3B ExpertSelector
Stage3C ExpertTaskBriefGenerator
Stage3D ExpertAcceptanceCriteriaGenerator
Stage3E Stage3MainComposer
Stage3F ExecuteWithPackage
Stage3G ConciseResultAndSelfCheck
```

## Execution Policy

Continue execution after Stage3 when:

- blocking questions are resolved or have accepted defaults,
- the user asked for a concrete deliverable or outcome,
- the task can be completed with available tools and workspace access.

Pause before execution when:

- unresolved blocking questions remain,
- execution would unexpectedly modify many files or external systems,
- credentials, paid services, network access, or destructive operations are required,
- the user explicitly asked only for analysis, planning, or the internal package.

## Task Classification

```yaml
TaskClassification:
  work_mode: implement | write_doc | design | analyze | test | research | plan | refactor | custom
  domain:
    - frontend_web
    - backend_api
    - game
    - workflow_automation
    - data_analysis
    - product_design
    - business_process
    - prompt_engineering
    - document_writing
    - custom
  downstream_agent_role: coding_agent | writing_agent | research_agent | product_agent | design_agent | testing_agent | general_agent
  risk_level: low | medium | high
  rationale: string
```

## Expert Task Brief

```yaml
ExpertTaskBrief:
  expert_role: string
  focus: string[]
  task_guidance: string[]
  recommended_approach: string[]
  suggested_steps: string[]
  constraints: string[]
  risks: string[]
  edge_cases: string[]
  do: string[]
  do_not: string[]
```

## Internal Package Schema

This schema is for internal reasoning and downstream execution. Do not render it to the user by default.

```yaml
AgentTaskGuidancePackage:
  package_id: string
  title: string
  objective: string
  expected_outcome: string
  downstream_agent_role: string
  recommended_work_mode: string

  context:
    user_original_request: string
    clarified_requirement_summary: string
    background: string
    target_users: string[]
    operating_environment: string

  confirmed_scope:
    in_scope: string[]
    out_of_scope: string[]
    non_goals: string[]

  requirements:
    functional_requirements: string[]
    non_functional_requirements: string[]
    interaction_requirements: string[]
    data_requirements: string[]
    workflow_requirements: string[]
    business_rules: string[]

  process_model:
    actors: object[]
    systems: object[]
    inputs: object[]
    outputs: object[]
    workflow_graph: object

  expert_task_guidance:
    primary_expert:
      role: string
      guidance: string[]
      recommended_approach: string[]
      suggested_steps: string[]
      constraints: string[]
      risks: string[]
      edge_cases: string[]
    supporting_experts:
      - role: string
        guidance: string[]
        recommended_approach: string[]
        suggested_steps: string[]
        constraints: string[]
        risks: string[]
        edge_cases: string[]

  consolidated_execution_plan:
    recommended_approach: string[]
    suggested_steps: string[]
    dependencies_or_tools: string[]
    files_or_artifacts_to_create: string[]
    integration_points: string[]
    constraints: string[]
    do: string[]
    do_not: string[]
    ask_before_changing: string[]
    autonomy_level: execute_directly | ask_before_major_tradeoffs | plan_first | docs_only

  expert_acceptance_criteria:
    - expert_role: string
      criteria: object[]

  consolidated_acceptance_criteria:
    must_pass: object[]
    should_pass: object[]
    nice_to_have: object[]

  risks_and_edge_cases:
    risks: string[]
    edge_cases: string[]
    fallback_strategy: string[]

  unresolved_questions:
    blocking: string[]
    non_blocking: string[]

  assumptions:
    accepted_defaults: object[]
    model_inferred_assumptions: string[]
    expert_recommendations: string[]

  conflicts:
    - description: string
      affected_fields: string[]
      suggested_resolution: string

  traceability:
    - item: string
      source: string
      confidence: number

  suggested_next_prompt: string
```

## Composer Rules

- Consolidate expert content into a clear execution plan.
- Preserve expert-specific details under `expert_task_guidance`.
- Do not invent new user requirements while composing.
- Move new professional advice into `expert_recommendations`.
- Keep the final package directly usable as a prompt to another agent.
- Use the package to execute the task immediately when the execution policy allows it.
- Use `suggested_next_prompt` internally as the execution instruction; do not display it unless the user asks for the internal package.

## User-Visible Reporting

After execution, report:

- completed result,
- important decisions/defaults used,
- files or artifacts created/changed,
- concise self-check against must-pass criteria,
- caveats, skipped checks, or non-blocking questions.

Do not dump the full package, full workflow graph, or full expert criteria unless requested.
