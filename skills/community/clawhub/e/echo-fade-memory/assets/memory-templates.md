# Memory Templates

These payload templates turn the reference skills' common workflows into `echo-fade-memory` requests.

## Preference Template

```json
{
  "content": "User prefers dark mode and concise answers.",
  "summary": "preference: dark mode and concise answers",
  "memory_type": "preference",
  "importance": 0.95,
  "source_refs": [
    {
      "kind": "chat",
      "ref": "session:2026-03-18"
    }
  ]
}
```

## Decision Template

```json
{
  "content": "Project decision: use chromem-go as the embedded vector store to keep setup lightweight and dependency-free.",
  "summary": "decision: use chromem-go for embedded vectors",
  "memory_type": "project",
  "importance": 0.9,
  "conflict_group": "project:vector-backend",
  "source_refs": [
    {
      "kind": "chat",
      "ref": "session:architecture"
    }
  ]
}
```

## Error / Learning Template

```json
{
  "content": "Learning: use /usr/bin/git instead of legacy /usr/local/bin/git when commit tooling requires --trailer support.",
  "summary": "error: use system git for trailer support",
  "memory_type": "project",
  "importance": 0.88,
  "source_refs": [
    {
      "kind": "chat",
      "ref": "session:git-workaround"
    }
  ]
}
```

## Feature Request Template

```json
{
  "content": "Feature request: expose emotional_weight in POST /v1/memories for emotionally salient facts.",
  "summary": "feature-request: emotional weight api",
  "memory_type": "goal",
  "importance": 0.7,
  "source_refs": [
    {
      "kind": "chat",
      "ref": "session:feature-request"
    }
  ]
}
```

## Session Handoff Template

```json
{
  "content": "Current state: Docker compose now uses chromem by default and restart policy unless-stopped. Next step is validating live recall workflows.",
  "summary": "session handoff: docker + chromem status",
  "memory_type": "working",
  "importance": 0.75,
  "source_refs": [
    {
      "kind": "chat",
      "ref": "session:handoff"
    }
  ]
}
```

## Prompt Pattern

When converting a reference-skill style learning into memory:

1. Put the full lesson in `content`
2. Make `summary` short and searchable
3. Use `importance` instead of `emotional_weight` for now
4. Always include `source_refs`
5. Use `conflict_group` when the fact may evolve over time
