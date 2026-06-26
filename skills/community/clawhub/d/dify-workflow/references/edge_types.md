# Dify Workflow Edge Types and Connections

This document describes edge (connection) types, handles, and routing behavior in Dify workflows.

## Edge Structure

Every edge in the workflow DSL has this structure:

```yaml
id: source_node_id-source_handle-target_node_id-target_handle
source: source_node_id
target: target_node_id
sourceHandle: handle_name
targetHandle: target
data:
  sourceType: source_node_type  # BlockEnum value
  targetType: target_node_type  # BlockEnum value
```

## Source Handles by Node Type

Source handles determine which output path from a node is being connected.

### Standard Nodes (EXECUTABLE type)
**Handle**: `source` (default)

Used by most processing nodes:
- llm, code, http-request, knowledge-retrieval
- template-transform, variable-aggregator, assigner
- tool, parameter-extractor, document-extractor
- list-operator, agent

**Example**:
```yaml
- id: "1732007415808-source-1732007420123-target"
  source: "1732007415808"
  target: "1732007420123"
  sourceHandle: source
  targetHandle: target
```

### Error Handling Nodes
**Handles**: `success-branch`, `fail-branch`

Used when `error_strategy: fail-branch` is set on code or http-request nodes.

**Success path** (normal execution):
```yaml
- id: "code_node-success-branch-next_node-target"
  source: code_node_id
  target: next_node_id
  sourceHandle: success-branch
  targetHandle: target
```

**Fail path** (on error):
```yaml
- id: "code_node-fail-branch-error_handler-target"
  source: code_node_id
  target: error_handler_id
  sourceHandle: fail-branch
  targetHandle: target
```

### Conditional Routing Nodes (BRANCH type)

#### If-Else Node
**Handles**: `true`, `false`

Evaluates conditions and routes to one of two paths:
```yaml
# True branch
- id: "ifelse_node-true-handler_a-target"
  source: ifelse_node_id
  target: handler_a_id
  sourceHandle: "true"
  targetHandle: target

# False branch
- id: "ifelse_node-false-handler_b-target"
  source: ifelse_node_id
  target: handler_b_id
  sourceHandle: "false"
  targetHandle: target
```

#### Question Classifier Node
**Handles**: Custom classification labels

Routes based on classification result. Each classification class becomes a handle:
```yaml
# Define classes in node config
classes:
  - id: support_request
    name: Support Request
  - id: sales_inquiry
    name: Sales Inquiry
  - id: general_question
    name: General Question

# Create edges for each class
- id: "classifier-support_request-support_handler-target"
  source: classifier_id
  target: support_handler_id
  sourceHandle: support_request
  targetHandle: target

- id: "classifier-sales_inquiry-sales_handler-target"
  source: classifier_id
  target: sales_handler_id
  sourceHandle: sales_inquiry
  targetHandle: target
```

### Container Nodes (Iteration/Loop)
**Handles**: `loop`, `source`

Container nodes have two output paths:

**Loop continuation** (during iteration):
```yaml
- id: "iteration_node-loop-iteration_end-target"
  source: iteration_node_id
  target: iteration_end_id
  sourceHandle: loop
  targetHandle: target
```

**Completion** (after all iterations):
```yaml
- id: "iteration_node-source-next_node-target"
  source: iteration_node_id
  target: next_node_id
  sourceHandle: source
  targetHandle: target
```

## Target Handles

Target handles are typically `target` for all nodes. This is the standard input connection point.

**Exception**: Container internal nodes (iteration-start, loop-start) use `target` but are only connected from their parent container.

## Edge Data Properties

### Internal State Properties (prefixed with `_`)

These properties are managed by the React Flow UI and track runtime state:

- `_hovering`: Mouse is hovering over edge
- `_connectedNodeIsHovering`: Connected node is being hovered
- `_connectedNodeIsSelected`: Connected node is selected
- `_isBundled`: Edge is part of a bundled group
- `_sourceRunningStatus`: Source node execution status
- `_targetRunningStatus`: Target node execution status
- `_waitingRun`: Edge is waiting for execution
- `_isTemp`: Temporary edge during drag operation

### Required Data Properties

- `sourceType`: BlockEnum type of source node (e.g., "llm", "code")
- `targetType`: BlockEnum type of target node

### Container Context Properties

- `isInIteration`: Edge is inside an iteration container
- `iteration_id`: Parent iteration node ID
- `isInLoop`: Edge is inside a loop container
- `loop_id`: Parent loop node ID

## Edge States During Execution

Edges have three possible states during workflow execution:

1. **UNKNOWN**: Initial state, not yet evaluated
2. **TAKEN**: Edge is traversed (condition met or path selected)
3. **SKIPPED**: Edge is not traversed (condition failed or alternative path chosen)

### State Transitions

**Standard edges**: UNKNOWN → TAKEN (when source node completes)

