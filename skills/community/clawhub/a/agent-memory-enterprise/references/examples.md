# Agent Memory Pro - Usage Examples

## Example 1: Basic Conversation Tracking

```python
from agent_memory import AgentMemorySystem

system = AgentMemorySystem()

# Track conversation
await system.context.add_message(
    user_id="user_123",
    role="user",
    content="What's the weather?"
)

await system.context.add_message(
    user_id="user_123",
    role="assistant",
    content="It's sunny today!"
)

# Get context for LLM
window = await system.context.get_conversation("user_123")
messages = window.messages
```

## Example 2: Multi-Step Task

```python
# Create a complex task
task = await system.tasks.create_task(
    user_id="user_123",
    goal="Generate monthly report",
    task_type="report_generation",
    steps=[
        "Fetch data from database",
        "Analyze trends",
        "Create visualizations",
        "Write summary"
    ]
)

# Execute and track
await system.tasks.start_step(task.id, 0)
# ... fetch data ...
await system.tasks.complete_step(task.id, 0, {"records": 1500})

await system.tasks.start_step(task.id, 1)
# ... analyze ...
await system.tasks.complete_step(task.id, 1, {"trend": "upward"})

# Check progress
progress = await system.tasks.get_progress(task.id)
print(f"Progress: {progress.current_step}/{len(progress.steps)}")
```

## Example 3: Learning User Preferences

```python
# Explicit preference
await system.users.update_preference(
    user_id="user_123",
    key="language",
    value="zh-CN",
    confidence=1.0
)

# Implicit preference (learned from behavior)
await system.users.update_preference(
    user_id="user_123",
    key="response_length",
    value="concise",
    confidence=0.7
)

# Use in responses
profile = await system.users.get_profile("user_123")
style = profile.preferences.get("response_length", "moderate")
```

## Example 4: Knowledge Retrieval

```python
# Index documents
await system.knowledge.index_document(
    doc_id="handbook_001",
    content="Company vacation policy...",
    metadata={"category": "hr", "department": "all"}
)

# Search
results = await system.knowledge.search(
    query="vacation policy",
    filters={"category": "hr"},
    top_k=3
)

for result in results:
    print(f"Relevance: {result.score}")
    print(f"Content: {result.chunk.content}")
```

## Example 5: Intelligent Retrieval

```python
# The router automatically selects relevant memories
working_memory = await system.router.retrieve(
    user_id="user_123",
    query="Continue working on the Q4 report",
    context={"current_task": task.id}
)

# Format for LLM prompt
prompt = system.injector.format(working_memory)
```

## Example 6: Experience Learning

```python
from agent_memory.models import ExperienceOutcome

# Record successful execution
await system.experience.record(
    task_type="data_analysis",
    outcome=ExperienceOutcome.SUCCESS,
    strategy={
        "steps": ["validate", "clean", "analyze"],
        "tools": ["pandas", "matplotlib"]
    },
    lessons=[
        "Always validate data quality first",
        "Use line charts for time series"
    ]
)

# Find best practices for similar tasks
patterns = await system.experience.find_patterns(
    task_type="data_analysis",
    min_success_rate=0.8
)

if patterns:
    best = patterns[0]
    print(f"Best strategy: {best.strategy}")
```

## Example 7: Complete Integration

```python
class AIAgent:
    def __init__(self):
        self.memory = AgentMemorySystem()
    
    async def handle_request(self, user_id: str, query: str):
        # Load relevant memories
        working = await self.memory.router.retrieve(
            user_id=user_id,
            query=query
        )
        
        # Build prompt with context
        prompt = self.memory.injector.format(working)
        
        # Call LLM
        response = await llm.generate(prompt + "\n\n" + query)
        
        # Update memories
        await self.memory.context.add_message(
            user_id=user_id,
            role="user",
            content=query
        )
        await self.memory.context.add_message(
            user_id=user_id,
            role="assistant",
            content=response
        )
        
        return response
```
