# Causal Chain Analysis - Design Patterns & Algorithms

Comprehensive collection of design patterns, algorithms, and implementation strategies for causal chain analysis in knowledge graphs.

## Traversal Algorithms

### Pattern 1: Depth-First Search (DFS) for Root Cause Analysis

Find all root causes by traversing backward through the graph until hitting nodes with no incoming edges.

**Use Case:** Identifying the deepest root causes in a chain

**Implementation:**
```python
def find_root_causes_dfs(graph, target_node, relation_types):
    """
    Find all root causes using depth-first search backward traversal.
    
    Args:
        graph: Graph structure with nodes and edges
        target_node: Node to analyze
        relation_types: List of causal relationship types to follow
    
    Returns:
        List of root cause nodes
    """
    visited = set()
    root_causes = []
    
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        
        # Get incoming causal edges
        incoming = graph.get_incoming_edges(
            node, 
            relation_types=relation_types
        )
        
        if not incoming:
            # No incoming edges = root cause
            root_causes.append(node)
        else:
            # Recurse on source nodes
            for source_node, edge_data in incoming:
                dfs(source_node)
    
    dfs(target_node)
    return root_causes


# Example usage:
root_causes = find_root_causes_dfs(
    graph=incident_graph,
    target_node="SystemOutage",
    relation_types=["causes", "leads_to", "results_in"]
)
# Returns: ["PowerSurge"]
```

**Complexity:** O(V + E) time, O(V) space  
**Best For:** Deep chains, comprehensive root cause identification

---

### Pattern 2: Breadth-First Search (BFS) for Effect Propagation

Find all effects by level, useful for understanding propagation waves.

**Use Case:** Assessing impact propagation and affected system levels

**Implementation:**
```python
def trace_effects_bfs(graph, source_node, relation_types, max_depth=None):
    """
    Find all downstream effects using BFS for level-by-level propagation.
    
    Args:
        graph: Graph structure
        source_node: Starting node
        relation_types: Causal relationship types to follow
        max_depth: Maximum traversal depth (None = unlimited)
    
    Returns:
        Dictionary with effects organized by level
    """
    from collections import deque
    
    visited = set()
    effects_by_level = {0: [source_node]}
    queue = deque([(source_node, 0)])
    
    while queue:
        current_node, depth = queue.popleft()
        
        if current_node in visited:
            continue
        visited.add(current_node)
        
        # Check depth limit
        if max_depth and depth >= max_depth:
            continue
        
        # Get outgoing causal edges
        outgoing = graph.get_outgoing_edges(
            current_node,
            relation_types=relation_types
        )
        
        for target_node, edge_data in outgoing:
            if target_node not in visited:
                next_depth = depth + 1
                if next_depth not in effects_by_level:
                    effects_by_level[next_depth] = []
                effects_by_level[next_depth].append(target_node)
                queue.append((target_node, next_depth))
    
    return effects_by_level


# Example usage:
effects = trace_effects_bfs(
    graph=infrastructure_graph,
    source_node="DatabaseFailure",
    relation_types=["triggers", "leads_to"],
    max_depth=4
)
# Returns: {0: ["DatabaseFailure"], 1: ["APIService"], 2: ["WebServer"], ...}
```

**Complexity:** O(V + E) time, O(V) space  
**Best For:** Level-by-level propagation analysis, proximity ranking

---

### Pattern 3: Topological Sort for Dependency Ordering

Establish a valid ordering respecting all causal dependencies (requires DAG).

**Use Case:** Event scheduling, dependency resolution, execution planning

**Implementation:**
```python
def topological_sort_causal_chain(graph, relation_types):
    """
    Perform topological sort on causal chains (works only on DAGs).
    
    Uses Kahn's algorithm for O(V + E) performance.
    """
    from collections import deque
    
    # Calculate in-degrees
    in_degree = {node: 0 for node in graph.nodes()}
    
    for node in graph.nodes():
        for target, _ in graph.get_outgoing_edges(node, relation_types):
            in_degree[target] += 1
    
    # Initialize queue with nodes having 0 in-degree
    queue = deque([n for n in graph.nodes() if in_degree[n] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        # Remove edges from current node
        for target, _ in graph.get_outgoing_edges(node, relation_types):
            in_degree[target] -= 1
            if in_degree[target] == 0:
                queue.append(target)
    
    # Check for cycles
    if len(topo_order) != len(graph.nodes()):
        raise ValueError("Graph contains cycles - topological sort not possible")
    
    return topo_order


# Example usage:
try:
    order = topological_sort_causal_chain(
        graph=workflow_graph,
        relation_types=["depends_on"]
    )
    # Execute in order: order[0], order[1], ...
except ValueError:
    # Handle cyclic dependencies
    pass
```

