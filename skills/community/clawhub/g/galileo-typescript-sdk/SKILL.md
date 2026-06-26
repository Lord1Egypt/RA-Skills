---
name: galileo-typescript-sdk
description: Complete reference for the Galileo AI platform TypeScript/JS SDK for evaluating, observing, and protecting GenAI applications. Use when building Node.js or TypeScript applications that need LLM evaluation, production observability, tracing, or runtime guardrails with Galileo.
license: MIT
compatibility: Requires Node.js 18+. Works with npm, yarn, or pnpm.
metadata:
  author: gyanesh-m
  version: "1.0.0"
  sdk-version: "2.0.0"
  sdk-repo: https://github.com/rungalileo/galileo-js
  docs: https://docs.galileo.ai
---

# Galileo TypeScript SDK

The Galileo TypeScript SDK (`galileo`) provides evaluation and observability workflows for GenAI applications in Node.js and TypeScript. It supports logging LLM calls, retriever operations, tool invocations, and multi-step workflows with built-in scoring.

**Additional references:**

- [Framework Integrations](references/INTEGRATIONS.md) — Vercel AI SDK, Mastra, LangGraph (JS), and more
- [Guardrail Metrics Reference](references/METRICS.md) — Scoring metrics available for evaluation workflows
- [Advanced Evaluation Patterns](references/EVALUATION.md) — Complex workflow evaluation and experiment design

## Installation

```bash
npm install galileo
```

Or with yarn/pnpm:

```bash
yarn add galileo
pnpm add galileo
```

## Quick Start

```typescript
import { wrapOpenAI, init, flush } from "galileo";
import OpenAI from "openai";

await init({ projectName: "my-project", logstream: "my-log-stream" });

const openai = wrapOpenAI(new OpenAI());
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Explain quantum computing in one sentence." }],
});

console.log(response.choices[0].message.content);

await flush();
```

## Authentication

Set the following environment variables in your `.env` file or shell:

```bash
GALILEO_API_KEY="your-api-key"            # Required — from Galileo console
GALILEO_CONSOLE_URL="https://app.galileo.ai"  # Console URL (or self-hosted)
```

Alternative authentication via username/password:

```bash
GALILEO_USERNAME="your-username"
GALILEO_PASSWORD="your-password"
```

## Observability

### Wrapped OpenAI Client (Auto-Logging)

The simplest way to trace all OpenAI calls — wrap the client and all calls are logged automatically:

```typescript
import { wrapOpenAI, init, flush } from "galileo";
import OpenAI from "openai";

await init({ projectName: "my-project", logstream: "production" });

const openai = wrapOpenAI(new OpenAI());
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "What is RAG?" }],
});

await flush();
```

Azure OpenAI is also supported via `wrapAzureOpenAI`.

### The `log()` Function Wrapper

Wrap any function to log its execution as a span. Supports sync, async, and generator functions:

```typescript
import { log, init, flush } from "galileo";

await init({ projectName: "my-project", logstream: "production" });

const retrieveDocuments = log(
  { spanType: "retriever", name: "vector-search" },
  async (query: string) => {
    const results = await vectorDb.search(query, { k: 5 });
    return results.map((r) => r.content);
  }
);

const generateResponse = log(
  { spanType: "llm", name: "gpt-4o-call" },
  async (query: string, context: string[]) => {
    const openai = new OpenAI();
    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [{ role: "user", content: `Context: ${context.join("\n")}\n\nQuestion: ${query}` }],
    });
    return response.choices[0].message.content;
  }
);

const ragPipeline = log(
  { spanType: "workflow", name: "rag-pipeline" },
  async (query: string) => {
    const docs = await retrieveDocuments(query);
    return generateResponse(query, docs);
  }
);

await ragPipeline("What are the benefits of RAG?");
await flush();
```

Supported span types: `workflow`, `llm`, `retriever`, `tool`, `agent`.

### GalileoLogger (Manual Spans)

For fine-grained control, use `GalileoLogger` directly to build traces with explicit spans:

```typescript
import { GalileoLogger } from "galileo";

const logger = new GalileoLogger({
  projectName: "my-project",
  logStreamName: "production",
});

logger.startTrace({ input: "Calculate 15 * 42" });

logger.addToolSpan({
  input: "15 * 42",
  output: "630",
  durationNs: 50000000,
});

logger.addLlmSpan({
  input: "The math tool returned 630. Respond to the user.",
  output: "15 multiplied by 42 equals 630.",
  durationNs: 800000000,
  model: "gpt-4o",
});

logger.conclude({ output: "15 multiplied by 42 equals 630." });

await logger.flush();
```

Available span methods: `addLlmSpan`, `addRetrieverSpan`, `addToolSpan`, `addWorkflowSpan`, `addAgentSpan`, `addProtectSpan`.

### Context API

Use `galileoContext` for scoped lifecycle management:

```typescript
import { galileoContext } from "galileo";

await galileoContext.init({ projectName: "my-project", logstream: "production" });

// ... trace your calls ...

await galileoContext.flush();
await galileoContext.reset();
```

