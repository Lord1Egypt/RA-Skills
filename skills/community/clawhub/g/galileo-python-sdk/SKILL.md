---
name: galileo-python-sdk
description: Complete reference for the Galileo AI platform Python SDK for evaluating, observing, and protecting GenAI applications. Use when building Python applications that need LLM evaluation, production observability, tracing, or runtime guardrails with Galileo.
license: MIT
compatibility: Requires Python 3.10+ (v2.x). Python 3.9 supported up to v1.39.x. Works with pip, poetry, or uv.
metadata:
  author: gyanesh-m
  version: "1.0.0"
  sdk-version: "2.1.1"
  sdk-repo: https://github.com/rungalileo/galileo-python
  docs: https://docs.galileo.ai
---

# Galileo Python SDK

The Galileo Python SDK (`galileo`) provides a unified interface for the Galileo AI platform — enabling evaluation, observability, and runtime guardrails for GenAI applications. It supports automatic tracing of LLM calls, custom span logging, evaluation experiments, and production-grade guardrails.

## SDK Version Detection

**Check installed versions before writing any code** to pick the right reference:

```python
import importlib.metadata, importlib.util

galileo_ver = importlib.metadata.version("galileo")        # e.g. "2.1.1"
pq_installed = importlib.util.find_spec("promptquality") is not None
pq_ver = importlib.metadata.version("promptquality") if pq_installed else None
print(f"galileo={galileo_ver}, promptquality={pq_ver}")
```

| Installed stack | Use |
|---|---|
| `galileo >= 2.0` (with or without `promptquality 0.x`) | This skill — `GalileoLogger`, `@log`, `galileo_context` |
| `galileo < 2.0` + `promptquality >= 1.0` | [Promptquality 1.x Reference](references/PROMPTQUALITY.md) |

> **Note:** `promptquality >= 1.0` and `galileo >= 2.0` are **mutually incompatible** — they require different major versions of `galileo-core`. Installing both will cause dependency conflicts.

**Additional references:**

- [Framework Integrations](references/INTEGRATIONS.md) — OpenAI, Anthropic, LangChain, LangGraph, CrewAI, PydanticAI, and more
- [Guardrail Metrics Reference](references/METRICS.md) — Hallucination Index, Context Adherence, Toxicity, PII, and all available metrics
- [Advanced Evaluation Patterns](references/EVALUATION.md) — Experiments, eval sets, prompt optimization, and scoring
- [Promptquality 1.x Reference](references/PROMPTQUALITY.md) — EvaluateRun, Scorers, ScorersConfiguration for the galileo 1.x stack

## Installation

```bash
pip install galileo
```

For evaluation features with the legacy prompt engineering interface:

```bash
pip install promptquality
```

For runtime guardrails:

```bash
pip install galileo-protect
```

## Quick Start

```python
import os
from galileo import galileo_context
from galileo.openai import openai

galileo_context.init(project="my-project", log_stream="my-log-stream")

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Explain quantum computing in one sentence."}],
    model="gpt-4o",
)

print(response.choices[0].message.content)

galileo_context.flush()
```

## Authentication

Set the following environment variables:

```bash
# .env file or shell environment
GALILEO_API_KEY="your-api-key"            # Required — from Galileo console
GALILEO_CONSOLE_URL="https://app.galileo.ai"  # Console URL (or self-hosted URL)
GALILEO_PROJECT="my-project"              # Optional — default project
GALILEO_LOG_STREAM="my-log-stream"        # Optional — default log stream
GALILEO_LOGGING_DISABLED="false"          # Optional — disable logging
```

For the legacy `promptquality` package, authenticate programmatically:

```python
import promptquality as pq
pq.login("https://app.galileo.ai")
```

## Observability and Tracing

### Initializing the Galileo Context

```python
from galileo import galileo_context

galileo_context.init(project="my-project", log_stream="my-log-stream")
```

### Wrapped OpenAI Client (Auto-Logging)

Import the Galileo-wrapped OpenAI client to automatically trace all calls:

```python
from galileo.openai import openai

client = openai.OpenAI()
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4o",
)
```

### The `@log` Decorator

Use `@log` to create spans for your functions. Supported span types: `workflow`, `llm`, `retriever`, `tool`.

```python
from galileo import log

@log
def my_workflow():
    result = call_openai()
    return result

@log(span_type="retriever")
def retrieve_documents(query: str):
    docs = vector_store.search(query)
    return docs

@log(span_type="tool")
def search_web(query: str):
    return web_api.search(query)
```

### Nested Workflows

```python
from galileo import log

@log
def agent_pipeline(user_input: str):
    context = retrieve_documents(user_input)
    tool_result = search_web(user_input)
    response = generate_response(user_input, context, tool_result)
    return response

@log(span_type="retriever")
def retrieve_documents(query: str):
    return ["doc1", "doc2"]

@log(span_type="tool")
def search_web(query: str):
    return "search result"

@log
def generate_response(query: str, context: list, tool_result: str):
    client = openai.OpenAI()
    return client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="gpt-4o",
    )
```

### Context Manager

Scope logging to a specific block and auto-flush on exit:

```python
from galileo import galileo_context

with galileo_context(project="my-project", log_stream="my-log-stream"):
    result = my_workflow()
    print(result)
```

### Flushing Traces

Upload captured traces to Galileo:

```python
galileo_context.flush()
```

## Evaluation

