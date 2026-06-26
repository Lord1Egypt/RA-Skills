---
name: cognimemo-memory
description: Universal AI memory infrastructure that stores, understands, and learns from past interactions. Works across ChatGPT, Claude, Gemini, DeepSeek, and any AI model. Provides cross-app persistent memory via simple API. Use when setting up long-term memory for agents, enabling context persistence across sessions, or when users want their AI to remember preferences, decisions, and history. Triggers on "cognimemo", "persistent memory", "cross-app memory", "ai memory", "remember across sessions".
---

# CogniMemo - Universal AI Memory

CogniMemo provides persistent, intelligent memory for AI applications. Unlike session-based memory that disappears, CogniMemo stores, understands, and learns from interactions over time.

## Why CogniMemo?

- **Cross-app memory** - Same memory across ChatGPT, Claude, Gemini, DeepSeek
- **Model-agnostic** - Works with OpenAI, Anthropic, Gemini, Mistral, Ollama
- **Auto-captured** - Decides what matters, no manual organization
- **Permission-based** - Users control what each app can access
- **Simple API** - REST API, SDKs, LangChain adapters

## How It Works

### 1. Memory Auto-Captured
CogniMemo captures from:
- Chat conversations
- Documents and links
- Tasks, decisions, notes
- User actions

### 2. AI Understands Context
Extracts:
- Entities (people, places, things)
- Relationships
- Patterns and habits
- Temporal context

### 3. Permission-Based Access
- Apps see only approved memory types
- Users can revoke access anytime
- Scoped by permission level

## Quick Start

### Step 1: Get API Key

1. Go to https://cognimemo.com
2. Create account
3. Generate API key from dashboard
4. Add to environment:

```bash
COGNIMEMO_API_KEY=your-api-key-here
```

### Step 2: Install SDK

```bash
# Python
pip install cognimemo

# Node.js
npm install @cognimemo/sdk
```

### Step 3: Initialize Client

```python
from cognimemo import CogniMemo

# Initialize with API key
memory = CogniMemo(api_key="your-api-key")

# Or from environment
memory = CogniMemo()  # Uses COGNIMEMO_API_KEY
```

## Core Operations

### Store Memory

```python
# Store a conversation
memory.store(
    user_id="user-123",
    content="User prefers Portuguese language responses",
    metadata={
        "type": "preference",
        "source": "chat",
        "confidence": 0.9
    }
)

# Store a decision
memory.store(
    user_id="user-123",
    content="Decided to use React for the frontend project",
    metadata={
        "type": "decision",
        "project": "web-app",
        "timestamp": "2026-03-16"
    }
)

# Store a task
memory.store(
    user_id="user-123",
    content="Need to prepare quarterly report by Friday",
    metadata={
        "type": "task",
        "deadline": "2026-03-20",
        "priority": "high"
    }
)
```

### Retrieve Memory

```python
# Semantic search
results = memory.search(
    user_id="user-123",
    query="What are the user's preferences?",
    limit=10
)

# Get specific type
preferences = memory.get_by_type(
    user_id="user-123",
    memory_type="preference"
)

# Get recent
recent = memory.get_recent(
    user_id="user-123",
    hours=24
)
```

### Update Memory

```python
# Update existing memory
memory.update(
    memory_id="mem-456",
    content="User prefers concise Portuguese responses",
    metadata={"confidence": 1.0}
)

# Add context to existing memory
memory.append(
    memory_id="mem-456",
    additional_context="Also prefers bullet points over paragraphs"
)
```

### Delete Memory

```python
# Delete specific memory
memory.delete(memory_id="mem-456")

# Clear all memories for a user
memory.clear(user_id="user-123")

# Clear by type
memory.clear(user_id="user-123", memory_type="task")
```

## Memory Types

| Type | Description | Example |
|------|-------------|---------|
| `preference` | User preferences | "Prefers dark mode" |
| `decision` | Decisions made | "Chose PostgreSQL for database" |
| `task` | Tasks to remember | "Finish report by Friday" |
| `fact` | Factual information | "Works at Acme Corp" |
| `context` | Session context | "Currently working on API integration" |
| `pattern` | Behavioral patterns | "Usually works late on Tuesdays" |

## Permission Scopes

```python
# Request specific permissions
auth_url = memory.get_auth_url(
    scopes=["preferences", "decisions", "tasks"],
    redirect_uri="https://your-app.com/callback"
)

# Check user permissions
permissions = memory.get_permissions(user_id="user-123")
# Returns: {"preferences": True, "decisions": True, "tasks": False}
```

