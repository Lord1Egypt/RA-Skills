"""
Causal Chain Analyzer - Production-Ready Implementation

Comprehensive causal analysis toolkit for knowledge graphs.
Supports root cause analysis, effect propagation, cycle detection, and chain ranking.

Author: Knowledge Graph Team
License: MIT
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import deque
from enum import Enum
import json


# ==================== Data Classes ====================

class TraversalAlgorithm(Enum):
    """Supported traversal algorithms."""
    DFS = "dfs"  # Depth-first search
    BFS = "bfs"  # Breadth-first search
    DIJKSTRA = "dijkstra"  # Confidence-weighted shortest path
    TOPOLOGICAL = "topological"  # Topological sort (DAG only)


class AnalysisDirection(Enum):
    """Direction of causal analysis."""
    BACKWARD = "backward"  # Find root causes (traverse backward)
    FORWARD = "forward"  # Trace effects (traverse forward)


@dataclass
class CausalRelationship:
    """Represents a causal relationship between nodes."""
    source: str
    target: str
    relation_type: str
    weight: float = 1.0  # Strength of causality (0.0 to 1.0)
    confidence: float = 0.5  # Certainty of relationship (0.0 to 1.0)
    latency_ms: Optional[float] = None  # Time delay between cause and effect
    severity: Optional[str] = None  # Impact severity
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CausalChain:
    """Represents a chain of causes or effects."""
    path: List[str]  # Ordered sequence of node IDs
    confidence: float = 1.0  # Cumulative confidence
    total_latency_ms: Optional[float] = None  # Total latency
    relationship_types: List[str] = field(default_factory=list)  # Types along path
    depth: int = field(init=False)  # Number of hops (calculated)

    def __post_init__(self):
        self.depth = len(self.path) - 1 if len(self.path) > 0 else 0


@dataclass
class ChainAnalysisResult:
    """Results from causal chain analysis."""
    target_node: str
    analysis_type: str  # "root_causes" or "effects"
    chains: List[CausalChain]
    root_causes: Optional[List[str]] = None  # For backward analysis
    affected_nodes: Optional[Set[str]] = None  # For forward analysis
    cycles_detected: List[List[str]] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'target_node': self.target_node,
            'analysis_type': self.analysis_type,
            'chains': [
                {
                    'path': chain.path,
                    'depth': chain.depth,
                    'confidence': chain.confidence,
                    'latency_ms': chain.total_latency_ms
                }
                for chain in self.chains
            ],
            'root_causes': list(self.root_causes) if self.root_causes else None,
            'affected_nodes': list(self.affected_nodes) if self.affected_nodes else None,
            'cycles_detected': self.cycles_detected,
            'statistics': self.statistics
        }


@dataclass
class CausalConfig:
    """Configuration for causal chain analysis."""
    # Graph data
    graph_data: Dict[str, Any]

    # Relationship settings
    causal_relation_types: List[str] = field(default_factory=lambda: [
        "causes", "leads_to", "results_in", "triggers", "depends_on",
        "influences", "contributes_to", "propagates_to"
    ])

    # Analysis settings
    max_depth: int = 10
    detect_cycles: bool = True
    confidence_threshold: float = 0.0  # Minimum confidence to include
    algorithm: TraversalAlgorithm = TraversalAlgorithm.BFS

    # Ranking settings
    ranking_strategy: str = "confidence"  # "confidence", "proximity", "composite"

    # Performance settings
    cache_paths: bool = True
    max_results: Optional[int] = None  # Limit result set size


# ==================== CausalChainAnalyzer ====================

class CausalChainAnalyzer:
    """
    Main analyzer for causal chains in knowledge graphs.

    Provides methods for:
    - Finding root causes of events
    - Tracing downstream effects
    - Detecting cycles and feedback loops
    - Ranking causal chains by various metrics
    - Analyzing chain structure and propagation
    """

    def __init__(self, config: CausalConfig):
        """Initialize analyzer with configuration."""
        self.config = config
        self._build_graph_structure()
        self._path_cache = {} if config.cache_paths else None

    def _build_graph_structure(self):
        """Build internal graph structure from config data."""
        self.nodes = set()
        self.edges = {}  # {source: {target: [relationships]}}
        self.reverse_edges = {}  # {target: {source: [relationships]}}

        # Add nodes
        if 'nodes' in self.config.graph_data:
            for node_id in self.config.graph_data['nodes']:
                self.nodes.add(node_id)
                self.edges[node_id] = {}
                self.reverse_edges[node_id] = {}

        # Add edges (relationships)
        if 'edges' in self.config.graph_data:
            for edge in self.config.graph_data['edges']:
                source = edge.get('source')
                target = edge.get('target')
                rel_type = edge.get('type', 'causes')

                if source and target:
                    # Ensure nodes exist
                    self.nodes.add(source)
                    self.nodes.add(target)

                    if source not in self.edges:
                        self.edges[source] = {}
                    if target not in self.edges:
                        self.edges[target] = {}
                    if source not in self.reverse_edges:
                        self.reverse_edges[source] = {}
                    if target not in self.reverse_edges:
                        self.reverse_edges[target] = {}

                    # Store edge with metadata
                    if target not in self.edges[source]:
                        self.edges[source][target] = []
                    self.edges[source][target].append(edge)

                    # Reverse mapping
                    if source not in self.reverse_edges[target]:
                        self.reverse_edges[target][source] = []
                    self.reverse_edges[target][source].append(edge)

    def find_root_causes(
        self,
        target_node: str,
        algorithm: Optional[TraversalAlgorithm] = None,
        confidence_threshold: Optional[float] = None
    ) -> ChainAnalysisResult:
        """
        Find all root causes of a target node by traversing backward.

        Root causes are nodes with no incoming causal edges.

        Args:
            target_node: The effect node to analyze
            algorithm: Traversal algorithm to use (default: config setting)
            confidence_threshold: Minimum confidence filter

        Returns:
            ChainAnalysisResult with root causes and causal chains
        """
        algo = algorithm or self.config.algorithm
        threshold = confidence_threshold if confidence_threshold is not None else self.config.confidence_threshold

        # Cache key
        cache_key = f"root_causes:{target_node}:{algo.value}:{threshold}"
        if self._path_cache and cache_key in self._path_cache:
            return self._path_cache[cache_key]

        if algo == TraversalAlgorithm.DFS:
            chains = self._find_root_causes_dfs(target_node, threshold)
        elif algo == TraversalAlgorithm.BFS:
            chains = self._find_root_causes_bfs(target_node, threshold)
        else:
            chains = self._find_root_causes_dfs(target_node, threshold)

        # Extract root causes
        root_causes = set()
        for chain in chains:
            if chain.path:
                root_causes.add(chain.path[0])

        # Detect cycles if enabled
        cycles = []
        if self.config.detect_cycles:
            cycles = self._detect_cycles_tarjan()

        # Build result
        result = ChainAnalysisResult(
            target_node=target_node,
            analysis_type="root_causes",
            chains=chains,
            root_causes=root_causes,
            cycles_detected=cycles,
            statistics={
                'total_chains': len(chains),
                'root_causes_count': len(root_causes),
                'average_depth': sum(c.depth for c in chains) / len(chains) if chains else 0,
                'max_depth': max((c.depth for c in chains), default=0)
            }
        )

        if self._path_cache:
            self._path_cache[cache_key] = result

        return result

    def trace_effects(
        self,
        source_node: str,
        algorithm: Optional[TraversalAlgorithm] = None,
        confidence_threshold: Optional[float] = None
    ) -> ChainAnalysisResult:
        """
        Trace all downstream effects of a source node by traversing forward.

        Args:
            source_node: The cause node to analyze
            algorithm: Traversal algorithm to use
            confidence_threshold: Minimum confidence filter

        Returns:
            ChainAnalysisResult with effects and propagation chains
        """
        algo = algorithm or self.config.algorithm
        threshold = confidence_threshold if confidence_threshold is not None else self.config.confidence_threshold

        cache_key = f"effects:{source_node}:{algo.value}:{threshold}"
        if self._path_cache and cache_key in self._path_cache:
            return self._path_cache[cache_key]

        if algo == TraversalAlgorithm.DFS:
            chains = self._trace_effects_dfs(source_node, threshold)
        elif algo == TraversalAlgorithm.BFS:
            chains = self._trace_effects_bfs(source_node, threshold)
        else:
            chains = self._trace_effects_bfs(source_node, threshold)

        # Extract affected nodes
        affected = set()
        for chain in chains:
            affected.update(chain.path[1:])  # Exclude source

        # Detect cycles if enabled
        cycles = []
        if self.config.detect_cycles:
            cycles = self._detect_cycles_tarjan()

        result = ChainAnalysisResult(
            target_node=source_node,
            analysis_type="effects",
            chains=chains,
            affected_nodes=affected,
            cycles_detected=cycles,
            statistics={
                'source_node': source_node,
                'propagation_paths': len(chains),
                'total_affected': len(affected),
                'average_depth': sum(c.depth for c in chains) / len(chains) if chains else 0,
                'max_depth': max((c.depth for c in chains), default=0)
            }
        )

        if self._path_cache:
            self._path_cache[cache_key] = result

        return result

    def detect_cycles(self) -> List[List[str]]:
        """
        Detect all cycles in the causal graph using Tarjan's algorithm.

        Returns:
            List of cycles, where each cycle is a list of nodes
        """
        return self._detect_cycles_tarjan()

    def analyze_chain_depth(self, source_node: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze chain depth statistics.

        Args:
            source_node: If provided, analyze from this node; otherwise analyze whole graph

        Returns:
            Dictionary with depth statistics
        """
        if source_node:
            # Analyze from specific node
            effects_result = self.trace_effects(source_node)
            chains = effects_result.chains
        else:
            # Analyze all chains in graph
            all_chains = []
            for node in self.nodes:
                result = self.trace_effects(node)
                all_chains.extend(result.chains)
            chains = all_chains

        if not chains:
            return {
                'nodes_analyzed': 1 if source_node else len(self.nodes),
                'total_chains': 0,
                'max_depth': 0,
                'average_depth': 0,
                'depth_distribution': {}
            }

        depths = [c.depth for c in chains]
        depth_dist = {}
        for d in depths:
            depth_dist[d] = depth_dist.get(d, 0) + 1

        return {
            'nodes_analyzed': 1 if source_node else len(self.nodes),
            'total_chains': len(chains),
            'max_depth': max(depths),
            'average_depth': sum(depths) / len(depths),
            'median_depth': sorted(depths)[len(depths) // 2],
            'depth_distribution': depth_dist
        }

    def rank_chains(
        self,
        chains: List[CausalChain],
        strategy: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Tuple[CausalChain, float]]:
        """
        Rank causal chains by specified strategy.

        Args:
            chains: List of chains to rank
            strategy: Ranking strategy ("confidence", "proximity", "composite")
            limit: Maximum results to return

        Returns:
            Sorted list of (chain, score) tuples
        """
        strategy = strategy or self.config.ranking_strategy

        scored = []
        for chain in chains:
            if strategy == "confidence":
                score = chain.confidence
            elif strategy == "proximity":
                # Inverse of depth (shorter = higher score)
                score = 1.0 / (chain.depth + 1) if chain.depth >= 0 else 0
            elif strategy == "composite":
                # Combination of confidence and proximity
                confidence_score = chain.confidence
                proximity_score = 1.0 / (chain.depth + 1) if chain.depth >= 0 else 0
                score = 0.6 * confidence_score + 0.4 * proximity_score
            else:
                score = chain.confidence

            scored.append((chain, score))

        # Sort by score descending
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)

        # Apply limit if specified
        if limit:
            ranked = ranked[:limit]

        return ranked

    def filter_by_confidence(
        self,
        chains: List[CausalChain],
        min_confidence: float
    ) -> List[CausalChain]:
        """Filter chains by minimum confidence threshold."""
        return [c for c in chains if c.confidence >= min_confidence]

    def filter_by_depth(
        self,
        chains: List[CausalChain],
        max_depth: int
    ) -> List[CausalChain]:
        """Filter chains by maximum depth."""
        return [c for c in chains if c.depth <= max_depth]

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall graph statistics."""
        return {
            'total_nodes': len(self.nodes),
            'total_edges': sum(
                len(targets)
                for targets in self.edges.values()
            ),
            'has_cycles': bool(self._detect_cycles_tarjan()),
            'average_branching_factor': self._calculate_branching_factor()
        }

    # ==================== Private Methods ====================

    def _find_root_causes_dfs(
        self,
        target: str,
        confidence_threshold: float
    ) -> List[CausalChain]:
        """DFS-based root cause finding."""
        chains = []
        visited = set()

        def dfs_backward(node: str, path: List[str], conf: float):
            if node in visited:
                return
            visited.add(node)

            # Get incoming edges
            incoming = self.reverse_edges.get(node, {})

            if not incoming:
                # No incoming edges = root cause
                if conf >= confidence_threshold:
                    chains.append(CausalChain(
                        path=path[::-1],  # Reverse to root->...->target
                        confidence=conf
                    ))
            else:
                # Recurse on sources
                for source, edges in incoming.items():
                    for edge in edges:
                        edge_conf = edge.get('confidence', 0.5)
                        new_conf = conf * edge_conf

                        if new_conf >= confidence_threshold and len(path) < self.config.max_depth:
                            dfs_backward(source, path + [source], new_conf)

            visited.discard(node)  # Allow revisiting in different paths

        dfs_backward(target, [target], 1.0)
        return chains

    def _find_root_causes_bfs(
        self,
        target: str,
        confidence_threshold: float
    ) -> List[CausalChain]:
        """BFS-based root cause finding."""
        chains = []
        queue = deque([(target, [target], 1.0)])
        visited_at_depth = {}

        while queue:
            node, path, conf = queue.popleft()

            # Check depth limit
            if len(path) - 1 >= self.config.max_depth:
                continue

            # Check confidence threshold
            if conf < confidence_threshold:
                continue

            incoming = self.reverse_edges.get(node, {})

            if not incoming:
                # Root cause found
                chains.append(CausalChain(
                    path=path[::-1],
                    confidence=conf
                ))
            else:
                for source, edges in incoming.items():
                    for edge in edges:
                        edge_conf = edge.get('confidence', 0.5)
                        new_conf = conf * edge_conf

                        if new_conf >= confidence_threshold:
                            queue.append((source, path + [source], new_conf))

        return chains

    def _trace_effects_dfs(
        self,
        source: str,
        confidence_threshold: float
    ) -> List[CausalChain]:
        """DFS-based effect tracing."""
        chains = []
        visited = set()

        def dfs_forward(node: str, path: List[str], conf: float):
            if node in visited:
                return
            visited.add(node)

            outgoing = self.edges.get(node, {})

            if not outgoing:
                # Terminal node
                if len(path) > 1:  # Only include if path has more than source
                    chains.append(CausalChain(
                        path=path,
                        confidence=conf
                    ))
            else:
                for target, edges in outgoing.items():
                    for edge in edges:
                        edge_conf = edge.get('confidence', 0.5)
                        new_conf = conf * edge_conf

                        if new_conf >= confidence_threshold and len(path) < self.config.max_depth:
                            dfs_forward(target, path + [target], new_conf)

            visited.discard(node)

        dfs_forward(source, [source], 1.0)
        return chains

    def _trace_effects_bfs(
        self,
        source: str,
        confidence_threshold: float
    ) -> List[CausalChain]:
        """BFS-based effect tracing."""
        chains = []
        queue = deque([(source, [source], 1.0)])
        visited = set()

        while queue:
            node, path, conf = queue.popleft()

            if node in visited and len(path) > 1:
                continue
            visited.add(node)

            if len(path) > 1:  # Add path if it has effects
                chains.append(CausalChain(
                    path=path,
                    confidence=conf
                ))

            # Check limits
            if len(path) >= self.config.max_depth + 1:
                continue

            outgoing = self.edges.get(node, {})
            for target, edges in outgoing.items():
                for edge in edges:
                    edge_conf = edge.get('confidence', 0.5)
                    new_conf = conf * edge_conf

                    if new_conf >= confidence_threshold:
                        queue.append((target, path + [target], new_conf))

        return chains

    def _detect_cycles_tarjan(self) -> List[List[str]]:
        """Detect cycles using Tarjan's algorithm."""
        index_counter = [0]
        stack = []
        indices = {}
        lowlinks = {}
        on_stack = {}
        cycles = []

        def strongconnect(node):
            indices[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            stack.append(node)
            on_stack[node] = True

            # Successors
            for successor in self.edges.get(node, {}):
                if successor not in indices:
                    strongconnect(successor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[successor])
                elif on_stack.get(successor, False):
                    lowlinks[node] = min(lowlinks[node], indices[successor])

            # SCC found
            if lowlinks[node] == indices[node]:
                component = []
                while True:
                    successor = stack.pop()
                    on_stack[successor] = False
                    component.append(successor)
                    if successor == node:
                        break

                # Report only actual cycles
                if len(component) > 1 or any(
                    t == node for t in self.edges.get(node, {})
                ):
                    cycles.append(component)

        for node in self.nodes:
            if node not in indices:
                strongconnect(node)

        return cycles

    def _calculate_branching_factor(self) -> float:
        """Calculate average branching factor."""
        total_edges = sum(len(targets) for targets in self.edges.values())
        non_leaf_nodes = sum(1 for node in self.nodes if self.edges.get(node))

        if non_leaf_nodes == 0:
            return 0

        return total_edges / non_leaf_nodes


# ==================== Example Usage ====================

if __name__ == "__main__":
    # Example: IT Debugging scenario
    config = CausalConfig(
        graph_data={
            "nodes": {
                "PowerFailure": {},
                "ServerDown": {},
                "DatabaseDown": {},
                "CacheDown": {},
                "APIGatewayDown": {},
                "AuthServiceDown": {},
                "DashboardDown": {}
            },
            "edges": [
                {
                    "source": "PowerFailure",
                    "target": "ServerDown",
                    "type": "causes",
                    "confidence": 0.99,
                    "weight": 0.95
                },
                {
                    "source": "ServerDown",
                    "target": "DatabaseDown",
                    "type": "leads_to",
                    "confidence": 0.95,
                    "weight": 0.90
                },
                {
                    "source": "ServerDown",
                    "target": "CacheDown",
                    "type": "leads_to",
                    "confidence": 0.90,
                    "weight": 0.85
                },
                {
                    "source": "DatabaseDown",
                    "target": "APIGatewayDown",
                    "type": "results_in",
                    "confidence": 0.85,
                    "weight": 0.80
                },
                {
                    "source": "APIGatewayDown",
                    "target": "AuthServiceDown",
                    "type": "triggers",
                    "confidence": 0.98,
                    "weight": 0.95
                },
                {
                    "source": "AuthServiceDown",
                    "target": "DashboardDown",
                    "type": "leads_to",
                    "confidence": 0.95,
                    "weight": 0.90
                }
            ]
        },
        max_depth=10,
        detect_cycles=True,
        algorithm=TraversalAlgorithm.BFS
    )

    analyzer = CausalChainAnalyzer(config)

    # Find root causes
    print("=== Root Cause Analysis ===")
    result = analyzer.find_root_causes("DashboardDown")
    print(f"Target: {result.target_node}")
    print(f"Root causes: {result.root_causes}")
    print(f"Chains found: {len(result.chains)}")
    for chain in result.chains:
        print(f"  Path: {' -> '.join(chain.path)}, Confidence: {chain.confidence:.2%}")

    # Trace effects
    print("\n=== Effect Tracing ===")
    result = analyzer.trace_effects("PowerFailure")
    print(f"Source: {result.target_node}")
    print(f"Affected nodes: {result.affected_nodes}")
    print(f"Propagation chains: {len(result.chains)}")

    # Get statistics
    print("\n=== Graph Statistics ===")
    stats = analyzer.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")



