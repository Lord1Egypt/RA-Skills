# {{WORKFLOW_NAME}} — AWP on Cloudflare Workers

{{WORKFLOW_DESCRIPTION}}

**AWP Compliance Level:** L{{COMPLIANCE_LEVEL}}
**Runtime:** Cloudflare Dynamic Workers

## Prerequisites

- [Node.js](https://nodejs.org/) 18+
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/) 4+
- A Cloudflare account

## Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Create Cloudflare resources

```bash
# Create KV namespace for workflow state
wrangler kv namespace create STATE
# → Copy the id into wrangler.toml under [[kv_namespaces]]

# If using memory (L3+):
wrangler d1 create {{WORKFLOW_NAME}}-db
wrangler r2 bucket create {{WORKFLOW_NAME}}-memory
# → Copy IDs into wrangler.toml
```

### 3. Set secrets

```bash
wrangler secret put LLM_API_KEY
# Enter your API key when prompted (e.g., OpenRouter, Anthropic, OpenAI)
```

### 4. Deploy

```bash
wrangler deploy
```

## Usage

### Run a workflow

```bash
curl -X POST https://{{WORKFLOW_NAME}}.{{SUBDOMAIN}}.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"task": "{{EXAMPLE_TASK}}"}'
```

### Local development

```bash
wrangler dev
# Then: curl http://localhost:8787 -d '{"task": "..."}'
```

### Health check

```bash
curl https://{{WORKFLOW_NAME}}.{{SUBDOMAIN}}.workers.dev/health
```

## Project Structure

```
src/
  index.ts      Dispatch Worker (orchestrator, DAG execution)
  types.ts      TypeScript type definitions
  llm.ts        LLM client (Workers AI + OpenAI-compatible)
  memory.ts     Memory manager (KV + D1 + R2)
```

## AWP Compatibility

This project was generated from an AWP workflow manifest. The standard AWP
files (`workflow.awp.yaml`, `agents/`) are included for validation and
portability. The `src/` directory contains the Cloudflare-compiled version.

To validate the AWP structure:

```bash
pip install awp-protocol
awp validate .
```
