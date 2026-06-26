# Stage1 Universal Process Model

Use Stage1 to convert the user's raw request into a rich process model. The model must preserve enough structure for later clarification and downstream agent execution.

## Principles

- Model the request as a process, not just a summary.
- Prefer a graph of nodes and edges over a linear list.
- Capture inputs, outputs, actors, systems, rules, exceptions, and uncertainty.
- Do not collapse important workflow details for brevity.
- Mark inferred defaults as assumptions unless the user confirms them.

## Schema

```yaml
UniversalProcessModel:
  request_summary: string
  business_goal:
    primary_goal: string
    success_outcome: string
  scope:
    included: string[]
    excluded_or_unknown: string[]
  actors:
    - id: string
      name: string
      role: string
  external_systems:
    - id: string
      name: string
      purpose: string
      known_or_assumed: confirmed | assumed | unknown
  data_objects:
    - name: string
      description: string
      fields: string[]
      lifecycle: string
  inputs:
    - name: string
      source: string
      type: string
      required: true | false
      notes: string
  outputs:
    - name: string
      consumer: string
      type: string
      success_condition: string
  workflow_graph:
    nodes:
      - node_id: string
        title: string
        description: string
        node_type: input_collect | transform | classify | decide | human_review | external_api | database_operation | notification | output_generate | end | custom
        actor: string
        system: string
        trigger: string
        preconditions: string[]
        required_inputs: string[]
        actions: string[]
        produced_outputs: string[]
        business_rules: string[]
        validation_rules: string[]
        failure_modes: string[]
        retry_or_fallback: string[]
        unresolved_points: string[]
    edges:
      - from_node: string
        to_node: string
        condition: string
        edge_type: normal | conditional | exception | rejection | retry | custom
  business_rules: string[]
  human_touchpoints: string[]
  exceptions: string[]
  assumptions: string[]
  open_questions:
    - question: string
      target_field: string
      reason: string
      blocking_level: blocking | important | optional
  confidence: number
  source_evidence:
    - item: string
      source: user_text | model_inference | prior_context
      quote_or_reason: string
```

## Modeling Guidance

For implementation requests, include likely implementation flow without choosing unconfirmed technology unless obvious from user context.

For document-writing requests, model the content production workflow: audience, message, source material, sections, review, and final output.

For games, model the game loop, player input, state updates, rules, rendering, end conditions, and restart flow.

For business processes, model actors, approvals, systems, data movement, decisions, exceptions, and final outputs.

## Stage1 Quality Bar

Stage1 is acceptable when another agent can answer:

- What is the user trying to accomplish?
- What is in scope and uncertain?
- What are the main process nodes and transitions?
- What information is confirmed versus inferred?
- Which missing details should Stage2 ask about?