### Running Experiments with `promptquality`

```python
import promptquality as pq

pq.login("https://app.galileo.ai")

template = "Explain {{topic}} to me like I'm a 5 year old"
data = {"topic": ["Quantum Physics", "Politics", "Large Language Models"]}

pq.run(
    project_name="my-first-project",
    template=template,
    dataset=data,
    settings=pq.Settings(
        model_alias="ChatGPT (16K context)",
        temperature=0.8,
        max_tokens=400,
    ),
)
```

### Evaluation Runs with Custom Workflows (galileo 2.x)

Use `GalileoLogger` to log traces for evaluation:

```python
from galileo import GalileoLogger

logger = GalileoLogger(project="my_project", log_stream="my_run")

eval_set = ["What are hallucinations?", "What are intrinsic hallucinations?"]
for input_text in eval_set:
    output = llm.call(input_text)
    logger.add_single_llm_span_trace(
        input=input_text,
        output=output,
        model="gpt-4o",
    )

logger.flush()
```

> For the `galileo < 2.0` + `promptquality >= 1.0` stack, use `EvaluateRun` — see [Promptquality 1.x Reference](references/PROMPTQUALITY.md).

See [Advanced Evaluation Patterns](references/EVALUATION.md) for more.

## Guardrails / Protect

### Creating a Protection Stage

```python
from galileo import GalileoMetrics
from galileo.stages import create_protect_stage
from galileo_core.schemas.protect.rule import Rule, RuleOperator
from galileo_core.schemas.protect.ruleset import Ruleset
from galileo_core.schemas.protect.stage import StageType

rule = Rule(
    metric=GalileoMetrics.input_toxicity,
    operator=RuleOperator.gt,
    target_value=0.1,
)

ruleset = Ruleset(rules=[rule])

stage = create_protect_stage(
    name="toxicity-guard",
    stage_type=StageType.central,
    prioritized_rulesets=[ruleset],
    description="Block toxic input.",
)
```

### Invoking Runtime Protection

```python
from galileo.protect import invoke_protect, ainvoke_protect
from galileo_core.schemas.protect.payload import Payload

payload = Payload(input="User message to check.")

response = invoke_protect(payload=payload, stage_name="toxicity-guard")

# Async variant
response = await ainvoke_protect(payload=payload, stage_name="toxicity-guard")
```

### Stage Types

- **Central stages** — Created and managed by governance teams; rulesets defined at creation time
- **Local stages** — Created without rulesets; rulesets supplied at runtime by application teams

See [Guardrail Metrics Reference](references/METRICS.md) for all available metrics.

## Common Patterns

### Multi-Turn Conversations

```python
from galileo import log
from galileo.openai import openai

client = openai.OpenAI()

@log
def chat(messages: list):
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
    )
    return response.choices[0].message.content

messages = []
messages.append({"role": "user", "content": "What is RAG?"})
reply = chat(messages)
messages.append({"role": "assistant", "content": reply})
messages.append({"role": "user", "content": "How do I implement it?"})
reply = chat(messages)
```

### RAG Pipeline with Retriever Spans

```python
from galileo import log
from galileo.openai import openai

client = openai.OpenAI()

@log(span_type="retriever")
def retrieve(query: str):
    results = vector_db.similarity_search(query, k=5)
    return [doc.page_content for doc in results]

@log
def rag_pipeline(question: str):
    context = retrieve(question)
    prompt = f"Context: {context}\n\nQuestion: {question}"
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4o",
    )
    return response.choices[0].message.content
```

### Agent Tool Calling

```python
from galileo import log

@log(span_type="tool")
def math_operation(a: float, b: float, op: str) -> str:
    if op == "add":
        return str(a + b)
    elif op == "multiply":
        return str(a * b)
    raise ValueError(f"Unknown op: {op}")

@log(span_type="tool")
def web_search(query: str):
    return search_api.query(query)

@log
def agent(user_input: str):
    plan = plan_actions(user_input)
    results = []
    for action in plan:
        if action.tool == "math_operation":
            results.append(math_operation(action.input))
        elif action.tool == "web_search":
            results.append(web_search(action.input))
    return synthesize(results)
```

## Best Practices

1. **Always set environment variables** for `GALILEO_API_KEY` and `GALILEO_CONSOLE_URL` rather than hardcoding credentials.
2. **Organize projects and log streams** by application, environment, or team to keep traces manageable.
3. **Call `galileo_context.flush()`** at the end of each request or batch to ensure traces are uploaded. In web servers, flush at the end of each request handler.
4. **Use the context manager** (`with galileo_context(...)`) for scoped logging that auto-flushes on exit.
5. **Use specific span types** (`retriever`, `tool`, `llm`, `workflow`) to get the most out of Galileo's trace visualization.
6. **Handle errors gracefully** — wrap `flush()` calls in try/except to prevent logging failures from crashing your application.
7. **Use the wrapped OpenAI client** (`from galileo.openai import openai`) for zero-config automatic tracing of all OpenAI calls.
8. **Leverage guardrail metrics** in production to catch hallucinations, toxic content, and PII before they reach end users.

## Resources

- **Documentation:** https://docs.galileo.ai
- **Python SDK repo:** https://github.com/rungalileo/galileo-python
- **SDK examples:** https://github.com/rungalileo/sdk-examples
- **PyPI:** https://pypi.org/project/galileo/
- **Galileo console:** https://app.galileo.ai
