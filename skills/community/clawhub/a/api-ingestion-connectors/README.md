# API Ingestion Connectors - Quick Reference

Modular structure for the **api-ingestion-connectors** skill - connects external APIs and ingests data into graph-ready structures.

## 📁 Structure

```
api-ingestion-connectors/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── connector-patterns.md        # API connector design patterns
│
├── examples/                        # Domain examples
│   └── example-connectors.md        # REST, GraphQL, OAuth, Pagination examples
│
└── scripts/                         # Utility scripts
    └── api_connector.py             # APIConnector implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand API ingestion
2. **Learn:** `references/connector-patterns.md` - Design patterns
3. **See:** `examples/example-connectors.md` - Real connector examples

### For Implementation

1. Use `scripts/api_connector.py` for creating API connectors
2. Supports: REST, GraphQL, authentication, pagination, transformation
3. Generates: Connector configs, ETL pipeline integration, graph-ready output

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `connector-patterns.md` | API connector patterns & best practices |
| `example-connectors.md` | REST, GraphQL, and OAuth connector examples |
| `api_connector.py` | Python APIConnector class |

## ⚡ Key Features

✓ REST API connector support  
✓ GraphQL API connector support  
✓ Multiple authentication methods (API keys, OAuth, Bearer tokens)  
✓ Automatic pagination handling  
✓ Request/response validation  
✓ Data transformation to graph-ready formats  
✓ Error handling and retry logic  
✓ Rate limiting support  

## 🔗 Usage Example

```python
from scripts.api_connector import APIConnector

# Create REST connector
rest_connector = APIConnector(
    name="github_users",
    api_type="rest",
    endpoint="https://api.github.com/users",
    method="GET"
)

# Add authentication
rest_connector.set_auth("bearer", token="your_token")

# Add pagination
rest_connector.set_pagination(
    type="page",
    param="page",
    page_size=30
)

# Execute and transform
response = rest_connector.fetch()
graph_data = rest_connector.transform_to_graph(response)
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Connector Patterns: `references/connector-patterns.md`
- Examples: `examples/example-connectors.md`
- Implementation: `scripts/api_connector.py`

---

**Lean, focused modular structure - only core functionality for API ingestion and graph transformation.**


