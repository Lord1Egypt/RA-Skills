---
name: agent-memory-enterprise
description: Enterprise-grade 5-layer agent memory system with routing, scoring, and multi-backend storage. Use when building production AI agents that need persistent memory with PostgreSQL, Redis, and ChromaDB support.
---

# Agent Memory Pro

Enterprise-grade 5-layer long-term memory system for AI agents with intelligent routing, importance scoring, and multi-backend storage support.

## Overview

This is a production-ready implementation of the 5-layer memory architecture from Wang Fuqiang's article "How to Design an Agent Long-term Memory System".

### 5 Memory Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Context Memory    - Conversation window management         │
│  (seconds-minutes) - Token budget + sliding window          │
├─────────────────────────────────────────────────────────────┤
│  Task Memory       - Multi-step task tracking               │
│  (minutes-hours)   - State machine + checkpoints            │
├─────────────────────────────────────────────────────────────┤
│  User Memory       - Persistent user profiles               │
│  (persistent)      - Version control + preferences          │
├─────────────────────────────────────────────────────────────┤
│  Knowledge Memory  - RAG document retrieval                 │
│  (persistent)      - Vector search + metadata               │
├─────────────────────────────────────────────────────────────┤
│  Experience Memory - Execution pattern learning             │
│  (long-term)       - Success/failure tracking               │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
from agent_memory import AgentMemorySystem, MemorySystemConfig

# Configure system
config = MemorySystemConfig(
    redis_url="redis://localhost:6379",
    postgres_url="postgresql://user:pass@localhost/db",
    chroma_path="./chroma_db"
)

# Initialize
system = AgentMemorySystem(config)

# Record conversation
await system.context.add_message(
    user_id="user_123",
    role="user",
    content="Help me analyze Q4 data"
)

# Create tracked task
task = await system.tasks.create_task(
    user_id="user_123",
    goal="Generate Q4 sales report",
    steps=["Collect data", "Analyze", "Generate report"]
)

# Update progress
await system.tasks.complete_step(task.id, 0, {"data": [...]})

# Intelligent retrieval
working_memory = await system.router.retrieve(
    user_id="user_123",
    query="Continue generating the report",
    context={"current_task": task.id}
)

# Format for LLM
prompt = system.injector.format(working_memory)
```

## Core Features

### 1. Context Memory

Conversation management with token budget control:

```python
from agent_memory.memories import ContextMemory
from agent_memory.models import MessageRole

context = ContextMemory(max_tokens=4000, max_messages=20)

await context.add_message(
    user_id="user_123",
    role=MessageRole.USER,
    content="Hello!"
)

# Get conversation window
window = await context.get_conversation(user_id="user_123")
```

### 2. Task Memory

Multi-step task tracking with state management:

```python
from agent_memory.memories import TaskMemory
from agent_memory.models import TaskState

# Create task
task = await task_memory.create_task(
    user_id="user_123",
    goal="Generate report",
    task_type="report_generation"
)

# Update state
await task_memory.start_step(task.id, step_index=0)
await task_memory.complete_step(task.id, 0, result={"status": "done"})

# Get progress
progress = await task_memory.get_progress(task.id)
```

### 3. User Memory

Persistent user profiles with preference learning:

```python
from agent_memory.memories import UserMemory

# Learn preference
await user_memory.update_preference(
    user_id="user_123",
    key="response_style",
    value="concise",
    confidence=0.9
)

# Get profile
profile = await user_memory.get_profile("user_123")
```

### 4. Knowledge Memory

RAG-based document retrieval:

```python
from agent_memory.memories import KnowledgeMemory

# Index document
await knowledge.index_document(
    doc_id="doc_001",
    content="Document content...",
    metadata={"category": "finance"}
)

# Search
results = await knowledge.search(
    query="Q4 sales",
    top_k=5
)
```

### 5. Experience Memory

Pattern learning from execution history:

```python
from agent_memory.memories import ExperienceMemory
from agent_memory.models import ExperienceOutcome

# Record experience
await experience.record(
    task_type="report_generation",
    outcome=ExperienceOutcome.SUCCESS,
    strategy={"steps": [...]},
    lessons=["Validate data first"]
)