## Integration with AI Models

### OpenAI / ChatGPT

```python
import openai
from cognimemo import CogniMemo

memory = CogniMemo()
user_id = "user-123"

# Get relevant context
context = memory.search(
    user_id=user_id,
    query="User preferences and recent decisions",
    limit=5
)

# Build prompt with memory
messages = [
    {"role": "system", "content": f"Context: {context}"},
    {"role": "user", "content": "Help me with my project"}
]

response = openai.chat.completions.create(
    model="gpt-4",
    messages=messages
)

# Store important info from conversation
memory.store(
    user_id=user_id,
    content="User asked about React component library",
    metadata={"type": "context", "session": "current"}
)
```

### Anthropic / Claude

```python
import anthropic
from cognimemo import CogniMemo

memory = CogniMemo()
user_id = "user-123"

# Get memory context
context = memory.search(
    user_id=user_id,
    query="User preferences",
    limit=10
)

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=f"Remember: {context}",
    messages=[{"role": "user", "content": "What should I work on?"}]
)
```

### LangChain Integration

```python
from langchain.memory import CogniMemoMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# Use CogniMemo as LangChain memory
memory = CogniMemoMemory(
    api_key="your-api-key",
    user_id="user-123"
)

chain = ConversationChain(
    llm=OpenAI(),
    memory=memory
)

# Memory automatically stored and retrieved
response = chain.predict(input="What did we discuss last time?")
```

## OpenClaw Integration

```python
# In OpenClaw skill or agent
from cognimemo import CogniMemo

class CogniMemoTool:
    """Tool for OpenClaw agents to access persistent memory."""
    
    def __init__(self, user_id: str):
        self.memory = CogniMemo()
        self.user_id = user_id
    
    def remember(self, content: str, memory_type: str = "context"):
        """Store something in memory."""
        self.memory.store(
            user_id=self.user_id,
            content=content,
            metadata={"type": memory_type}
        )
        return f"Remembered: {content}"
    
    def recall(self, query: str):
        """Search memory for relevant information."""
        results = self.memory.search(
            user_id=self.user_id,
            query=query,
            limit=10
        )
        return results
    
    def get_preferences(self):
        """Get user preferences."""
        return self.memory.get_by_type(
            user_id=self.user_id,
            memory_type="preference"
        )
```

## Storage Backends

CogniMemo supports multiple storage layers:

| Backend | Best For |
|---------|----------|
| Pinecone | Vector similarity search |
| Weaviate | Hybrid search |
| PostgreSQL | Relational queries |
| Redis | Fast retrieval |

Configure via environment:

```bash
COGNIMEMO_STORAGE=pinecone  # or weaviate, postgres, redis
COGNIMEMO_PINECONE_API_KEY=your-key
COGNIMEMO_PINECONE_ENV=us-west1-gcp
```

## Best Practices

### 1. Store Wisely
```python
# Good: Specific, structured memory
memory.store(
    user_id="user-123",
    content="User prefers dark mode in code editors",
    metadata={"type": "preference", "category": "ui"}
)

# Bad: Vague, unstructured
memory.store(user_id="user-123", content="user likes stuff")
```

### 2. Search Effectively
```python
# Use semantic queries
results = memory.search(
    user_id="user-123",
    query="What editor preferences does the user have?",
    limit=5
)
```

### 3. Respect Privacy
```python
# Check permissions before storing
if memory.has_permission(user_id, "preferences"):
    memory.store(...)
```

## Pricing

- **Free Tier**: 1,000 memories/month
- **Pro**: $29/month for 50,000 memories
- **Enterprise**: Custom pricing for unlimited

## Resources

- **Website**: https://cognimemo.com
- **Documentation**: https://docs.cognimemo.com
- **API Reference**: https://api.cognimemo.com/docs
- **GitHub**: https://github.com/cognimemo/sdk

## Error Handling

```python
from cognimemo import CogniMemo, CogniMemoError

try:
    memory.store(user_id="user-123", content="Important info")
except CogniMemoError as e:
    if e.code == "quota_exceeded":
        print("Free tier limit reached. Upgrade at cognimemo.com/pricing")
    elif e.code == "permission_denied":
        print("User has not granted permission for this memory type")
    else:
        raise
```