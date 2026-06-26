# Persistence Layer

## Rationale

Production agents are long-running. They must survive process restarts, support resumption after interrupts, and maintain consistency across turns that may span hours or days. Ephemeral in-memory state is a development convenience, not a production architecture.

## Checkpoint Backends by Environment

```bash
# Install the appropriate package for your environment:
pip install langgraph                        # includes InMemorySaver
pip install langgraph-checkpoint-sqlite      # SQLite (lightweight, single-server)
pip install langgraph-checkpoint-redis       # Redis (staging)
pip install langgraph-checkpoint-postgres    # Postgres (production)
```

```python
import os
import sqlite3

# Development — in-process, no external dependency
from langgraph.checkpoint.memory import InMemorySaver

# Lightweight staging / single-server — SQLite file on disk
from langgraph.checkpoint.sqlite import SqliteSaver

# Staging — Redis
from langgraph.checkpoint.redis import RedisSaver

# Production — Postgres
from langgraph.checkpoint.postgres import PostgresSaver


def get_checkpointer(env: str):
    if env == "development":
        return InMemorySaver()
    elif env == "sqlite":
        conn = sqlite3.connect("agent_sessions.db", check_same_thread=False)
        return SqliteSaver(conn)
    elif env == "staging":
        import redis
        r = redis.Redis.from_url("redis://redis:6379")
        return RedisSaver(r)
    else:  # production
        import psycopg
        conn = psycopg.connect("postgresql://user:pass@db:5432/agents")
        return PostgresSaver(conn)


checkpointer = get_checkpointer(os.getenv("ENV", "development"))
app = graph.compile(checkpointer=checkpointer)
```

## Session ID Pattern

```python
import uuid
from datetime import datetime
from langchain_core.messages import HumanMessage

def create_session(user_id: str, task_description: str) -> dict:
    """Create a new agent session with stable ID."""
    return {
        "session_id": str(uuid.uuid4()),
        "user_id": user_id,
        "task": task_description,
        "created_at": datetime.utcnow().isoformat(),
        "thread_id": str(uuid.uuid4()),   # LangGraph checkpoint key
    }

def resume_session(app, session_id: str, new_message: str) -> dict:
    """Resume an existing session — LangGraph loads checkpoint automatically."""
    config = {"configurable": {"thread_id": session_id}}
    return app.invoke(
        {"messages": [HumanMessage(new_message)]},
        config=config
    )

# Start a session
session = create_session("user-123", "refactor the auth module")
result = app.invoke(
    {"messages": [HumanMessage(session["task"])]},
    config={"configurable": {"thread_id": session["session_id"]}}
)

# Resume later — picks up exactly where it left off
result = resume_session(app, session["session_id"], "also add rate limiting")
```

## Session Branching (Fork)

Experiment with a different approach from a known-good checkpoint without losing the original.

```python
def fork_session(app, parent_session_id: str) -> str:
    """Fork a session from its current state into a new independent session."""
    parent_state = app.get_state(
        config={"configurable": {"thread_id": parent_session_id}}
    )
    fork_id = str(uuid.uuid4())
    app.update_state(
        config={"configurable": {"thread_id": fork_id}},
        values=parent_state.values
    )
    return fork_id
```

## Async Background Agent + Polling

```python
import asyncio
from fastapi import FastAPI

api = FastAPI()

@api.post("/agent/run")
async def start_agent(request: dict):
    session_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}
    asyncio.create_task(
        app.ainvoke(
            {"messages": [HumanMessage(request["task"])]},
            config=config
        )
    )
    return {"status": "accepted", "session_id": session_id}

async def poll_for_result(app, session_id: str, timeout: float = 300.0) -> dict:
    import asyncio
    start = asyncio.get_event_loop().time()
    while asyncio.get_event_loop().time() - start < timeout:
        state = app.get_state({"configurable": {"thread_id": session_id}})
        if state.next == ():    # no next nodes = finished
            return state.values
        await asyncio.sleep(5.0)
    raise TimeoutError(f"Session {session_id} did not complete within {timeout}s")
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `InMemorySaver` in production | State is lost on restart; use Redis or Postgres |
| Session ID not indexed | Store session ID → user ID mapping in a DB for lookup |
| No TTL on old sessions | Define cleanup policy; stale checkpoints grow storage unboundedly |
| Resume without validation | Verify session belongs to the requesting user before loading |
| `thread_id` reuse across users | Always generate a fresh UUID per session; never share thread IDs |
