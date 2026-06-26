# Agent Memory Pro - API Reference

## AgentMemorySystem

Main entry point for the memory system.

### Initialization

```python
from agent_memory import AgentMemorySystem, MemorySystemConfig

config = MemorySystemConfig(
    redis_url="redis://localhost:6379",
    postgres_url="postgresql://user:pass@localhost/db",
    chroma_path="./chroma_db"
)

system = AgentMemorySystem(config)
```

### Attributes

- `context`: ContextMemory - Conversation management
- `tasks`: TaskMemory - Task tracking
- `users`: UserMemory - User profiles
- `knowledge`: KnowledgeMemory - Document retrieval
- `experience`: ExperienceMemory - Pattern learning
- `router`: MemoryRouter - Intelligent retrieval
- `injector`: MemoryInjector - Prompt formatting

## ContextMemory

### Methods

#### add_message
```python
async def add_message(
    user_id: str,
    role: MessageRole,
    content: str,
    metadata: Optional[Dict] = None
) -> ContextMessage
```

#### get_conversation
```python
async def get_conversation(
    user_id: str,
    limit: Optional[int] = None
) -> ConversationWindow
```

#### clear_conversation
```python
async def clear_conversation(user_id: str) -> None
```

## TaskMemory

### Methods

#### create_task
```python
async def create_task(
    user_id: str,
    goal: str,
    task_type: str,
    steps: Optional[List[str]] = None
) -> Task
```

#### start_step
```python
async def start_step(task_id: str, step_index: int) -> None
```

#### complete_step
```python
async def complete_step(
    task_id: str,
    step_index: int,
    result: Any
) -> None
```

#### get_progress
```python
async def get_progress(task_id: str) -> TaskProgress
```

## MemoryRouter

### Methods

#### retrieve
```python
async def retrieve(
    user_id: str,
    query: str,
    context: Optional[Dict] = None
) -> WorkingMemory
```

## ImportanceScorer

### Methods

#### calculate
```python
async def calculate(
    memory: MemoryItem,
    query_context: str
) -> ImportanceScore
```

### Score Components

- `relevance`: float (0-1) - Semantic similarity
- `recency`: float (0-1) - Time-based decay
- `frequency`: float (0-1) - Access count
- `explicit`: float (0-1) - User rating

## Models

### ContextMessage
```python
class ContextMessage(BaseModel):
    id: str
    user_id: str
    role: MessageRole
    content: str
    timestamp: datetime
    token_count: int
```

### Task
```python
class Task(BaseModel):
    id: str
    user_id: str
    goal: str
    type: str
    steps: List[TaskStep]
    current_step: int
    state: TaskState
    created_at: datetime
    updated_at: datetime
```

### UserProfile
```python
class UserProfile(BaseModel):
    user_id: str
    preferences: Dict[str, UserPreference]
    version: int
    created_at: datetime
    updated_at: datetime
```
