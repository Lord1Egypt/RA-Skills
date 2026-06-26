# Ontology Skill

## Core Concept

A typed vocabulary + constraint system for representing knowledge as a verifiable graph.

## When to Use

- "Remember that..." → Create/update entity
- "What do I know about X?" → Query graph
- "Link X to Y" → Create relation
- "Show all tasks for project Z" → Graph traversal

## Storage

`memory/ontology/graph.jsonl` - append-only JSONL format

## Core Types

- **Person**: name (required), email?, phone?, notes?
- **Project**: name (required), status?, goals[], description?
- **Task**: title (required), status (required), due?, priority?, assignee?

## Relations

| Relation | From | To |
|----------|------|-----|
| has_owner | Project, Task | Person |
| assigned_to | Task | Person |
| belongs_to | Task | Project |
| blocks | Task | Task (acyclic) |

## CLI Commands

```bash
python3 scripts/ontology.py create --type Person --props '{"name":"Alice"}'
python3 scripts/ontology.py list --type Person
python3 scripts/ontology.py query --type Task --where '{"status":"open"}'
python3 scripts/ontology.py get --id p_001
python3 scripts/ontology.py relate --from proj_001 --rel has_owner --to p_001
```

## Validation

- Required properties must exist
- Enum values from predefined sets
- No circular dependencies for acyclic relations