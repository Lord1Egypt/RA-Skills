# AWP Platform Adapter: Cloudflare Dynamic Workers

This adapter generates deployment-ready TypeScript code for running AWP
workflows on **Cloudflare Workers** using Dynamic Worker Isolates.

## When to Use

Use this adapter when:
- You want serverless, globally distributed workflow execution (300+ locations)
- You need strong agent isolation via V8 Isolates (~5ms startup)
- You want auto-scaling with no concurrency limits
- You want edge-deployed AI workflows close to users
- You want to leverage Cloudflare's ecosystem (D1, R2, KV, Workers AI, Durable Objects)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│            Dispatch Worker (Orchestrator)            │
│                                                     │
│  - Reads embedded workflow.awp.yaml (as JSON)       │
│  - Executes DAG (sequential/parallel)               │
│  - Calls LLM for each agent                         │
│  - Validates output against schema                   │
│  - Manages state between agents                      │
│                                                     │
│  Bindings:                                          │
│    STATE   → KV Namespace (Workflow State)           │
│    MEMORY  → R2 Bucket (Long-term Memory)           │
│    DB      → D1 Database (Short-term/Daily Log)     │
│    AI      → Workers AI (optional LLM Backend)      │
├─────────────────────────────────────────────────────┤
│              Shared Infrastructure                   │
│                                                     │
│  KV Namespace     → Agent Configs + Runtime State   │
│  D1 (SQLite)      → Short-term Memory, Daily Logs   │
│  R2 Bucket        → Long-term Memory (MEMORY.md)    │
│  Workers AI       → LLM Inference (optional)        │
│  External API     → OpenAI/Anthropic/OpenRouter     │
└─────────────────────────────────────────────────────┘
```

### How Execution Works

The Dispatch Worker is the central orchestrator. Unlike the Python adapter
where each agent has an `agent.py`, the Cloudflare adapter embeds all agent
configs into the Dispatch Worker:

1. Reads the DAG from the embedded `workflow.awp.yaml`.
2. Topologically sorts agents by `depends_on`.
3. For each agent:
   a. Loads agent config (model, prompts, tools, output schema).
   b. Builds system prompt: `SYSTEM_PROMPT.md` + Skills + `MEMORY.md`.
   c. Builds user prompt: `00_INTRO.md` + State from predecessor agents.
   d. Calls LLM (Workers AI or external OpenAI-compatible API).
   e. Parses JSON response against `output_schema.json`.
   f. Stores result in state (KV).
   g. Optional: Writes daily log (D1), updates `MEMORY.md` (R2).
4. Returns final result as JSON.

### Memory Mapping

| AWP Memory Tier | Cloudflare Service | Lifecycle |
|----------------|-------------------|-----------|
| Working Memory | JS variables in Worker | Request-scoped, ephemeral |
| Short-term (Daily Log) | D1 (SQLite) | Persistent, queryable |
| Long-term (MEMORY.md) | R2 (Object Storage) | Unlimited persistence |

## Generated Files

When using this adapter, the skill generates the following files instead of
`agent.py`:

```
{{WORKFLOW_NAME}}/
  wrangler.toml                ← Cloudflare deployment config
  package.json                 ← npm dependencies
  tsconfig.json                ← TypeScript config
  src/
    index.ts                   ← Dispatch Worker (orchestrator)
    types.ts                   ← Shared TypeScript types
    llm.ts                     ← LLM client (OpenAI-compatible + Workers AI)
    memory.ts                  ← Memory manager (KV + D1 + R2)
    config/
      workflow.json            ← Compiled workflow.awp.yaml
      agents/
        {{AGENT_ID}}.json      ← Compiled agent configs
    prompts/
      {{AGENT_ID}}/
        system.md              ← SYSTEM_PROMPT.md
        user.md                ← 00_INTRO.md
    schemas/
      {{AGENT_ID}}.json        ← output_schema.json
  README.md                    ← Deployment instructions
```

**Note:** The standard AWP directory structure (`agents/`, `workflow.awp.yaml`)
is still generated alongside for validation and portability. The `src/` directory
contains the Cloudflare-specific compiled version.

## LLM Configuration

The adapter supports two LLM providers:

```yaml
# In agent.awp.yaml — OpenAI-compatible (default)
model:
  name: "anthropic/claude-sonnet-4-20250514"
  parameters:
    temperature: 0.2

# Cloudflare Workers AI
model:
  provider: workers-ai
  name: "@cf/meta/llama-3.1-70b-instruct"
  parameters:
    temperature: 0.2
```

Both are handled by `src/llm.ts`. Workers AI uses `env.AI.run()`, external
providers use `fetch()` against the OpenAI-compatible API.

## Deployment

### Prerequisites

```bash
npm install -g wrangler
wrangler login
```

### Setup Cloudflare Resources

```bash
cd {{WORKFLOW_NAME}}/

# Create KV namespace for state
wrangler kv namespace create STATE
# Copy the id into wrangler.toml

# Create D1 database for short-term memory (if L3+)
wrangler d1 create {{WORKFLOW_NAME}}-db
# Copy the database_id into wrangler.toml

# Create R2 bucket for long-term memory (if L3+)
wrangler r2 bucket create {{WORKFLOW_NAME}}-memory
```

### Set Secrets

```bash
# LLM API key (required for external providers)
wrangler secret put LLM_API_KEY

# Additional secrets declared in secrets.yaml
wrangler secret put SEARCH_API_KEY
```

### Deploy

```bash
npm install
wrangler deploy
```

### Invoke

```bash
# Via HTTP
curl -X POST https://{{WORKFLOW_NAME}}.{{ACCOUNT}}.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"task": "Research quantum computing trends"}'

# Via wrangler (local dev)
wrangler dev
# Then: curl http://localhost:8787 -d '{"task": "..."}'
```

## Costs

| Resource | Pricing | Typical Usage |
|----------|---------|---------------|
| Workers Requests | $0.30 / million | 1 request per workflow run |
| Workers CPU Time | $0.02 / million ms | ~50-200ms per agent |
| KV Reads | $0.50 / million | ~N reads per run (N = agents) |
| KV Writes | $5.00 / million | ~N writes per run |
| D1 Reads | $0.001 / million rows | Memory queries |
| D1 Writes | $1.00 / million rows | Daily log writes |
| R2 Storage | $0.015 / GB / month | MEMORY.md files |
| Workers AI | Varies by model | Per-token pricing |

For most workflows, costs are dominated by LLM inference (external API),
not Cloudflare infrastructure.

## Adapters Table Entry

| Platform | Adapter | Generated Files |
|----------|---------|----------------|
| **Cloudflare Dynamic Workers** | `adapters/cloudflare-dynamic-workers.md` | `src/index.ts`, `wrangler.toml`, TypeScript project |

## Dependencies

```json
{
  "dependencies": {
    "hono": "^4.0.0"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.0.0",
    "typescript": "^5.5.0",
    "wrangler": "^4.0.0"
  }
}
```

Environment variables (set via `wrangler secret put`):

```bash
LLM_API_KEY=sk-...          # API key for external LLM provider
LLM_MODEL=anthropic/claude-sonnet-4  # Model identifier
LLM_BASE_URL=https://openrouter.ai/api/v1  # API endpoint (default: OpenRouter)
```