# Find similar successful experiences
patterns = await experience.find_patterns(
    task_type="report_generation",
    min_success_rate=0.8
)
```

## Intelligent Routing

The `MemoryRouter` intelligently selects which memories to load:

```python
from agent_memory.routing import MemoryRouter

router = MemoryRouter(
    context=context,
    tasks=task_memory,
    users=user_memory,
    knowledge=knowledge_memory,
    experience=experience_memory
)

# Automatic feature extraction and routing
working_memory = await router.retrieve(
    user_id="user_123",
    query="Generate Q4 report for East region",
    context={"task_type": "report_generation"}
)
```

### Routing Features

- **Feature Extraction**: Automatically detects task complexity, knowledge needs, history
- **Selective Loading**: Only loads relevant memory types
- **Importance Scoring**: Ranks memories by relevance, recency, frequency
- **Token Budget**: Respects context window limits

## Importance Scoring

```python
from agent_memory.scoring import ImportanceScorer

scorer = ImportanceScorer(
    relevance_weight=0.3,
    recency_weight=0.25,
    frequency_weight=0.2,
    explicit_weight=0.25
)

score = await scorer.calculate(memory_item, query_context)
```

### Score Components

- **Relevance**: Semantic similarity to query
- **Recency**: Time decay function
- **Frequency**: Access count normalization
- **Explicit**: User-rated importance

## Storage Backends

### Redis (Context & Cache)

```python
from agent_memory.storage import RedisClient

redis = RedisClient(url="redis://localhost:6379")
```

### PostgreSQL (Task, User, Experience)

```python
from agent_memory.storage import PostgresClient

postgres = PostgresClient(url="postgresql://...")
```

### ChromaDB (Knowledge)

```python
from agent_memory.storage import ChromaClient

chroma = ChromaClient(path="./chroma_db")
```

## Configuration

```python
from agent_memory.config import MemorySystemConfig

config = MemorySystemConfig(
    # Redis for context & cache
    redis=RedisConfig(url="redis://localhost:6379"),
    
    # PostgreSQL for structured data
    postgres=PostgreSQLConfig(
        url="postgresql://user:pass@localhost/db"
    ),
    
    # Chroma for vector search
    chroma=ChromaConfig(path="./chroma_db"),
    
    # Memory-specific configs
    context=ContextMemoryConfig(max_tokens=4000),
    tasks=TaskMemoryConfig(),
    users=UserMemoryConfig(),
    knowledge=KnowledgeMemoryConfig(),
    experience=ExperienceMemoryConfig(),
    
    # Scoring config
    scoring=ScoringConfig(
        decay_half_life_days=7.0
    )
)
```

## Project Structure

```
agent_memory/
├── __init__.py              # System entry point
├── config.py                # Configuration management
├── exceptions.py            # Custom exceptions
├── core/
│   └── base_memory.py       # Abstract base classes
├── memories/                # 5 memory implementations
│   ├── context_memory.py
│   ├── task_memory.py
│   ├── user_memory.py
│   ├── knowledge_memory.py
│   └── experience_memory.py
├── models/                  # Pydantic data models
│   ├── base.py
│   ├── context.py
│   ├── task.py
│   ├── user.py
│   ├── knowledge.py
│   ├── experience.py
│   └── scoring.py
├── routing/                 # Intelligent routing
│   ├── router.py
│   └── feature_extractor.py
├── injection/               # Memory injection
│   ├── injector.py
│   └── formatters.py
├── scoring/                 # Importance scoring
│   ├── importance_scorer.py
│   └── decay.py
└── storage/                 # Backend clients
    ├── redis_client.py
    ├── postgres_client.py
    ├── postgres_models.py
    └── chroma_client.py

tests/                       # Comprehensive test suite
alembic/                     # Database migrations
pyproject.toml              # Project configuration
```

## Dependencies

- Python 3.10+
- Redis 5.0+
- PostgreSQL 14+
- ChromaDB 0.4+
- SQLAlchemy 2.0+ (async)
- Pydantic 2.0+
- sentence-transformers

## Testing

```bash
pytest tests/ -v --cov=agent_memory
```

## Migration

```bash
alembic upgrade head
```

## Reference

- Original Article: "如何设计一套Agent长期记忆系统" by Wang Fuqiang
- Architecture: 5-layer memory with routing and scoring
- GitHub: laojun509/MemCore