### Sessions

Group related traces into sessions for multi-turn conversations:

```typescript
import { init, flush, startSession, setSession, clearSession } from "galileo";

await init({ projectName: "my-project", logstream: "production" });

const sessionId = await startSession({ name: "user-conversation-123" });

// All traces created between setSession and clearSession are grouped
setSession(sessionId);
// ... log your traces ...
clearSession();

await flush();
```

## Evaluation

### Running an Experiment

Use `runExperiment` to evaluate your LLM pipeline against a dataset with automated scoring:

```typescript
import { runExperiment, GalileoMetrics } from "galileo";

const result = await runExperiment({
  name: "qa-eval-run",
  datasetName: "my-test-dataset",
  metrics: [GalileoMetrics.contextAdherence, GalileoMetrics.completeness, GalileoMetrics.inputToxicity],
  projectName: "eval-project",
  function: async (input) => {
    const response = await callYourLLM(input.question);
    return response;
  },
});

console.log("Experiment link:", result.link);
```

### Experiment with Inline Dataset

```typescript
import { runExperiment, GalileoMetrics } from "galileo";

const result = await runExperiment({
  name: "rag-eval",
  dataset: [
    { question: "What is ML?", expected: "Machine learning is..." },
    { question: "Explain AI", expected: "Artificial intelligence is..." },
  ],
  metrics: [GalileoMetrics.contextAdherence, GalileoMetrics.chunkAttributionUtilization, GalileoMetrics.completeness],
  projectName: "eval-project",
  function: async (input) => {
    const docs = await retrieve(input.question);
    return generateAnswer(input.question, docs);
  },
});
```

### Experiment with Prompt Template

```typescript
import { runExperiment, GalileoMetrics } from "galileo";

const result = await runExperiment({
  name: "prompt-eval",
  datasetName: "my-test-dataset",
  promptTemplate: { id: "your-prompt-template-id" },
  promptSettings: { model_alias: "GPT-4o", temperature: 0.7 },
  metrics: [GalileoMetrics.correctness, GalileoMetrics.instructionAdherence],
  projectName: "eval-project",
});
```

See [Advanced Evaluation Patterns](references/EVALUATION.md) for more.

## Common Patterns

### RAG Pipeline with Retriever Spans

```typescript
import { GalileoLogger } from "galileo";

const logger = new GalileoLogger({
  projectName: "rag-app",
  logStreamName: "production",
});

logger.startTrace({ input: "How does photosynthesis work?" });

logger.addRetrieverSpan({
  input: "How does photosynthesis work?",
  output: ["Photosynthesis is the process by which plants..."],
});

logger.addLlmSpan({
  input: "Using the context, explain photosynthesis.",
  output: "Photosynthesis is a process used by plants...",
  durationNs: 1500000000,
  model: "gpt-4o",
});

logger.conclude({ output: "Photosynthesis is a process used by plants..." });
await logger.flush();
```

### Nested Agent Workflows

```typescript
import { GalileoLogger } from "galileo";

const logger = new GalileoLogger({
  projectName: "agent-app",
  logStreamName: "production",
});

logger.startTrace({ input: "Research and summarize quantum computing" });

logger.addToolSpan({
  input: "search: quantum computing overview",
  output: "Search results...",
  durationNs: 200000000,
});

logger.addRetrieverSpan({
  input: "quantum computing",
  output: ["Doc1: Quantum bits...", "Doc2: Superposition..."],
});

logger.addLlmSpan({
  input: "Summarize the following research on quantum computing...",
  output: "Quantum computing leverages quantum mechanical phenomena...",
  durationNs: 2500000000,
  model: "gpt-4o",
});

logger.conclude({
  output: "Quantum computing leverages quantum mechanical phenomena...",
});

await logger.flush();
```

## Best Practices

1. **Call `init()` or create a `GalileoLogger`** before logging any traces.
2. **Always call `flush()`** at the end to upload traces to Galileo. In web servers, flush at the end of each request handler.
3. **Use `wrapOpenAI`** for zero-config automatic tracing of all OpenAI calls.
4. **Use `log()`** to wrap functions as spans — it handles sync, async, and generator functions automatically.
5. **Use `GalileoLogger`** when you need fine-grained control over individual spans.
6. **Use `runExperiment`** for evaluation runs — it handles dataset loading, scoring, and result upload.
7. **Set environment variables** in `.env` files rather than hardcoding API keys.
8. **Use accurate `durationNs` values** when manually creating spans for meaningful latency tracking.

## Legacy API

`GalileoObserveWorkflow` and `GalileoEvaluateWorkflow` are deprecated but still exported for backward compatibility. Use `GalileoLogger` (or `wrapOpenAI` / `log()`) and `runExperiment` instead.

## Resources

- **Documentation:** https://docs.galileo.ai
- **TypeScript SDK repo:** https://github.com/rungalileo/galileo-js
- **SDK examples:** https://github.com/rungalileo/sdk-examples
- **npm:** https://www.npmjs.com/package/galileo
- **Galileo console:** https://app.galileo.ai