**Complexity:** O(V + E) time  
**Limitations:** Only works on DAGs (acyclic graphs)  
**Best For:** Workflow scheduling, dependency resolution

---

### Pattern 4: Dijkstra's Algorithm for Confidence-Weighted Paths

Find shortest path considering edge weights as inverse confidence.

**Use Case:** Finding most confident causal paths

**Implementation:**
```python
def find_highest_confidence_path(graph, source, target):
    """
    Find path with maximum cumulative confidence using Dijkstra's algorithm.
    
    Confidence is treated as inverse distance (higher confidence = shorter path).
    """
    import heapq
    
    # Initialize distances and previous nodes
    distances = {node: float('-inf') for node in graph.nodes()}
    distances[source] = 1.0  # Start with confidence 1.0
    previous = {node: None for node in graph.nodes()}
    
    # Priority queue: (-confidence, node)
    pq = [(-1.0, source)]
    visited = set()
    
    while pq:
        neg_conf, current = heapq.heappop(pq)
        current_conf = -neg_conf
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == target:
            return current_conf, reconstruct_path(previous, source, target)
        
        # Explore neighbors
        for neighbor, edge_data in graph.get_outgoing_edges(current):
            edge_conf = edge_data.get('confidence', 0.5)
            new_conf = current_conf * edge_conf
            
            if new_conf > distances[neighbor]:
                distances[neighbor] = new_conf
                previous[neighbor] = current
                heapq.heappush(pq, (-new_conf, neighbor))
    
    return None, None  # No path found


def reconstruct_path(previous, source, target):
    """Reconstruct path from previous nodes dict."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    return path[::-1]


# Example usage:
confidence, path = find_highest_confidence_path(
    graph=causal_graph,
    source="RootCause",
    target="Impact"
)
# Returns: (0.756, ["RootCause", "Intermediate", "Impact"])
```

**Complexity:** O((V + E) log V)  
**Best For:** Finding most confident causal paths

---

## Cycle Detection Patterns

### Pattern 5: Tarjan's Algorithm for Strongly Connected Components

Identifies all cycles in the graph efficiently.

**Use Case:** Finding feedback loops, resolving circular dependencies

**Implementation:**
```python
def find_cycles_tarjan(graph, relation_types):
    """
    Find all strongly connected components (cycles) using Tarjan's algorithm.
    
    Returns:
        List of cycles, where each cycle is a list of nodes
    """
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    cycles = []
    
    def strongconnect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack[node] = True
        
        # Consider successors of node
        for successor, _ in graph.get_outgoing_edges(node, relation_types):
            if successor not in index:
                strongconnect(successor)
                lowlink[node] = min(lowlink[node], lowlink[successor])
            elif on_stack.get(successor, False):
                lowlink[node] = min(lowlink[node], index[successor])
        
        # If node is a root node, pop the stack and print an SCC
        if lowlink[node] == index[node]:
            component = []
            while True:
                successor = stack.pop()
                on_stack[successor] = False
                component.append(successor)
                if successor == node:
                    break
            
            # Only report cycles (components with >1 node or self-loop)
            if len(component) > 1 or any(
                target == node 
                for target, _ in graph.get_outgoing_edges(node, relation_types)
            ):
                cycles.append(component)
    
    for node in graph.nodes():
        if node not in index:
            strongconnect(node)
    
    return cycles


# Example usage:
cycles = find_cycles_tarjan(
    graph=dependency_graph,
    relation_types=["depends_on", "causes"]
)
if cycles:
    print(f"Found {len(cycles)} cycles:")
    for cycle in cycles:
        print(f"  Cycle: {' -> '.join(cycle)} -> {cycle[0]}")
```

**Complexity:** O(V + E) time, O(V) space  
**Best For:** Finding all cycles, identifying feedback loops

---

### Pattern 6: DFS-Based Cycle Detection

Simple cycle detection during traversal using color marking.

**Use Case:** Quick cycle detection, stopping on first cycle

