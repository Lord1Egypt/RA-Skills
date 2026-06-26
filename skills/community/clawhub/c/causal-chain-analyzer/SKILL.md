---
name: causal_chain_analyzer
title: Causal Chain Analyzer
description: Analyze and trace cause-effect chains in knowledge graphs to identify root causes, trace downstream impacts, and understand dependencies. Supports multiple traversal algorithms, cycle detection, probabilistic causality scoring, and chain ranking strategies.
category: reasoning
tags:
  - knowledge-graph
  - reasoning
  - causal-analysis
  - graph-analysis
  - dependency-tracing
  - root-cause-analysis
  - impact-propagation
  - cycle-detection
  - chain-ranking
  - probabilistic-reasoning
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🔍","homepage":"https://clawhub.com"}}
---

# Causal Chain Analyzer

**Identify and analyze cause-effect chains within knowledge graphs to perform root cause analysis and trace impact propagation.**

This skill enables comprehensive causal analysis by traversing directed graphs following causal relationships to discover root causes, trace downstream effects, detect cycles, and rank causality chains by strength or proximity.

## Quick Start

### Use When
- Identifying root causes of system failures or issues
- Tracing downstream impacts and effect propagation
- Analyzing dependencies in complex systems
- Debugging multi-step failure scenarios
- Performing impact analysis on decisions or changes
- Understanding how events or faults cascade through systems
- Detecting circular dependencies or feedback loops
- Building explainability for causality-based decisions

### Inputs
- Knowledge graph with nodes and causal relationships
- Target node for analysis (effect or starting point)
- Causal relationship types (causes, leads_to, results_in, etc.)
- Optional analysis parameters (max depth, confidence threshold, traversal algorithm)

### Outputs
- Root cause nodes (upstream causes with no incoming causal edges)
- Causal chains (ordered sequences of cause-effect pairs)
- Effect chains (downstream consequences from a source)
- Chain rankings (scored by proximity, confidence, or custom metrics)
- Cycle detection results (if present)
- Analysis statistics (chain depth, total nodes, confidence scores)

## Causal Relationships

### Supported Relationship Types

This skill operates on relationships representing **causal or dependency links**, including:

- `causes` - Direct causal relationship (A causes B)
- `leads_to` - Event progression (A leads to B)
- `results_in` - Direct outcome (A results in B)
- `triggers` - Activation relationship (A triggers B)
- `depends_on` - Dependency relationship (A depends on B)
- `influences` - Indirect causation (A influences B)
- `contributes_to` - Contributory cause (A contributes to B)
- `propagates_to` - Effect propagation (A propagates to B)

### Edge Properties

Relationships may include optional properties for ranking:
- `weight` - Strength of causality (0.0 to 1.0)
- `confidence` - Certainty of relationship (0.0 to 1.0)
- `latency` - Time delay between cause and effect
- `severity` - Impact severity of the relationship

## Core Concepts

### Root Cause
The initial triggering event or condition that starts a causal chain. Identified as nodes with no incoming causal edges.

```
Power_Surge (root cause) → Server_Shutdown → API_Failure → User_Impact
```

### Causal Chain
A directed path through the graph where each node triggers the next, representing the complete cause-effect sequence.

```
Chain: [A → B → C → D]
Depth: 4 nodes
Distance: 3 relationships
```

### Effect Propagation
How consequences spread through interconnected systems, potentially causing cascading failures or distributed impacts.

```
Single Cause: A
Propagates to: B, C, D (different effect paths)
Total Impact: 4 affected nodes
```

### Multi-Cause Scenarios
Events that result from multiple independent or dependent causes (AND/OR relationships).

```
A ─┐
   ├→ D (A AND B cause D)
B ─┘

A → C ─┐
       ├→ E (C OR D cause E)
B → D ─┘
```

### Cycle Detection
Identifying circular dependencies where causality loops back on itself (A→B→...→A).

```
Cycle: A → B → C → A
Risk: Infinite propagation without cycle breaking
```

## Analysis Algorithms

### Traversal Algorithms

#### 1. Depth-First Search (DFS)
- Explore single paths to maximum depth before backtracking
- Use: Deep chains, root cause identification
- Complexity: O(V + E) time, O(V) space

