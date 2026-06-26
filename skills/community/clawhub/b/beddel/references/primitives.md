# Primitives Reference

Beddel provides 7 built-in primitives. Each primitive receives a `config` dict and an `ExecutionContext`, and returns a result stored in `$stepResult.<step_id>`.

## llm

Single-turn LLM invocation.

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `model` | str | Yes | — | Model identifier (e.g. `gpt-4o`) |
| `prompt` | str | No* | — | User prompt (mutually exclusive with `messages`) |
| `messages` | list[dict] | No* | — | Chat-style message list |
| `temperature` | float | No | — | Sampling temperature |
| `max_tokens` | int | No | — | Max tokens to generate |
| `stream` | bool | No | `false` | Return async generator instead of dict |

```yaml
- id: summarize
  primitive: llm
  config:
    model: gpt-4o
    prompt: "Summarize: $input.text"
    temperature: 0.3
```

**Result:** `{content, model, usage: {prompt_tokens, completion_tokens, total_tokens}, finish_reason}`
Access: `$stepResult.summarize.content`

## chat

Multi-turn LLM invocation with context windowing.

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `model` | str | Yes | — | Model identifier |
| `system` | str | No | — | System message (prepended to messages) |
| `messages` | list[dict] | No | `[]` | Conversation history (`{role, content}`) |
| `max_messages` | int | No | `50` | Max non-system messages to retain |
| `max_context_tokens` | int | No | `null` | Token budget (estimated ~4 chars/token) |
| `temperature` | float | No | — | Sampling temperature |
| `max_tokens` | int | No | — | Max tokens to generate |
| `stream` | bool | No | `false` | Return async generator |

```yaml
- id: converse
  primitive: chat
  config:
    model: gpt-4o
    system: "You are a helpful assistant."
    messages:
      - { role: user, content: "Hello!" }
    max_messages: 20
```

**Result:** `{content, model, usage: {prompt_tokens, completion_tokens, total_tokens}, finish_reason}`

## output-generator

Template rendering with variable interpolation.

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `template` | str | Yes | — | Template with `$var` references |
| `format` | str | No | `text` | Output format: `json`, `markdown`, `text` |
| `indent` | int | No | `2` | JSON indent level (only for `json` format) |

```yaml
- id: render
  primitive: output-generator
  config:
    template: "Summary for $input.user: $stepResult.analyze.content"
    format: text
```

**Result:** A plain string (the rendered template). Unlike other primitives, output-generator does NOT return a dict.
Access: `$stepResult.render` (the value is the string itself)

## guardrail

Data validation against a dynamic Pydantic model.

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `data` | any | Yes | — | Data to validate |
| `schema` | dict | Yes | — | Schema with `fields` dict |
| `strategy` | str | No | `raise` | `raise`, `return_errors`, `correct`, `delegate` |
| `max_attempts` | int | No | `1` | Retry limit for `delegate` strategy |
| `model` | str | No | delegate_model | LLM model for `delegate` strategy |

Schema field descriptors: `{ type: str/int/float/bool/list/dict, required: bool }`

```yaml
- id: validate
  primitive: guardrail
  config:
    data: $stepResult.generate.content
    schema:
      fields:
        name: { type: str, required: true }
        score: { type: float }
    strategy: correct
```

**Result:** `{valid: bool, data: <parsed>, errors?: [str]}`
Access: `$stepResult.validate.data.name`, `$stepResult.validate.valid`

Strategy details:
- `raise`: throws `PrimitiveError` on failure
- `return_errors`: returns `{valid: false, errors: [...], data: <original>}`
- `correct`: strips markdown fences, parses JSON, re-validates; falls back to `return_errors`
- `delegate`: sends errors to LLM for correction, re-validates up to `max_attempts`

## call-agent

Nested workflow invocation.

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `workflow` | str | Yes | — | Workflow ID to load |
| `inputs` | dict | No | `{}` | Inputs for nested workflow (supports `$var` refs) |
| `max_depth` | int | No | `5` | Maximum nesting depth |

```yaml
- id: sub
  primitive: call-agent
  config:
    workflow: summarize-wf
    inputs:
      text: $stepResult.extract.content
    max_depth: 3
```

**Result:** dict of the nested workflow's step results (keyed by step id).

## tool

External tool invocation. Looks up a callable from the tool registry.

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `tool` | str | Yes | — | Tool name in the registry |
| `arguments` | dict | No | `{}` | Keyword arguments (supports `$var` refs) |
| `timeout` | int | No | `60` | Timeout in seconds |

Built-in tool `shell_exec` args: `cmd` (str), `timeout` (int, default 60), `cwd` (str|null), `fail_on_error` (bool, default false). Uses `shell=False` with `shlex.split()`.

```yaml
- id: run
  primitive: tool
  config:
    tool: shell_exec
    arguments:
      cmd: "ls -la $input.directory"
      timeout: 30
```

**Result:** `{tool, result: {exit_code, stdout, stderr, timed_out, truncated}, arguments, duration_ms}`
Access: `$stepResult.run.result.stdout`

## agent-exec

Delegates execution to an external agent backend via an adapter.

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `adapter` | str | Yes | — | Agent adapter name in the registry |
| `prompt` | str | Yes | — | Instruction for the agent (supports `$var` refs) |
| `model` | str | No | — | Model override |
| `sandbox` | str | No | `read-only` | `read-only`, `workspace-write`, `danger-full-access` |
| `tools` | list[str] | No | — | Tool names the agent may use |
| `output_schema` | dict | No | — | JSON Schema for structured output |

```yaml
- id: review
  primitive: agent-exec
  config:
    adapter: codex
    prompt: "Review $input.code for security issues"
    model: o3-mini
    sandbox: read-only
```

**Result:** `{output, files_changed, usage}`
Access: `$stepResult.review.output`