**Implementation:**
```python
def has_cycle_dfs(graph, relation_types):
    """
    Detect if graph contains cycles using DFS with color marking.
    
    Colors:
        WHITE (0): Unvisited
        GRAY (1): Currently being processed
        BLACK (2): Completely processed
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph.nodes()}
    parent = {node: None for node in graph.nodes()}
    
    def has_cycle_util(node):
        color[node] = GRAY
        
        for neighbor, _ in graph.get_outgoing_edges(node, relation_types):
            if color[neighbor] == WHITE:
                parent[neighbor] = node
                if has_cycle_util(neighbor):
                    return True
            elif color[neighbor] == GRAY:
                # Back edge found - cycle detected
                return True
        
        color[node] = BLACK
        return False
    
    # Check all nodes (for disconnected components)
    for node in graph.nodes():
        if color[node] == WHITE:
            if has_cycle_util(node):
                return True
    
    return False


# Example usage:
if has_cycle_dfs(graph, relation_types=["leads_to"]):
    print("Cyclic causal dependencies detected!")
```

**Complexity:** O(V + E) time  
**Best For:** Quick cycle detection, simpler than Tarjan's

---

## Chain Ranking Patterns

### Pattern 7: Proximity-Based Ranking

Rank chains by distance (closer causes/effects ranked higher).

**Use Case:** Identifying most immediate/direct impacts

**Implementation:**
```python
def rank_chains_by_proximity(graph, source, target):
    """
    Find all paths and rank by proximity (shortest paths first).
    
    Returns:
        List of (path, distance) tuples sorted by distance
    """
    from collections import deque
    
    # BFS to find all paths with distances
    visited = {source: 0}
    queue = deque([(source, [source])])
    paths_by_distance = []
    
    while queue:
        current, path = queue.popleft()
        current_dist = len(path) - 1
        
        if current == target:
            paths_by_distance.append((path, current_dist))
            continue
        
        for neighbor, _ in graph.get_outgoing_edges(current):
            if neighbor not in visited or visited[neighbor] == current_dist + 1:
                visited[neighbor] = current_dist + 1
                queue.append((neighbor, path + [neighbor]))
    
    # Sort by distance (ascending)
    return sorted(paths_by_distance, key=lambda x: x[1])


# Example usage:
ranked_paths = rank_chains_by_proximity(
    graph=incident_graph,
    source="RootCause",
    target="UserImpact"
)
for path, distance in ranked_paths:
    print(f"Distance {distance}: {' -> '.join(path)}")
```

**Complexity:** O(V + E) time  
**Best For:** Finding most direct causality

---

### Pattern 8: Confidence-Based Ranking

Score chains by cumulative edge confidence.

**Use Case:** Prioritizing likely causal chains

**Implementation:**
```python
def rank_chains_by_confidence(graph, all_paths):
    """
    Score paths by cumulative confidence (product of edge confidences).
    
    Returns:
        List of (path, confidence_score) tuples sorted by confidence descending
    """
    scored_paths = []
    
    for path in all_paths:
        confidence = 1.0
        
        # Multiply confidences along the path
        for i in range(len(path) - 1):
            source = path[i]
            target = path[i + 1]
            edge = graph.get_edge(source, target)
            
            # Default to 0.5 if confidence not specified
            edge_conf = edge.get('confidence', 0.5)
            confidence *= edge_conf
        
        scored_paths.append((path, confidence))
    
    # Sort by confidence descending
    return sorted(scored_paths, key=lambda x: x[1], reverse=True)


# Example usage:
paths = find_all_paths(graph, "Event", "Outcome")
ranked = rank_chains_by_confidence(graph, paths)
for path, conf in ranked:
    print(f"Confidence {conf:.2%}: {' -> '.join(path)}")
```

**Complexity:** O(P * L) where P = number of paths, L = path length  
**Best For:** Prioritizing likely chains

---

### Pattern 9: Composite Scoring (Multi-Criteria Ranking)

Combine multiple ranking criteria for sophisticated prioritization.

**Use Case:** Complex ranking with multiple factors

**Implementation:**
```python
def rank_chains_composite(graph, paths, weights=None):
    """
    Score paths using weighted combination of multiple criteria.
    
    Criteria:
        - Confidence: Product of edge confidences
        - Proximity: Inverse of path length (shorter = higher score)
        - Importance: Weighted by node/edge importance scores
    
    Args:
        weights: Dict of {criterion_name: weight}
    """
    if weights is None:
        weights = {
            'confidence': 0.5,
            'proximity': 0.3,
            'importance': 0.2
        }
    
    scored_paths = []
    
    for path in paths:
        # Calculate confidence score
        confidence = 1.0
        importance = 0.0
        
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i + 1])
            confidence *= edge.get('confidence', 0.5)
            importance += edge.get('importance', 0.5)
        
        # Average importance
        importance = importance / (len(path) - 1) if len(path) > 1 else 0.5
        
        # Proximity score (inverse of length)
        proximity = 1.0 / len(path)
        
        # Composite score
        composite = (
            weights['confidence'] * confidence +
            weights['proximity'] * proximity +
            weights['importance'] * importance
        )
        
        scored_paths.append({
            'path': path,
            'score': composite,
            'breakdown': {
                'confidence': confidence,
                'proximity': proximity,
                'importance': importance
            }
        })
    
    # Sort by composite score descending
    return sorted(scored_paths, key=lambda x: x['score'], reverse=True)


# Example usage:
results = rank_chains_composite(
    graph,
    paths,
    weights={'confidence': 0.6, 'proximity': 0.3, 'importance': 0.1}
)
```

