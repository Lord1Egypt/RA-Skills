---
name: ai-integration
description: Use when building AI-powered features with the Claude API or Anthropic SDK — structured outputs, tool calling, streaming, multi-provider routing, multi-agent orchestration, LLM evaluation, prompt engineering, agent memory, RAG pipelines, and production deployment. Covers single-agent, multi-agent, and agentic loop patterns for Next.js, Python, and TypeScript stacks.
license: MIT
metadata:
  author: Skill Forge (scout + minter)
  version: 2.0.0
  sources:
    - wshobson/agents (32,432 stars, MIT)
    - Anthropic SDK docs
    - instructor library (structured outputs)
    - LiteLLM (multi-provider routing)
    - Claude Code multi-agent research (2026-03-28)
  market: +178% YoY demand, $75-200/hr on Upwork
---

# AI Integration Skill

Comprehensive patterns for integrating the Anthropic Claude API into production systems — from basic API calls to full multi-agent orchestration with state management, memory, and evaluation.

## When to Use This Skill

Activate when:
- Building a Claude API integration or wrapper
- Implementing structured outputs, tool calling, or streaming
- Setting up multi-provider LLM routing (LiteLLM, fallbacks)
- Designing multi-agent orchestration or agentic loops
- Implementing RAG or persistent agent memory
- Evaluating LLM output quality or building evals
- Deploying agents to Next.js, Python FastAPI, or Docker

**Don't use this skill for:**
- Kubernetes/Terraform config unrelated to AI infra
- General React/Next.js features not involving LLM calls

---

## Core Principles

### 1. Single Agent vs Multi-Agent

| Pattern | When to Use | Cost |
|---------|-------------|------|
| **Single agent** | Linear tasks, simple I/O, <5 steps | Low |
| **Subagent delegation** | Parallel tasks, specialized expertise needed | Medium |
| **Multi-agent swarm** | Complex autonomous workflows, >10 steps | High — budget like a team |

> **Infrastructure math (2026):** Multi-agent compute costs jump ~3x when moving from single to orchestrated swarms. Budget before you build.

### 2. Agent Communication Patterns

**Hub-and-spoke (most common):** Orchestrator delegates to specialist agents.
```
orchestrator
  ├── researcher-agent   (web search, docs)
  ├── coder-agent        (code generation, tests)
  └── reviewer-agent     (quality, security check)
```

**Pipeline:** Output of one agent is input to next (linear, predictable).

**Swarm:** Agents with shared memory, no single orchestrator. Use for exploration tasks.

### 3. Context Window Management

```python
import anthropic

client = anthropic.Anthropic()

def sliding_window(messages: list[dict], max_tokens: int = 150_000) -> list[dict]:
    """Drop oldest messages to stay within token budget."""
    # Rough estimate: 1 token ≈ 4 chars
    while len(messages) > 2:
        total = sum(len(m["content"]) // 4 for m in messages)
        if total <= max_tokens:
            break
        messages = messages[1:]  # drop oldest non-system message
    return messages

def summarize_history(messages: list[dict]) -> list[dict]:
    """Compress old turns into a summary to reclaim context budget."""
    if len(messages) <= 4:
        return messages
    history = "\n".join(f"{m['role']}: {m['content']}" for m in messages[:-2])
    summary = client.messages.create(
        model="claude-haiku-4-5", max_tokens=512,
        messages=[{"role": "user", "content": f"Summarize concisely:\n{history}"}],
    ).content[0].text
    return [{"role": "user", "content": f"[Prior context]\n{summary}"}] + messages[-2:]
```

---

## Structured Outputs

### Pydantic binding with `instructor` (recommended)

```python
import anthropic
import instructor
from pydantic import BaseModel

class Entity(BaseModel):
    name: str
    type: str       # person | org | location | concept
    description: str

class ExtractionResult(BaseModel):
    entities: list[Entity]
    summary: str

# instructor patches the client — returns validated Pydantic models
client = instructor.from_anthropic(anthropic.Anthropic())

result: ExtractionResult = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Extract all entities from:\n{text}"}],
    response_model=ExtractionResult,
)
print(result.entities[0].name)   # fully typed, validated
```

### Schema enforcement without instructor (TypeScript)

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";

const client = new Anthropic();

const EntitySchema = z.object({
  entities: z.array(z.object({ name: z.string(), type: z.string() })),
  summary: z.string(),
});

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{
    role: "user",
    content: `Extract entities. Respond ONLY with valid JSON matching this schema:
{"entities": [{"name": string, "type": string}], "summary": string}

Text: ${inputText}`,
  }],
});

