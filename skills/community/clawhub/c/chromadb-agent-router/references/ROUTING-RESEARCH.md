# Routing Research Notes

## Evolution of the Semantic Router

### V1: Pure Embeddings (70.8%)
- Single embedding per agent, cosine similarity
- Ceiling at ~70% due to semantic overlap between categories

### V2: Per-Skill Max Similarity (70.8%)
- Multiple embeddings per route, use max similarity
- Same ceiling — the problem isn't resolution, it's intent ambiguity

### V3: Embeddings + Keyword + Action Verbs (100%)
- **Breakthrough**: Action verb stratification
- Ops verbs (deploy, install) → ALWAYS override topic
- Topic verbs (secure, harden) → override but route-specific
- Weak verbs (check, monitor) → let embeddings decide

### Key Insight: Keyword Stealing
- "docker" appears in ops, infrastructure, and dev routes
- A keyword must appear in EXACTLY ONE route
- Removing shared keywords improved accuracy by 8%

### French Handling
- nomic-embed-text is English-focused
- French normalization (accent removal) helps but isn't enough
- Action verb detection must run on ORIGINAL text (before normalization)
- Pattern: normalize for embeddings, original for verb detection

### ChromaDB vs Ollama Embeddings
- ChromaDB default (all-MiniLM-L6-v2): No external dependency, self-contained
- Ollama (nomic-embed-text): Better multilingual, requires Ollama service
- For a publishable skill: ChromaDB default is better (zero external deps)

### Performance on Raspberry Pi 5 (ARM64)
- ChromaDB: 646 queries/sec, 1.55ms/query, 32.7MB RAM
- Cold start: ~6s (download model first time, then cached)
- Warm queries: <5ms consistently

### Competing Approaches (ClawHub Survey, 2026-03-29)
- **openclaw-smart-router**: Model router (not agent router), x402 payments, flagged suspicious
- **intent-router**: Text classification via external API, $0.005/request, flagged suspicious
- **Our differentiation**: Local, free, agent-aware, bilingual, ARM64-compatible