**Complexity:** O(P * L)  
**Best For:** Sophisticated ranking with multiple criteria

---

## Filtering Patterns

### Pattern 10: Depth-Limited Traversal

Limit traversal depth to avoid explosions in large graphs.

**Use Case:** Controlling complexity in large graphs, focusing on nearby causes

**Implementation:**
```python
def trace_effects_depth_limited(graph, source, max_depth, relation_types):
    """
    Trace effects with depth limitation to control complexity.
    
    Args:
        max_depth: Maximum levels to traverse
    
    Returns:
        Effects organized by depth level
    """
    from collections import deque
    
    effects_by_level = {}
    queue = deque([(source, 0)])
    visited = set()
    
    while queue:
        node, depth = queue.popleft()
        
        if node in visited or depth > max_depth:
            continue
        
        visited.add(node)
        
        if depth not in effects_by_level:
            effects_by_level[depth] = []
        effects_by_level[depth].append(node)
        
        # Only continue if under max depth
        if depth < max_depth:
            for neighbor, _ in graph.get_outgoing_edges(node, relation_types):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
    
    return effects_by_level


# Example usage:
effects = trace_effects_depth_limited(
    graph=large_graph,
    source="RootCause",
    max_depth=3,
    relation_types=["causes"]
)
```

**Best For:** Large graphs, controlling traversal complexity

---

### Pattern 11: Confidence Threshold Filtering

Filter paths by minimum confidence threshold.

**Use Case:** Excluding low-certainty causal chains

**Implementation:**
```python
def filter_paths_by_confidence(graph, paths, min_confidence):
    """
    Keep only paths with confidence >= threshold.
    
    Args:
        min_confidence: Minimum acceptable confidence (0.0 to 1.0)
    
    Returns:
        Filtered list of (path, confidence) tuples
    """
    filtered = []
    
    for path in paths:
        confidence = 1.0
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i + 1])
            confidence *= edge.get('confidence', 0.5)
        
        if confidence >= min_confidence:
            filtered.append((path, confidence))
    
    return sorted(filtered, key=lambda x: x[1], reverse=True)


# Example usage:
high_confidence_paths = filter_paths_by_confidence(
    graph=causal_graph,
    paths=all_paths,
    min_confidence=0.75
)
```

**Best For:** Excluding uncertain causal links

---

### Pattern 12: Temporal Window Filtering

Filter edges based on temporal properties (latency, timestamp).

**Use Case:** Time-sensitive causal analysis

**Implementation:**
```python
def filter_paths_by_time_window(graph, paths, max_latency_ms):
    """
    Keep only paths where total latency <= max_latency_ms.
    
    Args:
        max_latency_ms: Maximum acceptable total latency in milliseconds
    
    Returns:
        Paths within time window
    """
    valid_paths = []
    
    for path in paths:
        total_latency = 0
        valid = True
        
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i + 1])
            latency = edge.get('latency_ms', 0)
            total_latency += latency
            
            if total_latency > max_latency_ms:
                valid = False
                break
        
        if valid:
            valid_paths.append((path, total_latency))
    
    return sorted(valid_paths, key=lambda x: x[1])


# Example usage:
fast_paths = filter_paths_by_time_window(
    graph=temporal_graph,
    paths=all_paths,
    max_latency_ms=500
)
```

**Best For:** Time-sensitive systems, latency-aware analysis

---

## Advanced Patterns

### Pattern 13: Multi-Path Comparison

Compare different causal paths to the same effect.

**Use Case:** Understanding alternative explanations, causal redundancy

