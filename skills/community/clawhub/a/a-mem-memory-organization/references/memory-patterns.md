# Memory Patterns

## Good Note Construction

Good notes are:

- atomic,
- specific,
- retrievable,
- linkable,
- easy to update conservatively.

Example:

```json
{
  "content": "The user prefers concise technical explanations and dislikes repetitive UI wording.",
  "context": "Communication preference for future coding and product responses.",
  "keywords": ["concise explanations", "technical writing", "UI wording"],
  "tags": ["preference", "communication", "ui-ux"],
  "category": "Preference"
}
```

Bad version:

```json
{
  "content": "The user said some things about style and also memory and maybe UI preferences.",
  "context": "General",
  "keywords": [],
  "tags": []
}
```

## Tag Heuristics

Use `keywords` for precise terms and entities.

Use `tags` for broader retrieval classes such as:

- `preference`
- `project-context`
- `decision`
- `bug`
- `research`
- `workflow`
- `architecture`
- `tooling`
- `ui-ux`
- `evaluation`

Do not create too many synonymous tags. Prefer a stable small vocabulary.

## Category Heuristics

Useful default categories:

- `Preference`
- `Project`
- `Decision`
- `Fact`
- `Workflow`
- `Bug`
- `Research`

## Linking Rules

Add links when:

- two notes refer to the same entity or subsystem,
- one note is a consequence of another,
- one note refines or supersedes another,
- one note is repeatedly retrieved alongside another.

Do not add links only because embeddings are vaguely similar.

## Conservative Evolution

Prefer these strategies in order:

1. Add a new note.
2. Link it to relevant prior notes.
3. Update tags/context on an older note only if confidence is high.
4. Mark older notes as superseded instead of overwriting the original claim.

This reduces semantic drift and memory pollution.

## Minimal Agent Integration

For an agent loop, integrate memory in four places:

1. Before response generation: retrieve relevant notes.
2. After response/tool completion: extract durable observations.
3. Before persistence: enrich note fields and search for neighbors.
4. Periodically: run conservative evolution over high-confidence clusters.

## Minimal File-Based Storage

If no DB exists yet, store notes in:

- `memory/notes.json`

Suggested layout:

```json
{
  "notes": [
    {
      "id": "note-001",
      "content": "Project uses FastAPI for the backend.",
      "context": "Repository architecture decision.",
      "keywords": ["FastAPI", "backend", "architecture"],
      "tags": ["project-context", "architecture", "backend"],
      "category": "Project",
      "timestamp": "202603161100",
      "links": []
    }
  ]
}
```
