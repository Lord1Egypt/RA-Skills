# Variable Resolution

The `VariableResolver` resolves `$namespace.path` references in step configs against the `ExecutionContext`.

## Syntax

```
$namespace.path.to.value
```

Regex: `$([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_.]*)`

Variables can appear anywhere in a string:
```yaml
prompt: "Hello $input.name, your score is $stepResult.score.content"
```

## Built-in Namespaces

### $input

Traverses `context.inputs` (workflow input parameters).

```yaml
# Given inputs: { user: { name: "Alice" } }
prompt: $input.user.name    # → "Alice"
```

### $stepResult

Traverses `context.step_results`. First path segment is the step id.

```yaml
prompt: $stepResult.analyze.content          # LLM content
data: $stepResult.run.result.stdout          # Tool stdout
template: $stepResult.validate.data.summary  # Guardrail parsed field
```

Result paths by primitive type:

| Primitive | Path Pattern | Example |
|-----------|-------------|---------|
| `llm` | `$stepResult.<id>.content` | `$stepResult.gen.content` |
| `chat` | `$stepResult.<id>.content` | `$stepResult.conv.content` |
| `tool` | `$stepResult.<id>.result.<field>` | `$stepResult.run.result.stdout` |
| `guardrail` | `$stepResult.<id>.data.<field>` | `$stepResult.check.data.name` |
| `guardrail` | `$stepResult.<id>.valid` | `$stepResult.check.valid` |
| `output-generator` | `$stepResult.<id>` | `$stepResult.render` |
| `call-agent` | `$stepResult.<id>.<child_step_id>` | `$stepResult.sub.child_step.content` |
| `agent-exec` | `$stepResult.<id>.output` | `$stepResult.review.output` |

### $env

Reads from `os.environ`. No dot traversal — the full path is the variable name.

```yaml
config:
  model: $env.BEDDEL_MODEL
```

## Path Traversal

Dot-separated segments walk nested dicts:

```
$stepResult.step1.result.stdout
    ↓ context.step_results
    ↓ ["step1"]        → step result dict
    ↓ ["result"]       → {exit_code, stdout, stderr, ...}
    ↓ ["stdout"]       → "hello world"
```

## SKIPPED Handling

When a step is skipped (falsy `if` condition), its result is the `SKIPPED` sentinel. Accessing any path on a SKIPPED result returns `SKIPPED` — it does not raise an error.

```yaml
# If step "optional" was skipped:
$stepResult.optional              # → SKIPPED
$stepResult.optional.content      # → SKIPPED
$stepResult.optional.data.name    # → SKIPPED
```

`SKIPPED` is falsy (like `None`) but distinguishable via identity. Use in conditions:

```yaml
if: "$stepResult.optional != SKIPPED"
```

## Full-String vs Embedded References

**Full-string reference** — the entire string is one `$ns.path`. Preserves the native type of the resolved value (dict, list, int, bool, etc.):

```yaml
data: $stepResult.analyze    # → dict (not stringified)
```

**Embedded reference** — mixed with literal text. Each token is resolved and stringified:

```yaml
prompt: "Result: $stepResult.analyze.content"  # → "Result: some text"
```

## Recursive Resolution

If a resolved value is itself a string containing a `$ns.path` reference, it resolves again. Max depth: 10.

```yaml
# If $input.template = "Hello $input.name" and $input.name = "Alice"
# Then resolving $input.template → "Hello Alice"
```

Embedded references do NOT recurse (only full-string refs do).

## Custom Namespaces

Register via `resolver.register_namespace(name, handler)`:

```python
def secret_handler(path: str, context: ExecutionContext) -> Any:
    return get_secret(path)

resolver.register_namespace("secrets", secret_handler)
# Now $secrets.api_key resolves via secret_handler
```

Name must match `^[a-zA-Z_][a-zA-Z0-9_]*$`.

## Error Codes

| Code | Meaning |
|------|---------|
| `BEDDEL-RESOLVE-001` | Unresolvable — path segment not found or unknown namespace |
| `BEDDEL-RESOLVE-002` | Circular reference detected in resolution chain |
| `BEDDEL-RESOLVE-003` | Max recursion depth (10) exceeded |
