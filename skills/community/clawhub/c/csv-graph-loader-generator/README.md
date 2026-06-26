# CSV Graph Loader Generator - Quick Reference

Modular structure for the **csv-graph-loader-generator** skill - converts CSV datasets into graph-ready structures for knowledge graph construction.

## 📁 Structure

```
csv-graph-loader-generator/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── loader-patterns.md           # CSV loader design patterns
│
├── examples/                        # Domain examples
│   └── example-loaders.md           # Business, Scientific, Social examples
│
└── scripts/                         # Utility scripts
    └── csv_loader.py                # CSVGraphLoader implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand CSV graph loading
2. **Learn:** `references/loader-patterns.md` - Design patterns
3. **See:** `examples/example-loaders.md` - Real CSV examples

### For Implementation

1. Use `scripts/csv_loader.py` for creating CSV loaders
2. Supports: Node detection, relationship inference, multiple output formats
3. Generates: Neo4j Cypher, RDF triples, property graphs, JSON graphs

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `loader-patterns.md` | CSV loader patterns & best practices |
| `example-loaders.md` | Business, Scientific, and Social examples |
| `csv_loader.py` | Python CSVGraphLoader class |

## ⚡ Key Features

✓ Automatic entity and relationship detection  
✓ Node type inference from data patterns  
✓ Multi-format output support  
✓ Neo4j Cypher generation  
✓ RDF triple creation  
✓ Property graph conversion  
✓ JSON graph output  
✓ Custom mapping definitions  
✓ Data validation and type inference  
✓ Duplicate entity handling  

## 🔗 Usage Example

```python
from scripts.csv_loader import CSVGraphLoader

# Create loader
loader = CSVGraphLoader(
    name="employees",
    csv_path="data/employees.csv"
)

# Define entity types
loader.define_entity("Person", id_column="person_id")
loader.define_entity("Company", id_column="company_name")

# Define relationships
loader.define_relationship("Person", "WORKS_AT", "Company", 
                          source_col="person_id", 
                          target_col="company_name")

# Generate outputs
cypher = loader.generate_cypher()
triples = loader.generate_triples()
graph_json = loader.to_graph_json()
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Loader Patterns: `references/loader-patterns.md`
- Examples: `examples/example-loaders.md`
- Implementation: `scripts/csv_loader.py`

---

**Lean, focused modular structure - only core functionality for CSV to graph conversion.**


