# codon

> Organize agent memory as a navigable filesystem. Every piece of information gets a numbered address — no search required.

Most memory skills answer: *how do I find it back?*
Codon answers: *where does this belong?*

## How it works

Codon creates a `MEMORY/` directory in your workspace with a numbered taxonomy:

```
MEMORY/
├── 10-19-People/
│   ├── 10.00-index.md
│   ├── 10.01-jane-smith-acme.md
│   └── 10.02-john-doe-partner.md
├── 20-29-Projects/
│   ├── 20.00-index.md
│   └── 20.01-website-redesign.md
├── 30-39-Resources/
│   └── 30.00-index.md
└── 40-49-Work/
    └── 40.00-index.md
```

Every memory has an address. Your agent navigates to it — no vector search, no query language, no API keys.

## Why not just use memory.md?

Flat files work until they don't. Once your agent has 50+ memories, a flat file becomes a wall of text it has to scan every time. Codon gives the agent a map: *"client contacts live in 10-19, always."*

## Why not ontology / vector search?

Those are databases. Codon is a filesystem. One requires Python and a query language. The other you can `ls`.

## Install

```bash
openclaw skills install codon
```

Then tell your agent: *"Initialize your memory system."*

## Zero dependencies

Pure bash + markdown. No Python, no database, no embeddings, no API keys.

## Extending with templates

The default taxonomy (People / Projects / Resources / Work) covers most use cases. Domain-specific templates are available separately for software engineering, market research, trading, and more.

## License

MIT