**Conditional edges**:
- If-else: One of (true/false) → TAKEN, the other → SKIPPED
- Question-classifier: Matching class → TAKEN, others → SKIPPED

**Error handling edges**:
- Success-branch: TAKEN on success, SKIPPED on error
- Fail-branch: SKIPPED on success, TAKEN on error

## Common Edge Patterns

### Sequential Flow
```yaml
Start → Node A → Node B → End

edges:
  - id: start-source-nodeA-target
    source: start_id
    sourceHandle: source
    target: nodeA_id
    targetHandle: target
  - id: nodeA-source-nodeB-target
    source: nodeA_id
    sourceHandle: source
    target: nodeB_id
    targetHandle: target
  - id: nodeB-source-end-target
    source: nodeB_id
    sourceHandle: source
    target: end_id
    targetHandle: target
```

### Branching and Merging
```yaml
Start → If-Else → [True → Handler A] → Aggregator → End
                 → [False → Handler B] →

edges:
  - id: start-source-ifelse-target
    source: start_id
    sourceHandle: source
    target: ifelse_id
    targetHandle: target
  - id: ifelse-true-handlerA-target
    source: ifelse_id
    sourceHandle: "true"
    target: handlerA_id
    targetHandle: target
  - id: ifelse-false-handlerB-target
    source: ifelse_id
    sourceHandle: "false"
    target: handlerB_id
    targetHandle: target
  - id: handlerA-source-aggregator-target
    source: handlerA_id
    sourceHandle: source
    target: aggregator_id
    targetHandle: target
  - id: handlerB-source-aggregator-target
    source: handlerB_id
    sourceHandle: source
    target: aggregator_id
    targetHandle: target
  - id: aggregator-source-end-target
    source: aggregator_id
    sourceHandle: source
    target: end_id
    targetHandle: target
```

### Error Handling Flow
```yaml
Start → Code → [Success → Next] → Aggregator → End
             → [Fail → Recovery] →

edges:
  - id: start-source-code-target
    source: start_id
    sourceHandle: source
    target: code_id
    targetHandle: target
  - id: code-success-branch-next-target
    source: code_id
    sourceHandle: success-branch
    target: next_id
    targetHandle: target
  - id: code-fail-branch-recovery-target
    source: code_id
    sourceHandle: fail-branch
    target: recovery_id
    targetHandle: target
  - id: next-source-aggregator-target
    source: next_id
    sourceHandle: source
    target: aggregator_id
    targetHandle: target
  - id: recovery-source-aggregator-target
    source: recovery_id
    sourceHandle: source
    target: aggregator_id
    targetHandle: target
```

### Iteration Loop
```yaml
Start → Iteration → Iteration-Start → Process → Iteration-End → Next
                 ↑                                             ↓
                 └─────────────────────────────────────────────┘

edges:
  - id: start-source-iteration-target
    source: start_id
    sourceHandle: source
    target: iteration_id
    targetHandle: target
  - id: iteration-loop-iteration_start-target
    source: iteration_id
    sourceHandle: loop
    target: iteration_start_id
    targetHandle: target
    data:
      isInIteration: true
      iteration_id: iteration_id
  - id: iteration_start-source-process-target
    source: iteration_start_id
    sourceHandle: source
    target: process_id
    targetHandle: target
    data:
      isInIteration: true
      iteration_id: iteration_id
  - id: process-source-iteration_end-target
    source: process_id
    sourceHandle: source
    target: iteration_end_id
    targetHandle: target
    data:
      isInIteration: true
      iteration_id: iteration_id
  - id: iteration-source-next-target
    source: iteration_id
    sourceHandle: source
    target: next_id
    targetHandle: target
```

## Edge Validation Rules

When creating or modifying edges, ensure:

1. **Unique IDs**: Each edge must have a unique ID
2. **Valid References**: Source and target must reference existing node IDs
3. **Handle Compatibility**: sourceHandle must match source node's available handles
4. **Type Matching**: data.sourceType and data.targetType must match actual node types
5. **No Self-Loops**: An edge cannot connect a node to itself (except for container loop logic)
6. **Branch Completeness**: Branching nodes should have edges for all possible outcomes
7. **Error Handling Pairs**: Nodes with fail-branch must have both success and fail edges
8. **Container Context**: Edges inside iteration/loop must have proper iteration_id/loop_id
9. **Root Node Isolation**: Root nodes (start, trigger nodes) cannot have incoming edges
10. **Convergence**: Branching paths should converge at a variable-aggregator before merging to single path

## Handle Naming Convention

Standard handle names follow these patterns:

- **Default**: `source` and `target`
- **Conditions**: `true`, `false`
- **Error handling**: `success-branch`, `fail-branch`
- **Container**: `loop`
- **Custom**: Classification labels (question-classifier)

Always use lowercase with hyphens for multi-word handles.
