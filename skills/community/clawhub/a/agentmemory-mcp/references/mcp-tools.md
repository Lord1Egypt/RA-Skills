# agentmemory MCP Tools Reference

Complete list of 43 MCP tools available via `agentmemory` MCP server.

## Core Memory Operations

### memory_recall
Retrieve semantically relevant memories.
```
memory_recall(query: string, limit?: number, threshold?: number)
```

### memory_save
Store new memories with optional metadata.
```
memory_save(content: string, type?: "observation" | "decision" | "fact" | "preference", tags?: string[])
```

### memory_smart_search
Hybrid BM25 + vector search.
```
memory_smart_search(query: string, limit?: number)
```

### memory_forget
Delete memories by ID or pattern.
```
memory_forget(pattern?: string, id?: string)
```

### memory_update
Update existing memory content or metadata.
```
memory_update(id: string, content?: string, tags?: string[])
```

---

## Navigation & Exploration

### memory_timeline
View memories chronologically.
```
memory_timeline(start?: date, end?: date, limit?: number)
```

### memory_tree
Hierarchical view of knowledge graph.
```
memory_tree(root?: string, depth?: number)
```

### memory_trace
View provenance/derivation chain of a memory.
```
memory_trace(id: string)
```

### memory_stats
Memory usage statistics.
```
memory_stats()
```

---

## Agent Integration

### memory_profile
Detailed agent memory profile.
```
memory_profile(agent_id?: string)
```

### memory_snapshot
Export all memories as JSON.
```
memory_snapshot(format?: "json" | "markdown")
```

### memory_import
Bulk import memories.
```
memory_import(memory: Memory[], strategy?: "merge" | "replace")
```

### memory_compact
Compress and consolidate memories.
```
memory_compact(threshold?: number)
```

---

## Knowledge Graph

### memory_relate
Create relationships between memories.
```
memory_relate(from_id: string, to_id: string, relationship?: string)
```

### memory_graph_query
Query knowledge graph.
```
memory_graph_query(query: string, depth?: number)
```

### memory_entities
List all entities in knowledge graph.
```
memory_entities(type?: string)
```

### memory_paths
Find paths between two memories.
```
memory_paths(from_id: string, to_id: string)
```

---

## Context & Sessions

### memory_context
Get context for current session.
```
memory_context(include_recent?: number)
```

### memory_inject
Inject memories into current context.
```
memory_inject(limit?: number, match?: string)
```

### memory_session
Session-specific memory operations.
```
memory_session(op: "save" | "load" | "clear", data?: any)
```

---

## Configuration

### memory_config
View/update agentmemory configuration.
```
memory_config(op: "get" | "set", key?: string, value?: any)
```

### memory_channels
List available memory channels.
```
memory_channels()
```

---

## Advanced

### memory_analyze
Analyze memory patterns.
```
memory_analyze(analysis_type?: "coverage" | "gaps" | "redundancy")
```

### memory_consolidate
Consolidate fragmented memories.
```
memory_consolidate(strategy?: "simple" | "semantic")
```

### memory_evict
Evict low-value memories.
```
memory_evict(threshold?: number, dry_run?: boolean)
```

---

## Usage in OpenClaw

### Before starting a task
```
Agent can call: memory_recall("project architecture decisions")
→ Returns relevant past decisions, avoiding re-explaining
```

### After completing a task
```
Agent can call: memory_save("Deployed backend to production via railway", 
  type="decision", tags=["deployment", "backend"])
→ Stores experience for future reference
```

### Check task deduplication
```
Agent can call: memory_smart_search("deploy backend production")
→ If match found, agent can reuse previous workflow
```