const parsed = EntitySchema.parse(JSON.parse(response.content[0].text));
```

---

## Tool Calling (Function Calling)

### Parallel tool calls + agentic loop (TypeScript)

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
  { name: "search_web", description: "Search the web",
    input_schema: { type: "object" as const, properties: { query: { type: "string" } }, required: ["query"] } },
  { name: "read_file", description: "Read a local file",
    input_schema: { type: "object" as const, properties: { path: { type: "string" } }, required: ["path"] } },
];

async function runAgentLoop(userMessage: string): Promise<string> {
  const messages: Anthropic.MessageParam[] = [{ role: "user", content: userMessage }];

  while (true) {
    const response = await client.messages.create({
      model: "claude-sonnet-4-6", max_tokens: 4096,
      tools, tool_choice: { type: "auto" },  // or { type: "tool", name: "search_web" }
      messages,
    });

    if (response.stop_reason === "end_turn") {
      return response.content.filter((b) => b.type === "text").map((b) => b.text).join("");
    }

    // Claude may call multiple tools in parallel — handle all at once
    const toolUses = response.content.filter((b) => b.type === "tool_use");
    const toolResults = await Promise.all(
      toolUses.map(async (tu) => ({
        type: "tool_result" as const,
        tool_use_id: (tu as Anthropic.ToolUseBlock).id,
        content: await executeTool((tu as Anthropic.ToolUseBlock).name, (tu as Anthropic.ToolUseBlock).input),
      }))
    );

    messages.push({ role: "assistant", content: response.content });
    messages.push({ role: "user", content: toolResults });
  }
}
```

---

## Streaming Responses

### Python streaming
```python
import anthropic

client = anthropic.Anthropic()

# Stream text
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()
    print(f"\n[{final.usage.input_tokens} in / {final.usage.output_tokens} out tokens]")
```

### TypeScript streaming
```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  stream: true,
  messages: [{ role: "user", content: prompt }],
});

for await (const chunk of stream) {
  if (chunk.type === "content_block_delta" && chunk.delta.type === "text_delta") {
    process.stdout.write(chunk.delta.text);
  }
}
```

### Next.js SSE streaming route
```typescript
// app/api/chat/route.ts
import Anthropic from "@anthropic-ai/sdk";
import { NextRequest } from "next/server";

const client = new Anthropic();

export async function POST(req: NextRequest) {
  const { messages } = await req.json();
  const stream = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 2048,
    stream: true,
    messages,
  });

  const encoder = new TextEncoder();
  const readable = new ReadableStream({
    async start(controller) {
      for await (const chunk of stream) {
        if (chunk.type === "content_block_delta" && chunk.delta.type === "text_delta") {
          controller.enqueue(encoder.encode(chunk.delta.text));
        }
      }
      controller.close();
    },
  });

  return new Response(readable, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
```

---

## Multi-Provider Routing (LiteLLM)

```python
from litellm import completion, Router

# Provider-agnostic call — same interface for Claude, OpenAI, Gemini
def llm_call(messages: list[dict], model: str = "claude-sonnet-4-6") -> str:
    response = completion(
        model=model,       # "claude-sonnet-4-6" | "gpt-4o" | "gemini/gemini-1.5-pro"
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content

# Automatic fallback: try primary model, fall back on error
response = completion(
    model="claude-opus-4-6",
    messages=messages,
    fallbacks=["claude-sonnet-4-6", "gpt-4o"],
    max_tokens=1024,
)

# Cost-aware routing: route by quality tier
router = Router(model_list=[
    {"model_name": "fast",    "litellm_params": {"model": "claude-haiku-4-5"}},
    {"model_name": "smart",   "litellm_params": {"model": "claude-sonnet-4-6"}},
    {"model_name": "premium", "litellm_params": {"model": "claude-opus-4-6"}},
])

# Pick tier based on task complexity
tier = "fast" if simple_task else "smart"
response = router.completion(model=tier, messages=messages)
print(response.choices[0].message.content)
```

---

## Prompt Versioning

```python
import hashlib

# Version-pinned prompt registry — pin versions to prevent silent regressions
PROMPTS = {
    "summarize:v1": "Summarize in {max_words} words:\n{text}",
    "summarize:v2": "Create a {max_words}-word summary focusing on key decisions:\n{text}",
}

def run_prompt(key: str, **kwargs) -> str:
    template = PROMPTS[key]
    hash_id = hashlib.sha256(template.encode()).hexdigest()[:8]
    # Log key + hash for reproducibility and A/B analysis
    print(f"[prompt] key={key} hash={hash_id}")
    return llm_call([{"role": "user", "content": template.format(**kwargs)}])
```

---

## Multi-Agent Orchestration

