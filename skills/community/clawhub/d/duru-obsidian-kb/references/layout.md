# Layout Reference

## Canonical Phase 1 structure

```text
<kb-root>/
  raw/
    articles/
    papers/
    repos/
    files/
  assets/
  wiki/
    concepts/
    sources/
    indexes/
    _meta/
  outputs/
  logs/
  manifest.json
  config.json
```

## File contracts

### manifest.json

Store a JSON object with this shape:

```json
{
  "version": 1,
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "entries": []
}
```

Each entry should resemble:

```json
{
  "id": "uuid-or-timestamp",
  "slug": "short-stable-slug",
  "title": "Human title",
  "source": "url-or-local-path",
  "source_type": "article|paper|repo|file",
  "raw_path": "raw/articles/example.md",
  "ingested_at": "ISO-8601",
  "tags": [],
  "status": "raw|stub|indexed|reviewed",
  "notes": "optional"
}
```

### config.json

Keep configuration minimal in Phase 1.
Example:

```json
{
  "name": "demo-kb",
  "default_output_format": "md",
  "obsidian_compatible": true
}
```

### wiki/sources/*.md

Generate one page per manifest entry.
Include frontmatter plus:

- title
- source link/path
- source type
- ingestion time
- tags
- status
- raw file link
- notes about extraction coverage

### wiki/indexes/*.md

Maintain these indexes:

- `sources.md` — master list of all sources
- `tags.md` — grouped by tag
- `concepts.md` — concept pages generated from tags
- `timeline.md` — grouped by ingestion date
- `topic-map.md` — topic memo entry points generated from concept tags

### wiki/concepts/*.md

Generate one concept page per tag.
Each page should list related source pages and provide backlinks to them.
