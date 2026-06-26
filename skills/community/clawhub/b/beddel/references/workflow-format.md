# Workflow YAML Format

A Beddel workflow is a YAML document parsed into a `Workflow` Pydantic model. Steps execute sequentially by default.

## Top-Level Fields

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `id` | str | Yes | — | Unique workflow identifier |
| `name` | str | Yes | — | Human-readable name |
| `description` | str | No | `""` | Longer description |
| `version` | str | No | `"1.0"` | Semantic version string |
| `input_schema` | dict | No | `null` | Input validation schema |
| `steps` | list[Step] | Yes | — | Ordered list of steps |
| `metadata` | dict | No | `{}` | Arbitrary metadata |
| `allowed_tools` | list[str] | No | `null` | Tool allowlist (`null` = all allowed) |
| `tools` | list[ToolDeclaration] | No | `null` | Inline tool declarations (`name` + `target` in `module:function` format) |

## Input Schema Format

The `input_schema` is a dict mapping field names to descriptors:

```yaml
input_schema:
  topic:
    type: str        # str, int, float, bool
    required: true
    default: "AI"
  max_results:
    type: int
    required: false
    default: 10
```

## Step Fields

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `id` | str | Yes | — | Unique step identifier within the workflow |
| `primitive` | str | Yes | — | Primitive name (`llm`, `chat`, `tool`, `guardrail`, `output-generator`, `call-agent`, `agent-exec`) |
| `config` | dict | No | `{}` | Primitive-specific configuration |
| `execution_strategy` | dict | No | `{type: fail}` | Error-handling strategy |
| `if` | str | No | `null` | Condition expression for branching |
| `then` | list[Step] | No | `null` | Steps to run when `if` is truthy |
| `else` | list[Step] | No | `null` | Steps to run when `if` is falsy |
| `timeout` | float | No | `null` | Timeout in seconds |
| `stream` | bool | No | `false` | Stream output from this step |
| `parallel` | bool | No | `false` | Reserved for future use |
| `metadata` | dict | No | `{}` | Arbitrary step metadata |

## Condition Expressions

The `if` field supports:
- Variable references: `$stepResult.check.data.valid`
- Comparisons: `$stepResult.score.content > 0.8`, `$input.mode == "fast"`
- Operators: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Boolean coercion: `"true"/"false"` (case-insensitive), empty string → false

## Complete Example

```yaml
id: analyze-and-report
name: Analyze and Report
description: Analyzes input text and generates a formatted report
version: "1.0"
input_schema:
  text:
    type: str
    required: true
  format:
    type: str
    required: false
    default: markdown
allowed_tools:
  - shell_exec

steps:
  - id: analyze
    primitive: llm
    config:
      model: gpt-4o
      prompt: "Analyze this text: $input.text"
      temperature: 0.3
    timeout: 30

  - id: validate
    primitive: guardrail
    config:
      data: $stepResult.analyze.content
      schema:
        fields:
          summary: { type: str, required: true }
      strategy: correct

  - id: report
    primitive: output-generator
    config:
      template: "# Report\n\n$stepResult.validate.data.summary"
      format: $input.format
    if: "$stepResult.validate.valid == true"

  - id: fallback
    primitive: output-generator
    config:
      template: "Analysis failed validation."
      format: text
    if: "$stepResult.validate.valid != true"
```
