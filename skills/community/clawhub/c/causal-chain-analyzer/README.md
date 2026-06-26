# Causal Chain Analyzer - Quick Reference

Analyze and trace **cause-effect chains** in knowledge graphs to identify root causes and downstream impacts. Perform root cause analysis, impact propagation, and dependency tracing across complex system graphs.

## 📁 Structure

```
causal-chain-analyzer/
│
├── SKILL.md                             # Skill definition & overview
│
├── references/                          # Technical guidance
│   └── causal-chain-patterns.md         # Analysis patterns & algorithms
│
├── examples/                            # Domain examples
│   └── causal-chain-examples.md         # Real-world causal analysis scenarios
│
└── scripts/                             # Utility scripts
    └── causal_chain_analyzer.py         # CausalChainAnalyzer implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand causal chain analysis fundamentals
2. **Learn:** `references/causal-chain-patterns.md` - Analysis patterns and algorithms
3. **See:** `examples/causal-chain-examples.md` - Real-world analysis scenarios

### For Implementation

1. Use `scripts/causal_chain_analyzer.py` for causal chain analysis operations
2. Supports: Graph traversal, cycle detection, chain ranking, confidence scoring
3. Features: Find root causes, trace effects, detect cycles, rank causal chains

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, use cases, concepts |
| `causal-chain-patterns.md` | Analysis patterns, algorithms, traversal strategies |
| `causal-chain-examples.md` | IT debugging, RCA, dependency tracing, risk analysis |
| `causal_chain_analyzer.py` | Python CausalChainAnalyzer class |

## ⚡ Key Features

✓ Find root causes of events or failures  
✓ Trace downstream effects and impacts  
✓ Detect and handle cyclic dependencies  
✓ Rank causal chains by proximity or confidence  
✓ Support multiple traversal algorithms (DFS, BFS, topological sort)  
✓ Filter chains by depth, confidence, or time windows  
✓ Analyze chain structure and propagation patterns  
✓ Handle complex multi-cause scenarios  
✓ Probabilistic causality scoring  
✓ Result mapping to graph structures  

## 🔗 Usage Example

```python
from scripts.causal_chain_analyzer import CausalChainAnalyzer, CausalConfig

# Create analyzer with configuration
config = CausalConfig(
    graph_data={
        "nodes": {"A": {}, "B": {}, "C": {}, "D": {}},
        "edges": [
            {"source": "A", "target": "B", "type": "causes"},
            {"source": "B", "target": "C", "type": "leads_to"},
            {"source": "C", "target": "D", "type": "results_in"}
        ]
    },
    causal_relation_types=["causes", "leads_to", "results_in"],
    max_depth=10,
    detect_cycles=True
)

analyzer = CausalChainAnalyzer(config)

# Find root causes of event D
root_causes = analyzer.find_root_causes("D")
print(f"Root causes: {root_causes}")

# Trace effects of event A
effects = analyzer.trace_effects("A")
print(f"Downstream effects: {effects}")

# Analyze chain structure
chain_analysis = analyzer.analyze_chain_depth()
print(f"Chain analysis: {chain_analysis}")
```

## 🧠 Causal Chain Concepts

### Root Cause
The initial event or condition that triggers a chain of effects, typically a node with no incoming causal edges.

### Causal Path
A sequence of nodes connected by causal relationships where each node's occurrence leads to the next, forming a directed path.

### Effect Propagation
How the consequences of an event spread through the graph, potentially causing cascading failures or reactions.

### Cycle Detection
Identifying circular dependencies where A→B→...→A, which can indicate feedback loops or data inconsistencies.

### Chain Ranking
Prioritizing causal chains based on strength (proximity, confidence scores, or weighted importance).

## 📖 See Also

- Skill Definition: `SKILL.md`
- Analysis Patterns: `references/causal-chain-patterns.md`
- Examples: `examples/causal-chain-examples.md`
- Implementation: `scripts/causal_chain_analyzer.py`

---

**Production-ready modular structure - complete causal analysis toolkit for knowledge graphs.**


