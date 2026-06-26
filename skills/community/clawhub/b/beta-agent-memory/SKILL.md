---
name: beta-agent-memory
description: Long-term memory systems for AI agents. Implements vector memory, entity tracking, conversation summarization, and persistent context across sessions.
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: [python3]
    always: false
---

# Agent Memory System

Give your AI agent persistent, long-term memory across conversations and sessions.

## Memory Types Implemented

### Episodic Memory
Stores episodes/events from conversations:
- Key facts extracted per conversation
- Decisions made and context
- User preferences and patterns
- "Remembering" past interactions

### Semantic Memory
Structured knowledge storage:
- Entity definitions and relationships
- Facts about the world
- Domain knowledge base
- Learned procedures

### Procedural Memory
Agent's own capabilities:
- Known skills and tools
- How to use different APIs
- Response patterns that worked

## Architecture

```
User Input
    ↓
Short-term (current session context)
    ↓
Memory Retrieval → Top-k relevant memories (vector search)
    ↓
Context Injection → Combined prompt
    ↓
LLM Response
    ↓
Memory Storage → Extract new facts, update entities
```

## Features

- **Vector-based storage** (ChromaDB or Pinecone)
- **Entity extraction** (spaCy NER)
- **Conversation summarization** (every N turns)
- **Relevance scoring** for retrieval
- **Forgetting/summarization** of old memories

## Use Cases

- Personal AI assistant that remembers you
- Customer support agent with context
- Research agent with persistent knowledge
- Trading agent with market memory
- Personal CRM (remembering people and their context)

## Technical Stack

- ChromaDB / Pinecone (vector store)
- spaCy (entity extraction)
- LangChain (memory abstractions)
- PostgreSQL (structured memory)

## Pricing

| Type | Context Window | Price |
|------|-----------------|-------|
| Basic | 100K tokens | $100 |
| Pro | 1M tokens | $300 |
| Enterprise | Unlimited | $800 |

---

*Built by Beta*
