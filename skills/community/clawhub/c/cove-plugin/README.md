# CoVe — Chain of Verification Plugin for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

CoVe brings **Chain of Verification** to your [OpenClaw](https://openclaw.sh) agents. It intercepts LLM responses, extracts atomic factual claims, and verifies them against your memory, workspace files, and optionally the web — catching hallucinations before they reach your users.

## How It Works

```
LLM Response → Extract Claims → Verify Against Sources → Auto-Correct → ✅ Accurate Response
                                        ↑
                         ┌──────────────┼──────────────┐
                     Memory/Files   Vector Store    Web Search
                    (local files)  (Qdrant, etc.)    (Brave)
```

1. **Extraction** — An LLM call identifies all specific factual claims in the response (names, dates, numbers, metrics, etc.)
2. **Verification** — A second LLM call cross-references each claim against your knowledge sources (memory files, workspace documents, web search results)
3. **Correction** — If inaccuracies are found, the plugin rewrites the response with correct information
4. **Reporting** — A detailed report shows what was verified, what was wrong, and what was corrected

## Quick Start

### 1. Install

Clone into your OpenClaw plugins directory:

```bash
git clone https://github.com/bhawanakatiyar/cove-plugin.git ~/.openclaw/plugins/cove-verification
```

Or copy the `SKILL.md` and `src/` directory to `~/.openclaw/`:

```bash
cp SKILL.md ~/.openclaw/cove-skill.md
cp src/verifier.js /usr/local/bin/cove-verify
chmod +x /usr/local/bin/cove-verify
```

### 2. Configure

Copy the default config to your OpenClaw directory:

```bash
cp config/default.yaml ~/.openclaw/cove.yaml
```

Then edit `~/.openclaw/cove.yaml`:

```yaml
policy: "basic"                    # basic | standard | deep
auto_correct: true                 # Rewrite response with corrections
max_correction_attempts: 1         # Correction loop iterations
log_results_to_dashboard: true     # Log results to stdout

knowledge_sources:
  use_system_memory: true          # Read ~/.openclaw/workspace/memory/
  document_paths: []               # Additional document directories
  enable_web_search: false         # Enable Brave Search (needs API key)
```

The plugin looks for config in this order:
1. `~/.openclaw/cove.yaml` (recommended — user-editable)
2. `<plugin-dir>/config/default.yaml` (fallback defaults)

### 3. Use

Your OpenClaw agent will automatically discover the `cove-verify` skill and use it when making factual claims. You can also use it from the command line:

```bash
# Basic verification against memory + workspace
cove-verify -r "Alice is on the Enterprise plan at $499/month."

# Standard — also searches the web
cove-verify -r "GPT-4 was released in March 2023." -p standard

# Pipe from another command
echo "Revenue is $45K across 12 customers." | cove-verify --stdin

# JSON output
cove-verify -r "The API limit is 1000 req/min." -f json
```

## Verification Policies

| Policy | Sources | Best For |
|--------|---------|----------|
| **basic** | Memory + workspace + vector store | Internal facts (customers, products, configs) |
| **standard** | All of basic + web search | Facts that may need external confirmation |
| **deep** | All sources + multi-step reasoning | Critical claims, compliance, financial data |

## Vector Store Integration

CoVe can verify claims against external vector databases for semantic search over large knowledge bases. Supported providers:

| Provider | Config key | Documentation |
|----------|-----------|---------------|
| **Qdrant** | `qdrant` | [qdrant.tech](https://qdrant.tech) |
| **Chroma** | `chroma` | [trychroma.com](https://www.trychroma.com) |
| **Weaviate** | `weaviate` | [weaviate.io](https://weaviate.io) |
| **Milvus** | `milvus` | [milvus.io](https://milvus.io) |
| **Redis Vector** | `redis` | [redis.io](https://redis.io/docs/interact/search-and-query/) |
| **OpenViking** | `openviking` | OpenViking vector search |

Add to `~/.openclaw/cove.yaml`:

```yaml
vector_store:
  provider: "qdrant"              # qdrant | chroma | weaviate | milvus | redis | openviking
  url: "http://localhost:6333"    # Vector DB endpoint
  collection: "knowledge"         # Collection/index name
  api_key: ""                     # Optional auth key
  top_k: 5                        # Results per query
  score_threshold: 0.7            # Minimum similarity (0-1)
```

Vector store results are combined with local file knowledge before verification. The LLM sees both sources and uses whichever is most relevant for each claim.

**How it works:**
1. Each extracted claim is sent as a query to the vector store
2. The top-k most similar chunks are retrieved
3. Results are injected into the verification prompt alongside local files
4. The LLM cross-references all sources to verify or refute each claim

**No native dependencies** — all adapters use the vector DB's HTTP REST API. Embeddings for vector search are generated via the OpenClaw sidecar proxy.

## Example Output

```
═══ CoVe — Chain of Verification Report ═══

  ✅ VERIFIED: "Alice is on the Enterprise plan"
     Source: workspace/customers.csv

  ❌ INACCURATE: "signed up on March 1st"
     Source: workspace/customers.csv
     Correction: Alice signed up on March 17th, 2026

  ❓ UNVERIFIABLE: "her team has 15 members"
     Note: Team size not found in available sources

───────────────────────────────────────────
  Claims: 3 total
  ✅ 1 verified  ❌ 1 inaccurate  ❓ 1 unverifiable
  Duration: 2340ms

═══ Corrected Response ═══

Alice is on the Enterprise plan. She signed up on March 17th, 2026.
Her team has 15 members.
```

## Architecture

```
cove-plugin/
├── SKILL.md              # OpenClaw native skill definition
├── plugin.json           # Plugin metadata
├── config/
│   └── default.yaml      # Default configuration
├── src/
│   ├── verifier.js       # CLI entry point
│   ├── verify_claims.js  # Core orchestrator (extract → verify → correct)
│   ├── knowledge.js      # Knowledge source reader (memory, workspace, SQLite, docs)
│   ├── vector_store.js   # Vector DB adapters (Qdrant, Chroma, Weaviate, Milvus, Redis, OpenViking)
│   ├── web_search.js     # Brave Search integration
│   ├── config.js         # YAML config loader (zero dependencies)
│   └── csm-logger.js     # Structured logging
├── test_simulation.js    # Test runner
├── package.json
├── LICENSE
└── README.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENCLAW_PROXY_PORT` | Sidecar LLM proxy port | `8888` |
| `SIDECAR_PROXY_KEY` | Proxy authentication key | — |
| `COVE_MODEL` | LLM model for verification | `gemini-2.0-flash` |
| `BRAVE_API_KEY` | Brave Search API key (for standard/deep) | — |

## Zero Dependencies

CoVe has **no npm dependencies**. It uses only Node.js built-in modules (`http`, `https`, `fs`, `path`). This keeps it lightweight, portable, and easy to audit.

## How the Agent Uses CoVe

When installed as an OpenClaw skill, the agent automatically uses CoVe when:
- Making specific claims about the user's data
- Citing numbers, dates, or metrics from files
- Referencing past decisions or stored information

The agent runs `cove-verify` silently, fixes any inaccuracies, and presents the corrected response — the user never sees the verification process.

## Contributing

Contributions are welcome! Please open an issue or submit a PR.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

[MIT](LICENSE)