```
Graph: A→B→C
       A→D→E
DFS Order: A, B, C, D, E (depth-first)
```

#### 2. Breadth-First Search (BFS)
- Explore all neighbors at current depth before going deeper
- Use: Effect propagation, proximity analysis
- Complexity: O(V + E) time, O(V) space

```
Graph: A→B→C
       A→D→E
BFS Order: A, B, D, C, E (level-by-level)
```

#### 3. Topological Sort
- Total ordering of nodes respecting causal dependencies
- Use: Event scheduling, dependency resolution
- Complexity: O(V + E) time
- Limitation: Only works on acyclic graphs (DAGs)

#### 4. Shortest Path
- Find the minimum steps from cause to effect
- Use: Identifying most direct causality
- Complexity: O(V log V + E) with Dijkstra

### Ranking Strategies

#### Proximity-Based Ranking
Prioritize causes by distance (closer causes ranked higher).

```
A --(1)-- B --(1)-- C --(1)-- Target
Ranking: A(distance=3), B(distance=2), C(distance=1)
```

#### Confidence-Based Ranking
Score chains by cumulative confidence of relationships.

```
Chain: A --(0.9)-- B --(0.7)-- C
Score: 0.9 * 0.7 = 0.63 (confidence product)
```

#### Weighted Importance Ranking
Prioritize by relationship weights or edge properties.

```
Edges: [weight, confidence]
A --(0.8, 0.9)-- B --(0.6, 0.7)-- C
Combined score: (0.8 * 0.9) * (0.6 * 0.7) = 0.3024
```

#### Probabilistic Causality Scoring
Bayesian approach incorporating base rates and conditional probabilities.

```
P(Effect|Cause) * P(Cause) / P(Effect)
Scores reflect likelihood of causal relationship
```

### Cycle Detection Methods

#### Tarjan's Algorithm
Identifies strongly connected components (cycles) in directed graphs.
- Complexity: O(V + E) time, O(V) space
- Result: Returns all cycles and their components

#### DFS-Based Detection
Tracks visited nodes during traversal; back edge indicates cycle.
- Complexity: O(V + E) time
- Use: Simple cycle detection during traversal

#### Feedback Arc Set
Minimum set of edges to remove to make graph acyclic.
- Use: Understanding feedback loops
- Complexity: NP-hard (approximation algorithms available)

## Core Analysis Procedures

### Finding Root Causes

1. Start at target node (effect)
2. Traverse backward following incoming causal edges
3. Continue until reaching nodes with no incoming causal edges
4. Collect all discovered root causes
5. Rank by proximity or confidence

```
Target: User_Login_Error
Backward traversal: User_Login_Error ← API_Failure ← Server_Down ← Power_Surge
Root causes: [Power_Surge]
```

### Tracing Effects

1. Start at source node (initial cause)
2. Traverse forward following outgoing causal edges
3. Continue until reaching terminal nodes (no outgoing edges)
4. Collect all affected nodes
5. Analyze propagation paths

```
Source: Database_Corrupted
Forward traversal: Database_Corrupted → Query_Failures → Service_Degradation
Effects: [Query_Failures, Service_Degradation]
Affected: 2 downstream nodes
```

### Analyzing Chain Structure

1. Identify root causes and leaf effects
2. Calculate chain depth (maximum path length)
3. Measure breadth (branching factor)
4. Determine completeness (connected all nodes)
5. Score by coverage and complexity

```
Chain Metrics:
- Max depth: 5 hops
- Nodes involved: 12
- Branching factor: 2.4 avg
- Coverage: 85% of graph
```

### Confidence-Based Filtering

1. Calculate cumulative confidence along chains
2. Filter chains below threshold
3. Weight results by confidence scores
4. Provide confidence intervals

```
Threshold: 0.6
Chain A: 0.9 * 0.8 * 0.7 = 0.504 (FILTERED OUT - below threshold)
Chain B: 0.95 * 0.9 = 0.855 (INCLUDED)
```

