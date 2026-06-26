# Memory System Documentation

## Overview

The Memory System provides a three-layer architecture for persistent cross-session memory, designed with privacy-first principles and local-only storage.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Memory System                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Episodic       │  │   Semantic      │  │    User         │ │
│  │  Memory         │  │   Memory        │  │    Model        │ │
│  │                 │  │                 │  │                 │ │
│  │ • Interactions  │  │ • Facts         │  │ • Profile       │ │
│  │ • Context       │  │ • Concepts      │  │ • Preferences   │ │
│  │ • Outcomes      │  │ • Relations     │  │ • History       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Storage Layer                             ││
│  │  • Local SQLite Database                                     ││
│  │  • JSON Configuration Files                                  ││
│  │  • No Cloud/External Storage                                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Episodic Memory

Stores interaction history with context and outcomes.

### Data Structure

```python
class Episode:
    id: str
    timestamp: datetime
    user_input: str
    context: dict
    actions: list
    outcome: str
    feedback: Optional[str]
    importance: float  # 0.0 - 1.0
```

### Key Operations

| Operation | Description |
|-----------|-------------|
| `add_episode()` | Store a new interaction episode |
| `get_recent()` | Retrieve recent N episodes |
| `search()` | Search episodes by query |
| `cleanup()` | Remove old/low-importance episodes |

### Configuration

```yaml
episodic:
  max_episodes: 10000
  retention_days: 90
  importance_threshold: 0.3
  cleanup_interval: "weekly"
```

---

## Layer 2: Semantic Memory

Stores extracted facts, concepts, and relationships.

### Data Structure

```python
class Knowledge:
    id: str
    type: str  # "fact" | "concept" | "relation"
    content: str
    source_episode: str
    confidence: float
    last_accessed: datetime
    access_count: int
```

### Key Operations

| Operation | Description |
|-----------|-------------|
| `add_fact()` | Store a new fact |
| `get_concepts()` | Retrieve related concepts |
| `find_relations()` | Find connections between concepts |
| `validate()` | Verify fact accuracy |

### Fact Extraction

Facts are extracted from successful interactions using:

1. **Pattern Recognition**: Identify recurring information
2. **Confidence Scoring**: Rate reliability (0.0 - 1.0)
3. **Deduplication**: Avoid storing duplicate facts
4. **User Confirmation**: High-stakes facts require confirmation

---

## Layer 3: User Model

Stores user preferences, profile, and interaction history.

### Data Structure

```python
class UserModel:
    user_id: str
    profile: dict  # name, role, timezone, etc.
    preferences: dict  # output_format, detail_level, etc.
    interaction_stats: dict
    created_at: datetime
    updated_at: datetime
```

### Preference Categories

| Category | Examples |
|----------|----------|
| **Output Style** | format, detail_level, language |
| **Workflow** | preferred_tools, shortcuts |
| **Communication** | tone, response_length |
| **Scheduling** | timezone, working_hours |

### Preference Learning

Preferences are learned through:

1. **Explicit Setting**: User directly sets preference
2. **Behavior Analysis**: Detect patterns in user choices
3. **Feedback Integration**: User corrections update preferences

---

## Storage Implementation

### Local SQLite Database

```sql
-- Episodes table
CREATE TABLE episodes (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    user_input TEXT,
    context TEXT,
    actions TEXT,
    outcome TEXT,
    importance REAL
);

-- Knowledge table
CREATE TABLE knowledge (
    id TEXT PRIMARY KEY,
    type TEXT,
    content TEXT,
    confidence REAL,
    last_accessed TEXT
);

-- User model table
CREATE TABLE user_models (
    user_id TEXT PRIMARY KEY,
    profile TEXT,
    preferences TEXT,
    updated_at TEXT
);
```

### File Structure

```
memory/
├── episodes.db      # SQLite database
├── user_config.json # User preferences
└── cache/           # Temporary cache
```

---

## Privacy & Security

### Core Principles

1. **Local-Only Storage**: No cloud or external storage
2. **User Consent**: All operations require user awareness
3. **Data Minimization**: Only store necessary information
4. **Easy Deletion**: Users can clear memory anytime

### Data Access Control

```python
class MemoryManager:
    def get_memory(self, user_id, memory_type):
        """All memory access is logged and auditable."""
        self._log_access(user_id, memory_type, "read")
        return self._secure_read(user_id, memory_type)
    
    def clear_memory(self, user_id, memory_type=None):
        """Users can clear their own memory."""
        if memory_type:
            self._clear_type(user_id, memory_type)
        else:
            self._clear_all(user_id)
        self._log_access(user_id, memory_type, "clear")
```

---

## Usage Examples

### Store an Episode

```python
from scripts.memory_manager import MemoryManager

memory = MemoryManager()

# Store interaction
episode_id = memory.add_episode(
    user_input="分析这份报告",
    context={"file": "report.pdf", "pages": 50},
    actions=["load", "extract", "summarize"],
    outcome="成功生成摘要"
)
```

### Retrieve Context

```python
# Get relevant context for current task
context = memory.get_context(
    user_id="default",
    query="分析报告",
    max_tokens=2000
)

# context contains:
# - Recent relevant episodes
# - Related facts
# - User preferences
```

### Manage Preferences

```python
# Set preference
memory.set_preference(
    user_id="default",
    category="output",
    key="format",
    value="markdown"
)

# Get preference
format_pref = memory.get_preference(
    user_id="default",
    category="output",
    key="format"
)
```

---

## Performance Optimization

### Caching Strategy

- **Hot Cache**: Frequently accessed items in memory
- **Warm Cache**: Recent items on disk
- **Cold Storage**: Old items compressed

### Cleanup Policies

1. **Time-based**: Remove items older than retention period
2. **Importance-based**: Remove low-importance items first
3. **Size-based**: Cleanup when exceeding size limit

### Monitoring

```python
# Get memory stats
stats = memory.get_stats()

print(f"Episodes: {stats['episodes_count']}")
print(f"Storage size: {stats['storage_size_mb']} MB")
print(f"Average retrieval time: {stats['avg_retrieval_ms']} ms")
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow retrieval | Too many episodes | Run cleanup |
| Missing data | Database corruption | Restore from backup |
| High memory usage | Large cache | Reduce cache size |

### Recovery

```python
# Backup memory
memory.backup("memory_backup.json")

# Restore memory
memory.restore("memory_backup.json")

# Clear all (user request)
memory.clear_all(user_id="default")
```

---

## Best Practices

1. **Regular Cleanup**: Run cleanup weekly
2. **Monitor Size**: Keep storage under limit
3. **Backup Important Data**: Before major operations
4. **User Awareness**: Inform users about memory usage
5. **Privacy First**: Never store sensitive data without consent