**Implementation:**
```python
def compare_alternative_paths(graph, target_node, relation_types):
    """
    Find and compare all paths leading to target node.
    
    Returns:
        List of paths with comparative analysis
    """
    all_paths = find_all_paths_to_target(graph, target_node, relation_types)
    
    compared = []
    for i, path in enumerate(all_paths):
        # Calculate confidence
        confidence = 1.0
        for j in range(len(path) - 1):
            edge = graph.get_edge(path[j], path[j + 1])
            confidence *= edge.get('confidence', 0.5)
        
        compared.append({
            'path_num': i,
            'path': path,
            'length': len(path),
            'confidence': confidence,
            'root_cause': path[0],
            'intermediate_nodes': path[1:-1]
        })
    
    # Sort by confidence
    compared.sort(key=lambda x: x['confidence'], reverse=True)
    
    return compared
```

**Use Case:** "Are there multiple independent causes for this failure?"

---

### Pattern 14: Transitive Closure with Confidence

Compute all reachable nodes with confidence scores.

**Use Case:** Understanding complete impact scope

**Implementation:**
```python
def transitive_closure_with_confidence(graph, source, relation_types):
    """
    Compute transitive closure: all reachable nodes with confidence scores.
    
    Returns:
        Dict mapping each reachable node to its maximum confidence score
    """
    visited = {source: 1.0}
    queue = [(source, 1.0)]
    
    while queue:
        current, current_conf = queue.pop(0)
        
        for target, edge_data in graph.get_outgoing_edges(current, relation_types):
            edge_conf = edge_data.get('confidence', 0.5)
            new_conf = current_conf * edge_conf
            
            if target not in visited or new_conf > visited[target]:
                visited[target] = new_conf
                queue.append((target, new_conf))
    
    return visited


# Example usage:
reachable = transitive_closure_with_confidence(
    graph=incident_graph,
    source="RootCause",
    relation_types=["causes", "leads_to"]
)
print(f"Total impact: {len(reachable)} nodes affected")
for node, conf in sorted(reachable.items(), key=lambda x: x[1], reverse=True):
    print(f"  {node}: {conf:.2%} confidence")
```

**Best For:** Computing complete impact scope

---

## Performance Optimization Patterns

### Pattern 15: Path Caching

Cache frequently computed paths for performance.

**Use Case:** Repeated analysis on same graph

**Implementation:**
```python
class CachedCausalAnalyzer:
    def __init__(self, graph):
        self.graph = graph
        self.path_cache = {}
        self.cause_cache = {}
    
    def find_root_causes_cached(self, target, relation_types):
        """Find root causes with caching."""
        cache_key = (target, tuple(sorted(relation_types)))
        
        if cache_key in self.cause_cache:
            return self.cause_cache[cache_key]
        
        causes = find_root_causes_dfs(self.graph, target, relation_types)
        self.cause_cache[cache_key] = causes
        return causes
    
    def trace_effects_cached(self, source, relation_types):
        """Trace effects with caching."""
        cache_key = (source, tuple(sorted(relation_types)))
        
        if cache_key in self.path_cache:
            return self.path_cache[cache_key]
        
        effects = trace_effects_bfs(self.graph, source, relation_types)
        self.path_cache[cache_key] = effects
        return effects
    
    def clear_cache(self):
        """Clear caches (call after graph modifications)."""
        self.path_cache.clear()
        self.cause_cache.clear()
```

**Best For:** Repeated queries on static graphs

---

## Summary

| Pattern | Algorithm | Complexity | Best Use |
|---------|-----------|-----------|----------|
| 1. Root Cause (DFS) | Depth-First Search | O(V+E) | Finding deepest causes |
| 2. Effect Tracing (BFS) | Breadth-First Search | O(V+E) | Level-by-level propagation |
| 3. Ordering | Topological Sort | O(V+E) | DAG scheduling |
| 4. Confidence Paths | Dijkstra's | O((V+E)logV) | Best confidence path |
| 5. Cycles | Tarjan's | O(V+E) | Find all cycles |
| 6. Cycle Detection | DFS Color | O(V+E) | Quick cycle check |
| 7. Proximity Ranking | BFS + Sort | O(V+E+PlogP) | Distance-based ranking |
| 8. Confidence Ranking | Scoring | O(P*L) | Confidence-based ranking |
| 9. Composite Ranking | Multi-criteria | O(P*L) | Complex scoring |
| 10. Depth Limiting | BFS Limited | O(V+E) | Control complexity |
| 11. Confidence Filter | Threshold | O(P*L) | Exclude uncertain chains |
| 12. Temporal Filter | Time-based | O(P*L) | Time-sensitive analysis |
| 13. Path Comparison | Multi-path | O(P*(V+E)) | Compare alternatives |
| 14. Transitive Closure | DFS Full | O(V+E) | Complete impact |
| 15. Caching | Memoization | O(1) lookup | Performance |