## Error Handling

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Infinite loops | Cyclic graph detected | Enable cycle detection, apply cycle breaking |
| Depth explosion | Very deep chains | Set max_depth limit, use BFS instead |
| Memory overflow | Too many branches | Limit branching factor, paginate results |
| No root causes found | Target is isolated | Check graph connectivity, verify relationship types |
| Conflicting causes | Circular dependencies | Run Tarjan's algorithm, resolve feedback loops |
| Low confidence | Weak causal links | Increase confidence threshold, inspect edge weights |
| Missing relationships | Incomplete graph | Verify data ingestion, check relationship creation |
| Timeout | Complex graph | Optimize traversal, cache intermediate results |

### Error Recovery

- **Cycle breaking**: Remove weakest edges in cycle
- **Depth limits**: Interrupt traversal at max depth
- **Confidence filtering**: Exclude low-confidence chains
- **Timeout handling**: Return partial results with progress indicator
- **Data validation**: Verify node existence and relationship types

## Best Practices

✓ **Define causal relationships clearly** - Use consistent relationship types and semantics  
✓ **Add confidence scores** - Weight relationships by certainty for better ranking  
✓ **Enable cycle detection** - Prevent infinite loops in complex graphs  
✓ **Set reasonable depth limits** - Avoid memory issues with very deep chains  
✓ **Use appropriate algorithms** - DFS for deep chains, BFS for propagation analysis  
✓ **Rank results meaningfully** - Apply proximity or confidence-based scoring  
✓ **Validate root causes** - Verify causes have no incoming causal edges  
✓ **Document assumptions** - Clarify causal semantics for your domain  
✓ **Cache traversals** - Store frequently used paths for performance  
✓ **Monitor performance** - Track analysis time and result quality  
✓ **Handle partial results** - Return best-effort answers for timeout scenarios  
✓ **Version relationship types** - Allow evolution of causal definitions  

## Advanced Features

### Multi-Cause Analysis
Handle events caused by multiple independent or dependent causes, including AND/OR logic for cause combinations.

### Temporal Causality
Consider time ordering when relationships include temporal properties (latency, timestamp).

### Strength Degradation
Apply decay functions to reduce confidence in distant causes (causality weakens over distance).

### Custom Scoring Functions
Define domain-specific scoring for combining multiple ranking criteria.

### Batch Analysis
Analyze multiple targets or sources simultaneously for comparative impact assessment.

### Path Comparison
Compare different causal paths to the same effect to identify alternative explanations.

## Integration Points

This skill integrates with:

- **Graph Path Reasoning Analyzer** - Find alternative paths and structural patterns
- **Transitive Closure Generator** - Compute all reachable nodes from a source
- **Graph Rule Engine Builder** - Define complex causal rules
- **Ontology-Based Inference Helper** - Apply domain ontologies to causal relationships
- **Graph Query Optimization Assistant** - Optimize traversal queries
- **Graph Schema Validation** - Validate causal relationship schemas
- **Multi-Hop Reasoning Query Builder** - Build complex reasoning queries

## Recommended Libraries

### Graph Processing
- `networkx` - Graph construction, traversal algorithms
- `igraph` - Fast graph algorithms and cycle detection
- `graphlib` - Topological sorting and DAG operations
- `pygraphviz` - Graph visualization

### Data Structures
- `dataclasses` - Python classes for configuration
- `typing` - Type hints for clarity
- `collections` - Deque for BFS traversal

### Analysis
- `itertools` - Combinatorial path generation
- `heapq` - Priority queues for weighted traversal
- `functools` - Memoization for path caching

### Visualization
- `matplotlib` - Graph plotting
- `plotly` - Interactive visualization
- `pyvis` - Interactive network visualization

### Testing & Validation
- `pytest` - Test framework
- `hypothesis` - Property-based testing

## Related Skills

- **Graph Path Reasoning Analyzer** - Find specific paths and patterns
- **Transitive Closure Generator** - Compute all reachable nodes
- **Graph Rule Engine Builder** - Define inference rules
- **Ontology-Based Inference Helper** - Apply domain semantics
- **Multi-Hop Reasoning Query Builder** - Complex query construction

---

**Version:** 1.0.0
