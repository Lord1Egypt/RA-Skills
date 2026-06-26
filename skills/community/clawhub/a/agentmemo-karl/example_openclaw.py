"""Example: Using agentMemo v3.0.0 with OpenClaw agents."""
from client import AgentMemoClient

vault = AgentMemoClient("http://localhost:8790")

# Store memories with tags
vault.store("User prefers dark mode and compact layouts", namespace="preferences",
            importance=0.9, tags=["ui", "user-pref"])
vault.store("Meeting with design team scheduled for Friday 2pm", namespace="calendar",
            importance=0.7, ttl_seconds=86400*7, tags=["meeting", "design"])
vault.store("Bug fix: pagination offset was off by one in /api/users", namespace="engineering",
            importance=0.6, metadata={"pr": "#142", "repo": "main-app"}, tags=["bugfix", "api"])

# Semantic search across all namespaces
results = vault.search("UI preferences", limit=5, mode="semantic")
for r in results["results"]:
    tags = ", ".join(r.get("tags", []))
    print(f"[{r['score']:.3f}] ({r['namespace']}) {r['text']} [{tags}]")

# Keyword search
results = vault.search("pagination bug", mode="keyword", limit=5)
print(f"\nKeyword results: {len(results['results'])}")

# Hybrid search (semantic + keyword fusion)
results = vault.search("dark mode preferences", mode="hybrid", limit=5)
print(f"Hybrid results: {len(results['results'])}")

# Budget-constrained search (fit in 500 tokens)
results = vault.search("recent bugs", budget_tokens=500, namespace="engineering")
print(f"\nUsed {results['total_tokens']}/{results['budget_tokens']} tokens")

# Update a memory (creates version history)
mem = vault.search("dark mode", limit=1)["results"][0]
vault.update(mem["id"], text="User prefers dark mode, compact layouts, and large fonts",
             tags=["ui", "user-pref", "accessibility"])

# View version history
versions = vault.versions(mem["id"])
print(f"\nVersion history: {len(versions)} versions")

# Batch operations
result = vault.batch(
    create=[
        {"text": "Agent A completed task X", "namespace": "logs", "tags": ["agent-a"]},
        {"text": "Agent B started task Y", "namespace": "logs", "tags": ["agent-b"]},
    ],
    search=[
        {"q": "task completion", "namespace": "logs", "mode": "semantic"},
    ],
)
print(f"\nBatch: created {len(result['created'])}, searched {len(result['searches'])}")

# Publish events
vault.publish_event("task.completed", {"task": "deploy-v2", "status": "success"}, namespace="engineering")

# Health & metrics
health = vault.health()
print(f"\nHealth: {health['status']} (v{health['version']})")

metrics = vault.metrics()
print(f"Cache: {metrics['embedding_cache_hits']} hits, {metrics['embedding_cache_misses']} misses")
print(f"HNSW: {metrics['hnsw_index_size']} vectors")

# Export/Import
export = vault.export_memories(namespace="preferences")
print(f"\nExported {export['exported']} memories from preferences")

# Stats
stats = vault.stats()
print(f"\n{stats['total_memories']} memories, {stats['total_events']} events, {stats['storage_size_human']}")
