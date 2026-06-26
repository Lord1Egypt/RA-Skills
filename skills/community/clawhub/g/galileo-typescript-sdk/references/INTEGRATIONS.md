# Framework Integrations (TypeScript)

Galileo integrates with TypeScript/JS frameworks via **OpenTelemetry + OpenInference** instrumentation, enabling automatic tracing of LLM calls across your application.

## Vercel AI SDK

Trace Vercel AI SDK calls using the OpenTelemetry integration:

```typescript
import { openai } from "@ai-sdk/openai";
import { generateText } from "ai";

// Enable telemetry in Vercel AI SDK
const result = await generateText({
  model: openai("gpt-4o"),
  prompt: "What is quantum computing?",
  experimental_telemetry: { isEnabled: true },
});
```

Configure the OpenTelemetry exporter to send traces to Galileo:

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";

const exporter = new OTLPTraceExporter({
  url: "https://app.galileo.ai/api/otel/v1/traces",
  headers: {
    Authorization: `Bearer ${process.env.GALILEO_API_KEY}`,
  },
});

const sdk = new NodeSDK({ traceExporter: exporter });
sdk.start();
```

## Mastra

Mastra provides built-in telemetry support. Configure the Galileo OTLP endpoint:

```typescript
import { Mastra } from "@mastra/core";

const mastra = new Mastra({
  telemetry: {
    serviceName: "my-mastra-app",
    exporter: {
      type: "otlp",
      endpoint: "https://app.galileo.ai/api/otel/v1/traces",
      headers: {
        Authorization: `Bearer ${process.env.GALILEO_API_KEY}`,
      },
    },
  },
});
```

## LangGraph (JS)

Use the OpenInference LangChain instrumentor for JavaScript:

```typescript
import { LangChainInstrumentor } from "@arizeai/openinference-instrumentation-langchain";

const instrumentor = new LangChainInstrumentor();
instrumentor.manuallyInstrument();
```

All LangGraph node executions, edges, and LLM calls are automatically traced.

## OpenAI (Node.js)

Use the OpenInference OpenAI instrumentor:

```typescript
import { OpenAIInstrumentor } from "@arizeai/openinference-instrumentation-openai";

const instrumentor = new OpenAIInstrumentor();
instrumentor.manuallyInstrument();
```

## Setting Up the OpenTelemetry Exporter

The common pattern for all framework integrations:

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";
import { SimpleSpanProcessor } from "@opentelemetry/sdk-trace-base";

const exporter = new OTLPTraceExporter({
  url: `${process.env.GALILEO_CONSOLE_URL}/api/otel/v1/traces`,
  headers: {
    Authorization: `Bearer ${process.env.GALILEO_API_KEY}`,
  },
});

const sdk = new NodeSDK({
  traceExporter: exporter,
  spanProcessors: [new SimpleSpanProcessor(exporter)],
});

sdk.start();

process.on("SIGTERM", () => sdk.shutdown());
```

## Combining Native SDK with OpenTelemetry

You can use the Galileo TypeScript SDK alongside OpenTelemetry-instrumented frameworks for comprehensive coverage:

```typescript
import { wrapOpenAI, init, flush } from "galileo";
import OpenAI from "openai";

await init({ projectName: "hybrid-project", logstream: "production" });

const openai = wrapOpenAI(new OpenAI());
const response = await instrumentedLangGraphAgent(userQuery);

await flush();
```
