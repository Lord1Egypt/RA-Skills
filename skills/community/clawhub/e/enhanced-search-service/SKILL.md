# Enhanced Search Service

## Description

Provides enhanced memory search by combining co-occurrence graph analysis and semantic vector similarity. This plugin sits between memory storage and query interfaces, offering improved relevance ranking through contextual relationships and semantic understanding.

## Core Capabilities

- **Unified Search**: Combines co-occurrence graph expansion with semantic vector similarity
- **Relevance Ranking**: Multi-factor scoring (text match, co-occurrence strength, semantic similarity)
- **Context Awareness**: Leverages memory relationships to surface relevant but non-obvious connections
- **Plugin Architecture**: Independent service that can be upgraded/replaced without affecting other components

## Dependencies

- **Co-occurrence Engine** (`co-occurrence-engine`): Provides relationship graph for contextual expansion
- **Semantic Vector Store** (`semantic-vector-store`): Provides semantic similarity scoring
- **Memory Integration** (`memory-integration`): Optional, for direct memory access if needed

## Usage

### As a Plugin User

```python
from enhanced_search_adapter import EnhancedSearchAdapter

adapter = EnhancedSearchAdapter()
results = adapter.enhance_search("query about memory sync", max_results=10)
```

### As a System Integrator

The plugin provides an adapter that implements the standard memory adapter interface with additional enhancement methods.

## Skill Files

```
enhanced-search-service/
├── SKILL.md (this file)
├── scripts/
│   └── enhanced_search_service.py  # Core service implementation
├── integration/
│   └── adapter/
│       └── enhanced_search_adapter.py  # Adapter for star architecture
└── references/
    ├── api.md           # API documentation
    └── architecture.md  # Design and integration notes
```

## Configuration

Default configuration (can be overridden via adapter initialization):

```yaml
search:
  co_occurrence_weight: 0.3
  semantic_weight: 0.5
  text_match_weight: 0.2
  max_expansion: 5
  min_relevance_threshold: 0.1
```

## Integration with Star Architecture

This plugin connects to the Memory Sync Enhanced (MSE) hub through its adapter. It consumes data from:
- Co-occurrence engine (for relationship data)
- Semantic vector store (for similarity data)

It produces enhanced search results for:
- Memory Integration system
- Direct user queries
- Other plugins needing sophisticated search

## Health Checks

The adapter provides health monitoring for:
- Dependency availability (co-occurrence engine, semantic vector store)
- Search performance metrics
- Result quality indicators

## Version History

- **v0.1.0** (initial): Basic enhancement combining co-occurrence scores with semantic similarity
- **v0.2.0** (planned): Advanced fusion algorithms and caching
- **v0.3.0** (planned): Learning-based weighting adaptation

## Development Notes

This is a Phase 3 split from the original memory-integration plugin. The goal is to create a single-function plugin focused solely on search enhancement, following the star architecture principle of separation of concerns.