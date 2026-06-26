# ETL Pipeline Generator - Quick Reference

Modular structure for the **etl-pipeline-generator** skill - designs automated ETL pipelines for transforming and loading data into graph databases.

## 📁 Structure

```
etl-pipeline-generator/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── pipeline-patterns.md         # ETL pipeline design patterns
│
├── examples/                        # Domain examples
│   └── example-pipelines.md         # Real ETL pipeline examples
│
└── scripts/                         # Utility scripts
    └── etl_generator.py             # ETLPipelineGenerator implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand ETL pipeline generation
2. **Learn:** `references/pipeline-patterns.md` - Design patterns
3. **See:** `examples/example-pipelines.md` - Real pipeline examples

### For Implementation

1. Use `scripts/etl_generator.py` for creating ETL pipelines
2. Supports: Extract, Transform, Load orchestration
3. Generates: YAML pipelines, DAG definitions, Python scripts

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `pipeline-patterns.md` | ETL pipeline patterns & best practices |
| `example-pipelines.md` | Real-world ETL pipeline examples |
| `etl_generator.py` | Python ETLPipelineGenerator class |

## ⚡ Key Features

✓ Multi-stage pipeline orchestration  
✓ Extract from diverse sources (CSV, JSON, API, Database)  
✓ Multiple transformation strategies  
✓ Load to graph databases (Neo4j, RDF, Property Graph)  
✓ Data validation and quality checks  
✓ Pipeline scheduling and monitoring  
✓ Idempotent operations  
✓ Error handling and recovery  
✓ Multiple output formats (YAML, DAG, Python)  
✓ Integration with existing skills  

## 🔗 Usage Example

```python
from scripts.etl_generator import ETLPipelineGenerator

# Create pipeline
pipeline = ETLPipelineGenerator(
    name="customer_ingestion",
    description="Load customer data into knowledge graph"
)

# Define extract stage
pipeline.add_extract(
    source_type="csv",
    source_path="data/customers.csv"
)

# Define transform stage
pipeline.add_transform(
    operations=[
        "normalize_entities",
        "detect_relationships",
        "validate_schema"
    ]
)

# Define load stage
pipeline.add_load(
    target="neo4j",
    database="kg_prod"
)

# Generate pipeline
yaml_config = pipeline.to_yaml()
python_script = pipeline.to_python_script()
dag = pipeline.to_dag()
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Pipeline Patterns: `references/pipeline-patterns.md`
- Examples: `examples/example-pipelines.md`
- Implementation: `scripts/etl_generator.py`

---

**Lean, focused modular structure - only core functionality for ETL pipeline generation.**


