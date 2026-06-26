# Framework Integrations

Galileo integrates with popular LLM frameworks primarily via **OpenTelemetry + OpenInference** instrumentation. This enables automatic tracing without modifying your application code beyond adding the Galileo exporter.

## OpenAI (Wrapped Client)

The simplest integration — use Galileo's wrapped OpenAI client for automatic tracing:

```python
from galileo.openai import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4o",
)
```

All calls through this client are automatically logged to Galileo with full span details.

## OpenAI (Async)

```python
from galileo.openai import openai

client = openai.AsyncOpenAI()

response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4o",
)
```

## Anthropic

Use OpenTelemetry + OpenInference instrumentation to trace Anthropic calls:

```python
from openinference.instrumentation.anthropic import AnthropicInstrumentor

AnthropicInstrumentor().instrument()
```

Then use the Anthropic client as usual — spans are automatically exported to Galileo.

## LangChain

```python
from openinference.instrumentation.langchain import LangChainInstrumentor

LangChainInstrumentor().instrument()
```

All LangChain chain invocations, LLM calls, and retriever operations are automatically traced.

## LangGraph

```python
from openinference.instrumentation.langchain import LangChainInstrumentor

LangChainInstrumentor().instrument()
```

LangGraph builds on LangChain, so the same instrumentor captures graph node executions, edges, and state transitions.

## CrewAI

```python
from openinference.instrumentation.crewai import CrewAIInstrumentor

CrewAIInstrumentor().instrument()
```

Traces crew executions, agent steps, and tool calls within CrewAI workflows.

## PydanticAI

Use the OpenTelemetry integration to trace PydanticAI agent calls:

```python
from openinference.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument()
```

Since PydanticAI uses OpenAI-compatible clients under the hood, instrumenting the OpenAI layer captures all calls.

## Strands Agents

```python
from openinference.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument()
```

Strands Agents using OpenAI-compatible providers are traced via the OpenAI instrumentor.

## Google ADK

For Google's Agent Development Kit, use the Vertex AI instrumentor:

```python
from openinference.instrumentation.vertexai import VertexAIInstrumentor

VertexAIInstrumentor().instrument()
```

## Setting Up the OpenTelemetry Exporter for Galileo

To send OpenTelemetry traces to Galileo, configure the exporter:

```python
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

exporter = OTLPSpanExporter(
    endpoint="https://app.galileo.ai/api/otel/v1/traces",
    headers={"Authorization": f"Bearer {os.environ['GALILEO_API_KEY']}"},
)

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)
```

Then call the relevant instrumentor (e.g., `LangChainInstrumentor().instrument()`) and all traces flow to Galileo automatically.

## Combining Galileo Native Logging with OpenTelemetry

You can use Galileo's native `@log` decorator alongside OpenTelemetry-instrumented frameworks:

```python
from galileo import log, galileo_context
from openinference.instrumentation.langchain import LangChainInstrumentor

LangChainInstrumentor().instrument()
galileo_context.init(project="my-project", log_stream="production")

@log
def my_pipeline(query: str):
    chain = build_langchain_rag_chain()
    return chain.invoke({"question": query})
```