### Orchestrator pattern (Python)
```python
import anthropic, asyncio

client = anthropic.Anthropic()

AGENTS = {
    "planner":     "Break this task into subtasks. Output JSON: {\"research_tasks\": [], \"code_tasks\": []}",
    "researcher":  "Research the provided topics. Be concise and factual.",
    "coder":       "Write clean, tested Python code for the provided specs.",
    "synthesizer": "Combine these results into a final cohesive answer.",
}

def call_agent(role: str, content: str, model: str = "claude-sonnet-4-6") -> str:
    resp = client.messages.create(
        model=model,
        max_tokens=2048,
        system=AGENTS[role],
        messages=[{"role": "user", "content": content}],
    )
    return resp.content[0].text

async def orchestrate(task: str) -> str:
    """Hub-and-spoke orchestrator: plan → parallel execute → synthesize."""
    import json
    plan = json.loads(call_agent("planner", task))

    research, code = await asyncio.gather(
        asyncio.to_thread(call_agent, "researcher", str(plan.get("research_tasks", []))),
        asyncio.to_thread(call_agent, "coder",      str(plan.get("code_tasks", []))),
    )
    return call_agent("synthesizer", f"Research:\n{research}\n\nCode:\n{code}")
```

---

## Agent Memory Patterns

### Medium-term: SQLite (cross-session)
```python
import sqlite3, json

conn = sqlite3.connect("agent_memory.db")
conn.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT, updated_at TEXT)")

def remember(key: str, value: dict):
    conn.execute("INSERT OR REPLACE INTO memory VALUES (?, ?, datetime('now'))", [key, json.dumps(value)])
    conn.commit()

def recall(key: str) -> dict | None:
    row = conn.execute("SELECT value FROM memory WHERE key=?", [key]).fetchone()
    return json.loads(row[0]) if row else None
```

### Long-term: Vector DB (semantic search / RAG)
```python
from qdrant_client import QdrantClient
import anthropic

qdrant = QdrantClient(":memory:")
claude = anthropic.Anthropic()

def rag_query(query: str, context_collection: str = "memory") -> str:
    hits = qdrant.search(collection_name=context_collection,
                         query_vector=get_embedding(query), limit=5)
    context = "\n".join(h.payload["text"] for h in hits)
    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=f"Answer using this context:\n{context}",
        messages=[{"role": "user", "content": query}],
    )
    return response.content[0].text
```

---

## LLM Evaluation

### Basic eval harness
```python
import anthropic

def run_eval(cases: list[tuple[str, str]], system_prompt: str) -> dict:
    """cases: list of (input, expected_output) tuples."""
    client = anthropic.Anthropic()
    results = {"pass": 0, "fail": 0, "score": 0.0, "cases": []}
    for inp, expected in cases:
        actual = client.messages.create(
            model="claude-haiku-4-5", max_tokens=512,  # use cheap model for evals
            system=system_prompt,
            messages=[{"role": "user", "content": inp}],
        ).content[0].text.strip()
        passed = actual == expected
        results["pass" if passed else "fail"] += 1
        results["cases"].append({"input": inp, "actual": actual, "pass": passed})
    results["score"] = results["pass"] / len(cases)
    return results
```

### LLM-as-judge
```python
import json

def llm_judge(question: str, answer: str, rubric: str) -> dict:
    response = client.messages.create(
        model="claude-haiku-4-5",
        messages=[{"role": "user", "content": f"""Rate this answer 1-5.

Question: {question}
Answer: {answer}
Rubric: {rubric}

Output JSON: {{"score": int, "reasoning": str}}"""}],
        max_tokens=256,
    )
    return json.loads(response.content[0].text)
```

---

## Production Deployment

### Error handling and retries
```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({ maxRetries: 3, timeout: 60_000 });

try {
  const response = await client.messages.create({ /* ... */ });
} catch (err) {
  if (err instanceof Anthropic.RateLimitError) {
    const retryAfter = Number(err.headers?.["retry-after"] ?? 30) * 1000;
    await new Promise((r) => setTimeout(r, retryAfter));
  } else if (err instanceof Anthropic.APIConnectionError) {
    // network issue — SDK will auto-retry up to maxRetries
  }
}
```

### Cost tracking
```python
def track_cost(response: anthropic.types.Message) -> float:
    PRICES = {
        "claude-opus-4-6":    (0.015, 0.075),   # (input, output) per 1k tokens
        "claude-sonnet-4-6":  (0.003, 0.015),
        "claude-haiku-4-5":   (0.00025, 0.00125),
    }
    model = response.model
    if model not in PRICES:
        return 0.0
    in_cost  = response.usage.input_tokens  / 1000 * PRICES[model][0]
    out_cost = response.usage.output_tokens / 1000 * PRICES[model][1]
    return in_cost + out_cost
```

---

## Prompt Engineering

- **Chain-of-thought:** Prefix with `Think step by step:` or enumerate reasoning steps before the answer.
- **Output format pinning:** Specify format in system prompt AND show a concrete example. Never rely on defaults for structured data.
- **Temperature:** `0` = deterministic (evals, extraction) | `0.3-0.7` = balanced | `1.0` = creative/diverse.

---

## Related Skills

- `temporal-testing` — test async agent workflows
- `browser-automation` — give agents web browsing capability
- `frontend-design` — build AI-powered Next.js UIs
- `data-analysis-report` — agent-driven data analysis pipelines
- `llm-observability` — trace and monitor LLM calls in production
